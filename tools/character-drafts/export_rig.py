"""Export a character draft as an animation rig for the game (D-039, D-050).

The parts that rely on soft shading (blur filters, which Flutter's SVG support
does not render) become cropped high-resolution PNG layers; everything that
bends or moves every frame (arms with sleeves, legs, irises, shadow, sparkles)
is written as vector data and drawn by code in Flutter. The poses come from the
same POSE_DATA used by the draft sheets, so the game animates the approved poses.

Usage:
    python3 export_rig.py elide

Output:
    assets/images/characters/<name>/char_<name>_<part>.png
    assets/animations/char_<name>_rig.json
"""

import importlib
import json
import os
import sys
import xml.etree.ElementTree as ET

import parts

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
SCALE = 3  # PNG pixels per rig unit
PAD = 2  # transparent border around each cropped part, in pixels
SCENE_W, SCENE_H = 400, 540
ANCHOR = (200, 270)  # where anchored parts (hands, feet) are drawn for export

BROWS = ("normal", "happy", "up", "curious")
MOUTHS = ("smile", "open", "o", "curious")
EYE_KINDS = ("open", "wide", "smiling", "happy", "closed")
HAND_KINDS = ("back", "palm", "fist", "thumb")


def render_surface(defs, content):
    import gi

    gi.require_version("Rsvg", "2.0")
    import cairo
    from gi.repository import Rsvg

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SCENE_W * SCALE}" '
        f'height="{SCENE_H * SCALE}" viewBox="0 0 {SCENE_W} {SCENE_H}">{defs}{content}</svg>'
    )
    handle = Rsvg.Handle.new_from_data(svg.encode())
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SCENE_W * SCALE, SCENE_H * SCALE)
    ctx = cairo.Context(surf)
    vp = Rsvg.Rectangle()
    vp.x, vp.y, vp.width, vp.height = 0, 0, SCENE_W * SCALE, SCENE_H * SCALE
    handle.render_document(ctx, vp)
    surf.flush()
    return surf


def alpha_bbox(surf):
    """Bounding box (x0, y0, x1, y1) of the non-transparent pixels."""
    w, h, stride = surf.get_width(), surf.get_height(), surf.get_stride()
    data = bytes(surf.get_data())
    x0, y0, x1, y1 = w, h, -1, -1
    for y in range(h):
        alpha = data[y * stride + 3 : y * stride + 4 * w : 4]
        stripped = alpha.lstrip(b"\0")
        if not stripped:
            continue
        left = len(alpha) - len(stripped)
        right = len(alpha.rstrip(b"\0"))
        x0, x1 = min(x0, left), max(x1, right)
        y0 = min(y0, y)
        y1 = y + 1
    if x1 < 0:
        raise ValueError("empty part")
    return (
        max(x0 - PAD, 0),
        max(y0 - PAD, 0),
        min(x1 + PAD, w),
        min(y1 + PAD, h),
    )


def export_part(defs, content, path, anchor=None):
    """Render one part, crop it and save it; returns its rect in rig units.

    With an anchor the rect is relative to it (parts drawn around an origin)."""
    import cairo

    surf = render_surface(defs, content)
    x0, y0, x1, y1 = alpha_bbox(surf)
    crop = cairo.ImageSurface(cairo.FORMAT_ARGB32, x1 - x0, y1 - y0)
    ctx = cairo.Context(crop)
    ctx.set_source_surface(surf, -x0, -y0)
    ctx.paint()
    crop.write_to_png(path)
    ax, ay = anchor or (0, 0)
    return [
        round(x0 / SCALE - ax, 3),
        round(y0 / SCALE - ay, 3),
        round((x1 - x0) / SCALE, 3),
        round((y1 - y0) / SCALE, 3),
    ]


def pct(value, default):
    if value is None:
        return default
    return float(value.rstrip("%")) / 100 if value.endswith("%") else float(value)


def gradients(defs):
    """Read the gradients of a draft's <defs> (single source of the colors)."""
    out = {}
    for el in ET.fromstring(defs):
        tag = el.tag.split("}")[-1]
        if tag not in ("radialGradient", "linearGradient"):
            continue
        stops = [
            [
                pct(s.get("offset"), 0),
                s.get("stop-color"),
                float(s.get("stop-opacity", "1")),
            ]
            for s in el
        ]
        if tag == "radialGradient":
            out[el.get("id")] = dict(
                type="radial",
                cx=pct(el.get("cx"), 0.5),
                cy=pct(el.get("cy"), 0.5),
                r=pct(el.get("r"), 0.5),
                stops=stops,
            )
        else:
            out[el.get("id")] = dict(
                type="linear",
                x1=pct(el.get("x1"), 0),
                y1=pct(el.get("y1"), 0),
                x2=pct(el.get("x2"), 1),
                y2=pct(el.get("y2"), 0),
                stops=stops,
            )
    return out


def url_id(fill):
    return fill[5:-1] if fill.startswith("url(#") else fill


