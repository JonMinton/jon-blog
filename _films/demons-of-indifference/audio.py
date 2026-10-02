"""Speech, timeline, score and effects.

    python3 audio.py            # laptop or butler: needs macOS `say` and numpy

1. Speaks every line of script.py with `say`, trims silence, and processes the demon's voice.
2. Lays the lines end to end and writes build/timeline.json (cues, lines, sections, duration).
3. Synthesises a drone score and the effects from beats.py's schedules, ducks the music under
   speech, and writes build/mix.wav (48 kHz stereo).
"""
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np
from scipy.signal import lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beats as B  # noqa: E402
import editions as E  # noqa: E402
import script as S  # noqa: E402

SR = 48000
BUILD = os.path.join(HERE, "build")
VOX = os.path.join(BUILD, "vox")
os.makedirs(VOX, exist_ok=True)
rng = np.random.default_rng(3)


# ---------------------------------------------------------------- io

def read_wav(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        n = w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(axis=1)
    if sr != SR:
        t_old = np.arange(len(x)) / sr
        t_new = np.arange(int(len(x) * SR / sr)) / SR
        x = np.interp(t_new, t_old, x).astype(np.float32)
    return x


def write_wav(path, stereo):
    s = np.clip(stereo, -1, 1)
    data = (s * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def tts(speaker, text, idx):
    voice, rate = S.VOICES[speaker]
    out = os.path.join(VOX, f"{idx:03d}_{speaker}.wav")
    subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", out,
                    "--data-format=LEI16@24000", text], check=True)
    x = read_wav(out)
    # trim leading and trailing silence
    env = np.convolve(np.abs(x), np.ones(480) / 480, mode="same")
    on = np.where(env > 0.004)[0]
    if len(on):
        x = x[max(0, on[0] - 480): on[-1] + 2400]
    if speaker == "DEMON":
        x = demonise(x)
    return x / max(1e-6, np.abs(x).max()) * 0.8


def demonise(x):
    """Ring modulation, a sub-octave shadow and a short dark echo: unmistakably not a person."""
    t = np.arange(len(x)) / SR
    ring = x * np.sin(2 * np.pi * 47 * t)
    # sub-octave shadow: full-wave rectify then low-pass gives energy an octave and more below
    rect = np.abs(x) * np.sign(np.sin(2 * np.pi * 61 * t))
    sub = lowpass(rect, 260)
    y = 0.62 * x + 0.55 * ring + 0.35 * sub
    y = np.tanh(1.6 * y) / np.tanh(1.6)
    y = np.concatenate([y, np.zeros(int(0.5 * SR), dtype=np.float32)])
    out = y.copy()
    for d, g in ((0.083, 0.28), (0.171, 0.16), (0.29, 0.08)):
        k = int(d * SR)
        out[k:] += g * lowpass(y[:-k], 2200)
    return out.astype(np.float32)


def lowpass(x, fc):
    """Two cascaded one-pole low-pass filters."""
    a = math.exp(-2 * math.pi * fc / SR)
    y = lfilter([1 - a], [1, -a], x)
    return lfilter([1 - a], [1, -a], y).astype(np.float32)


def highpass(x, fc):
    return x - lowpass(x, fc)


# ---------------------------------------------------------------- 1 and 2: speech and timeline

def build_timeline():
    stats = E.stats()
    fills = {
        "wordcount_line": ("The story runs to just under three thousand words. "
                           "Explaining it took another two thousand."),
    }
    t = 0.0
    cues, lines, sections, clips = {}, [], {}, []
    idx = 0
    for sec, items in S.SECTIONS:
        s0 = t
        for it in items:
            kind = it[0]
            if kind == "pause":
                t += it[1]
            elif kind == "cue":
                cues[it[1]] = round(t, 3)
            elif kind == "say":
                speaker, text = it[1], it[2]
                gap = it[3] if len(it) > 3 else S.GAP
                if text == "{tir_line}":
                    m, s = divmod(int(t - cues["puff"]), 60)
                    text = f"Time in realm: {m} minutes, {s} seconds."
                text = fills.get(text.strip("{}"), text)
                x = tts(speaker, text, idx)
                idx += 1
                d = len(x) / SR
                if speaker == "DEMON":
                    d -= 0.45  # the echo tail may overlap what follows
                lines.append({"speaker": speaker, "text": text, "start": round(t, 3),
                              "end": round(t + d, 3), "section": sec})
                clips.append((t, x, speaker))
                t += d + gap
        sections[sec] = [round(s0, 3), round(t, 3)]
    tl = {"fps": B.FPS, "duration": round(t, 3), "cues": cues, "lines": lines,
          "sections": sections, "stats": stats}
    with open(os.path.join(BUILD, "timeline.json"), "w") as f:
        json.dump(tl, f, indent=1)
    B._TL = tl
    return tl, clips


# ---------------------------------------------------------------- 3: score and effects

