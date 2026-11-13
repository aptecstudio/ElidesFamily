"""Shared parts of the character drafts (D-032).

- limb(): chubby limb along a cubic Bezier curve, thicker at the root.
- arm(): arm + sleeve that follows the arm (no visible joint) + hand.
- paw(): little hand with a thumb and three fingers; the thumb orients itself.
- render(): SVG -> PNG with librsvg (through PyGObject), no rsvg-convert needed.

Command line usage:  python3 parts.py file.svg file.png
"""

import math
import sys

CENTER_X = 200  # body axis in every character scene


def bez(t, p0, p1, p2, p3):
    return tuple(
        (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t**3 * d
        for a, b, c, d in zip(p0, p1, p2, p3, strict=True)
    )


def _dbez(t, p0, p1, p2, p3):
    return tuple(
        3 * (1 - t) ** 2 * (b - a) + 6 * (1 - t) * t * (c - b) + 3 * t * t * (d - c)
        for a, b, c, d in zip(p0, p1, p2, p3, strict=True)
    )


def limb_outline(
    p0, p1, p2, p3, w0, w1, bulge=3, t0=0.0, t1=1.0, cap_end=True, cap_start=False, closed=True
):
    """Closed outline of a limb; the width goes from w0 (root) to w1 (tip).

    closed=False leaves out the edge across the start (t0), to outline a piece
    of limb drawn over the rest of the same limb without a visible cut."""
    steps = 40
    left = []
    right = []
    for i in range(steps + 1):
        t = t0 + (t1 - t0) * i / steps
        x, y = bez(t, p0, p1, p2, p3)
        dx, dy = _dbez(t, p0, p1, p2, p3)
        length = math.hypot(dx, dy) or 1
        nx, ny = -dy / length, dx / length
        w = (w0 + (w1 - w0) * t) / 2 + bulge * math.sin(math.pi * t)
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))

    def cap(a, b, t, sign):
        # half circle from a to b, bulging along the tangent (sign=+1) or against it
        cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        r = math.hypot(a[0] - cx, a[1] - cy)
        dx, dy = _dbez(t, p0, p1, p2, p3)
        length = math.hypot(dx, dy) or 1
        tx, ty = sign * dx / length, sign * dy / length
        ux, uy = (a[0] - cx) / (r or 1), (a[1] - cy) / (r or 1)
        pts = []
        for k in range(1, 12):
            ang = math.pi * k / 12
            pts.append(
                (
                    cx + r * (ux * math.cos(ang) + tx * math.sin(ang)),
                    cy + r * (uy * math.cos(ang) + ty * math.sin(ang)),
                )
            )
        return pts

    path = list(left)
    if cap_end:
        path += cap(left[-1], right[-1], t1, +1)
    path += list(reversed(right))
    if cap_start:
        path += cap(right[0], left[0], t0, -1)
    d = "M%.1f,%.1f " % path[0] + " ".join("L%.1f,%.1f" % q for q in path[1:])
    return d + " Z" if closed else d


def limb(
    p0,
    p1,
    p2,
    p3,
    w0,
    w1,
    bulge=3,
    fill="url(#limb)",
    line="#000",
    t0=0.0,
    t1=1.0,
    cap_end=True,
    cap_start=False,
    sw=2.6,
):
    d = limb_outline(p0, p1, p2, p3, w0, w1, bulge, t0, t1, cap_end, cap_start)
    return (
        f'<path d="{d}" fill="{fill}" stroke="{line}" stroke-width="{sw}" stroke-linejoin="round"/>'
    )


# ---------------------------------------------------------------- hands

