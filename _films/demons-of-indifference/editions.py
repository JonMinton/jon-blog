"""Read the four published editions straight from the blog's .qmd files.

Runs on the laptop (the butler has no copy of the blog). pages.py and audio.py use it; the
numbers it produces are written to build/editions.json for the HUD.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
POSTS = os.path.join(HERE, "..", "..", "posts", "fiction")
SLUGS = {
    "uncorrupted": "demons-of-indifference-uncorrupted",
    "mild": "demons-of-indifference-mild-corruption",
    "high": "demons-of-indifference-high-corruption",
    "over": "demons-of-indifference-mild-corruption-overexplained",
}

SPAN = re.compile(r"\[([^\]]*)\]\{\.demon\}")
FNREF = re.compile(r"\[\^(claude-[a-z0-9-]+)\]")


def raw(ed):
    with open(os.path.join(POSTS, SLUGS[ed], "index.qmd")) as f:
        return f.read()


def story(ed):
    """Body paragraphs after the preface callout, footnote definitions removed."""
    t = raw(ed)
    t = t.split("\n:::\n", 1)[1]
    paras = [p.strip() for p in t.split("\n\n") if p.strip()]
    return [p for p in paras if not p.startswith("[^")]


def footnotes(ed="over"):
    out = []
    for p in raw(ed).split("\n\n"):
        m = re.match(r"\[\^(claude-[a-z0-9-]+)\]:\s*(.*)", p.strip(), re.S)
        if m:
            body = m.group(2).replace("**Demon footnote (Claude):**", "").strip()
            out.append((m.group(1), body))
    return out


def plain(p):
    """Paragraph text with demon markup and footnote refs stripped."""
    return FNREF.sub("", SPAN.sub(lambda m: m.group(1), p))


def tokens(p):
    """Split a paragraph into (text, is_demon, footnote_id) runs."""
    out = []
    pos = 0
    pat = re.compile(r"\[([^\]]*)\]\{\.demon\}|\[\^(claude-[a-z0-9-]+)\]")
    for m in pat.finditer(p):
        if m.start() > pos:
            out.append((p[pos:m.start()], False, None))
        if m.group(1) is not None:
            out.append((m.group(1), True, None))
        else:
            out.append(("", True, m.group(2)))
        pos = m.end()
    if pos < len(p):
        out.append((p[pos:], False, None))
    return out


def find(ed, start):
    for p in story(ed):
        if plain(p).lstrip("*").startswith(start) or p.startswith(start):
            return p
    raise KeyError(f"{ed}: no paragraph starting {start!r}")


def words(s):
    return len(re.findall(r"[A-Za-z0-9'’-]+", s))


def stats():
    s = {}
    for ed in SLUGS:
        st = story(ed)
        s[ed] = {
            "story_words": sum(words(plain(p)) for p in st),
            "demon_spans": sum(len(SPAN.findall(p)) for p in st),
            "demon_words": sum(words(" ".join(SPAN.findall(p))) for p in st),
        }
    fns = footnotes()
    s["over"]["footnotes"] = len(fns)
    s["over"]["footnote_words"] = sum(words(b) for _, b in fns)
    return s


if __name__ == "__main__":
    print(json.dumps(stats(), indent=1))
