"""Draft of Dad (Papà, white Labrador) — same head as Elide and Rio, adult body.

Dad is not tall and a bit chubby: his body is just slightly longer than the
kids', with a soft tummy. He wears a hoodie and jeans.

Usage:
    python3 dad.py dad_poses.svg          # sheet with the 6 poses
    python3 dad.py dad_model.svg single   # idle model sheet
"""

import math
import sys

import parts
import poses

LINE = "#B89C78"  # warm white fur outline
SWL = "#4E8F36"  # hoodie outline
JL = "#2C5590"  # jeans outline
EYE = "#3A2618"
MOUTHL = "#7A3E2A"
H = 580  # scene height (the kids use 540)
GROUND = 544  # ground shadow
LEAN_PIVOT = (200, 530)
WAIST = (200, 420)  # the upper body breathes from here

DEFS = """<defs>
<filter id="b3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>
<radialGradient id="fur" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#FFF6E5"/><stop offset="1" stop-color="#E9DCC4"/></radialGradient>
<radialGradient id="ear" cx="35%" cy="25%" r="85%"><stop offset="0" stop-color="#FFF3DE"/><stop offset="1" stop-color="#E2CCA8"/></radialGradient>
<radialGradient id="limb" cx="35%" cy="30%" r="85%"><stop offset="0" stop-color="#FFFBF2"/><stop offset="1" stop-color="#E6D6BA"/></radialGradient>
<radialGradient id="muzzle" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F6ECDA"/></radialGradient>
<radialGradient id="sweater" cx="38%" cy="25%" r="85%"><stop offset="0" stop-color="#C4EFA8"/><stop offset="0.55" stop-color="#9BDB7C"/><stop offset="1" stop-color="#6FB552"/></radialGradient>
<radialGradient id="rib" cx="38%" cy="25%" r="85%"><stop offset="0" stop-color="#B2E594"/><stop offset="1" stop-color="#7FC262"/></radialGradient>
<radialGradient id="jeans" cx="38%" cy="25%" r="85%"><stop offset="0" stop-color="#8CB8E8"/><stop offset="0.55" stop-color="#5A8FD0"/><stop offset="1" stop-color="#3C6CAE"/></radialGradient>
<linearGradient id="iris" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#24140A"/><stop offset="0.5" stop-color="#5A3518"/><stop offset="1" stop-color="#A87444"/></linearGradient>
<linearGradient id="nose" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E4E44"/><stop offset="1" stop-color="#33221E"/></linearGradient>
<clipPath id="headC"><path d="M200,72 C276,72 322,120 324,188 C326,238 300,280 252,296 C236,302 218,304 200,304 C182,304 164,302 148,296 C100,280 74,238 76,188 C78,120 124,72 200,72 Z"/></clipPath>
<clipPath id="torsoC"><path d="M172,301 Q200,296 228,301 C241,307 250,319 253,334 C258,354 266,370 264,390 L264,412 Q200,424 136,412 L136,390 C134,370 142,354 147,334 C150,319 159,307 172,301 Z"/></clipPath>
<clipPath id="eyeLC"><ellipse cx="150" cy="198" rx="30" ry="31"/></clipPath>
<clipPath id="eyeRC"><ellipse cx="250" cy="198" rx="30" ry="31"/></clipPath>
</defs>"""

HEADP = "M200,72 C276,72 322,120 324,188 C326,238 300,280 252,296 C236,302 218,304 200,304 C182,304 164,302 148,296 C100,280 74,238 76,188 C78,120 124,72 200,72 Z"
TORSOP = "M172,301 Q200,296 228,301 C241,307 250,319 253,334 C258,354 266,370 264,390 L264,412 Q200,424 136,412 L136,390 C134,370 142,354 147,334 C150,319 159,307 172,301 Z"


