"""The Demons of Indifference: build the whole scene procedurally in Blender 5.2 and render frames.

    blender -b --factory-startup -P build_scene.py -- [--preview] [--frames A B] [--stills 12.5,40,...]
                                                      [--out build/frames] [--save scene.blend]

Stills are given in seconds. Every timing comes from beats.py (build/timeline.json, written by
audio.py); page states come from build/pages (pages.py) and build/anchors.json.

The set: a dark chapel floor; four lecterns in a row, one per edition, each holding an e-paper
tablet; an incense stand beside each; the foot-long cobalt-blue demon; puffs of sulphur; the
overexplained edition's 29 footnote slips; and, for the slop, a field of cloned lecterns that
multiplies into the dark.
"""
import json
import math
import os
import random
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beats as B  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
PREVIEW = "--preview" in argv
FRAMES = None
STILLS = None
OUT = os.path.join(HERE, "build", "frames")
SAVE = None
STEP = 1
for i, a in enumerate(argv):
    if a == "--frames":
        FRAMES = (int(argv[i + 1]), int(argv[i + 2]))
    elif a == "--stills":
        STILLS = [float(x) for x in argv[i + 1].split(",")]
    elif a == "--out":
        OUT = argv[i + 1]
    elif a == "--save":
        SAVE = argv[i + 1]
    elif a == "--step":
        STEP = int(argv[i + 1])

FPS = B.FPS
C = B.cue
PAGES = os.path.join(HERE, "build", "pages")
with open(os.path.join(HERE, "build", "anchors.json")) as f:
    ANCH = json.load(f)["anchors"]

random.seed(11)
bpy.ops.wm.read_factory_settings(use_empty=True)
prefs = bpy.context.preferences.edit
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start = 0
scene.frame_end = B.n_frames() - 1


def fr(t):
    return t * FPS


# ---------------------------------------------------------------- helpers

def link(obj, parent=None, coll=None):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    (coll or scene.collection).objects.link(obj)
    if parent is not None:
        obj.parent = parent
    return obj


def empty(name, loc=(0, 0, 0), parent=None, coll=None):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    return link(e, parent, coll)


def key(obj, path, t, value=None, interp="BEZIER"):
    prefs.keyframe_new_interpolation_type = interp
    if value is not None:
        setattr(obj, path, value)
    obj.keyframe_insert(path, frame=fr(t))


def keysock(sock, t, value, interp="BEZIER"):
    prefs.keyframe_new_interpolation_type = interp
    sock.default_value = value
    sock.keyframe_insert("default_value", frame=fr(t))