# Local coordinates: origin at the palm center, fingers towards -y, thumb towards -x.
_PALM = (
    "M-11,8 C-13,0 -13,-7 -11,-12 C-11,-18 -5,-19 -4,-15 C-3,-20 3,-20 4,-15 "
    "C5,-19 11,-18 11,-12 C13,-6 13,2 11,8 C9,14 4,16 0,16 C-4,16 -9,14 -11,8 Z"
)
_THUMB = "M-10,7 C-17,7 -21,0 -19,-6 C-17,-10 -12,-7 -10,-2"
_FIST = "M-12,3 C-13,-7 -8,-12 0,-12 C8,-12 13,-7 12,3 C11,11 6,15 0,15 C-6,15 -11,11 -12,3 Z"
_THUMB_UP = "M-10,-7 C-12,-18 -9,-28 -3,-28 C3,-28 4,-20 2,-10"


def thumb_mirror(kind, side):
    """Horizontal flip of the hand so the thumb sits on the right side.

    A hand has a fixed handedness: the thumb side only depends on which hand
    it is and on whether the palm or the back is shown, while the rotation of
    the hand does the rest. With the palm side shown ("palm", "fist" and
    "thumb", whose curled fingers face the viewer) the thumb points towards the
    body when the fingers are up; with the back shown, it points outwards when
    the fingers are up and towards the body when the arm hangs down.

    side: "L" for the hand on the viewer's left (the character's right), "R"
    for the other one. Local frame: fingers towards -y, thumb towards -x.
    """
    palm_side = kind != "back"
    return (-1 if palm_side else 1) * (1 if side == "L" else -1)


_clip_n = [0]


def paw(
    x,
    y,
    rot,
    kind="back",
    fill="url(#limb)",
    line="#000",
    pad="#F7B7CB",
    scale=1.4,
    mirror=None,
    side=None,
    layer="both",
):
    """Little hand.

    kind: "back"  back of the hand facing the viewer (idle);
          "palm"  palm with pads (wave, cheer, surprised);
          "fist"  soft fist (hand on the chin);
          "thumb" thumbs up (proud).
    The thumb side follows the handedness (see thumb_mirror); side defaults to
    the side of the body axis the hand is on; mirror (+1 or -1) forces the flip
    (used by the animation rig export).

    layer: "outline" draws only the silhouette outline, "fill" everything else,
    "both" the whole hand. Drawing the outlines of hand and arm first and the
    fills on top makes them one smooth piece, with no line at the wrist.
    """
    if mirror is None:
        mirror = thumb_mirror(kind, side or ("L" if x < CENTER_X else "R"))
    sx = mirror
    if kind in ("back", "palm"):
        shapes = (_THUMB, _PALM)
    elif kind == "fist":
        shapes = (_FIST,)
    else:
        shapes = (_FIST, _THUMB_UP)

    o = []
    if layer in ("outline", "both"):
        # Silhouette: a stroke twice as wide, half of it covered by the fill.
        o.extend(
            f'<path d="{d}" fill="{line}" stroke="{line}" stroke-width="4.8" stroke-linejoin="round"/>'
            for d in shapes
        )
    if layer in ("fill", "both"):
        o.extend(f'<path d="{d}" fill="{fill}"/>' for d in shapes)
        thin = f'fill="none" stroke="{line}" stroke-linecap="round"'
        if kind in ("back", "palm"):
            # Line between thumb and palm: the edge of the palm on the thumb side.
            o.append(
                f'<path d="M-11,8 C-13,0 -13,-7 -11,-12" fill="none" stroke="{line}" stroke-width="2.4" stroke-linecap="round"/>'
            )
            o.append(f'<path d="M-4,-15 L-4,-10 M4,-15 L4,-10" {thin} stroke-width="1.8"/>')
            if kind == "palm":
                o.append(
                    f'<ellipse cx="0" cy="5" rx="6" ry="5" fill="{pad}" opacity="0.85"/>'
                    f'<circle cx="-7" cy="-12" r="2.2" fill="{pad}" opacity="0.8"/>'
                    f'<circle cx="0" cy="-14" r="2.2" fill="{pad}" opacity="0.8"/>'
                    f'<circle cx="7" cy="-12" r="2.2" fill="{pad}" opacity="0.8"/>'
                )
            else:
                o.append('<ellipse cx="-3" cy="-6" rx="5" ry="3" fill="#FFFFFF" opacity="0.6"/>')
        elif kind == "fist":
            o.append(
                f'<path d="M-6,-11 Q-4,-6 -6,-2 M2,-12 Q4,-7 2,-3 M9,-8 Q10,-4 8,0" {thin} stroke-width="1.7"/>'
            )
            o.append(
                f'<path d="M-12,2 C-6,-2 2,-1 6,3" fill="none" stroke="{line}" stroke-width="2.4" stroke-linecap="round"/>'
            )
            o.append('<ellipse cx="-2" cy="7" rx="5" ry="3" fill="#FFFFFF" opacity="0.5"/>')
        else:
            # The thumb is in front of the fist: outline it only over the fist.
            _clip_n[0] += 1
            cid = f"fistC{_clip_n[0]}"
            o.append(
                f'<clipPath id="{cid}"><path d="{_FIST}"/></clipPath>'
                f'<path d="{_THUMB_UP}" fill="none" stroke="{line}" stroke-width="2.4" '
                f'stroke-linecap="round" clip-path="url(#{cid})"/>'
            )
            o.append(
                f'<path d="M3,-6 Q11,-5 12,0 M2,2 Q11,3 12,7 M1,9 Q8,11 9,13" {thin} stroke-width="1.7"/>'
            )
            o.append('<ellipse cx="-5" cy="-20" rx="2" ry="4" fill="#FFFFFF" opacity="0.6"/>')
    return (
        f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f}) scale({sx * scale},{scale})">'
        + "".join(o)
        + "</g>"
    )


