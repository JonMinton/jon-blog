"""Page textures for the four tablets, in every state the film needs, plus the 29 footnote slips.

    python3 pages.py        # laptop: reads the blog's .qmd files through editions.py

The look follows Jon's manuscript (a reMarkable export): pale e-paper, a dot grid, a plain sans.
The demon's hand is red MedievalSharp, as on the blog. Every passage is quoted from the editions.
"""
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import editions as E  # noqa: E402

OUT = os.path.join(HERE, "build", "pages")
os.makedirs(OUT, exist_ok=True)

PW, PH = 1500, 2000
MARGIN = 125
PAPER = (241, 240, 235)
INK = (28, 28, 30)
RED = (164, 19, 60)
DOT = (196, 196, 192)
AMBER = (255, 196, 60)
BLUE = (13, 110, 253)

SANS = "/System/Library/Fonts/Avenir Next.ttc"
SERIF = "/System/Library/Fonts/NewYork.ttf"
DEMON = os.path.join(HERE, "fonts", "MedievalSharp-Regular.ttf")
_f = {}
ANCHOR_WANT = {"cobolt": "cobolt", "Ignatious": "Ignatious", "tricker": "tricker", "note": "demon",
               "turns": "turns", "byline": "Minton", "tired": "arithmetic", "ending": "unsummoned",
               "joss": "Joss", "wrong": "Wrong", "storeys": "storeys"}
ANCHORS = {}
CURRENT = [None]


def font(path, size, index=0):
    k = (path, size, index)
    if k not in _f:
        _f[k] = ImageFont.truetype(path, size, index=index)
    return _f[k]


def sans(size):
    return font(SANS, size, 5)  # Avenir Next Medium


def sans_bold(size):
    return font(SANS, size, 0)


def paper():
    im = Image.new("RGB", (PW, PH), PAPER)
    d = ImageDraw.Draw(im)
    for y in range(40, PH, 46):
        for x in range(40, PW, 46):
            d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=DOT)
    return im


# ---------------------------------------------------------------- text layout

def runs_from(markup):
    """Markup (with [..]{.demon} and [^claude-..]) to runs (text, demon, fnid)."""
    markup = markup.replace("*", "")
    return E.tokens(markup)


class Layout:
    def __init__(self, size=46, lead=1.5):
        self.size = size
        self.lead = lead
        self.f_plain = sans(size)
        self.f_demon = font(DEMON, int(size * 1.08))
        self.f_sup = font(DEMON, int(size * 0.62))
        self.space = self.f_plain.getlength(" ")

    def fnt(self, style):
        return {"plain": self.f_plain, "demon": self.f_demon, "sup": self.f_sup}[style]

    def words(self, runs, fnums):
        """Group runs into unbreakable words of styled segments."""
        words, cur = [], []
        for text, demon, fnid in runs:
            if fnid:
                cur.append((str(fnums.setdefault(fnid, len(fnums) + 1)), "sup"))
                continue
            style = "demon" if demon else "plain"
            for piece in re.split(r"(\s+)", text):
                if piece == "":
                    continue
                if piece.isspace():
                    if cur:
                        words.append(cur)
                        cur = []
                else:
                    cur.append((piece, style))
        if cur:
            words.append(cur)
        return words

    def width(self, word):
        return sum(self.fnt(st).getlength(tx) for tx, st in word)

    def place(self, paras, x0, y0, w, fnums=None, para_gap=0.55):
        """Returns placed segments [(x, y, text, style)] and the final y."""
        fnums = {} if fnums is None else fnums
        lh = self.size * self.lead
        placed = []
        y = y0
        for runs in paras:
            x = x0
            for word in self.words(runs, fnums):
                ww = self.width(word)
                if x > x0 and x + ww > x0 + w:
                    x = x0
                    y += lh
                for tx, st in word:
                    placed.append((x, y, tx, st))
                    x += self.fnt(st).getlength(tx)
                x += self.space
            y += lh * (1 + para_gap)
        return placed, y

    def draw(self, d, placed, red=RED, ink=INK, highlight=(), hcol=AMBER):
        for x, y, tx, st in placed:
            for key, sub in ANCHOR_WANT.items():
                if key not in ANCHORS.setdefault(CURRENT[0], {}) and sub in tx:
                    ANCHORS[CURRENT[0]][key] = (round(x), round(y))
        for x, y, tx, st in placed:
            if any(h in tx for h in highlight):
                f = self.fnt(st)
                l, t, r, b = d.textbbox((x, y), tx, font=f, anchor="ls")
                d.rounded_rectangle((l - 8, t - 6, r + 8, b + 10), radius=10, fill=hcol)
        for x, y, tx, st in placed:
            f = self.fnt(st)
            if st == "sup":
                d.text((x + 2, y - self.size * 0.45), tx, font=f, fill=red, anchor="ls")
            else:
                d.text((x, y), tx, font=f, fill=red if st == "demon" else ink, anchor="ls")