def env_ar(n, a, r):
    e = np.ones(n, dtype=np.float32)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def add(buf, t, x, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= len(buf) or i + len(x) <= 0:
        return
    x = x[: len(buf) - i]
    l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    buf[i:i + len(x), 0] += gain * l * x
    buf[i:i + len(x), 1] += gain * r * x


def noise(d):
    return rng.standard_normal(int(d * SR)).astype(np.float32)


def sine(f, d, phase=0.0):
    t = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * f * t + phase).astype(np.float32)


def bell(f0, d=4.0):
    t = np.arange(int(d * SR)) / SR
    x = np.zeros_like(t)
    for ratio, g, decay in ((1, 1, 1.4), (2.76, 0.5, 2.6), (5.4, 0.25, 4), (8.9, 0.12, 6), (0.5, 0.3, 1.0)):
        x += g * np.sin(2 * np.pi * f0 * ratio * t) * np.exp(-decay * t)
    return (x * env_ar(len(t), 0.004, 0.2)).astype(np.float32) * 0.35


def puff():
    d = 1.6
    t = np.arange(int(d * SR)) / SR
    thump = np.sin(2 * np.pi * (90 * np.exp(-3 * t)) * t) * np.exp(-4 * t)
    hiss = lowpass(noise(d), 1800) * np.exp(-3.2 * t) * 1.4
    crack = highpass(noise(d), 3000) * np.exp(-25 * t) * 0.6
    return (0.9 * thump + hiss + crack).astype(np.float32)


def scratch(d=0.18):
    n = noise(d)
    t = np.arange(len(n)) / SR
    fm = 1 + 0.6 * np.sin(2 * np.pi * rng.uniform(18, 30) * t)
    x = highpass(lowpass(n, 6500), 1800) * fm
    return (x * env_ar(len(x), 0.01, d * 0.6)).astype(np.float32) * 0.5


def flutter(d=0.35):
    n = noise(d)
    t = np.arange(len(n)) / SR
    am = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rng.uniform(28, 45) * t))
    x = highpass(lowpass(n, 5000), 600) * am
    return (x * env_ar(len(x), 0.02, d * 0.7)).astype(np.float32) * 0.45


def click():
    n = noise(0.025)
    t = np.arange(len(n)) / SR
    return (highpass(n, 2500) * np.exp(-180 * t)).astype(np.float32) * 0.5


def strike():
    d = 1.4
    t = np.arange(int(d * SR)) / SR
    x = highpass(noise(d), 1200) * (np.exp(-12 * t) + 0.08 * np.exp(-1.5 * t))
    crackle = np.zeros_like(x)
    for _ in range(40):
        i = rng.integers(0, len(x) - 400)
        crackle[i:i + 200] += rng.uniform(0.2, 0.6) * np.exp(-np.arange(200) / 30)
    return (x * 0.6 + crackle * 0.4 * np.exp(-1.2 * t)).astype(np.float32)


def pad(freqs, d, detune=0.003):
    t = np.arange(int(d * SR)) / SR
    x = np.zeros_like(t)
    for f in freqs:
        for k in (-1, 0, 1):
            x += np.sin(2 * np.pi * f * (1 + k * detune) * t + rng.uniform(0, 6.28))
            x += 0.3 * np.sin(2 * np.pi * 2 * f * (1 + k * detune) * t + rng.uniform(0, 6.28))
    return lowpass(x.astype(np.float32), 900) / (len(freqs) * 3)


def score(tl, N):
    """Music bed: a D drone throughout, shaped by section; a warm D major turn at the coda."""
    mus = np.zeros((N, 2), dtype=np.float32)
    T = N / SR
    cues = tl["cues"]
    secs = tl["sections"]
    D2, A2, D3, F3, A3, Fs3, C3 = 73.42, 110.0, 146.83, 174.61, 220.0, 185.0, 130.81

    # base drone, the whole film, with slow breathing
    drone = pad([D2, A2, D3], T)
    t = np.arange(len(drone)) / SR
    breath = 0.75 + 0.25 * np.sin(2 * np.pi * t / 11.0)
    level = np.full(len(drone), 0.22, dtype=np.float32)

    def ramp(a, b, v0, v1):
        i0, i1 = int(a * SR), int(b * SR)
        level[i0:i1] = np.linspace(v0, v1, max(1, i1 - i0))
        level[i1:] = v1

    ramp(0, 2.5, 0.0, 0.16)
    ramp(cues["incense"], cues["incense"] + 3, 0.16, 0.24)
    ramp(cues["title"], cues["title"] + 1.5, 0.24, 0.36)
    ramp(cues["ed1"], cues["ed1"] + 2, 0.36, 0.22)
    ramp(cues["lift"], cues["lift"] + 1.5, 0.22, 0.10)
    ramp(cues["ed4"], cues["ed4"] + 1.5, 0.10, 0.22)
    ramp(cues["pullback"], cues["pullback"] + 4, 0.22, 0.34)
    ramp(cues["coda"], cues["coda"] + 3, 0.34, 0.12)
    ramp(cues["end"] + 3, T, 0.12, 0.0)
    d = drone * breath * level
    mus[:, 0] += d
    mus[:, 1] += np.roll(d, 300)

    # minor colour for the title and the high corruption, major for the coda
    for (a, b), chord, g in (((cues["title"] - 0.5, cues["ed1"] + 1.5), [D3, F3, A3], 0.30),
                              ((cues["flood"], secs["high"][1]), [D3, F3, A3, C3], 0.18),
                              ((cues["pullback"], secs["slop"][1]), [D2, D3, F3, A3, C3], 0.26),
                              ((cues["coda"] + 0.5, cues["fin"]), [D3, Fs3, A3], 0.26)):
        x = pad(chord, b - a, detune=0.004)
        x *= env_ar(len(x), 2.0, 2.5)
        add(mus, a, x, g, -0.2)
        add(mus, a + 0.013, x, g, 0.2)

    # a slow heartbeat under the slop, quickening as the lecterns multiply
    a, b = cues["pullback"], secs["slop"][1]
    tt = a
    while tt < b:
        beat = sine(55, 0.35) * np.exp(-np.arange(int(0.35 * SR)) / SR * 9).astype(np.float32)
        add(mus, tt, beat, 0.5)
        add(mus, tt + 0.28, beat, 0.3)
        tt += 1.6 - 0.6 * B.smooth(a, cues["terminal"], tt)

    # bells mark each edition
    for name, f in (("title", 293.66), ("ed1", 293.66), ("ed2", 329.63), ("ed3", 349.23),
                    ("ed4", 392.0), ("end", 293.66)):
        add(mus, cues[name], bell(f), 0.5, -0.3)
        add(mus, cues[name] + 0.02, bell(f * 1.002), 0.4, 0.3)
    return mus