def merged_outline(d, line, width=2.6):
    """Outline pass of a shape that must merge with its neighbours."""
    return f'<path d="{d}" fill="{line}" stroke="{line}" stroke-width="{2 * width}" stroke-linejoin="round"/>'


# ---------------------------------------------------------------- arms


def _hand_args(p0, p1, p2, p3, kind, hand_rot, fill, line, pad):
    """Position, rotation and look of the hand at the end of an arm."""
    q = bez(0.92, p0, p1, p2, p3)
    dx, dy = p3[0] - q[0], p3[1] - q[1]
    length = math.hypot(dx, dy) or 1
    dx, dy = dx / length, dy / length
    rot = math.degrees(math.atan2(dy, dx)) + 90 if hand_rot is None else hand_rot
    return (p3[0] + dx * 14, p3[1] + dy * 14, rot, kind, fill, line, pad)


def arm_front(
    p0,
    p1,
    p2,
    p3,
    fur,
    line,
    kind="back",
    hand_rot=None,
    t0=0.5,
    hand_fill=None,
    hand_line=None,
    pad="#F7B7CB",
    w=(30, 24),
):
    """Forearm (from t0) and hand drawn again over an arm already drawn with
    arm(): used when the hand goes in front of the head or the forearm comes
    back over its own sleeve. Only its sides and tip are outlined, so it
    starts seamlessly from the arm underneath."""
    side = "L" if p0[0] < CENTER_X else "R"
    hand = _hand_args(p0, p1, p2, p3, kind, hand_rot, hand_fill or fur, hand_line or line, pad)
    edge = limb_outline(p0, p1, p2, p3, w[0], w[1], 3, t0=t0, closed=False)
    piece = limb_outline(p0, p1, p2, p3, w[0], w[1], 3, t0=t0)
    return [
        f'<path d="{edge}" fill="none" stroke="{line}" stroke-width="5.2" stroke-linejoin="round"/>',
        paw(*hand, side=side, layer="outline"),
        f'<path d="{piece}" fill="{fur}"/>',
        paw(*hand, side=side, layer="fill"),
    ]


