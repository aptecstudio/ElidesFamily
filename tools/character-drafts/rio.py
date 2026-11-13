"""Draft of Rio (honey French bulldog) — same construction as elide.py.

Usage:
    python3 rio.py rio_poses.svg          # sheet with the 6 poses
    python3 rio.py rio_model.svg single   # idle model sheet
"""

import math
import sys

import parts
import poses

LINE = "#A8692A"  # honey fur outline
WLINE = "#C9A27A"  # white patches outline
SLINE = "#2A7AAE"  # overalls outline
TLINE = "#C9A23A"  # T-shirt outline
EYE = "#4A2E1C"
MOUTHL = "#7A3E2A"

DEFS = """<defs>
<filter id="b3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>
<radialGradient id="fur" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#FFD9A0"/><stop offset="0.55" stop-color="#E8B060"/><stop offset="1" stop-color="#C98A3E"/></radialGradient>
<radialGradient id="limb" cx="35%" cy="30%" r="85%"><stop offset="0" stop-color="#FBCB86"/><stop offset="1" stop-color="#CC8E45"/></radialGradient>
<radialGradient id="white" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#FFF6E8"/><stop offset="1" stop-color="#EAD9C4"/></radialGradient>
<radialGradient id="overall" cx="38%" cy="25%" r="85%"><stop offset="0" stop-color="#A6E0FA"/><stop offset="0.55" stop-color="#5DBDEB"/><stop offset="1" stop-color="#3A98CC"/></radialGradient>
<radialGradient id="shirt" cx="38%" cy="25%" r="85%"><stop offset="0" stop-color="#FFF0B8"/><stop offset="0.6" stop-color="#FFE08A"/><stop offset="1" stop-color="#E8C25A"/></radialGradient>
<linearGradient id="iris" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A2010"/><stop offset="0.5" stop-color="#7A4A22"/><stop offset="1" stop-color="#D2A46A"/></linearGradient>
<linearGradient id="nose" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A5244"/><stop offset="1" stop-color="#3A2420"/></linearGradient>
<linearGradient id="earIn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD0C4"/><stop offset="1" stop-color="#E89A8C"/></linearGradient>
<clipPath id="headC"><path d="M200,72 C276,72 322,120 324,188 C326,238 300,280 252,296 C236,302 218,304 200,304 C182,304 164,302 148,296 C100,280 74,238 76,188 C78,120 124,72 200,72 Z"/></clipPath>
<clipPath id="torsoC"><path d="M156,300 Q200,292 244,300 C252,330 258,370 261,400 C263,420 262,434 257,442 L212,444 Q200,430 188,444 L143,442 C138,434 137,420 139,400 C142,370 148,330 156,300 Z"/></clipPath>
<clipPath id="eyeLC"><ellipse cx="150" cy="198" rx="30" ry="31"/></clipPath>
<clipPath id="eyeRC"><ellipse cx="250" cy="198" rx="30" ry="31"/></clipPath>
</defs>"""

HEADP = "M200,72 C276,72 322,120 324,188 C326,238 300,280 252,296 C236,302 218,304 200,304 C182,304 164,302 148,296 C100,280 74,238 76,188 C78,120 124,72 200,72 Z"
TORSOP = "M156,300 Q200,292 244,300 C252,330 258,370 261,400 C263,420 262,434 257,442 L212,444 Q200,430 188,444 L143,442 C138,434 137,420 139,400 C142,370 148,330 156,300 Z"


