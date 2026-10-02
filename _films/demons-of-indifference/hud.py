"""Overlays over the rendered frames: subtitles, the spell, the clock, edition cards, counters,
the footnote mappings, the live render log, the title and end cards; plus bloom, grain and fades.

    python hud.py build/frames build/final [--only 300,1200]
"""
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beats as B  # noqa: E402

W, H = 1920, 1080
FPS = B.FPS
SANS = "/System/Library/Fonts/Avenir Next.ttc"
SERIF = "/System/Library/Fonts/NewYork.ttf"
BASK = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
MONO = "/System/Library/Fonts/Menlo.ttc"
DEMON = os.path.join(HERE, "fonts", "MedievalSharp-Regular.ttf")
WHITE = (238, 236, 230)
GREY = (150, 152, 160)
RED = (255, 107, 107)       # the blog's dark-mode demon red
DEEP = (164, 19, 60)
AMBER = (255, 196, 60)
GREEN = (120, 220, 140)

_f = {}
SCALE = 1


def font(path, size, index=0):
    k = (path, size, index)
    if k not in _f:
        _f[k] = ImageFont.truetype(path, size, index=index)
    return _f[k]


def sans(size, bold=False):
    return font(SANS, size, 2 if bold else 7)


def demon(size):
    return font(DEMON, size)


def a8(alpha):
    return int(255 * max(0.0, min(1.0, alpha)))


def fade(t, a, b, fi=0.3, fo=0.3):
    """1 inside [a, b], ramping in over fi and out over fo."""
    if t < a or t > b:
        return 0.0
    return min(B.smooth(a, a + fi, t) if fi else 1.0, 1 - B.smooth(b - fo, b, t) if fo else 1.0)