def callout(d, lay, y, markup, demon=False):
    """A Quarto 'callout-note' box, as at the top of each edition."""
    x0, w = MARGIN, PW - 2 * MARGIN
    runs = runs_from(markup)
    if demon:
        runs = [(t, True, f) for t, _, f in runs]
    placed, y1 = lay.place([runs], x0 + 40, y + 70, w - 70, para_gap=0)
    d.rectangle((x0, y, x0 + w, y1 - 10), outline=(200, 200, 200), width=2)
    d.rectangle((x0, y, x0 + 9, y1 - 10), fill=BLUE)
    lay.draw(d, placed)
    return y1 + 40


def page(name, blocks, title=None, byline=None, size=54, highlight=()):
    """blocks: list of markup paragraphs; '…' alone is an ellipsis separator."""
    CURRENT[0] = name
    im = paper()
    d = ImageDraw.Draw(im)
    y = 190
    if title:
        d.text((MARGIN, y), title, font=font(SERIF, 86), fill=INK, anchor="ls")
        y += 70
        if byline:
            lay = Layout(40, 1.4)
            placed, y = lay.place([runs_from(byline)], MARGIN, y + 20, PW - 2 * MARGIN, para_gap=0)
            lay.draw(d, placed)
        y += 30
    lay = Layout(size)
    fnums = {}
    paras = []
    for b in blocks:
        if isinstance(b, tuple) and b[0] == "callout":
            if paras:
                placed, y = lay.place(paras, MARGIN, y, PW - 2 * MARGIN, fnums)
                lay.draw(d, placed, highlight=highlight)
                paras = []
            y = callout(d, Layout(44, 1.45), y, b[1], demon=b[2])
            y += 40
            continue
        paras.append(runs_from(b))
    placed, y = lay.place(paras, MARGIN, y + lay.size, PW - 2 * MARGIN, fnums)
    lay.draw(d, placed, highlight=highlight)
    im.save(os.path.join(OUT, name + ".png"))
    return im, y, fnums


def excerpt(markup, start=None, end=None):
    """Cut a paragraph between two anchor strings (inclusive), adding ellipses at the cuts."""
    a = markup.index(start) if start else 0
    b = markup.index(end) + len(end) if end else len(markup)
    s = markup[a:b]
    return ("… " if a > 0 else "") + s + (" …" if b < len(markup) else "")


def footnote_page(name, base_blocks, fns, size=50):
    """The overexplained page: the story shrinks to the top, the footnotes take the rest."""
    im, y, fnums = page(name + "_tmp", base_blocks, size=size)
    ANCHORS[name] = ANCHORS.pop(name + "_tmp", {})
    os.remove(os.path.join(OUT, name + "_tmp.png"))
    d = ImageDraw.Draw(im)
    y += 10
    d.line((MARGIN, y, MARGIN + 380, y), fill=RED, width=3)
    y += 30
    lay = Layout(30, 1.36)
    order = sorted(fnums.items(), key=lambda kv: kv[1])
    bodies = dict(fns)
    for fid, n in order:
        paras = [[(f"{n}. ", True, None), (bodies[fid], True, None)]]
        placed, y2 = lay.place(paras, MARGIN, y + lay.size, PW - 2 * MARGIN, para_gap=0.2)
        lay.draw(d, placed)
        y = y2
        if y > PH - 60:
            break
    im.save(os.path.join(OUT, name + ".png"))