def limb(p0, p1, p2, p3, w0, w1, bulge=3, fill="url(#limb)", layer="both"):
    steps = 40

    def bez_at(t, a, b, c, d):
        return (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t**3 * d

    def dbez_at(t, a, b, c, d):
        return 3 * (1 - t) ** 2 * (b - a) + 6 * (1 - t) * t * (c - b) + 3 * t * t * (d - c)

    left = []
    right = []
    for i in range(steps + 1):
        t = i / steps
        x = bez_at(t, p0[0], p1[0], p2[0], p3[0])
        y = bez_at(t, p0[1], p1[1], p2[1], p3[1])
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
    if layer == "outline":
        return parts.merged_outline(d, LINE)
    if layer == "fill":
        return f'<path d="{d}" fill="{fill}"/>'
    return (
        f'<path d="{d}" fill="{fill}" stroke="{LINE}" stroke-width="2.6" stroke-linejoin="round"/>'
    )


FOOT_D = "M-21,4 C-23,-8 -12,-14 0,-14 C12,-14 23,-8 21,4 C21,11 12,14 0,14 C-12,14 -21,11 -21,4 Z"


def foot(x, y, layer="both"):
    """Foot; layer "outline" / "fill" / "both" as in parts.paw, so the foot
    and the leg merge into one piece."""
    o = [f'<g transform="translate({x},{y}) scale(1.25)">']
    if layer in ("outline", "both"):
        o.append(parts.merged_outline(FOOT_D, LINE, 2.6 / 1.25))
    if layer in ("fill", "both"):
        o.append(f'<path d="{FOOT_D}" fill="url(#limb)"/>')
        o.append(
            f'<path d="M-9,3 C-10,8 -9,11 -8,13 M0,4 C0,9 0,12 0,14 M9,3 C10,8 9,11 8,13" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'
        )
        o.append('<ellipse cx="-6" cy="-6" rx="7" ry="3" fill="#FFE7BF" opacity="0.8"/>')
    o.append("</g>")
    return "".join(o)


TAIL_D = "M254,420 C276,420 288,406 280,394 C276,388 268,392 270,398"
TAIL_ROOT = (254, 420)
# Legs: Bezier control points, root width, tip width, bulge; foot position.
LEGS = (
    (((172, 432), (171, 450), (171, 468), (172, 486)), 44, 38, 2, (170, 496)),
    (((228, 432), (229, 450), (229, 468), (228, 486)), 44, 38, 2, (230, 496)),
)


def tail():
    """Short curly tail, typical of the French bulldog."""
    return (
        f'<path d="{TAIL_D}" fill="none" stroke="{LINE}" stroke-width="21" stroke-linecap="round"/>'
        f'<path d="{TAIL_D}" fill="none" stroke="#E2A85A" stroke-width="16" stroke-linecap="round"/>'
    )


def body_lower():
    o = [tail()]
    # Each leg and its foot are one piece: all the outlines, then the fills.
    for layer in ("outline", "fill"):
        for pts, w0, w1, bulge, _ in LEGS:
            o.append(limb(*pts, w0, w1, bulge, layer=layer))
        for *_, (fx, fy) in LEGS:
            o.append(foot(fx, fy, layer))
    return "".join(o)


def torso():
    """Butter-yellow striped T-shirt + sky-blue overalls."""
    o = []
    o.append(f'<path d="{TORSOP}" fill="url(#shirt)"/>')
    o.append('<g clip-path="url(#torsoC)">')
    for y in (310, 328, 346):
        o.append(f'<rect x="120" y="{y}" width="160" height="7" fill="#FFFFFF" opacity="0.85"/>')
    # overalls: bib + shorts
    o.append(
        f'<path d="M168,322 Q200,318 232,322 L236,364 C252,366 262,372 264,390 L264,450 L136,450 L136,390 C138,372 148,366 164,364 Z" fill="url(#overall)" stroke="{SLINE}" stroke-width="2.6" stroke-linejoin="round"/>'
    )
    o.append(
        '<ellipse cx="200" cy="370" rx="60" ry="10" fill="#1F5F8A" opacity="0.35" filter="url(#b6)"/>'
    )
    o.append(
        '<ellipse cx="258" cy="410" rx="22" ry="50" fill="#1F5F8A" opacity="0.3" filter="url(#b12)"/>'
    )
    o.append(
        '<ellipse cx="160" cy="400" rx="12" ry="34" fill="#DDF4FF" opacity="0.5" filter="url(#b6)"/>'
    )
    o.append("</g>")
    o.append(
        f'<path d="{TORSOP}" fill="none" stroke="{SLINE}" stroke-width="2.6" stroke-linejoin="round"/>'
    )
    # seams and hems of the shorts
    o.append(
        '<path d="M170,326 Q200,322 230,326 L233,360 Q200,366 167,360 Z" fill="none" stroke="#FFFFFF" stroke-width="1.6" stroke-dasharray="3 3" opacity="0.8"/>'
    )
    o.append(
        f'<path d="M145,434 L188,436 M212,436 L255,434" fill="none" stroke="{SLINE}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>'
    )
    o.append(
        f'<path d="M200,368 L200,432" fill="none" stroke="{SLINE}" stroke-width="1.6" stroke-linecap="round" opacity="0.55"/>'
    )
    # small pocket with an embroidered bone
    o.append(
        f'<path d="M186,334 L214,334 L213,352 Q200,358 187,352 Z" fill="#76CCF2" stroke="{SLINE}" stroke-width="2" stroke-linejoin="round"/>'
    )
    o.append(
        '<g transform="translate(200,344)"><rect x="-6" y="-1.6" width="12" height="3.2" fill="#FFFFFF"/>'
        '<circle cx="-6.5" cy="-2.2" r="2.4" fill="#FFFFFF"/><circle cx="-6.5" cy="2.2" r="2.4" fill="#FFFFFF"/>'
        '<circle cx="6.5" cy="-2.2" r="2.4" fill="#FFFFFF"/><circle cx="6.5" cy="2.2" r="2.4" fill="#FFFFFF"/></g>'
    )
    return "".join(o)


def sleeves():
    """Neckline and overall straps (the sleeves follow the arm, see parts.arm)."""
    o = []
    # neckline with the white chest patch
    o.append(
        f'<path d="M174,300 Q200,330 226,300 Q200,293 174,300 Z" fill="url(#white)" stroke="{TLINE}" stroke-width="3" stroke-linejoin="round"/>'
    )
    o.append(
        f'<path d="M190,312 Q196,316 200,314 M204,318 Q208,316 210,312" fill="none" stroke="{WLINE}" stroke-width="1.6" stroke-linecap="round"/>'
    )
    # straps and buttons
    for x0, y0, x1, y1 in ((171, 324, 162, 298), (229, 324, 238, 298)):
        o.append(
            f'<path d="M{x0},{y0} L{x1},{y1}" stroke="{SLINE}" stroke-width="15" stroke-linecap="round"/>'
        )
        o.append(
            f'<path d="M{x0},{y0} L{x1},{y1}" stroke="url(#overall)" stroke-width="10" stroke-linecap="round"/>'
        )
        o.append(
            f'<circle cx="{x0}" cy="{y0 + 2}" r="5.5" fill="#FFE08A" stroke="{TLINE}" stroke-width="1.8"/>'
        )
    return "".join(o)


def head_base():
    o = []
    # Rio's right ear (viewer's left): bat-like, upright and round
    o.append('<g transform="translate(400,0) scale(-1,1)">')
    o.append(
        f'<path d="M228,98 C228,54 256,20 290,20 C326,22 334,72 316,150 Z" fill="url(#fur)" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
    )
    o.append(
        '<path d="M244,100 C246,64 266,38 290,38 C314,42 318,84 304,136 Z" fill="url(#earIn)"/>'
    )
    o.append("</g>")
    o.append(f'<path d="{HEADP}" fill="url(#fur)"/>')
    o.append(
        '<g clip-path="url(#headC)">'
        '<ellipse cx="200" cy="300" rx="130" ry="30" fill="#A86A2A" opacity="0.4" filter="url(#b12)"/>'
        '<ellipse cx="318" cy="200" rx="18" ry="90" fill="#B07330" opacity="0.35" filter="url(#b12)"/>'
        '<ellipse cx="170" cy="112" rx="56" ry="24" fill="#FFE7BF" opacity="0.9" filter="url(#b6)"/>'
        # white blaze from the forehead down to the muzzle
        f'<path d="M200,104 C210,104 214,140 216,180 C218,206 226,222 232,232 L168,232 C174,222 182,206 184,180 C186,140 190,104 200,104 Z" fill="url(#white)" stroke="{WLINE}" stroke-width="2"/>'
        "</g>"
    )
    o.append(
        f'<path d="{HEADP}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
    )
    # Rio's left ear (viewer's right): soft, folded, falling on the side of the head
    o.append('<g transform="translate(400,0) scale(-1,1)">')
    o.append(
        f'<path d="M160,90 C130,74 86,78 64,104 C48,124 50,160 64,182 C70,190 80,188 86,178 C96,160 104,140 118,124 C130,110 146,102 162,100 Z" fill="url(#fur)" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
    )
    o.append(
        '<path d="M150,92 C118,86 90,98 76,122" fill="none" stroke="#FFE7BF" stroke-width="5" stroke-linecap="round" opacity="0.7"/>'
    )
    o.append(
        f'<path d="M154,100 C130,104 112,120 100,140" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round" opacity="0.5"/>'
    )
    o.append(
        '<ellipse cx="70" cy="168" rx="7" ry="11" fill="#B07330" opacity="0.35" filter="url(#b3)"/>'
    )
    o.append("</g>")
    # small forehead wrinkles
    o.append(
        f'<path d="M176,128 Q186,122 192,128 M208,128 Q214,122 224,128" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>'
    )
    # wide white muzzle
    o.append(
        f'<path d="M200,218 C250,218 280,242 280,270 C280,296 244,306 200,306 C156,306 120,296 120,270 C120,242 150,218 200,218 Z" fill="url(#white)" stroke="{WLINE}" stroke-width="2"/>'
    )
    o.append(
        '<ellipse cx="112" cy="252" rx="17" ry="10" fill="#FF8D7A" opacity="0.45" filter="url(#b3)"/><ellipse cx="288" cy="252" rx="17" ry="10" fill="#FF8D7A" opacity="0.45" filter="url(#b3)"/>'
    )
    # whisker dots
    for x, y in ((158, 262), (150, 272), (162, 276), (242, 262), (250, 272), (238, 276)):
        o.append(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WLINE}"/>')
    # big dark shiny nose
    o.append(
        '<path d="M182,232 Q200,224 218,232 Q221,246 207,252 L193,252 Q179,246 182,232 Z" fill="url(#nose)" stroke="#2E1C18" stroke-width="2" stroke-linejoin="round"/>'
    )
    o.append('<ellipse cx="194" cy="234" rx="6" ry="2.6" fill="#FFFFFF" opacity="0.85"/>')
    o.append(
        '<path d="M193,244 Q196,246 197,243 M203,243 Q204,246 207,244" fill="none" stroke="#1E120F" stroke-width="1.8" stroke-linecap="round"/>'
    )
    return "".join(o)


# Eye geometry, shared with the animation rig (export_rig.py).
EYE_X = (150, 250)
EYE_CY, EYE_RX, EYE_RY = 198, 30, 31
OPEN_EYES = ("open", "wide", "smiling")
PUPIL = "#1A0E08"


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
    return f'<path d="M{cx - 34},232 Q{cx},210 {cx + 34},232 L{cx + 34},240 L{cx - 34},240 Z" fill="#E8B060"/>'


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
        f'<path d="{d}" fill="none" stroke="#9A5E24" stroke-width="5" stroke-linecap="round"/>'
        for d in shapes
    )