def bez(t, p0, p1, p2, p3):
    return tuple(
        (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t**3 * d
        for a, b, c, d in zip(p0, p1, p2, p3, strict=True)
    )


def limb(p0, p1, p2, p3, w0, w1, bulge=3, fill="url(#limb)", line=LINE, t0=0.0):
    steps = 40

    def dbez_at(t, a, b, c, d):
        return 3 * (1 - t) ** 2 * (b - a) + 6 * (1 - t) * t * (c - b) + 3 * t * t * (d - c)

    left = []
    right = []
    for i in range(steps + 1):
        t = t0 + (1 - t0) * i / steps
        x, y = bez(t, p0, p1, p2, p3)
        dx = dbez_at(t, p0[0], p1[0], p2[0], p3[0])
        dy = dbez_at(t, p0[1], p1[1], p2[1], p3[1])
        length = math.hypot(dx, dy) or 1
        nx, ny = -dy / length, dx / length
        w = (w0 + (w1 - w0) * t) / 2 + bulge * math.sin(math.pi * t)
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    d = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % q for q in left[1:])
    d += " A%.1f,%.1f 0 0 1 %.1f,%.1f " % (w1 / 2, w1 / 2, right[-1][0], right[-1][1])
    d += " ".join("L%.1f,%.1f" % q for q in reversed(right)) + " Z"
    return (
        f'<path d="{d}" fill="{fill}" stroke="{line}" stroke-width="2.6" stroke-linejoin="round"/>'
    )


# Long hoodie sleeve with a ribbed cuff; the hand comes out of the cuff.
ARM = dict(fill="sweater", line=SWL, w0=31, w1=25, bulge=2, hand_offset=16)
CUFF = dict(fill="rib", line=SWL, t0=0.84, w0=31, w1=27)
HAND_FILL = "url(#limb)"
HAND_LINE = LINE
PAD = "#E8A9A0"


def _sleeve(p, t0=0.0, closed=True):
    return parts.limb_outline(*p, ARM["w0"], ARM["w1"], ARM["bulge"], t0=t0, closed=closed)


def _cuff(p):
    d = parts.limb_outline(*p, CUFF["w0"], CUFF["w1"], ARM["bulge"], t0=CUFF["t0"])
    return f'<path d="{d}" fill="url(#rib)" stroke="{SWL}" stroke-width="2.6" stroke-linejoin="round"/>'


def _hand(p, kind, hand_rot, layer):
    p0, p1, p2, p3 = p
    q = bez(0.92, p0, p1, p2, p3)
    dx, dy = p3[0] - q[0], p3[1] - q[1]
    length = math.hypot(dx, dy) or 1
    dx, dy = dx / length, dy / length
    rot = math.degrees(math.atan2(dy, dx)) + 90 if hand_rot is None else hand_rot
    side = "L" if p0[0] < parts.CENTER_X else "R"
    off = ARM["hand_offset"]
    return parts.paw(
        p3[0] + dx * off,
        p3[1] + dy * off,
        rot,
        kind,
        HAND_FILL,
        HAND_LINE,
        PAD,
        side=side,
        layer=layer,
    )


def arm(p0, p1, p2, p3, kind="back", hand_rot=None):
    """Arm in the long hoodie sleeve, ribbed cuff and hand. Sleeve and hand
    outlines first, then the fills, as in parts.arm()."""
    p = (p0, p1, p2, p3)
    sleeve = _sleeve(p)
    return [
        parts.merged_outline(sleeve, SWL),
        _hand(p, kind, hand_rot, "outline"),
        f'<path d="{sleeve}" fill="url(#sweater)"/>',
        _cuff(p),
        _hand(p, kind, hand_rot, "fill"),
    ]


def arm_front(p0, p1, p2, p3, kind="back", hand_rot=None, t0=0.5):
    """Forearm and hand drawn again in front, like parts.arm_front()."""
    p = (p0, p1, p2, p3)
    return [
        f'<path d="{_sleeve(p, t0, closed=False)}" fill="none" stroke="{SWL}" stroke-width="5.2" stroke-linejoin="round"/>',
        _hand(p, kind, hand_rot, "outline"),
        f'<path d="{_sleeve(p, t0)}" fill="url(#sweater)"/>',
        _cuff(p),
        _hand(p, kind, hand_rot, "fill"),
    ]