def slip(i, fid, body):
    w, h = 620, 330
    im = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, h - 1), outline=(205, 200, 190), width=3)
    d.text((26, 52), f"[^{fid}]", font=font(DEMON, 34), fill=RED, anchor="ls")
    lay = Layout(26, 1.32)
    first = " ".join(body.split()[:34]) + " …"
    placed, _ = lay.place([[(first, True, None)]], 26, 100, w - 52, para_gap=0)
    lay.draw(d, placed)
    im.save(os.path.join(OUT, f"slip_{i:02d}.png"))


def main():
    U, M, H, O = "uncorrupted", "mild", "high", "over"

    # 1. Uncorrupted: the codex, Iggy, and the three preserved errors
    pre_u = ("**A note from the demon (Claude):** This edition reproduces Jon's manuscript exactly as "
             "written: no proofreading, no corrections, no improvements. No demon has touched the text below.")
    pre_u = pre_u.replace("**", "")
    p1 = [
        ("callout", pre_u, False),
        E.find(U, '"And at the end it had some suggested spells'),
        E.find(U, '"And he did, and it did."'),
        E.find(U, '"Oh," replies Steve\'s Dad.'),
        E.find(U, '"Preposterous name,"'),
        excerpt(E.find(U, '"Not quite. These days'), "Though he says"),
    ]
    page("p1", p1)
    page("p1_err", p1, highlight=("cobolt", "Ignatious", "tricker"))
    p1r = [("callout", pre_u, True)] + p1[1:]
    page("p1_pref", p1r)

    # 2. Mild: cobalt, the deleted "demons", trickier
    def p2(ed, para54):
        return [
            E.find(ed, '"And at the end it had some suggested spells'),
            E.find(ed if para54 == "mild" else U, '"Well, it turns out'),
            E.find(ed, 'A pause. No riposte.'),
            excerpt(E.find(ed, '"Not quite. These days'), "Though he says"),
        ]
    page("p2a", p2(U, U))
    page("p2b", p2(M, U))
    page("p2c", p2(M, "mild"))

    # 3. High: the opening, the byline, and the lift
    title = "The Demons of Indifference"
    page("p3a", [E.find(U, "When Steve woke"), E.find(U, "After the grogginess")],
         title=title, byline="Jon Minton")
    hi = [E.story(H)[0], E.find(H, "[Steve surfaces"), E.find(H, "After the grogginess")]
    page("p3b", hi, title=title, byline="Jon Minton")
    page("p3c", hi, title=title, byline="Jon Minton [& Claude Fable 5 (a demon)]{.demon}")
    lift = E.find(H, "*[How high is this building?]{.demon}*")
    hand = E.find(H, "Just then, Steve feels a hand")
    tired = "[The arithmetic is very simple, and he is very tired.]{.demon}"
    ending = E.story(H)[-1]
    page("p3d", [lift, hand])
    page("p3e", [lift, tired, hand])
    page("p3f", [lift, tired, hand, "…", ending])

    # 4. Overexplained: footnote markers, then the footnotes swallow the page
    p4 = [E.find(O, '"All millionaires now."'), E.find(O, '"Bloody Big Joss'), E.find(O, '"Yes. Joss stick'), E.find(O, '"It\'s just a big sloppy bubble."'),
          E.find(O, '"But it worked, after a fashion.'), E.find(O, '"Wrong way."')]
    page("p4a", [E.plain(p) for p in p4])
    page("p4b", p4)
    fns = E.footnotes()
    footnote_page("p4c", p4, fns)
    for i, (fid, body) in enumerate(fns):
        slip(i, fid, body)
    import json
    with open(os.path.join(HERE, "build", "anchors.json"), "w") as f:
        json.dump({"size": [PW, PH], "anchors": ANCHORS}, f, indent=1)
    print(json.dumps(ANCHORS))


if __name__ == "__main__":
    main()