def principled(name, color, rough=0.5, metal=0.0, emit=None, strength=0.0, alpha=1.0, sss=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if sss:
        p.inputs["Subsurface Weight"].default_value = sss
    if emit is not None:
        p.inputs["Emission Color"].default_value = (*emit, 1)
        p.inputs["Emission Strength"].default_value = strength
    if alpha < 1.0:
        p.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "BLENDED"
    return m


def emission(name, color, strength, alpha=None):
    """Emission, optionally mixed with transparency; returns (material, alpha socket or None)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*color, 1)
    em.inputs["Strength"].default_value = strength
    if alpha is None:
        nt.links.new(em.outputs[0], out.inputs["Surface"])
        return m, None
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs["Fac"].default_value = alpha
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    m.surface_render_method = "BLENDED"
    m.use_transparency_overlap = False
    return m, mix.inputs["Fac"]


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def shade_smooth(obj):
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def prim(kind, name, mat=None, parent=None, coll=None, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1),
         smooth=True, **kw):
    getattr(bpy.ops.mesh, f"primitive_{kind}_add")(**kw)
    o = bpy.context.active_object
    o.name = name
    o.location, o.rotation_euler, o.scale = loc, rot, scale
    link(o, parent, coll)
    if mat:
        assign(o, mat)
    if smooth:
        shade_smooth(o)
    return o


def image(name):
    return bpy.data.images.load(os.path.join(PAGES, name + ".png"), check_existing=True)


# ---------------------------------------------------------------- render settings

scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 25 if PREVIEW else 100
scene.eevee.taa_render_samples = 4 if PREVIEW else 24
scene.eevee.use_raytracing = True
scene.eevee.volumetric_start = 0.5
scene.eevee.volumetric_end = 30.0
scene.eevee.volumetric_tile_size = "8"
scene.eevee.volumetric_samples = 48
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "None"
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
wn = world.node_tree
wn.nodes["Background"].inputs["Color"].default_value = (0.004, 0.005, 0.009, 1)
wn.nodes["Background"].inputs["Strength"].default_value = 1.0
vol = wn.nodes.new("ShaderNodeVolumePrincipled")
vol.inputs["Density"].default_value = 0.035
vol.inputs["Color"].default_value = (0.75, 0.78, 0.9, 1)
wn.links.new(vol.outputs[0], wn.nodes["World Output"].inputs["Volume"])

# ---------------------------------------------------------------- materials

M_FLOOR = principled("floor", (0.018, 0.017, 0.02), rough=0.32)
nt = M_FLOOR.node_tree
noi = nt.nodes.new("ShaderNodeTexNoise")
noi.inputs["Scale"].default_value = 3.0
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.012, 0.012, 0.014, 1)
ramp.color_ramp.elements[1].color = (0.03, 0.028, 0.03, 1)
nt.links.new(noi.outputs["Fac"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
rr = nt.nodes.new("ShaderNodeMapRange")
rr.inputs["To Min"].default_value = 0.22
rr.inputs["To Max"].default_value = 0.55
nt.links.new(noi.outputs["Fac"], rr.inputs["Value"])
nt.links.new(rr.outputs[0], nt.nodes["Principled BSDF"].inputs["Roughness"])

M_WOOD = principled("wood", (0.07, 0.035, 0.018), rough=0.45)
M_BRASS = principled("brass", (0.55, 0.38, 0.12), rough=0.3, metal=1.0)
M_BEZEL = principled("bezel", (0.03, 0.03, 0.033), rough=0.35)
M_STICK = principled("stick", (0.12, 0.05, 0.03), rough=0.8)
M_DEMON = principled("demon", (0.0, 0.045, 0.42), rough=0.32, emit=(0.0, 0.12, 0.85), strength=0.25,
                     sss=0.15)
M_HORN = principled("horn", (0.06, 0.01, 0.015), rough=0.25)
M_WING = principled("wing", (0.0, 0.02, 0.16), rough=0.5, emit=(0.0, 0.06, 0.5), strength=0.2)
M_WING.use_backface_culling = False
M_EYE, _ = emission("eye", (1.0, 0.75, 0.15), 14.0)
M_TIP, _ = emission("tip", (1.0, 0.32, 0.05), 0.0)
TIP_STRENGTH = M_TIP.node_tree.nodes["Emission"].inputs["Strength"]
M_SMOKE, _ = emission("smoke", (0.5, 0.52, 0.6), 0.35, alpha=0.07)

floor = prim("plane", "floor", M_FLOOR, size=120, smooth=False)

# ---------------------------------------------------------------- the four lecterns

XS = [-3.6, -1.2, 1.2, 3.6]
TILT = math.radians(35)
TOP_Z = 1.12
N_PAGE = Vector((0, -math.sin(TILT), math.cos(TILT)))
U_PAGE = Vector((0, math.cos(TILT), math.sin(TILT)))
SW, SH = 0.33, 0.44  # screen size, 3:4
PW, PH = 1500, 2000


def tablet_center(i):
    return Vector((XS[i], 0.0, TOP_Z + 0.03))


def page_point(i, px, py):
    """3D point on lectern i's screen for page pixel (px, py)."""
    c = tablet_center(i) + N_PAGE * 0.009
    return c + Vector((1, 0, 0)) * ((px / PW - 0.5) * SW) + U_PAGE * ((0.5 - py / PH) * SH)


def page_material(name, states):
    """Image states cross-faded by keyed Mix factors; a 'screen' level dims it to black.
    Returns (material, [mix factor sockets], screen socket)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    p.inputs["Roughness"].default_value = 0.55
    prev = None
    facs = []
    for st in states:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = image(st)
        tex.interpolation = "Cubic"
        if prev is None:
            prev = tex.outputs["Color"]
            continue
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.inputs[0].default_value = 0.0
        nt.links.new(prev, mix.inputs[6])
        nt.links.new(tex.outputs["Color"], mix.inputs[7])
        prev = mix.outputs[2]
        facs.append(mix.inputs[0])
    scr = nt.nodes.new("ShaderNodeValue")
    scr.outputs[0].default_value = 0.0
    dim = nt.nodes.new("ShaderNodeMix")
    dim.data_type = "RGBA"
    dim.blend_type = "MULTIPLY"
    dim.inputs[0].default_value = 1.0
    nt.links.new(prev, dim.inputs[6])
    nt.links.new(scr.outputs[0], dim.inputs[7])
    # the multiply blend wants a colour; a value plugs in as grey
    nt.links.new(dim.outputs[2], p.inputs["Base Color"])
    nt.links.new(dim.outputs[2], p.inputs["Emission Color"])
    p.inputs["Emission Strength"].default_value = 0.3
    return m, facs, scr.outputs[0]


def lectern(name, x, y=0.0, coll=None, page_states=("p1",)):
    root = empty(name, (x, y, 0), coll=coll)
    prim("cylinder", name + "_base", M_WOOD, root, coll, loc=(0, 0, 0.03), radius=0.26, depth=0.06,
         vertices=48)
    prim("cylinder", name + "_col", M_WOOD, root, coll, loc=(0, 0, 0.56), radius=0.055, depth=1.02,
         vertices=24)
    prim("cylinder", name + "_ring", M_BRASS, root, coll, loc=(0, 0, 0.97), radius=0.07, depth=0.04,
         vertices=24)
    top = prim("cube", name + "_top", M_WOOD, root, coll, loc=(0, 0, TOP_Z), rot=(TILT, 0, 0),
               scale=(0.23, 0.29, 0.02), smooth=False)
    prim("cube", name + "_lip", M_WOOD, root, coll,
         loc=(0, -0.29 * math.cos(TILT), TOP_Z - 0.29 * math.sin(TILT) + 0.03), rot=(TILT, 0, 0),
         scale=(0.23, 0.012, 0.03), smooth=False)
    bez = prim("cube", name + "_bezel", M_BEZEL, root, coll, loc=Vector((0, 0, TOP_Z + 0.03 - 0.004)),
               rot=(TILT, 0, 0), scale=(0.19, 0.25, 0.006), smooth=False)
    bevel = bez.modifiers.new("bevel", "BEVEL")
    bevel.width = 0.012
    bevel.segments = 3
    scr = prim("plane", name + "_screen", None, root, coll,
               loc=Vector((0, 0, TOP_Z + 0.03)) + N_PAGE * 0.0035, rot=(TILT, 0, 0),
               scale=(SW / 2, SH / 2, 1), smooth=False, size=2)
    mat, facs, level = page_material(name + "_page", page_states)
    assign(scr, mat)
    return root, facs, level


def incense_stand(name, x, y, coll=None, lit_at=None):
    root = empty(name, (x, y, 0), coll=coll)
    prim("cylinder", name + "_foot", M_BRASS, root, coll, loc=(0, 0, 0.015), radius=0.12, depth=0.03)
    prim("cylinder", name + "_pole", M_BRASS, root, coll, loc=(0, 0, 0.48), radius=0.012, depth=0.94)
    prim("uv_sphere", name + "_bowl", M_BRASS, root, coll, loc=(0, 0, 0.95), scale=(1, 1, 0.45),
         radius=0.07, segments=32, ring_count=16)
    tips = []
    for k, (ang, lean) in enumerate(((0, 0.12), (2.1, 0.2), (4.2, 0.16))):
        L = 0.34
        dx, dy = math.sin(lean) * math.cos(ang), math.sin(lean) * math.sin(ang)
        mid = Vector((dx * L / 2, dy * L / 2, 0.97 + math.cos(lean) * L / 2))
        st = prim("cylinder", f"{name}_stick{k}", M_STICK, root, coll, loc=mid, radius=0.0025,
                  depth=L, vertices=8, smooth=False)
        st.rotation_euler = Vector((0, 0, 1)).rotation_difference(
            Vector((dx, dy, math.cos(lean)))).to_euler()
        tip_loc = Vector((dx * L, dy * L, 0.97 + math.cos(lean) * L))
        tip = prim("uv_sphere", f"{name}_tip{k}", M_TIP, root, coll, loc=tip_loc, radius=0.005,
                   segments=8, ring_count=6)
        tips.append(tip)
        if lit_at is not None:
            smoke(f"{name}_smoke{k}", tip, lit_at, coll)
    return root, tips


SMOKE_PUFF = None


def smoke(name, tip, start_t, coll=None):
    global SMOKE_PUFF
    if SMOKE_PUFF is None:
        SMOKE_PUFF = prim("ico_sphere", "smoke_puff", M_SMOKE, None, None, loc=(0, 0, -50),
                          radius=0.02, subdivisions=3)
    em = prim("uv_sphere", name, None, tip, coll, loc=(0, 0, 0.004), radius=0.003, segments=6,
              ring_count=4)
    em.hide_render = False
    ps = em.modifiers.new("smoke", "PARTICLE_SYSTEM").particle_system.settings
    ps.count = 700 if not PREVIEW else 200
    ps.frame_start = fr(start_t)
    ps.frame_end = scene.frame_end
    ps.lifetime = 130
    ps.lifetime_random = 0.4
    ps.emit_from = "VOLUME"
    ps.normal_factor = 0.0
    ps.object_align_factor = (0, 0, 0.07)
    ps.factor_random = 0.01
    ps.brownian_factor = 0.04
    ps.effector_weights.gravity = 0.0
    ps.render_type = "OBJECT"
    ps.instance_object = SMOKE_PUFF
    ps.particle_size = 1.0
    ps.size_random = 0.7
    ps.use_size_deflect = False
    ps.use_rotations = True
    ps.rotation_factor_random = 1.0
    em.show_instancer_for_render = False
    return em


lecterns, facs, levels = [], [], []
STATES = [
    ("p1", "p1_err", "p1_pref"),
    ("p2a", "p2b", "p2c"),
    ("p3a", "p3b", "p3c", "p3d", "p3e", "p3f"),
    ("p4a", "p4b", "p4c"),
]
stands = []
for i, x in enumerate(XS):
    r, f, lv = lectern(f"L{i}", x, page_states=STATES[i])
    lecterns.append(r)
    facs.append(f)
    levels.append(lv)
    lit = C("incense") + (0.0 if i == 0 else 0.5 + 0.4 * i)
    s, tips = incense_stand(f"I{i}", x - 0.55, 0.22, lit_at=lit)
    stands.append((s, tips, lit))

# incense tips glow from their lighting time
keysock(TIP_STRENGTH, C("incense") - 0.05, 0.0, "LINEAR")
keysock(TIP_STRENGTH, C("incense") + 0.35, 60.0, "LINEAR")
keysock(TIP_STRENGTH, C("incense") + 0.9, 22.0, "LINEAR")
keysock(TIP_STRENGTH, C("end") + 6, 22.0, "LINEAR")
keysock(TIP_STRENGTH, C("fin"), 0.0, "LINEAR")


# page state changes
def xfade(sock, t0, dur):
    keysock(sock, t0, 0.0)
    keysock(sock, t0 + dur, 1.0)


xfade(facs[0][0], C("errors") - 0.1, 0.6)          # p1 -> errors highlighted
xfade(facs[0][1], C("preface") + 0.3, 0.8)         # -> preface turns red, highlights gone
mt = B.mild_edit_times()
xfade(facs[1][0], mt[0], mt[-1] - mt[0])           # p2a -> p2b as the scratches land
d0, d1 = B.deletion_window()
xfade(facs[1][1], d0, d1 - d0)                     # p2b -> p2c: "demons" goes
f0, f1 = B.flood_window()
xfade(facs[2][0], f0, f1 - f0)                     # p3a -> p3b: the flood
xfade(facs[2][1], C("byline") + 0.2, 0.7)          # -> byline
xfade(facs[2][2], C("lift") + 0.1, 0.5)            # -> the lift page
xfade(facs[2][3], C("tired") - 0.1, 1.2)           # -> the tired line
xfade(facs[2][4], C("lift_ending") + 0.8, 1.6)     # -> the new ending
xfade(facs[3][0], C("ed4") + 1.6, 1.0)             # p4a -> footnote markers
xfade(facs[3][1], C("slips") + 0.4, 2.2)           # -> footnotes swallow the page

# ---------------------------------------------------------------- lamps and screens

lamps = []
for i, x in enumerate(XS):
    ld = bpy.data.lights.new(f"lamp{i}", "SPOT")
    ld.energy = 0.0
    ld.color = (1.0, 0.78, 0.55)
    ld.spot_size = math.radians(38)
    ld.spot_blend = 0.6
    ld.shadow_soft_size = 0.25
    lo = bpy.data.objects.new(f"lamp{i}", ld)
    link(lo)
    lo.location = (x + 0.4, -1.3, 3.4)
    tr = lo.constraints.new("TRACK_TO")
    tr.target = lecterns[i]
    tr.track_axis = "TRACK_NEGATIVE_Z"
    tr.up_axis = "UP_Y"
    lamps.append(ld)
    # aim at the top of the column, not the floor
    aim = empty(f"aim{i}", (x, 0, 1.0))
    tr.target = aim

LAMP_MAX = 210.0
# (time, [level per lectern]) - levels hold until the next entry, with ramps between
LEVELS = [
    (0.0, [0, 0, 0, 0]),
    (C("incense") + 0.2, [0, 0, 0, 0]),
    (C("puff") + 0.3, [0.45, 0, 0, 0]),
    (C("title") - 0.2, [0.45, 0, 0, 0]),
    (C("title") + 1.8, [0.6, 0.6, 0.6, 0.6]),
    (C("ed1") + 0.2, [0.6, 0.6, 0.6, 0.6]),
    (C("ed1") + 1.6, [1, 0.18, 0.18, 0.18]),
    (C("ed2") + 0.2, [1, 0.18, 0.18, 0.18]),
    (C("ed2") + 1.6, [0.18, 1, 0.18, 0.18]),
    (C("ed3") + 0.2, [0.18, 1, 0.18, 0.18]),
    (C("ed3") + 1.6, [0.18, 0.18, 1, 0.18]),
    (C("lift"), [0.18, 0.18, 1, 0.18]),
    (C("lift") + 1.2, [0.08, 0.08, 0.5, 0.08]),
    (C("ed4") + 0.2, [0.08, 0.08, 0.5, 0.08]),
    (C("ed4") + 1.6, [0.18, 0.18, 0.18, 1]),
    (C("pullback"), [0.18, 0.18, 0.18, 1]),
    (C("pullback") + 2.0, [0.8, 0.8, 0.8, 0.8]),
    (C("coda"), [0.8, 0.8, 0.8, 0.8]),
    (C("coda") + 2.0, [1, 0.12, 0.12, 0.12]),
    (C("end") + 2.0, [1, 0.12, 0.12, 0.12]),
    (C("fin") - 0.5, [0, 0, 0, 0]),
]
for t, lv in LEVELS:
    for i in range(4):
        prefs.keyframe_new_interpolation_type = "BEZIER"
        lamps[i].energy = LAMP_MAX * lv[i]
        lamps[i].keyframe_insert("energy", frame=fr(t))
        # screens: dark until the incense, then never fully off while a lamp is on
        keysock(levels[i], t, 0.0 if max(lv) == 0 else 0.35 + 0.65 * lv[i])

# a cool rim from behind so silhouettes read against the dark
rim = bpy.data.lights.new("rim", "AREA")
rim.energy = 300
rim.size = 12
rim.color = (0.45, 0.55, 1.0)
ro = bpy.data.objects.new("rim", rim)
link(ro)
ro.location = (0, 6, 4.5)
ro.rotation_euler = (math.radians(-60), 0, 0)
prefs.keyframe_new_interpolation_type = "BEZIER"
for t, e in ((0, 0), (C("title"), 0), (C("title") + 2, 300), (C("fin") - 1, 300), (C("fin"), 0)):
    rim.energy = e
    rim.keyframe_insert("energy", frame=fr(t))


# ---------------------------------------------------------------- the demon

def build_demon(name, coll=None, glow_light=True):
    root = empty(name, coll=coll)
    body = empty(name + "_body", parent=root, coll=coll)  # bob and lean live here
    bob = body.driver_add("location", 2).driver
    bob.type = "SCRIPTED"
    bob.expression = "0.018*sin(frame*0.16)"
    sway = body.driver_add("rotation_euler", 1).driver
    sway.type = "SCRIPTED"
    sway.expression = "0.08*sin(frame*0.07)"
    prim("uv_sphere", name + "_torso", M_DEMON, body, coll, loc=(0, 0, 0.1), scale=(1, 0.85, 1.25),
         radius=0.055, segments=32, ring_count=16)
    prim("uv_sphere", name + "_belly", M_DEMON, body, coll, loc=(0, -0.02, 0.085), scale=(0.9, 0.8, 1),
         radius=0.045, segments=24, ring_count=12)
    prim("uv_sphere", name + "_head", M_DEMON, body, coll, loc=(0, -0.005, 0.205), scale=(1.05, 0.95, 0.95),
         radius=0.052, segments=32, ring_count=16)
    for s in (-1, 1):
        prim("cone", f"{name}_horn{s}", M_HORN, body, coll, loc=(0.03 * s, 0.0, 0.262),
             rot=(0.0, 0.5 * s, 0), radius1=0.012, radius2=0.0, depth=0.055, vertices=16)
        prim("uv_sphere", f"{name}_eye{s}", M_EYE, body, coll, loc=(0.02 * s, -0.045, 0.214),
             scale=(1, 0.6, 1.2), radius=0.009, segments=12, ring_count=8)
        prim("uv_sphere", f"{name}_ear{s}", M_DEMON, body, coll, loc=(0.052 * s, 0.0, 0.215),
             rot=(0, 0.9 * s, 0), scale=(0.35, 0.35, 1.0), radius=0.02, segments=12, ring_count=8)
        arm = prim("cylinder", f"{name}_arm{s}", M_DEMON, body, coll, loc=(0.06 * s, -0.01, 0.105),
                   rot=(0.3, -0.5 * s, 0), radius=0.009, depth=0.075, vertices=10)
        prim("uv_sphere", f"{name}_hand{s}", M_DEMON, body, coll, loc=(0.078 * s, -0.022, 0.072),
             radius=0.012, segments=12, ring_count=8)
        prim("cylinder", f"{name}_leg{s}", M_DEMON, body, coll, loc=(0.025 * s, 0, 0.02),
             radius=0.011, depth=0.06, vertices=10)
        prim("uv_sphere", f"{name}_foot{s}", M_DEMON, body, coll, loc=(0.027 * s, -0.012, -0.01),
             scale=(1, 1.5, 0.6), radius=0.013, segments=12, ring_count=8)
        # wing: a flattened, pointed membrane on a hinge
        hinge = empty(f"{name}_hinge{s}", (0.02 * s, 0.04, 0.14), parent=body, coll=coll)
        wm = bpy.data.meshes.new(f"{name}_wingm{s}")
        vs = [(0, 0, 0), (0.06 * s, 0.01, 0.075), (0.125 * s, 0.02, 0.06), (0.115 * s, 0.02, 0.0),
              (0.085 * s, 0.015, 0.02), (0.06 * s, 0.01, -0.02), (0.035 * s, 0.005, 0.0)]
        wm.from_pydata(vs, [], [list(range(len(vs)))])
        w = bpy.data.objects.new(f"{name}_wing{s}", wm)
        link(w, hinge, coll)
        assign(w, M_WING)
        sol = w.modifiers.new("sol", "SOLIDIFY")
        sol.thickness = 0.002
        flap = hinge.driver_add("rotation_euler", 2).driver
        flap.type = "SCRIPTED"
        flap.expression = f"{0.6 * s}*sin(frame*1.3) - {0.35 * s}"
    # tail: a curve with a barb
    cu = bpy.data.curves.new(name + "_tailc", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.005
    cu.bevel_resolution = 3
    sp = cu.splines.new("BEZIER")
    pts = [(0, 0.05, 0.04), (0.03, 0.1, 0.0), (0.07, 0.12, 0.06), (0.09, 0.1, 0.12)]
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    tail = bpy.data.objects.new(name + "_tail", cu)
    link(tail, body, coll)
    tail.data.materials.append(M_DEMON)
    prim("cone", name + "_barb", M_HORN, body, coll, loc=(0.09, 0.1, 0.13), rot=(0.4, 0.5, 0),
         radius1=0.014, radius2=0.0, depth=0.03, vertices=3, smooth=False)
    if glow_light:
        gl = bpy.data.lights.new(name + "_glow", "POINT")
        gl.energy = 6.0
        gl.color = (0.25, 0.45, 1.0)
        gl.shadow_soft_size = 0.05
        go = bpy.data.objects.new(name + "_glow", gl)
        link(go, body, coll)
        go.location = (0, -0.12, 0.15)
        return root, gl
    return root, None


demon, demon_glow = build_demon("Demon")
DEMON_EMIT = M_DEMON.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]


def beside(i, dx=0.46, dy=0.16, dz=0.12):
    c = tablet_center(i)
    return Vector((c.x + dx, c.y + dy, c.z + dz))


# Demon path: (time, location, z-rotation, scale). Holds between entries, eased.
D = [
    (0.0, beside(0), 0.0, 0.0),
    (C("puff") - 0.02, beside(0), 0.0, 0.0),
    (C("puff") + 0.18, beside(0), 0.0, 1.25),
    (C("puff") + 0.4, beside(0), 0.0, 1.0),
    (C("title") - 0.3, beside(0), 0.0, 1.0),
    (C("errors") - 0.3, beside(0), 0.5, 1.0),
    (C("errors") + 0.5, beside(0, 0.32, 0.04, 0.1), 0.9, 1.0),   # leans in...
    (C("errors") + 1.0, beside(0, 0.46, 0.2, 0.16), 0.3, 1.0),  # ...and is pulled back
    (C("ed2") + 0.2, beside(0, 0.46, 0.2, 0.16), 0.3, 1.0),
    (C("ed2") + 1.0, beside(0, 1.2, 0.5, 0.75), 0.0, 1.0),
    (C("ed2") + 1.9, beside(1, 0.36, 0.14, 0.06), 0.8, 1.0),
    (C("ed3") + 0.2, beside(1, 0.36, 0.14, 0.06), 0.8, 1.0),
    (C("ed3") + 1.0, beside(1, 1.2, 0.5, 0.75), 0.0, 1.0),
    (C("ed3") + 1.9, beside(2, 0.3, -0.1, 0.12), 0.6, 1.0),
    (C("flood"), beside(2, 0.3, -0.1, 0.12), 0.6, 1.0),
    (C("flood") + 1.6, beside(2, 0.3, -0.12, 0.2), 0.3, 1.4),
    (C("lift") - 0.2, beside(2, 0.3, -0.12, 0.2), 0.3, 1.4),
    (C("lift") + 1.0, beside(2, 0.34, 0.1, 0.24), 0.9, 1.0),
    (C("ed4") + 0.2, beside(2, 0.34, 0.1, 0.24), 0.9, 1.0),
    (C("ed4") + 1.0, beside(2, 1.2, 0.5, 0.75), 0.0, 1.0),
    (C("ed4") + 1.9, beside(3, 0.3, -0.12, 0.14), 0.5, 1.0),
    (C("pullback") + 0.3, beside(3, 0.3, -0.12, 0.14), 0.5, 1.0),
    (C("pullback") + 4.0, Vector((0, -0.6, 2.1)), 0.0, 1.6),
    (C("coda") - 0.2, Vector((0, -0.6, 2.1)), 0.0, 1.6),
    (C("coda") + 1.6, beside(0, 0.12, 0.2, 0.18), -0.3, 0.9),     # sits on the tablet's top edge
    (C("puff_out") - 0.3, beside(0, 0.12, 0.2, 0.18), -0.3, 0.9),
    (C("puff_out") - 0.1, beside(0, 0.12, 0.2, 0.18), -0.3, 1.2),
    (C("puff_out") + 0.1, beside(0, 0.12, 0.2, 0.18), -0.3, 0.0),
]
for t, loc, rz, s in D:
    key(demon, "location", t, loc.copy())
    key(demon, "rotation_euler", t, (0, 0, rz))
    key(demon, "scale", t, (s, s, s))

# quill pecks during the mild edits: small darts towards the page
base = beside(1, 0.36, 0.14, 0.06)
for k, t in enumerate(mt):
    key(demon, "location", t - 0.08, base.copy())
    key(demon, "location", t, base + Vector((-0.06 - 0.01 * (k % 3), -0.02, -0.05)))
    key(demon, "location", t + 0.1, base.copy())

# the demon glows hotter as its hand grows heavier
for t, e in ((0, 0.6), (C("flood"), 0.6), (C("flood") + 2, 2.2), (C("lift"), 2.2), (C("lift") + 1.2, 0.35),
             (C("ed4") + 1, 0.8), (C("pullback"), 0.8), (C("pullback") + 3, 1.6), (C("coda"), 1.6),
             (C("coda") + 2, 0.6)):
    keysock(DEMON_EMIT, t, e)
for t, e in ((0, 6), (C("flood"), 6), (C("flood") + 2, 14), (C("lift") + 1.2, 3), (C("ed4") + 1, 6)):
    prefs.keyframe_new_interpolation_type = "BEZIER"
    demon_glow.energy = e
    demon_glow.keyframe_insert("energy", frame=fr(t))


# ---------------------------------------------------------------- puffs of sulphur

def sulphur(name, t0, center, size=1.0):
    root = empty(name, center)
    mat, a = emission(name + "_m", (0.95, 0.85, 0.35), 3.5, alpha=0.0)
    rnd = random.Random(name)
    for k in range(16):
        off = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.5, 1))).normalized() \
            * rnd.uniform(0.02, 0.09) * size
        prim("ico_sphere", f"{name}_{k}", mat, root, loc=off, radius=rnd.uniform(0.03, 0.06) * size,
             subdivisions=2)
    key(root, "scale", t0 - 0.05, (0.2, 0.2, 0.2))
    key(root, "scale", t0 + 0.25, (1.0, 1.0, 1.0))
    key(root, "scale", t0 + 1.6, (1.8, 1.8, 2.2))
    keysock(a, t0 - 0.05, 0.0, "LINEAR")
    keysock(a, t0, 0.95, "LINEAR")
    keysock(a, t0 + 0.4, 0.55, "LINEAR")
    keysock(a, t0 + 1.6, 0.0, "LINEAR")
    key(root, "location", t0, center.copy())
    key(root, "location", t0 + 1.6, center + Vector((0, 0, 0.25)))
    root.hide_render = True
    key(root, "hide_render", t0 - 0.1, False, "CONSTANT")
    root.hide_render = True
    key(root, "hide_render", t0 - 0.2, True, "CONSTANT")
    key(root, "hide_render", t0 + 1.7, True, "CONSTANT")
    for ch in root.children:
        ch.hide_render = True
        key(ch, "hide_render", t0 - 0.2, True, "CONSTANT")
        key(ch, "hide_render", t0 - 0.05, False, "CONSTANT")
        key(ch, "hide_render", t0 + 1.7, True, "CONSTANT")


sulphur("puff_in", C("puff"), beside(0) + Vector((0, 0, 0.13)))
sulphur("puff_out", C("puff_out"), beside(0, 0.12, 0.2, 0.3))

# ---------------------------------------------------------------- the footnote slips

slips = []
st = B.slip_times()
fade_out = C("pullback") + 3.5
for k in range(29):
    mat = bpy.data.materials.new(f"slip{k}")
    mat.use_nodes = True
    nt = mat.node_tree
    p = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = image(f"slip_{k:02d}")
    nt.links.new(tex.outputs["Color"], p.inputs["Base Color"])
    nt.links.new(tex.outputs["Color"], p.inputs["Emission Color"])
    p.inputs["Emission Strength"].default_value = 0.7
    p.inputs["Roughness"].default_value = 0.7
    o = prim("plane", f"slip{k}", mat, size=1, scale=(0.155, 0.0825, 1), smooth=False)
    o.data.materials[0] = mat
    slips.append(o)
    rnd = random.Random(k)
    t0 = st[k]
    ang0 = rnd.uniform(0, 2 * math.pi)
    r_end = rnd.uniform(0.45, 1.05)
    z_end = rnd.uniform(1.2, 2.3)
    spin = rnd.choice((-1, 1)) * rnd.uniform(0.25, 0.45)
    origin = tablet_center(3) + N_PAGE * 0.02
    t = t0 - 0.1
    o.hide_render = True
    key(o, "hide_render", t0 - 0.1, True, "CONSTANT")
    key(o, "hide_render", t0, False, "CONSTANT")
    key(o, "hide_render", fade_out + 1.5, True, "CONSTANT")
    while t < fade_out + 1.5:
        tau = max(0.0, t - t0)
        grow = 1 - math.exp(-1.6 * tau)
        ang = ang0 + spin * tau
        r = 0.05 + r_end * grow
        z = origin.z + (z_end - origin.z) * grow + 0.03 * math.sin(tau * 1.3 + k)
        if t > C("pullback"):
            u = t - C("pullback")
            r += 0.8 * u
            z += 0.9 * u
        pos = Vector((origin.x + r * math.cos(ang), origin.y + r * math.sin(ang) - 0.1, z))
        if tau == 0:
            pos = origin.copy()
        s = min(1.0, tau / 0.3)
        key(o, "location", t, pos, "LINEAR")
        key(o, "rotation_euler", t, (math.radians(70) + 0.2 * math.sin(tau + k), 0.15 * math.sin(tau * 0.7 + k),
                                     ang * 0.25 + rnd.uniform(-0.3, 0.3) * 0 + 0.0), "LINEAR")
        key(o, "scale", t, (0.155 * s, 0.0825 * s, 1), "LINEAR")
        t += 4 / FPS

# ---------------------------------------------------------------- the slop: cloned lecterns

protos = []
for k, states in enumerate((("p1",), ("p2c",), ("p3c",), ("p4c",))):
    coll = bpy.data.collections.new(f"proto{k}")
    scene.collection.children.link(coll)
    lectern(f"P{k}", 0, coll=coll, page_states=states)
    for ob in coll.objects:
        if ob.name.endswith("_page") or "_screen" in ob.name:
            pass
    # the clone screens are on, at a fixed level
    m = bpy.data.materials[f"P{k}_page"]
    for n in m.node_tree.nodes:
        if n.type == "VALUE":
            n.outputs[0].default_value = 0.8
    incense_stand(f"PI{k}", -0.55, 0.22, coll=coll)
    d, _ = build_demon(f"PD{k}", coll=coll, glow_light=False)
    d.location = (0.31, -0.12, TOP_Z + 0.17)
    d.rotation_euler = (0, 0, 0.5)
    protos.append(coll)
    bpy.context.view_layer.layer_collection.children[coll.name].exclude = True

m0, m1 = B.multiply_window()
spots = []
for row in range(0, 8):
    for col in range(-6, 7):
        x = col * 2.4 + (1.2 if row % 2 else 0)
        y = row * 2.6
        if row == 0 and -2 <= col <= 1:
            continue  # the four real lecterns
        if row == 0 and col in (-2, 2):
            pass
        spots.append((x, y))
maxd = max(math.hypot(x, y) for x, y in spots)
for n, (x, y) in enumerate(spots):
    inst = bpy.data.objects.new(f"clone{n}", None)
    inst.instance_type = "COLLECTION"
    inst.instance_collection = protos[random.randrange(4)]
    link(inst)
    inst.location = (x, y, 0)
    inst.rotation_euler = (0, 0, random.uniform(-0.12, 0.12))
    tpop = m0 + (m1 - m0) * (math.hypot(x, y) / maxd) ** 0.8 + random.uniform(-0.15, 0.15)
    key(inst, "scale", tpop - 0.01, (0.001, 0.001, 0.001))
    key(inst, "scale", tpop + 0.22, (1.12, 1.12, 1.12))
    key(inst, "scale", tpop + 0.4, (1.0, 1.0, 1.0))
    key(inst, "scale", C("coda") + 0.5, (1.0, 1.0, 1.0))
    key(inst, "scale", C("coda") + 3.0 + 1.5 * random.random(), (0.001, 0.001, 0.001))
    inst.hide_render = True
    key(inst, "hide_render", tpop - 0.05, True, "CONSTANT")
    key(inst, "hide_render", tpop, False, "CONSTANT")
    key(inst, "hide_render", C("coda") + 5.0, True, "CONSTANT")

# ---------------------------------------------------------------- camera

cam_data = bpy.data.cameras.new("cam")
cam_data.sensor_width = 36
cam_data.clip_start = 0.02
cam_data.clip_end = 200
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 2.8
cam = bpy.data.objects.new("cam", cam_data)
link(cam)
scene.camera = cam
target = empty("cam_target")
trk = cam.constraints.new("TRACK_TO")
trk.target = target
trk.track_axis = "TRACK_NEGATIVE_Z"
trk.up_axis = "UP_Y"
cam_data.dof.focus_object = target


def anchor(i, state, name):
    px, py = ANCH[state][name]
    return page_point(i, px + 250, py - 20)


def read(i, d=1.35, at=None, side=0.0):
    """Reading shot: camera along the page normal at distance d, looking at `at` (default centre)."""
    tgt = at if at is not None else tablet_center(i)
    return tgt + N_PAGE * d + Vector((side, 0, 0)), tgt


def medium(i, dx=0.25, dy=-1.6, dz=0.4, look=(0.12, 0, 0.08)):
    c = tablet_center(i)
    return c + Vector((dx, dy, dz)), c + Vector(look)


WIDE = (Vector((0, -7.8, 2.4)), Vector((0, 0, 1.0)))
dm = beside(0)
SHOTS = [
    # (time, (camera, target), lens)
    (0.0, (tablet_center(0) + Vector((-0.6, -1.6, 0.25)), tablet_center(0) + Vector((-0.3, 0, 0.0))), 45),
    (C("incense") - 0.5, (tablet_center(0) + Vector((-0.75, -1.3, 0.15)), Vector((XS[0] - 0.55, 0.22, 1.2))), 50),
    (C("incense") + 1.6, (tablet_center(0) + Vector((-0.6, -1.15, 0.12)), Vector((XS[0] - 0.5, 0.2, 1.22))), 50),
    (C("puff") + 0.1, (dm + Vector((0.05, -1.05, 0.08)), dm + Vector((0, 0, 0.13))), 50),
    (C("title") - 0.6, (dm + Vector((0.02, -0.8, 0.06)), dm + Vector((0, 0, 0.13))), 50),
    (C("title") + 1.8, (WIDE[0] + Vector((0.4, 0.4, 0.2)), WIDE[1]), 35),
    (C("ed1") - 0.2, (WIDE[0], WIDE[1]), 35),
    (C("ed1") + 2.0, read(0, 1.3), 50),
    (C("errors") - 0.3, read(0, 1.18), 50),
    (C("preface") - 0.2, read(0, 1.12), 50),
    (C("preface") + 1.0, read(0, 0.75, anchor(0, "p1", "note")), 50),
    (C("ed2"), read(0, 0.7, anchor(0, "p1", "note")), 50),
    (C("ed2") + 2.0, read(1, 1.3), 50),
    (C("deletion") - 0.2, read(1, 1.15), 50),
    (C("deletion") + 0.4, read(1, 0.62, anchor(1, "p2c", "turns")), 50),
    (C("ed3") - 0.2, read(1, 0.58, anchor(1, "p2c", "turns")), 50),
    (C("ed3") + 2.0, read(2, 1.3), 50),
    (C("byline") - 0.2, read(2, 1.2), 50),
    (C("byline") + 0.6, read(2, 0.7, anchor(2, "p3c", "byline")), 50),
    (C("lift") - 0.1, read(2, 0.68, anchor(2, "p3c", "byline")), 50),
    (C("lift") + 1.0, read(2, 1.0, anchor(2, "p3d", "storeys"), side=0.08), 50),
    (C("tired") - 0.2, read(2, 0.9, anchor(2, "p3d", "storeys"), side=0.06), 50),
    (C("tired") + 0.8, read(2, 0.62, anchor(2, "p3e", "tired")), 50),
    (C("lift_ending"), read(2, 0.6, anchor(2, "p3e", "tired")), 50),
    (C("lift_ending") + 2.2, read(2, 0.75, anchor(2, "p3f", "ending")), 50),
    (C("ed4") - 0.2, read(2, 0.72, anchor(2, "p3f", "ending")), 50),
    (C("ed4") + 2.0, medium(3, -0.9, -1.9, 0.55, (0.0, 0, 0.25)), 40),
    (C("mappings") + 2, medium(3, -0.5, -2.3, 0.75, (0.0, 0, 0.35)), 40),
    (C("pudding"), medium(3, 0.2, -2.1, 0.6, (0.0, 0, 0.25)), 40),
    (C("rune") + 1.0, read(3, 1.25, side=0.1), 50),
    (C("pullback") + 0.2, read(3, 1.15, side=0.1), 50),
    (C("pullback") + 5.0, (Vector((1.5, -6.5, 4.2)), Vector((0, 2, 0.9))), 30),
    (C("multiply") + 7.0, (Vector((-1.0, -11.0, 6.8)), Vector((0, 6, 0.6))), 28),
    (C("terminal") + 4.0, (Vector((-3.0, -12.5, 7.6)), Vector((0, 7, 0.5))), 28),
    (C("coda") - 0.3, (Vector((-4.0, -13.0, 8.0)), Vector((0, 7, 0.5))), 28),
    (C("coda") + 3.5, medium(0, 0.4, -1.75, 0.5, (0.1, 0.1, 0.2)), 45),
    (C("vanish"), medium(0, 0.3, -1.4, 0.45, (0.1, 0.12, 0.24)), 45),
    (C("end") + 1.0, medium(0, 0.25, -1.3, 0.42, (0.1, 0.12, 0.24)), 45),
    (C("fin"), medium(0, 0.2, -1.2, 0.4, (0.1, 0.12, 0.24)), 45),
]
for t, (cl, tg), lens in SHOTS:
    key(cam, "location", t, Vector(cl))
    key(target, "location", t, Vector(tg))
    prefs.keyframe_new_interpolation_type = "BEZIER"
    cam_data.lens = lens
    cam_data.keyframe_insert("lens", frame=fr(t))
# depth of field: shallow in close-ups, deep in wides
for t, fs in ((0, 2.8), (C("title"), 2.8), (C("title") + 1.5, 8), (C("ed1") + 1, 4.0), (C("ed4") + 1.5, 5.6),
              (C("pullback") + 1, 11), (C("coda") + 2, 3.2)):
    prefs.keyframe_new_interpolation_type = "BEZIER"
    cam_data.dof.aperture_fstop = fs
    cam_data.dof.keyframe_insert("aperture_fstop", frame=fr(t))

# ---------------------------------------------------------------- go

if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, SAVE))
os.makedirs(OUT, exist_ok=True)
if STILLS:
    for s in STILLS:
        f = int(round(s * FPS))
        scene.frame_set(f)
        scene.render.filepath = os.path.join(OUT, f"still_{f:05d}.png")
        bpy.ops.render.render(write_still=True)
else:
    if FRAMES:
        scene.frame_start, scene.frame_end = FRAMES
    scene.frame_step = STEP
    scene.render.filepath = os.path.join(OUT, "")
    scene.render.use_overwrite = False
    bpy.ops.render.render(animation=True)
print("done")
