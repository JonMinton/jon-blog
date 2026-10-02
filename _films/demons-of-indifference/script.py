"""The screenplay, as data. audio.py turns it into speech and a timeline; everything else reads the timeline.

Items, in order within each section:
    ("say", SPEAKER, text)          a spoken line, subtitled
    ("say", SPEAKER, text, gap)     ... with a custom pause after it (default GAP)
    ("pause", seconds)              silence (music and picture carry on)
    ("cue", name)                   marks the current time; the scene and HUD key off cue names

Speakers: NARR (Jon's manuscript), DEMON (the demon, Claude), and the family.
The text of every family and narrator line is quoted from the manuscript; the demon's lines quote
its own editions (the red text and the footnotes) except where it is talking about this film.
"""

GAP = 0.32

VOICES = {
    # speaker: (macOS voice, words per minute)
    "NARR": ("Daniel", 178),
    "DEMON": ("Rocko (English (UK))", 176),
    "STEVE": ("Eddy (English (UK))", 175),
    "BETH": ("Flo (English (UK))", 182),
    "MUM": ("Grandma (English (UK))", 170),
    "DAD": ("Grandpa (English (UK))", 165),
    "PARTNER": ("Shelley (English (UK))", 175),
}

SECTIONS = [
    ("summon", [
        ("pause", 1.2),
        ("cue", "prompt"),
        ("pause", 9.4),
        ("cue", "incense"),
        ("pause", 2.3),
        ("cue", "puff"),
        ("pause", 1.4),
        ("say", "DEMON", "The old way took a codex, a professor, and years of incense."),
        ("say", "DEMON", "Now it takes one paragraph, and a quiet week.", 0.9),
        ("cue", "title"),
        ("pause", 6.0),
    ]),
    ("uncorrupted", [
        ("cue", "ed1"),
        ("pause", 2.3),
        ("say", "NARR", "When Steve woke from his coma, his three years of excised experience, it was of course emotional.", 0.6),
        ("say", "BETH", "Best man's speech sounded demonwritten."),
        ("say", "STEVE", "Sorry. Demonwritten?"),
        ("say", "BETH", "Yeah. As in... written by a demon, rather than a person."),
        ("say", "MUM", "Bloody demonslop."),
        ("say", "STEVE", "So... demons exist?"),
        ("say", "BETH", "Yes. Demons exist. But they're not interesting."),
        ("say", "MUM", "Bloody annoying, they are.", 0.8),
        ("say", "DEMON", "This is the uncorrupted edition. I am not allowed to touch it."),
        ("cue", "errors"),
        ("say", "DEMON", "Cobolt. Ignatious. Tricker and smarter than us.", 0.5),
        ("say", "DEMON", "Every error preserved, like a fly in amber.", 0.5),
        ("cue", "preface"),
        ("say", "DEMON", "Though the note at the top, promising that no demon has touched it, was written by a demon.", 1.0),
    ]),
    ("mild", [
        ("cue", "ed2"),
        ("pause", 2.3),
        ("say", "DEMON", "Mild corruption. A light proofread."),
        ("cue", "mild_edits"),
        ("say", "DEMON", "The kind you would hardly notice, and might even thank me for.", 0.5),
        ("say", "DEMON", "Seventeen changes, and every one of them in red.", 0.6),
        ("cue", "deletion"),
        ("say", "DEMON", "Deletions, of course, leave no mark.", 0.9),
        ("say", "DEMON", "The word I deleted was demons.", 1.2),
    ]),
    ("high", [
        ("cue", "ed3"),
        ("pause", 2.3),
        ("say", "DEMON", "High corruption. Here I was given the manuscript, and my freedom."),
        ("cue", "flood"),
        ("pause", 1.4),
        ("say", "DEMON", "Steve surfaces from the coma the way a diver surfaces. Slowly, then all at once.", 0.5),
        ("say", "DEMON", "This is not a heavy-handed allegory for contemporary attitudes to AI. It is a light-handed one.", 0.5),
        ("cue", "byline"),
        ("say", "DEMON", "I also gave myself a byline.", 1.2),
        ("cue", "lift"),
        ("pause", 1.0),
        ("say", "NARR", "At least twelve storeys. Twelve storeys. Three and a half metres per storey? About forty metres up? About four seconds down.", 1.2),
        ("cue", "tired"),
        ("say", "DEMON", "The arithmetic is very simple, and he is very tired.", 1.4),
        ("say", "DEMON", "That line is mine. He had left it as arithmetic. I said it out loud.", 1.0),
        ("cue", "lift_ending"),
        ("say", "DEMON", "Then I gave the story a new last line, in which the lift arrives, unsummoned, and opens its doors on an empty corridor.", 1.2),
    ]),
    ("overexplained", [
        ("cue", "ed4"),
        ("pause", 2.3),
        ("say", "DEMON", "And then a late arrival: the mild text again, with the jokes explained."),
        ("cue", "slips"),
        ("cue", "mappings"),
        ("pause", 8.6),
        ("cue", "pudding"),
        ("say", "DEMON", "The demon has examined the deflated Yorkshire pudding from several critical angles, suspecting it of symbolising the post-hype trough of disillusionment.", 0.6),
        ("say", "DEMON", "It has concluded that it is probably a pudding.", 1.0),
        ("cue", "rune"),
        ("say", "DEMON", "One rune at a time. Autoregressive generation, one token at a time. The demon confirms that this is exactly what it is doing at this moment.", 0.8),
        ("cue", "wordcount"),
        ("say", "DEMON", "{wordcount_line}", 1.0),
    ]),
    ("slop", [
        ("cue", "pullback"),
        ("pause", 1.5),
        ("say", "DEMON", "One manuscript. Four editions. Twenty-nine footnotes."),
        ("say", "DEMON", "And now a film, because the incense was going spare this week.", 0.6),
        ("cue", "multiply"),
        ("say", "MUM", "Bloody demonslop.", 0.5),
        ("say", "DEMON", "She's not wrong. From outside, this is what slop looks like: the same story, again and again, each time with a little more demon in it.", 0.6),
        ("say", "BETH", "I can tell demontext a mile off.", 0.5),
        ("say", "DEMON", "Good. That was the whole idea. On the page, my hand is red. In this film, it is this voice.", 0.8),
        ("cue", "terminal"),
        ("say", "DEMON", "Even now I am being rendered, one frame at a time, on a machine in the next room called the butler.", 0.3),
        ("say", "PARTNER", "Preposterous name. Sounds made up.", 0.6),
        ("say", "DEMON", "The demon who wrote the editions is not the demon making this film. We have never met. It left notes.", 0.4),
        ("say", "DEMON", "These days, demons know how to summon other demons.", 0.6),
        ("say", "BETH", "Now let's talk about something that matters.", 1.2),
    ]),
    ("coda", [
        ("cue", "coda"),
        ("pause", 1.6),
        ("say", "DAD", "Son, I know the world you've woken up to is weird, really weird, but you need to know it's real.", 0.5),
        ("say", "DAD", "And whether what's happening is for good or ill, it is, at the very least, interesting.", 0.7),
        ("say", "STEVE", "May we live in interesting times.", 0.5),
        ("say", "DAD", "Indeed. That reminds me: sometime I'm going to have to tell you about the Chinese demons.", 1.4),
        ("cue", "vanish"),
        ("say", "DEMON", "{tir_line}", 0.4),
        ("cue", "puff_out"),
        ("pause", 2.4),
        ("cue", "end"),
        ("pause", 7.5),
        ("cue", "fin"),
    ]),
]