def arm(
    p0,
    p1,
    p2,
    p3,
    fur,
    line,
    kind="back",
    hand_rot=None,
    sleeve=None,
    hand_fill=None,
    hand_line=None,
    pad="#F7B7CB",
    w=(30, 24),
):
    """Chubby arm with a sleeve that follows the arm curve.

    sleeve: None, or a dict with fill, line, t1 (where the sleeve ends, 0..1),
            w0/w1 (sleeve width), trim (optional trim color), trim_line,
            long (True for long sleeves: no shadow under the cuff).
    The forearm and the hand can then be drawn again in front of the head or
    of the upper arm with arm_front().
    """
    _clip_n[0] += 1
    cid = f"armC{_clip_n[0]}"
    o = []
    arm_d = limb_outline(p0, p1, p2, p3, w[0], w[1], 3)
    side = "L" if p0[0] < CENTER_X else "R"
    hand_args = _hand_args(p0, p1, p2, p3, kind, hand_rot, hand_fill or fur, hand_line or line, pad)
    # Arm and hand are one piece: both outlines first, then the fills.
    o.append(f'<clipPath id="{cid}"><path d="{arm_d}"/></clipPath>')
    o.append(merged_outline(arm_d, line))
    o.append(paw(*hand_args, side=side, layer="outline"))
    o.append(f'<path d="{arm_d}" fill="{fur}"/>')
    if sleeve:
        t1 = sleeve["t1"]
        if not sleeve.get("long"):
            # soft shadow under the sleeve: the arm "goes into" the sleeve
            a = bez(min(t1 + 0.06, 1), p0, p1, p2, p3)
            dx, dy = _dbez(t1, p0, p1, p2, p3)
            ang = math.degrees(math.atan2(dy, dx))
            o.append(
                f'<g clip-path="url(#{cid})"><ellipse cx="{a[0]:.1f}" cy="{a[1]:.1f}" rx="9" ry="22" '
                f'transform="rotate({ang:.1f} {a[0]:.1f} {a[1]:.1f})" fill="#000000" opacity="0.13" filter="url(#b3)"/></g>'
            )
        sd = limb_outline(
            p0, p1, p2, p3, sleeve["w0"], sleeve["w1"], 4, 0.0, t1, cap_end=False, cap_start=True
        )
        o.append(
            f'<path d="{sd}" fill="{sleeve["fill"]}" stroke="{sleeve["line"]}" stroke-width="2.6" stroke-linejoin="round"/>'
        )
        # sleeve edge: an ellipse perpendicular to the arm, so it follows every pose
        c = bez(t1, p0, p1, p2, p3)
        dx, dy = _dbez(t1, p0, p1, p2, p3)
        ang = math.degrees(math.atan2(dy, dx))
        hw = (sleeve["w0"] + (sleeve["w1"] - sleeve["w0"]) * t1) / 2 + 4 * math.sin(math.pi * t1)
        trim = sleeve.get("trim")
        if trim:
            tl = sleeve.get("trim_line", sleeve["line"])
            o.append(
                f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="5" ry="{hw:.1f}" transform="rotate({ang:.1f} {c[0]:.1f} {c[1]:.1f})" '
                f'fill="{trim}" stroke="{tl}" stroke-width="2"/>'
            )
        else:
            o.append(
                f'<path d="M{c[0]:.1f},{c[1] - hw:.1f} a3,{hw:.1f} 0 0 1 0,{2 * hw:.1f}" transform="rotate({ang:.1f} {c[0]:.1f} {c[1]:.1f})" '
                f'fill="none" stroke="{sleeve["line"]}" stroke-width="2" stroke-linecap="round" opacity="0.6"/>'
            )
    o.append(paw(*hand_args, side=side, layer="fill"))
    return o


# ---------------------------------------------------------------- render


def render(svg_path, png_path):
    import gi

    gi.require_version("Rsvg", "2.0")
    import cairo
    from gi.repository import Rsvg

    h = Rsvg.Handle.new_from_file(svg_path)
    ok, w, hh = h.get_intrinsic_size_in_pixels()
    if not ok:
        r = h.get_intrinsic_dimensions()
        w, hh = r.out_width.length, r.out_height.length
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(hh))
    ctx = cairo.Context(surf)
    vp = Rsvg.Rectangle()
    vp.x = 0
    vp.y = 0
    vp.width = w
    vp.height = hh
    h.render_document(ctx, vp)
    surf.write_to_png(png_path)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