def lips():
    """The bulldog's "W"-shaped upper lip."""
    return f'<path d="M200,252 L200,262 M200,262 Q190,272 176,266 M200,262 Q210,272 224,266" fill="none" stroke="{MOUTHL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'


def mouth(kind="smile"):
    if kind == "smile":
        return lips() + (
            f'<path d="M172,262 Q170,268 175,270 M228,262 Q230,268 225,270" fill="none" stroke="{MOUTHL}" stroke-width="2" stroke-linecap="round"/>'
        )
    if kind == "open":
        # open mouth with a little pink tongue
        return (
            '<path d="M176,266 Q200,274 224,266 Q224,294 200,296 Q176,294 176,266 Z" fill="#6E2A2A" stroke="#7A3E2A" stroke-width="2.4" stroke-linejoin="round"/>'
            '<path d="M186,284 Q200,276 214,284 Q214,300 200,302 Q186,300 186,284 Z" fill="#FF8FA3" stroke="#D9607A" stroke-width="1.8"/>'
            '<path d="M200,284 L200,294" stroke="#D9607A" stroke-width="1.6" stroke-linecap="round"/>'
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
MARKS_COLOR = "#4A2E1C"
PAD = "#B9705A"


def blush_cheeks():
    return '<ellipse cx="114" cy="248" rx="20" ry="12" fill="#FF7F6A" opacity="0.4" filter="url(#b3)"/><ellipse cx="286" cy="248" rx="20" ry="12" fill="#FF7F6A" opacity="0.4" filter="url(#b3)"/>'


def sparkle(x, y, s, c=poses.SPARKLE):
    return f'<path transform="translate({x},{y}) scale({s})" d="{SPARKLE_D}" fill="{c}"/>'


SL, SR = (150, 316), (250, 316)
SLEEVE = dict(
    fill="url(#shirt)", line=TLINE, t1=0.28, w0=42, w1=36, trim="#FFE9A6", trim_line=TLINE
)


def arm(p0, p1, p2, p3, kind="back", hand_rot=None, fold=None):
    return parts.arm(p0, p1, p2, p3, "url(#limb)", LINE, kind, hand_rot, SLEEVE, pad=PAD, fold=fold)


# Poses shared with Elide (same body): see poses.py.
POSE_DATA = poses.kid_poses(SL, SR, accents=("#8FD3F4", "#FFB5A7"))
body = torso
collar = sleeves

if __name__ == "__main__":
    poses.main(sys.modules[__name__], "#4A2E1C")
