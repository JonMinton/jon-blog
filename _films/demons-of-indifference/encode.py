"""Encode frames plus the mix to H.264/AAC with Blender's sequencer (the butler has no ffmpeg).

    blender -b --factory-startup -P encode.py -- build/final build/mix.wav out.mp4 [fps] [width height]
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[sys.argv.index("--") + 1:]
src, wav, dst = (os.path.join(HERE, a) for a in args[:3])
fps = int(args[3]) if len(args) > 3 else 24
w, h = (int(args[4]), int(args[5])) if len(args) > 5 else (1920, 1080)
files = sorted(f for f in os.listdir(src) if f.endswith(".png") or f.endswith(".jpg"))
scene = bpy.context.scene
scene.render.fps = fps
scene.render.resolution_x, scene.render.resolution_y = w, h
scene.render.resolution_percentage = 100
se = scene.sequence_editor_create()
coll = se.strips if hasattr(se, "strips") else se.sequences
strip = coll.new_image("frames", os.path.join(src, files[0]), 1, 1)
for f in files[1:]:
    strip.elements.append(f)
coll.new_sound("mix", wav, 2, 1)
scene.frame_start, scene.frame_end = 1, len(files)
ims = scene.render.image_settings
if hasattr(ims, "media_type"):
    ims.media_type = "VIDEO"
ims.file_format = "FFMPEG"
ff = scene.render.ffmpeg
ff.format = "MPEG4"
ff.codec = "H264"
ff.constant_rate_factor = "HIGH"
ff.ffmpeg_preset = "GOOD"
ff.audio_codec = "AAC"
ff.audio_bitrate = 192
ff.audio_channels = "STEREO"
ff.audio_mixrate = 48000
scene.render.filepath = dst
scene.render.use_file_extension = False
bpy.ops.render.render(animation=True)
