"""Shared timing: loads build/timeline.json (written by audio.py) and derives every schedule that
picture and sound both need, so the scratch you hear is the edit you see.

Standard library only: Blender's bundled Python imports this too.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 24

PROMPT = ("with opus 5.5. usage rate over week is low and capabilities very high. Please review the "
          "variants of the demons-of-indifference stories along with the tooling used to create videos "
          "like roboduck in showcase repos and similar, making use of blender on butler. Produce a video "
          "based on the demons-of-indifference story and its variants. This can be a 4th wall mashup of "
          "all 4 variants and the slop-based metacommentary of releasing all 4. Video can be up to 5 "
          "minutes.")

MAPPINGS = [
    ("the TIR metric", "METR's time horizons"),
    ("Professor Sir Ignatious Haunting", "Geoffrey Hinton"),
    ("Big Joss", "GPUs and datacentres"),
    ("the codex", "the Voynich manuscript"),
    ("glass in the smoothie", "glue on pizza"),
    ("the Baphomet clause", "Mata v. Avianca"),
    ("Indian coder farms", "the Mechanical Turk"),
    ("demonslop", "AI slop"),
    ("the Chinese demons", "DeepSeek"),
]

_TL = None


def tl():
    global _TL
    if _TL is None:
        with open(os.path.join(HERE, "build", "timeline.json")) as f:
            _TL = json.load(f)
    return _TL


def cue(name):
    return tl()["cues"][name]


def duration():
    return tl()["duration"]


def n_frames():
    return int(math.ceil(duration() * FPS))


def smooth(a, b, x):
    if x <= a:
        return 0.0
    if x >= b:
        return 1.0
    t = (x - a) / (b - a)
    return t * t * (3 - 2 * t)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


# ---------------------------------------------------------------- derived schedules (seconds)

def typing():
    """(start, end) of the prompt being typed."""
    s = cue("prompt") + 0.5
    return s, s + 6.4


def typed_chars(t):
    a, b = typing()
    return int(len(PROMPT) * clamp((t - a) / (b - a)))


def mild_edit_times():
    s = cue("mild_edits") + 0.2
    rnd = random.Random(17)
    ts = sorted(s + 3.6 * (i / 16) + rnd.uniform(-0.08, 0.08) for i in range(17))
    return ts


def flood_window():
    s = cue("flood")
    return s, s + 3.2


def high_edit_times():
    a, b = flood_window()
    rnd = random.Random(153)
    return sorted(a + (b - a) * (rnd.random() ** 0.8) for _ in range(136))


def deletion_window():
    s = cue("deletion") + 0.3
    return s, s + 1.3


def slip_times():
    s = cue("slips") + 0.15
    return [s + 2.6 * (i / 28) ** 0.9 for i in range(29)]


def mapping_times():
    s = cue("mappings") + 0.2
    step = (cue("pudding") - 0.4 - s) / len(MAPPINGS)
    return [(s + i * step, s + (i + 1) * step) for i in range(len(MAPPINGS))]


def multiply_window():
    s = cue("multiply") - 0.6
    return s, s + 7.0


def line_at(t):
    for ln in tl()["lines"]:
        if ln["start"] <= t < ln["end"]:
            return ln
    return None


def speaking(t, speaker=None):
    ln = line_at(t)
    return ln is not None and (speaker is None or ln["speaker"] == speaker)