def foot(x, y):
    return (
        f'<g transform="translate({x},{y}) scale(1.25)">'
        f'<path d="M-21,4 C-23,-8 -12,-14 0,-14 C12,-14 23,-8 21,4 C21,11 12,14 0,14 C-12,14 -21,11 -21,4 Z" fill="url(#limb)" stroke="{LINE}" stroke-width="2.6"/>'
        f'<path d="M-9,3 C-10,8 -9,11 -8,13 M0,4 C0,9 0,12 0,14 M9,3 C10,8 9,11 8,13" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'
        f'<ellipse cx="-6" cy="-6" rx="7" ry="3" fill="#FFFFFF" opacity="0.8"/></g>'
    )


TAIL_ROOT = (246, 404)


def tail():
    """Labrador tail: thick at the root, tapering and hanging down."""
    return limb((246, 404), (274, 412), (288, 430), (290, 458), 24, 12, 1, "url(#limb)", LINE)


def body_lower():
    return tail() + lower()


def lower():
    """Jeans and feet: they do not bend, so the rig keeps them as one layer."""
    o = []
    # jeans: short full legs, rolled-up hem
    for x in (174, 226):
        o.append(
            f'<path d="M{x - 26},410 L{x - 24},502 Q{x},508 {x + 24},502 L{x + 26},410 Z" fill="url(#jeans)" stroke="{JL}" stroke-width="2.6" stroke-linejoin="round"/>'
        )
        o.append(
            f'<path d="M{x - 25},492 Q{x},498 {x + 25},492 L{x + 25},506 Q{x},512 {x - 25},506 Z" fill="#7FA9DE" stroke="{JL}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        sx = x + 11 if x < 200 else x - 11
        o.append(
            f'<path d="M{sx},424 L{sx},486" fill="none" stroke="#E8B060" stroke-width="1.6" stroke-dasharray="4 3" opacity="0.8"/>'
        )
    o.append(
        f'<path d="M140,398 L260,398 L262,428 Q244,438 226,434 L200,430 L174,434 Q156,438 138,428 Z" fill="url(#jeans)" stroke="{JL}" stroke-width="2.6" stroke-linejoin="round"/>'
    )
    o.append(
        f'<path d="M200,410 L200,430" fill="none" stroke="{JL}" stroke-width="2" stroke-linecap="round"/>'
    )
    o.append(foot(172, 520))
    o.append(foot(228, 520))
    return "".join(o)


def torso(layer="both"):
    """Meadow-green hoodie with kangaroo pocket and ribbed hem; layer as in
    Elide's dress(), so the shoulders and the sleeves are one piece."""
    if layer == "outline":
        return parts.merged_outline(TORSOP, SWL)
    o = []
    o.append(f'<path d="{TORSOP}" fill="url(#sweater)"/>')
    o.append(
        '<g clip-path="url(#torsoC)">'
        '<ellipse cx="200" cy="304" rx="64" ry="16" fill="#3F7A2B" opacity="0.4" filter="url(#b6)"/>'
        '<ellipse cx="258" cy="370" rx="22" ry="60" fill="#3F7A2B" opacity="0.3" filter="url(#b12)"/>'
        '<ellipse cx="166" cy="340" rx="14" ry="40" fill="#E4FAD4" opacity="0.5" filter="url(#b6)"/>'
        f'<path d="M130,396 Q200,408 270,396 L272,430 L128,430 Z" fill="url(#rib)" stroke="{SWL}" stroke-width="2"/>'
        "</g>"
    )
    for x in range(144, 260, 8):
        dy = 0 if abs(x - 200) > 40 else 3
        o.append(
            f'<path d="M{x},{400 + dy} L{x},{412 + dy}" stroke="{SWL}" stroke-width="1.4" opacity="0.5"/>'
        )
    # kangaroo pocket
    o.append(
        f'<path d="M168,356 L232,356 C238,368 244,380 250,392 Q200,400 150,392 C156,380 162,368 168,356 Z" fill="url(#sweater)" stroke="{SWL}" stroke-width="2.4" stroke-linejoin="round"/>'
    )
    o.append(
        f'<path d="M168,356 C164,370 160,382 156,390 M232,356 C236,370 240,382 244,390" fill="none" stroke="{SWL}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>'
    )
    if layer == "both":
        o.append(
            f'<path d="{TORSOP}" fill="none" stroke="{SWL}" stroke-width="2.6" stroke-linejoin="round"/>'
        )
    return "".join(o)


def collar():
    """Hood resting on the shoulders, with drawstrings."""
    return (
        f'<path d="M146,316 C134,292 156,278 200,280 C244,278 266,292 254,316 Q200,300 146,316 Z" fill="url(#sweater)" stroke="{SWL}" stroke-width="2.6" stroke-linejoin="round"/>'
        '<path d="M156,306 Q200,292 244,306" fill="none" stroke="#3F7A2B" stroke-width="5" stroke-linecap="round" opacity="0.45"/>'
        '<path d="M188,306 C186,322 188,338 185,352 M212,306 C214,322 212,338 215,352" fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round"/>'
        '<path d="M188,306 C186,322 188,338 185,352 M212,306 C214,322 212,338 215,352" fill="none" stroke="#D8D0C0" stroke-width="1" stroke-linecap="round" opacity="0.6"/>'
        '<rect x="182" y="350" width="6" height="9" rx="2" fill="#E8B060" stroke="#B88A3A" stroke-width="1.2"/>'
        '<rect x="212" y="350" width="6" height="9" rx="2" fill="#E8B060" stroke="#B88A3A" stroke-width="1.2"/>'
    )


def ears():
    """Soft Labrador ears, slightly raised (more expressive in animations)."""
    one = (
        f'<path d="M152,86 C120,70 76,76 58,102 C44,124 46,162 60,186 C70,198 84,194 90,180 C98,150 114,120 144,106 Z" fill="url(#ear)" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
        '<path d="M140,90 C112,84 84,94 70,114" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.8"/>'
        f'<path d="M138,108 C116,118 100,140 90,170" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round" opacity="0.5"/>'
    )
    return one + f'<g transform="translate(400,0) scale(-1,1)">{one}</g>'


def head_base():
    o = []
    o.append(f'<path d="{HEADP}" fill="url(#fur)"/>')
    o.append(
        '<g clip-path="url(#headC)"><ellipse cx="200" cy="300" rx="130" ry="30" fill="#CDB892" opacity="0.45" filter="url(#b12)"/>'
        '<ellipse cx="318" cy="200" rx="18" ry="90" fill="#D6C29E" opacity="0.4" filter="url(#b12)"/>'
        '<ellipse cx="170" cy="112" rx="56" ry="24" fill="#FFFFFF" opacity="0.95" filter="url(#b6)"/></g>'
    )
    o.append(
        f'<path d="{HEADP}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
    )
    o.append(ears())
    # Labrador muzzle, slightly elongated
    o.append(
        '<path d="M200,218 C244,218 270,242 270,268 C270,294 240,306 200,306 C160,306 130,294 130,268 C130,242 156,218 200,218 Z" fill="url(#muzzle)" stroke="#D8C6A6" stroke-width="2"/>'
    )
    o.append(
        '<ellipse cx="112" cy="252" rx="17" ry="10" fill="#FF9D8A" opacity="0.4" filter="url(#b3)"/><ellipse cx="288" cy="252" rx="17" ry="10" fill="#FF9D8A" opacity="0.4" filter="url(#b3)"/>'
    )
    for x, y in ((160, 262), (152, 272), (164, 276), (240, 262), (248, 272), (236, 276)):
        o.append(f'<circle cx="{x}" cy="{y}" r="1.8" fill="#C9B08A"/>')
    o.append(
        '<path d="M180,230 Q200,222 220,230 Q223,245 208,252 L192,252 Q177,245 180,230 Z" fill="url(#nose)" stroke="#2A1A16" stroke-width="2" stroke-linejoin="round"/>'
    )
    o.append('<ellipse cx="193" cy="232" rx="6.5" ry="2.8" fill="#FFFFFF" opacity="0.85"/>')
    o.append(
        '<path d="M193,243 Q196,246 197,243 M203,243 Q204,246 207,243" fill="none" stroke="#1E120F" stroke-width="1.8" stroke-linecap="round"/>'
    )
    return "".join(o)


# Eye geometry, shared with the animation rig (export_rig.py).
EYE_X = (150, 250)
EYE_CY, EYE_RX, EYE_RY = 198, 30, 31
OPEN_EYES = ("open", "wide", "smiling")
PUPIL = "#140A05"


def iris_geometry(cx, side, dx=0, dy=0, kind="open"):
    """Center, iris radius and pupil radius of an open eye."""
    r = 25 if kind != "wide" else 21
    pr = 11.5 if kind != "wide" else 8
    ix = cx + (1 if side == "L" else -1) + dx
    iy = 201 + dy + (0 if kind != "wide" else -3)
    return ix, iy, r, pr


def eye_cover(cx, kind):
    """Cheek that rises and closes the eye from below (inside the eye clip)."""
    if kind != "smiling":
        return ""
    return f'<path d="M{cx - 34},232 Q{cx},210 {cx + 34},232 L{cx + 34},240 L{cx - 34},240 Z" fill="#FFF6E5"/>'


def eye(cx, side, dx=0, dy=0, kind="open"):
    """Like Elide but without eyelashes (male character)."""
    clip = "eyeLC" if side == "L" else "eyeRC"
    if kind not in OPEN_EYES:
        return eye_lids(cx, side, kind)
    ix, iy, r, pr = iris_geometry(cx, side, dx, dy, kind)
    return (
        f'<ellipse cx="{cx}" cy="{EYE_CY}" rx="{EYE_RX}" ry="{EYE_RY}" fill="#FFFFFF" stroke="{EYE}" stroke-width="2.2"/>'
        f'<g clip-path="url(#{clip})"><circle cx="{ix}" cy="{iy}" r="{r}" fill="url(#iris)"/><circle cx="{ix}" cy="{iy + 1}" r="{pr}" fill="{PUPIL}"/>'
        f'<ellipse cx="{ix + 8}" cy="{iy - 10}" rx="7.5" ry="8.5" fill="#FFFFFF"/><circle cx="{ix - 9}" cy="{iy + 10}" r="3.4" fill="#FFFFFF" opacity="0.9"/>'
        + eye_cover(cx, kind)
        + "</g>"
        + eye_lids(cx, side, kind)
    )


def eye_lids(cx, side, kind="open"):
    """Everything drawn over the iris (lid, cheek line), or the whole eye
    when it is closed ("happy" arc, "closed" blink)."""
    o = []
    if kind in OPEN_EYES:
        if kind == "smiling":
            o.append(
                f'<path d="M{cx - 26},222 Q{cx},212 {cx + 26},222" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'
            )
        lift = -5 if kind == "wide" else 0
        if side == "L":
            o.append(
                f'<path d="M121,{193 + lift} Q150,{164 + lift} 179,{191 + lift}" fill="none" stroke="{EYE}" stroke-width="4" stroke-linecap="round"/>'
            )
        else:
            o.append(
                f'<path d="M221,{191 + lift} Q250,{164 + lift} 279,{193 + lift}" fill="none" stroke="{EYE}" stroke-width="4" stroke-linecap="round"/>'
            )
    elif kind == "happy":
        o.append(
            f'<path d="M{cx - 25},206 Q{cx},182 {cx + 25},206" fill="none" stroke="{EYE}" stroke-width="4.6" stroke-linecap="round"/>'
        )
    elif kind == "closed":
        o.append(
            f'<path d="M{cx - 26},202 Q{cx},216 {cx + 26},202" fill="none" stroke="{EYE}" stroke-width="4.4" stroke-linecap="round"/>'
        )
    return "".join(o)


def brows(kind="normal"):
    shapes = {
        "normal": ("M128,156 Q145,148 163,153", "M237,153 Q255,148 272,156"),
        "happy": ("M128,152 Q146,140 164,148", "M236,148 Q254,140 272,152"),
        "up": ("M128,142 Q146,128 164,138", "M236,138 Q254,128 272,142"),
        "curious": ("M128,156 Q145,150 163,155", "M236,140 Q256,128 274,140"),
    }[kind]
    return "".join(
        f'<path d="{d}" fill="none" stroke="#C9AE86" stroke-width="5" stroke-linecap="round"/>'
        for d in shapes
    )


def lips():
    return f'<path d="M200,252 L200,262 M200,262 Q190,270 178,266 M200,262 Q210,270 222,266" fill="none" stroke="{MOUTHL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'


def mouth(kind="smile"):
    if kind == "smile":
        return (
            lips()
            + f'<path d="M180,272 Q200,286 220,272" fill="none" stroke="{MOUTHL}" stroke-width="2.4" stroke-linecap="round"/>'
        )
    if kind == "open":
        return (
            '<path d="M176,266 Q200,274 224,266 Q224,294 200,296 Q176,294 176,266 Z" fill="#6E2A2A" stroke="#7A3E2A" stroke-width="2.4" stroke-linejoin="round"/>'
            '<path d="M186,284 Q200,276 214,284 Q212,296 200,297 Q188,296 186,284 Z" fill="#FF8FA3"/>'
            + lips()
        )
    if kind == "o":
        return lips() + (
            '<ellipse cx="200" cy="280" rx="8.5" ry="9" fill="#6E2A2A" stroke="#7A3E2A" stroke-width="2.2"/>'
            '<ellipse cx="200" cy="284" rx="5" ry="3" fill="#FF8FA3"/>'
        )
    if kind == "curious":
        return (
            f'<path d="M200,252 L200,262 M200,262 Q190,270 178,268 M200,262 Q212,268 222,262" fill="none" stroke="{MOUTHL}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<path d="M222,262 Q226,262 227,258" fill="none" stroke="{MOUTHL}" stroke-width="2" stroke-linecap="round"/>'
        )


SPARKLE_D = "M0,-10 L2.5,-2.5 L10,0 L2.5,2.5 L0,10 L-2.5,2.5 L-10,0 L-2.5,-2.5 Z"
SURPRISE_MARKS = "M330,94 L340,78 M344,110 L360,104 M60,94 L50,78"
MARKS_COLOR = "#3A2618"


def blush_cheeks():
    return '<ellipse cx="114" cy="248" rx="20" ry="12" fill="#FF8D7A" opacity="0.4" filter="url(#b3)"/><ellipse cx="286" cy="248" rx="20" ry="12" fill="#FF8D7A" opacity="0.4" filter="url(#b3)"/>'


def sparkle(x, y, s, c=poses.SPARKLE):
    return f'<path transform="translate({x},{y}) scale({s})" d="{SPARKLE_D}" fill="{c}"/>'


# The adults use the same pose table (same head), shoulders a bit lower.
SL, SR = (148, 336), (252, 336)
POSE_DATA = poses.kid_poses(SL, SR, accents=("#8FD3F4", "#FFB5A7"), shadow=100)
body = torso

if __name__ == "__main__":
    poses.main(sys.modules[__name__], "#3A2618")
