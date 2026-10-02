# The Demons of Indifference: the film

A 4th-wall mashup of the four editions of *The Demons of Indifference* (`posts/fiction/demons-of-indifference-*`),
and of the slop-based metacommentary of publishing one story four times. About 4:52, 1080p, 24 fps, with voices.

The set is a dark chapel with four lecterns in a row, one per edition. Each holds an e-paper tablet whose page
is set from the edition's actual text: the manuscript's dot grid and plain sans, with the demon's hand in red
MedievalSharp as on the blog. A foot-long cobalt-blue demon is summoned by Jon's prompt (shown as "the spell,
as cast"), visits each edition, makes its edits, and narrates in a ring-modulated voice. The family's lines are
quoted from the manuscript. In the slop section the lecterns multiply into the dark, each with its own small
demon, while a live render log shows the film being rendered on the butler. It ends where the story does,
with the Chinese demons, and a puff of sulphur.

| Section | Beat |
|---|---|
| Summon | The prompt typed on black; incense lit; the demon appears; title card |
| I. Uncorrupted | The "demons exist, but they're not interesting" exchange; the preserved errors highlighted; the "no demon has touched this" note turns out to be in demon hand |
| II. Mild | 17 edits land as red; the deleted word ("demons") vanishes without a mark |
| III. High | The page floods red; the demon's byline; the lift, and the demon owning the line it added |
| IV. Overexplained | 29 footnote slips fly out; what the footnotes say it means; the Yorkshire pudding; word counts |
| Slop | Lecterns multiply to 104 "editions"; the render log; "Preposterous name. Sounds made up." |
| Coda | Dad's speech, the Chinese demons, time in realm, end card |

## Pipeline

| File | Runs on | What it does |
|---|---|---|
| `script.py` | | The screenplay as data: lines, speakers, pauses, named cues |
| `editions.py` | laptop | Reads the four `.qmd` editions: paragraphs, demon spans, footnotes, word counts |
| `audio.py` | laptop | `say` for every line (the demon's voice ring-modulated), lays them end to end into `build/timeline.json`, synthesises the drone score and effects, writes `build/mix.wav` |
| `beats.py` | both | Loads the timeline and derives every shared schedule (edit scratches, slips, mappings), so sound and picture agree |
| `pages.py` | laptop | Page textures for each tablet state, the 29 footnote slips, and `build/anchors.json` (where key lines sit on each page, for the camera) |
| `build_scene.py` | butler | Blender 5.2: builds the set, the demon and every animation procedurally, renders frames (EEVEE, ~1.4 s a frame on the M4) |
| `hud.py` | butler | Subtitles, the spell, the time-in-realm clock, edition cards, counters, mappings, the render log, title and end cards; light bloom, vignette, grain |
| `encode.py` | butler | Blender's sequencer muxes frames and `mix.wav` to H.264/AAC (the butler has no ffmpeg) |
| `render.sh` | butler | `build_scene.py` → `hud.py` → `encode.py` |

```
python3 audio.py && python3 pages.py                      # laptop
rsync -a --exclude build/vox --exclude build/frames ./ claudejonathansonbutlerbot@butler.local:~/demons-film/
ssh claudejonathansonbutlerbot@butler.local 'cd ~/demons-film && ./render.sh'
```

Preview: `build_scene.py -- --preview --step 4 --out build/preview`, then `hud.py build/preview build/pfinal --step 4 --scale 0.5`
and `encode.py -- build/pfinal build/mix.wav preview.mp4 6 960 540`.

Stills for checking staging: `build_scene.py -- --stills 45,88.5,132 --out build/stills` (seconds).

Changing any line in `script.py` moves every cue after it: rerun `audio.py` and `pages.py` (anchors) before rendering.

`fonts/MedievalSharp-Regular.ttf` is from Google Fonts (SIL Open Font License), the same face the blog loads for demon script.
