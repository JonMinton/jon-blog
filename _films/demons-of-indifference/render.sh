#!/bin/zsh
# Full pipeline on the butler: scene -> build/frames, HUD -> build/final, encode -> the film.
# (audio.py and pages.py run on the laptop first: they need the blog's .qmd files.)
set -e
cd "$(dirname "$0")"
BLENDER=/opt/homebrew/bin/blender
PY=~/miniconda/bin/python
$BLENDER -b --factory-startup -P build_scene.py -- --out build/frames 2>&1 | grep -E "Error|Traceback|done|Saved: .*00\.png"
$PY hud.py build/frames build/final
$BLENDER -b --factory-startup -P encode.py -- build/final build/mix.wav demons-of-indifference.mp4 2>&1 | tail -3
ls -la demons-of-indifference.mp4