def wrap(text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f.getlength(trial) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def shadow_text(layer, xy, s, f, fill, alpha, anchor="la", blur=6, spread=2):
    """Text with a soft dark halo so it reads over anything."""
    sh = Image.new("L", (W, H), 0)
    ds = ImageDraw.Draw(sh)
    ds.text(xy, s, font=f, fill=a8(alpha * 0.9), anchor=anchor, stroke_width=spread)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    black.putalpha(sh)
    layer.alpha_composite(black)
    ImageDraw.Draw(layer).text(xy, s, font=f, fill=(*fill, a8(alpha)), anchor=anchor)


# ---------------------------------------------------------------- elements

def subtitles(layer, t):
    ln = B.line_at(t)
    if ln is None:
        return
    a = fade(t, ln["start"] - 0.05, ln["end"] + 0.15, 0.12, 0.2)
    sp, text = ln["speaker"], ln["text"]
    if sp == "DEMON":
        f, fill = demon(46), RED
    elif sp == "NARR":
        f, fill = font(SANS, 40, 4), WHITE  # italic: the manuscript's own voice
    else:
        f, fill = sans(40), WHITE
    lines = wrap(text, f, 1380)
    lh = int(f.size * 1.32)
    y = H - 70 - lh * (len(lines) - 1)
    wmax = max(f.getlength(s) for s in lines)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(band).rounded_rectangle((W // 2 - wmax / 2 - 28, y - lh + 4, W // 2 + wmax / 2 + 28,
                                            y + lh * (len(lines) - 1) + 22), radius=16,
                                           fill=(6, 6, 10, a8(a * 0.8)))
    layer.alpha_composite(band.filter(ImageFilter.GaussianBlur(3)))
    if sp not in ("DEMON", "NARR"):
        tag = {"PARTNER": "STEVE'S PARTNER"}.get(sp, sp)
        shadow_text(layer, (W // 2, y - lh + 6), tag, sans(22, True), GREY, a, anchor="ms")
    for i, s in enumerate(lines):
        shadow_text(layer, (W // 2, y + i * lh), s, f, fill, a, anchor="ms")


def spell(layer, t):
    """The prompt, typed in a terminal, on black."""
    a0 = B.cue("prompt")
    a = fade(t, a0 - 0.2, B.cue("incense") + 0.4, 0.5, 0.9)
    if a <= 0:
        return
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = 300, 250, 1620, 800
    d.rounded_rectangle((x0, y0, x1, y1), radius=14, fill=(14, 14, 18, a8(a * 0.96)),
                        outline=(70, 70, 80, a8(a)), width=2)
    for k, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse((x0 + 22 + 26 * k, y0 + 20, x0 + 38 + 26 * k, y0 + 36), fill=(*c, a8(a)))
    d.text(((x0 + x1) // 2, y0 + 28), "claude — ~/repos/quarto-blog/jon-blog", font=font(MONO, 20),
           fill=(*GREY, a8(a)), anchor="mm")
    shadow_text(layer, (x0, y0 - 40), "The spell, as cast", demon(44), RED, a)
    d.text((x1, y0 - 40), "2 October 2026", font=sans(26), fill=(*GREY, a8(a)), anchor="ra")
    n = B.typed_chars(t)
    f = font(MONO, 27)
    lines = wrap(B.PROMPT[:n], f, x1 - x0 - 140) if n else [""]
    y = y0 + 90
    for i, s in enumerate(lines):
        if i == 0:
            d.text((x0 + 40, y), ">", font=f, fill=(*RED, a8(a)))
        d.text((x0 + 80, y), s, font=f, fill=(*WHITE, a8(a)))
        y += 40
    if int(t * 2.2) % 2 == 0 or n < len(B.PROMPT):
        cx = x0 + 80 + f.getlength(lines[-1]) + 4
        d.rectangle((cx, y - 40 + 4, cx + 14, y - 40 + 34), fill=(*WHITE, a8(a)))


def tir(layer, t):
    p = B.cue("puff")
    end = B.cue("puff_out")
    if t < p:
        return
    a = fade(t, p + 0.6, end + 2.6, 0.8, 1.2)
    if a <= 0:
        return
    el = min(t, end) - p
    h, rem = divmod(el, 3600)
    m, s = divmod(rem, 60)
    cs = int((el % 1) * 100)
    d = ImageDraw.Draw(layer)
    shadow_text(layer, (W - 60, 52), "TIME IN REALM", sans(20, True), GREY, a * 0.9, anchor="ra")
    shadow_text(layer, (W - 60, 78), f"{int(h):02d}:{int(m):02d}:{int(s):02d}.{cs:02d}", font(MONO, 34),
                WHITE if t < end else RED, a, anchor="ra")


EDITIONS = [
    ("ed1", "EDITION I", "Uncorrupted", "Jon's manuscript, exactly as written."),
    ("ed2", "EDITION II", "Mild Corruption", "A light proofread."),
    ("ed3", "EDITION III", "High Corruption", "The demon, given the manuscript and its freedom."),
    ("ed4", "EDITION IV", "Mild Corruption (Overexplained)", "The jokes, explained."),
]


def edition_card(layer, t):
    for cue, num, name, desc in EDITIONS:
        c = B.cue(cue)
        a = fade(t, c + 0.2, c + 5.2, 0.6, 0.9)
        if a <= 0:
            continue
        slide = 30 * (1 - B.smooth(c + 0.2, c + 1.0, t))
        shadow_text(layer, (80 - slide, 70), num, sans(24, True), RED, a)
        shadow_text(layer, (80 - slide, 102), name, font(SERIF, 64), WHITE, a)
        shadow_text(layer, (82 - slide, 184), desc, font(BASK, 32, 2), GREY, a)


def counter(layer, t):
    """Bottom-right: how much of the page is the demon's."""
    st = B.tl()["stats"]
    secs = B.tl()["sections"]
    rows = None
    for name, key in (("uncorrupted", "ed1"), ("mild", "ed2"), ("high", "ed3"), ("overexplained", "ed4")):
        a0, a1 = secs[name]
        if a0 <= t < a1:
            a = fade(t, B.cue(key) + 1.0, a1 + 0.3, 0.6, 0.6)
            if name == "uncorrupted":
                rows = [("DEMON EDITS", "0", WHITE), ("WORDS IN RED", "0", WHITE)]
            elif name == "mild":
                n = sum(1 for x in B.mild_edit_times() if x <= t)
                w = round(st["mild"]["demon_words"] * n / 17)
                rows = [("DEMON EDITS", f"{n}", RED if n else WHITE), ("WORDS IN RED", f"{w}", RED if w else WHITE)]
            elif name == "high":
                f0, f1 = B.flood_window()
                u = B.clamp((t - f0) / (f1 - f0))
                n = int(round(153 * u ** 0.9)) if t >= f0 else 0
                w = int(round(st["high"]["demon_words"] * u)) if t >= f0 else 0
                rows = [("DEMON EDITS", f"{n}", RED if n else WHITE), ("WORDS IN RED", f"{w}", RED if w else WHITE)]
            else:
                k = sum(1 for x in B.slip_times() if x <= t)
                fw = int(round(st["over"]["footnote_words"] * k / 29))
                rows = [("DEMON EDITS", "17", RED), ("FOOTNOTES", f"{k}", RED if k else WHITE),
                        ("WORDS IN RED", f"{16 + fw:,}", RED)]
            break
    if not rows or a <= 0:
        return
    y = H - 200 - 62 * (len(rows) - 2)
    for label, val, col in rows:
        shadow_text(layer, (W - 60, y), label, sans(19, True), GREY, a, anchor="ra")
        shadow_text(layer, (W - 60, y + 24), val, font(MONO, 32), col, a, anchor="ra")
        y += 62


def mappings(layer, t):
    ts = B.mapping_times()
    a = fade(t, ts[0][0] - 0.2, B.cue("pudding") + 0.6, 0.4, 0.8)
    if a <= 0:
        return
    d = ImageDraw.Draw(layer)
    x0, y0 = 70, 250
    d.rounded_rectangle((x0 - 30, y0 - 70, x0 + 900, y0 + 9 * 58 + 20), radius=14,
                        fill=(8, 8, 14, a8(a * 0.72)))
    shadow_text(layer, (x0, y0 - 52), "WHAT THE FOOTNOTES SAY IT MEANS", sans(20, True), GREY, a)
    for i, ((left, right), (s, _)) in enumerate(zip(B.MAPPINGS, ts)):
        if t < s:
            break
        b = a * B.smooth(s, s + 0.35, t)
        y = y0 + i * 58
        d.text((x0, y), left, font=sans(30), fill=(*WHITE, a8(b)))
        lx = x0 + sans(30).getlength(left) + 16
        d.text((lx, y + 2), "→", font=sans(30), fill=(*GREY, a8(b)))
        d.text((lx + 46, y - 2), right, font=demon(34), fill=(*RED, a8(b)))


def wordcount(layer, t):
    c = B.cue("wordcount")
    a = fade(t, c + 0.2, B.cue("pullback") + 0.5, 0.5, 0.6)
    if a <= 0:
        return
    st = B.tl()["stats"]
    story, notes = st["mild"]["story_words"], st["over"]["footnote_words"]
    g1 = B.smooth(c + 0.3, c + 1.6, t)
    g2 = B.smooth(c + 2.6, c + 4.2, t)
    d = ImageDraw.Draw(layer)
    x0, y0, full = 560, 600, 800
    d.rounded_rectangle((x0 - 40, y0 - 80, x0 + full + 260, y0 + 160), radius=14, fill=(8, 8, 14, a8(a * 0.7)))
    for i, (label, n, col, g, f) in enumerate((("Story", story, WHITE, g1, sans(30)),
                                               ("Footnotes", notes, RED, g2, demon(32)))):
        y = y0 + i * 100
        d.text((x0, y - 44), label, font=f, fill=(*col, a8(a)))
        w = full * n / story * g
        d.rectangle((x0, y, x0 + w, y + 26), fill=(*col, a8(a * 0.9)))
        d.text((x0 + w + 16, y - 6), f"{int(n * g):,} words", font=font(MONO, 26), fill=(*col, a8(a)))


def editions_tally(layer, t):
    m0, m1 = B.multiply_window()
    a = fade(t, m0, B.cue("coda") + 1.0, 0.4, 1.0)
    if a <= 0:
        return
    u = B.clamp((t - m0) / (m1 - m0)) ** 1.25
    n = 4 + int(round(100 * u))
    shadow_text(layer, (80, 70), "EDITIONS", sans(24, True), GREY, a)
    shadow_text(layer, (80, 100), f"{n}", font(MONO, 64), RED if n > 4 else WHITE, a)


def terminal(layer, t, frame):
    c = B.cue("terminal")
    a = fade(t, c + 0.1, B.cue("coda") - 0.3, 0.4, 0.8)
    if a <= 0:
        return
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = 60, 610, 980, 900
    d.rounded_rectangle((x0, y0, x1, y1), radius=12, fill=(10, 10, 14, a8(a * 0.88)),
                        outline=(70, 70, 80, a8(a)), width=2)
    f = font(MONO, 21)
    N = B.n_frames()
    rows = [("claudejonathansonbutlerbot@butler ~/demons-film % ./render.sh", GREY),
            ("Blender 5.2.2 LTS (EEVEE, Metal)", GREY)]
    for k in range(4, 0, -1):
        if frame - k >= 0:
            rows.append((f"Saved: 'build/frames/{frame - k:05d}.png'", GREY))
    rows.append((f"Fra:{frame} | Rendering | Sample {1 + (frame * 7) % 24}/24", WHITE))
    y = y0 + 20
    for s, col in rows[-7:]:
        d.text((x0 + 24, y), s, font=f, fill=(*col, a8(a)))
        y += 30
    # progress bar: this frame, of this film
    bx0, bx1, by = x0 + 24, x1 - 24, y1 - 40
    d.rectangle((bx0, by, bx1, by + 14), outline=(*GREY, a8(a)), width=1)
    d.rectangle((bx0 + 2, by + 2, bx0 + 2 + (bx1 - bx0 - 4) * frame / N, by + 12), fill=(*RED, a8(a)))
    d.text((bx1, by - 30), f"frame {frame:,} of {N:,}", font=f, fill=(*WHITE, a8(a)), anchor="ra")


def title_card(layer, t):
    c = B.cue("title")
    a = fade(t, c + 0.3, B.cue("ed1") + 0.3, 1.0, 0.9)
    if a <= 0:
        return
    shadow_text(layer, (W // 2, 420), "The Demons of Indifference", font(SERIF, 104), WHITE, a, anchor="mm",
                blur=12, spread=4)
    b = a * B.smooth(c + 1.6, c + 2.6, t)
    shadow_text(layer, (W // 2, 530), "in four editions", demon(60), RED, b, anchor="mm", blur=10, spread=3)
    e = a * B.smooth(c + 2.4, c + 3.4, t)
    shadow_text(layer, (W // 2, 640), "Being not in any way a heavy-handed allegory for contemporary attitudes to AI",
                font(BASK, 34, 2), GREY, e, anchor="mm")


def end_card(layer, t):
    c = B.cue("end")
    a = B.smooth(c, c + 1.2, t)
    if a <= 0:
        return
    out = 1 - B.smooth(B.cue("fin") - 0.8, B.cue("fin"), t)
    d = ImageDraw.Draw(layer)
    d.rectangle((0, 0, W, H), fill=(0, 0, 0, a8(a * 0.82)))
    rows = [
        (c + 0.8, 330, "The Demons of Indifference", font(SERIF, 76), WHITE),
        (c + 1.6, 430, "A story by Jon Minton, published in four editions.", font(BASK, 36, 2), WHITE),
        (c + 2.4, 520, "Demon hand: Claude Fable 5 (the editions) and Claude Opus 5.5 (this film)", sans(28), GREY),
        (c + 2.9, 566, "Voices: macOS text-to-speech.  Rendered in Blender, on the butler.", sans(28), GREY),
        (c + 4.2, 700, "Deletions, of course, leave no mark.", demon(48), RED),
    ]
    for t0, y, s, f, col in rows:
        b = a * out * B.smooth(t0, t0 + 0.8, t)
        if b > 0:
            d.text((W // 2, y), s, font=f, fill=(*col, a8(b)), anchor="mm")


# ---------------------------------------------------------------- post

def bloom(a):
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    mask = np.clip((lum - 0.9) / 0.1, 0, 1)[..., None]
    bright = Image.fromarray((a * mask * 255).astype(np.uint8))
    small = bright.resize((W // 4, H // 4), Image.BILINEAR)
    b1 = np.asarray(small.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR), dtype=np.float32)
    b2 = np.asarray(small.filter(ImageFilter.GaussianBlur(12)).resize((W, H), Image.BILINEAR), dtype=np.float32)
    return a + (b1 * 0.10 + b2 * 0.16) / 255.0


_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIGNETTE = (1 - 0.42 * (((_xx - W / 2) / (W / 2)) ** 2 + ((_yy - H / 2) / (H / 2)) ** 2) ** 1.4)[..., None]
VIGNETTE = np.clip(VIGNETTE, 0.35, 1).astype(np.float32)


def black_level(t):
    """How much of the picture is black: the spell opens on black; the film ends on it."""
    inc = B.cue("incense")
    k = 1 - B.smooth(inc + 0.1, inc + 1.4, t)
    k = max(k, B.smooth(B.cue("fin") - 0.6, B.cue("fin"), t))
    return k


def process(args):
    src, dst, frame, scale = args
    t = frame / FPS
    if os.path.exists(src):
        img = Image.open(src).convert("RGB")
        if img.size != (W, H):
            img = img.resize((W, H), Image.BICUBIC)
    else:
        img = Image.new("RGB", (W, H), (0, 0, 0))
    a = np.asarray(img).astype(np.float32) / 255.0
    a = bloom(a) * VIGNETTE
    rng = np.random.default_rng(frame)
    a += rng.normal(0, 0.012, (H, W, 1)).astype(np.float32)
    a *= 1 - black_level(t)
    base = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    spell(layer, t)
    title_card(layer, t)
    tir(layer, t)
    edition_card(layer, t)
    counter(layer, t)
    mappings(layer, t)
    wordcount(layer, t)
    editions_tally(layer, t)
    terminal(layer, t, frame)
    end_card(layer, t)
    subtitles(layer, t)
    base.alpha_composite(layer)
    out = base.convert("RGB")
    if scale != 1:
        out = out.resize((int(W * scale), int(H * scale)), Image.BILINEAR)
    out.save(dst)
    return frame


def main():
    src_dir, dst_dir = sys.argv[1], sys.argv[2]
    os.makedirs(dst_dir, exist_ok=True)
    only = None
    global SCALE
    step = int(sys.argv[sys.argv.index("--step") + 1]) if "--step" in sys.argv else 1
    if "--scale" in sys.argv:
        SCALE = float(sys.argv[sys.argv.index("--scale") + 1])
    if "--only" in sys.argv:
        only = [int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")]
    frames = only if only else range(0, B.n_frames(), step)
    jobs = []
    for f in frames:
        src = os.path.join(src_dir, f"{f:04d}.png")
        if not os.path.exists(src):
            src = os.path.join(src_dir, f"{f:05d}.png")
        if not os.path.exists(src):
            src = os.path.join(src_dir, f"still_{f:05d}.png")
        jobs.append((src, os.path.join(dst_dir, f"{f:05d}.png"), f, SCALE))
    with ProcessPoolExecutor() as ex:
        for i, _ in enumerate(ex.map(process, jobs, chunksize=4)):
            if i % 500 == 0:
                print("hud", i, flush=True)


if __name__ == "__main__":
    main()