def main():
    name = sys.argv[1]
    sys.argv = [sys.argv[0]]  # the draft modules must not see our arguments
    ch = importlib.import_module(name)

    img_dir = os.path.join(ROOT, "assets", "images", "characters", name)
    anim_dir = os.path.join(ROOT, "assets", "animations")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(anim_dir, exist_ok=True)
    asset_dir = f"assets/images/characters/{name}"
    defs = ch.DEFS
    part_rects = {}

    def part(key, content, anchor=None):
        file = f"char_{name}_{key}.png"
        rect = export_part(defs, content, os.path.join(img_dir, file), anchor)
        part_rects[key] = dict(file=f"{asset_dir}/{file}", rect=rect)
        print(f"  {key:22s} {rect}")

    print(f"Exporting {name}:")
    part("head", ch.head_base())
    part("blush", ch.blush_cheeks())
    for kind in BROWS:
        part(f"brows_{kind}", ch.brows(kind))
    for kind in MOUTHS:
        part(f"mouth_{kind}", ch.mouth(kind))
    for side, cx in (("L", ch.EYE_X[0]), ("R", ch.EYE_X[1])):
        clip = "eyeLC" if side == "L" else "eyeRC"
        for kind in EYE_KINDS:
            cover = ch.eye_cover(cx, kind)
            content = (f'<g clip-path="url(#{clip})">{cover}</g>' if cover else "") + ch.eye_lids(
                cx, side, kind
            )
            part(f"eye_{side.lower()}_{kind}", content)
    part("dress", ch.dress())
    part("collar", ch.sleeves())
    part("tail", ch.tail())
    # Hands and feet come in two layers, so the game can merge them with the
    # limbs like the drafts do: all outlines first, then all fills.
    for layer in ("outline", "fill"):
        part(f"foot_{layer}", ch.foot(*ANCHOR, layer), ANCHOR)
        for kind in HAND_KINDS:
            hand = parts.paw(*ANCHOR, 0, kind, "url(#limb)", ch.LINE, mirror=1, layer=layer)
            part(f"hand_{kind}_{layer}", hand, ANCHOR)

    sleeve = dict(ch.SLEEVE)
    rig = dict(
        name=name,
        size=[SCENE_W, SCENE_H],
        centerX=parts.CENTER_X,
        parts=part_rects,
        gradients=gradients(defs),
        line=ch.LINE,
        limbStroke=2.6,
        limbFill="limb",
        arm=dict(w0=30, w1=24, bulge=3, handOffset=14),
        sleeve=dict(
            fill=url_id(sleeve["fill"]),
            line=sleeve["line"],
            t1=sleeve["t1"],
            w0=sleeve["w0"],
            w1=sleeve["w1"],
            trim=sleeve.get("trim"),
            trimLine=sleeve.get("trim_line", sleeve["line"]),
            long=bool(sleeve.get("long")),
        ),
        legs=[
            dict(points=[list(p) for p in pts], w0=w0, w1=w1, bulge=bulge, foot=list(foot))
            for pts, w0, w1, bulge, foot in ch.LEGS
        ],
        tailRoot=list(ch.TAIL_ROOT),
        headPivot=[200, 300],
        leanPivot=[200, 500],
        shadow=dict(cx=200, cy=520, ry=11, color="#1D5A3A", opacity=0.28),
        eyes=dict(
            x=list(ch.EYE_X),
            cy=ch.EYE_CY,
            rx=ch.EYE_RX,
            ry=ch.EYE_RY,
            line=ch.EYE,
            lineWidth=2.2,
            iris="iris",
            pupil="#0E1330",
            open=list(ch.OPEN_EYES),
            geometry={
                kind: dict(
                    zip(("x", "y", "r", "pupil"), ch.iris_geometry(0, "L", 0, 0, kind), strict=True)
                )
                for kind in ch.OPEN_EYES
            },
        ),
        sparkle=dict(d=ch.SPARKLE_D),
        marks=dict(d=ch.SURPRISE_MARKS, color="#3B2C55", width=3.5),
        poses={
            pose: dict(
                lift=d["lift"],
                lean=d["lean"],
                shadow=d["shadow"],
                arms=[
                    dict(
                        side=a["side"],
                        points=[list(p) for p in a["points"]],
                        kind=a["kind"],
                        handRot=a["hand_rot"],
                        layer=a["layer"],
                        fold=a.get("fold"),
                    )
                    for a in d["arms"]
                ],
                face=dict(
                    eyes=list(d["face"]["eyes"]),
                    look=list(d["face"]["look"]),
                    brows=d["face"]["brows"],
                    mouth=d["face"]["mouth"],
                    tilt=d["face"]["tilt"],
                    blush=d["face"]["blush"],
                ),
                sparkles=[list(s) for s in d.get("sparkles", ())],
                marks=bool(d.get("marks")),
            )
            for pose, d in ch.POSE_DATA.items()
        },
    )
    path = os.path.join(anim_dir, f"char_{name}_rig.json")
    with open(path, "w") as fh:
        json.dump(rig, fh, indent=1)
        fh.write("\n")
    print(f"Rig written to {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