def effects(tl, N):
    fx = np.zeros((N, 2), dtype=np.float32)
    cues = tl["cues"]
    a, b = B.typing()
    n = len(B.PROMPT)
    for i in range(0, n, 3):
        add(fx, a + (b - a) * i / n + rng.uniform(0, 0.01), click(), 0.35, rng.uniform(-0.3, 0.3))
    add(fx, cues["incense"], strike(), 0.7, -0.4)
    add(fx, cues["incense"] + 0.6, strike(), 0.5, 0.4)
    add(fx, cues["puff"], puff(), 0.9)
    add(fx, cues["puff_out"] - 0.15, puff(), 0.9)
    for t in B.mild_edit_times():
        add(fx, t, scratch(), 0.6, rng.uniform(-0.4, 0.4))
    s, e = B.deletion_window()
    whoosh = lowpass(noise(e - s), 2500) * env_ar(int((e - s) * SR), 0.9, 0.3)
    add(fx, s, whoosh[::-1].copy(), 0.25)
    for t in B.high_edit_times()[::2]:
        add(fx, t, scratch(rng.uniform(0.08, 0.2)), 0.35, rng.uniform(-0.7, 0.7))
    add(fx, cues["byline"] + 0.1, scratch(0.6), 0.7)
    for t in B.slip_times():
        add(fx, t, flutter(), 0.5, rng.uniform(-0.8, 0.8))
    for s, _ in B.mapping_times():
        add(fx, s, click(), 0.8)
        add(fx, s + 0.05, bell(880, 0.6), 0.12)
    add(fx, cues["terminal"], sine(1320, 0.08) * env_ar(int(0.08 * SR), 0.005, 0.03), 0.15)
    s, e = B.multiply_window()
    for k in range(60):
        t = s + (e - s) * (k / 60) ** 0.7
        add(fx, t, puff()[: int(0.5 * SR)] * env_ar(int(0.5 * SR), 0.001, 0.3), 0.06, rng.uniform(-1, 1))
    return fx


def main():
    tl, clips = build_timeline()
    N = int((tl["duration"] + 0.5) * SR)
    vox = np.zeros((N, 2), dtype=np.float32)
    for t, x, sp in clips:
        pan = {"DEMON": 0.0, "NARR": 0.0, "BETH": -0.25, "MUM": 0.25, "DAD": 0.2, "STEVE": -0.1,
               "PARTNER": -0.3}[sp]
        add(vox, t, x, 0.95 if sp == "DEMON" else 0.85, pan)
    mus = score(tl, N)
    # duck the music under speech
    act = np.zeros(N, dtype=np.float32)
    for ln in tl["lines"]:
        act[int(ln["start"] * SR): int(ln["end"] * SR)] = 1
    duck = 1 - 0.45 * lowpass(act, 2.0)
    mus *= duck[:, None]
    fx = effects(tl, N)
    mix = vox + mus + fx
    mix /= max(1.0, np.abs(mix).max() / 0.95)
    write_wav(os.path.join(BUILD, "mix.wav"), mix)
    print(f"duration {tl['duration']:.1f} s, {len(tl['lines'])} lines")
    for k, v in tl["sections"].items():
        print(f"  {k:14s} {v[0]:7.1f} {v[1]:7.1f}  ({v[1]-v[0]:.1f} s)")


if __name__ == "__main__":
    main()
