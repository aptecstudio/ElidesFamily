"""Draft of Mom (Mamma, honey cat with white patches) — head like Elide, adult body like Dad.

Usage:
    python3 mom.py mom_poses.svg          # sheet with the 6 poses
    python3 mom.py mom_model.svg single   # idle model sheet
"""

import math
import sys

import parts

OUT = sys.argv[1]
LINE = "#A8692A"  # honey fur outline
WLINE = "#C9A27A"  # white parts outline
DLINE = "#6E5BB0"  # dress outline
EYE = "#3B2C2A"
MOUTHL = "#B8406A"
H = 580  # adult scene height (like Dad)

DEFS = """<defs>
<filter id="b3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>
<radialGradient id="fur" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#FFD9A0"/><stop offset="0.55" stop-color="#E8B060"/><stop offset="1" stop-color="#C98A3E"/></radialGradient>
<radialGradient id="limb" cx="35%" cy="30%" r="85%"><stop offset="0" stop-color="#FBCB86"/><stop offset="1" stop-color="#CC8E45"/></radialGradient>
<radialGradient id="white" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#FFF6E8"/><stop offset="1" stop-color="#EAD9C4"/></radialGradient>
<radialGradient id="dress" cx="38%" cy="25%" r="85%"><stop offset="0" stop-color="#E6DDFB"/><stop offset="0.55" stop-color="#C7B8F5"/><stop offset="1" stop-color="#9E8BDB"/></radialGradient>
<radialGradient id="belt" cx="38%" cy="25%" r="85%"><stop offset="0" stop-color="#A897E0"/><stop offset="1" stop-color="#7A64C2"/></radialGradient>
<linearGradient id="iris" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0F4A2A"/><stop offset="0.5" stop-color="#2E9B5A"/><stop offset="1" stop-color="#A8E6A0"/></linearGradient>
<linearGradient id="nose" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9BB8"/><stop offset="1" stop-color="#D9507A"/></linearGradient>
<linearGradient id="earIn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD0DE"/><stop offset="1" stop-color="#F49DB8"/></linearGradient>
<clipPath id="headC"><path d="M200,72 C276,72 322,120 324,188 C326,238 300,280 252,296 C236,302 218,304 200,304 C182,304 164,302 148,296 C100,280 74,238 76,188 C78,120 124,72 200,72 Z"/></clipPath>
<clipPath id="skirtC"><path d="M148,356 Q200,348 252,356 C264,388 276,428 284,462 Q200,482 116,462 C124,428 136,388 148,356 Z"/></clipPath>
<clipPath id="eyeLC"><ellipse cx="150" cy="198" rx="30" ry="31"/></clipPath>
<clipPath id="eyeRC"><ellipse cx="250" cy="198" rx="30" ry="31"/></clipPath>
</defs>"""

HEADP = "M200,72 C276,72 322,120 324,188 C326,238 300,280 252,296 C236,302 218,304 200,304 C182,304 164,302 148,296 C100,280 74,238 76,188 C78,120 124,72 200,72 Z"
BODICEP = "M154,302 Q200,294 246,302 C258,322 262,342 256,362 L144,362 C138,342 142,322 154,302 Z"
SKIRTP = (
    "M148,356 Q200,348 252,356 C264,388 276,428 284,462 Q200,482 116,462 C124,428 136,388 148,356 Z"
)


def bez(t, p0, p1, p2, p3):
    return tuple(
        (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t**3 * d
        for a, b, c, d in zip(p0, p1, p2, p3, strict=True)
    )


def limb(
    p0,
    p1,
    p2,
    p3,
    w0,
    w1,
    bulge=3,
    fill="url(#limb)",
    line=LINE,
    t0=0.0,
    t1=1.0,
    cap=True,
    layer="both",
):
    steps = 40

    def dbez_at(t, a, b, c, d):
        return 3 * (1 - t) ** 2 * (b - a) + 6 * (1 - t) * t * (c - b) + 3 * t * t * (d - c)

    left = []
    right = []
    for i in range(steps + 1):
        t = t0 + (t1 - t0) * i / steps
        x, y = bez(t, p0, p1, p2, p3)
        dx = dbez_at(t, p0[0], p1[0], p2[0], p3[0])
        dy = dbez_at(t, p0[1], p1[1], p2[1], p3[1])
        length = math.hypot(dx, dy) or 1
        nx, ny = -dy / length, dx / length
        w = (w0 + (w1 - w0) * t) / 2 + bulge * math.sin(math.pi * t)
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    d = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % q for q in left[1:])
    if cap:
        d += " A%.1f,%.1f 0 0 1 %.1f,%.1f " % (w1 / 2, w1 / 2, right[-1][0], right[-1][1])
    else:
        d += " L%.1f,%.1f " % right[-1]
    d += " ".join("L%.1f,%.1f" % q for q in reversed(right)) + " Z"
    if layer == "outline":
        return parts.merged_outline(d, line)
    if layer == "fill":
        return f'<path d="{d}" fill="{fill}"/>'
    return (
        f'<path d="{d}" fill="{fill}" stroke="{line}" stroke-width="2.6" stroke-linejoin="round"/>'
    )


def arm(p0, p1, p2, p3, kind="back", hand_rot=None):
    """Honey arm, short lavender puff sleeve, white paw."""
    return parts.arm(
        p0,
        p1,
        p2,
        p3,
        "url(#limb)",
        LINE,
        kind,
        hand_rot,
        SLEEVE,
        hand_fill="url(#white)",
        hand_line=WLINE,
        pad="#F7B7CB",
    )


SLEEVE = dict(fill="url(#dress)", line=DLINE, t1=0.34, w0=40, w1=34)


FOOT_D = "M-21,4 C-23,-8 -12,-14 0,-14 C12,-14 23,-8 21,4 C21,11 12,14 0,14 C-12,14 -21,11 -21,4 Z"


def foot(x, y, layer="both"):
    """Foot; layer "outline" / "fill" / "both" as in parts.paw, so the foot
    and the leg merge into one piece."""
    o = [f'<g transform="translate({x},{y}) scale(1.25)">']
    if layer in ("outline", "both"):
        o.append(parts.merged_outline(FOOT_D, WLINE, 2.6 / 1.25))
    if layer in ("fill", "both"):
        o.append(f'<path d="{FOOT_D}" fill="url(#white)"/>')
        o.append(
            f'<path d="M-9,3 C-10,8 -9,11 -8,13 M0,4 C0,9 0,12 0,14 M9,3 C10,8 9,11 8,13" fill="none" stroke="{WLINE}" stroke-width="2" stroke-linecap="round"/>'
        )
        o.append('<ellipse cx="-6" cy="-6" rx="7" ry="3" fill="#FFFFFF" opacity="0.8"/>')
    o.append("</g>")
    return "".join(o)


def body_lower():
    o = []
    # cat tail, curled like Elide's
    o.append(
        f'<path d="M258,440 C304,442 330,404 324,366 C320,340 298,336 292,352 C288,364 302,370 306,360" fill="none" stroke="{LINE}" stroke-width="22" stroke-linecap="round"/>'
    )
    o.append(
        '<path d="M258,440 C304,442 330,404 324,366 C320,340 298,336 292,352 C288,364 302,370 306,360" fill="none" stroke="#E2A85A" stroke-width="17" stroke-linecap="round"/>'
    )
    # Each leg and its foot are one piece: all the outlines, then the fills.
    for layer in ("outline", "fill"):
        o.append(limb((174, 446), (173, 468), (173, 488), (174, 506), 44, 38, 2, layer=layer))
        o.append(limb((226, 446), (227, 468), (227, 488), (226, 506), 44, 38, 2, layer=layer))
        o.append(foot(172, 520, layer))
        o.append(foot(228, 520, layer))
    return "".join(o)


def dress():
    o = []
    # knee-length bell skirt
    o.append(f'<path d="{SKIRTP}" fill="url(#dress)"/>')
    o.append(
        '<g clip-path="url(#skirtC)">'
        '<ellipse cx="262" cy="420" rx="30" ry="70" fill="#5E4BA0" opacity="0.3" filter="url(#b12)"/>'
        '<ellipse cx="160" cy="410" rx="16" ry="50" fill="#FFFFFF" opacity="0.45" filter="url(#b6)"/></g>'
    )
    o.append(
        f'<path d="{SKIRTP}" fill="none" stroke="{DLINE}" stroke-width="2.6" stroke-linejoin="round"/>'
    )
    o.append(
        f'<path d="M170,372 Q162,420 152,462 M200,370 L200,470 M230,372 Q238,420 248,462" fill="none" stroke="{DLINE}" stroke-width="1.6" stroke-linecap="round" opacity="0.35"/>'
    )
    o.append(
        '<path d="M122,452 Q200,470 278,452" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="4 4" opacity="0.8"/>'
    )
    # bodice
    o.append(
        f'<path d="{BODICEP}" fill="url(#dress)" stroke="{DLINE}" stroke-width="2.6" stroke-linejoin="round"/>'
    )
    o.append(
        '<ellipse cx="200" cy="304" rx="60" ry="14" fill="#5E4BA0" opacity="0.35" filter="url(#b6)"/>'
    )
    # neckline with the white chest
    o.append(
        f'<path d="M174,300 Q200,332 226,300 Q200,293 174,300 Z" fill="url(#white)" stroke="{DLINE}" stroke-width="2.4" stroke-linejoin="round"/>'
    )
    # belt with a little bow
    o.append(
        f'<path d="M142,352 Q200,344 258,352 L258,366 Q200,358 142,366 Z" fill="url(#belt)" stroke="{DLINE}" stroke-width="2.2" stroke-linejoin="round"/>'
    )
    o.append(
        '<g transform="translate(222,358)">'
        f'<path d="M0,0 C-8,-12 -24,-12 -24,-2 C-24,8 -8,8 0,0 Z" fill="url(#belt)" stroke="{DLINE}" stroke-width="2"/>'
        f'<path d="M0,0 C8,-12 24,-12 24,-2 C24,8 8,8 0,0 Z" fill="url(#belt)" stroke="{DLINE}" stroke-width="2"/>'
        f'<path d="M-3,2 L-10,20 L-4,17 L-2,22 L2,4 M3,2 L10,20 L4,17 L2,22" fill="url(#belt)" stroke="{DLINE}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<rect x="-5" y="-6" width="10" height="12" rx="4" fill="#B6A6EA" stroke="{DLINE}" stroke-width="1.8"/>'
        '<ellipse cx="-14" cy="-5" rx="4" ry="2" fill="#FFFFFF" opacity="0.6"/></g>'
    )
    return "".join(o)


def glasses():
    """Round glasses with a thin dark-lavender frame."""
    return (
        f'<circle cx="150" cy="198" r="39" fill="#FFFFFF" fill-opacity="0.12" stroke="{DLINE}" stroke-width="4"/>'
        f'<circle cx="250" cy="198" r="39" fill="#FFFFFF" fill-opacity="0.12" stroke="{DLINE}" stroke-width="4"/>'
        f'<path d="M189,194 Q200,186 211,194" fill="none" stroke="{DLINE}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M111,192 L82,186 M289,192 L318,186" fill="none" stroke="{DLINE}" stroke-width="4" stroke-linecap="round"/>'
        '<path d="M124,176 Q132,166 144,164 M224,176 Q232,166 244,164" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.75"/>'
    )


def head_base():
    o = []
    o.append(
        f'<path d="M98,138 C88,96 92,58 106,50 C126,54 150,76 166,92 Z" fill="url(#fur)" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
    )
    o.append(
        '<path d="M108,124 C100,94 102,72 112,68 C128,74 142,86 152,98 Z" fill="url(#earIn)"/>'
    )
    o.append(
        f'<path d="M302,138 C312,96 308,58 294,50 C274,54 250,76 234,92 Z" fill="url(#fur)" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
    )
    o.append(
        '<path d="M292,124 C300,94 298,72 288,68 C272,74 258,86 248,98 Z" fill="url(#earIn)"/>'
    )
    o.append(f'<path d="{HEADP}" fill="url(#fur)"/>')
    o.append(
        '<g clip-path="url(#headC)"><ellipse cx="200" cy="300" rx="130" ry="30" fill="#A86A2A" opacity="0.4" filter="url(#b12)"/>'
        '<ellipse cx="318" cy="200" rx="18" ry="90" fill="#B07330" opacity="0.35" filter="url(#b12)"/>'
        '<ellipse cx="170" cy="112" rx="56" ry="24" fill="#FFE7BF" opacity="0.9" filter="url(#b6)"/></g>'
    )
    o.append(
        f'<path d="{HEADP}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
    )
    o.append(
        f'<path d="M80,206 L66,212 L80,220 L70,230 L86,232 M320,206 L334,212 L320,220 L330,230 L314,232" fill="url(#fur)" stroke="{LINE}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>'
    )
    # soft side-swept tuft, like Elide's
    o.append(
        f'<path d="M162,90 C170,60 210,48 240,66 C224,66 212,74 206,86 C196,76 178,76 162,90 Z" fill="url(#fur)" stroke="{LINE}" stroke-width="2.8" stroke-linejoin="round"/>'
    )
    # white muzzle
    o.append(
        f'<path d="M200,222 C240,222 266,244 266,268 C266,292 236,302 200,302 C164,302 134,292 134,268 C134,244 160,222 200,222 Z" fill="url(#white)" stroke="{WLINE}" stroke-width="2"/>'
    )
    o.append(
        '<ellipse cx="112" cy="250" rx="18" ry="11" fill="#FF8DB0" opacity="0.45" filter="url(#b3)"/><ellipse cx="288" cy="250" rx="18" ry="11" fill="#FF8DB0" opacity="0.45" filter="url(#b3)"/>'
    )
    o.append(
        '<path d="M187,236 Q200,231 213,236 Q209,249 200,253 Q191,249 187,236 Z" fill="url(#nose)" stroke="#B8406A" stroke-width="2" stroke-linejoin="round"/><ellipse cx="196" cy="237" rx="4" ry="2" fill="#FFFFFF" opacity="0.9"/>'
    )
    o.append(
        f'<path d="M200,253 L200,259" fill="none" stroke="{MOUTHL}" stroke-width="2.2" stroke-linecap="round"/>'
    )
    return "".join(o)


def eye(cx, side, dx=0, dy=0, kind="open"):
    """Like Elide (with eyelashes), green iris."""
    o = []
    clip = "eyeLC" if side == "L" else "eyeRC"
    left = side == "L"
    if kind in ("open", "wide", "smiling"):
        o.append(
            f'<ellipse cx="{cx}" cy="198" rx="30" ry="31" fill="#FFFFFF" stroke="{EYE}" stroke-width="2.2"/>'
        )
        r = 25 if kind != "wide" else 21
        pr = 11.5 if kind != "wide" else 8
        ix = cx + (1 if left else -1) + dx
        iy = 201 + dy + (0 if kind != "wide" else -3)
        o.append(
            f'<g clip-path="url(#{clip})"><circle cx="{ix}" cy="{iy}" r="{r}" fill="url(#iris)"/><circle cx="{ix}" cy="{iy + 1}" r="{pr}" fill="#08200F"/>'
            f'<ellipse cx="{ix + 8}" cy="{iy - 10}" rx="7.5" ry="8.5" fill="#FFFFFF"/><circle cx="{ix - 9}" cy="{iy + 10}" r="3.4" fill="#FFFFFF" opacity="0.9"/>'
        )
        if kind == "smiling":
            o.append(
                f'<path d="M{cx - 34},232 Q{cx},210 {cx + 34},232 L{cx + 34},240 L{cx - 34},240 Z" fill="#E8B060"/>'
            )
        o.append("</g>")
        if kind == "smiling":
            o.append(
                f'<path d="M{cx - 26},222 Q{cx},212 {cx + 26},222" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'
            )
        lift = -5 if kind == "wide" else 0
        if left:
            o.append(
                f'<path d="M121,{193 + lift} Q150,{162 + lift} 179,{191 + lift}" fill="none" stroke="{EYE}" stroke-width="4" stroke-linecap="round"/>'
            )
            o.append(
                f'<path d="M123,{185 + lift} Q115,{180 + lift} 109,{181 + lift} M128,{177 + lift} Q122,{171 + lift} 117,{169 + lift}" fill="none" stroke="{EYE}" stroke-width="2.8" stroke-linecap="round"/>'
            )
        else:
            o.append(
                f'<path d="M221,{191 + lift} Q250,{162 + lift} 279,{193 + lift}" fill="none" stroke="{EYE}" stroke-width="4" stroke-linecap="round"/>'
            )
            o.append(
                f'<path d="M277,{185 + lift} Q285,{180 + lift} 291,{181 + lift} M272,{177 + lift} Q278,{171 + lift} 283,{169 + lift}" fill="none" stroke="{EYE}" stroke-width="2.8" stroke-linecap="round"/>'
            )
    elif kind == "happy":
        o.append(
            f'<path d="M{cx - 25},206 Q{cx},182 {cx + 25},206" fill="none" stroke="{EYE}" stroke-width="4.6" stroke-linecap="round"/>'
        )
        ox = cx - 25 if left else cx + 25
        s_ = -1 if left else 1
        o.append(
            f'<path d="M{ox},204 Q{ox + 7 * s_},200 {ox + 12 * s_},201 M{ox + 3 * -s_},196 Q{ox + 3 * s_},190 {ox + 7 * s_},188" fill="none" stroke="{EYE}" stroke-width="2.6" stroke-linecap="round"/>'
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
        f'<path d="{d}" fill="none" stroke="#9A5E24" stroke-width="4.2" stroke-linecap="round"/>'
        for d in shapes
    )


def mouth(kind="smile"):
    if kind == "smile":
        return (
            f'<path d="M180,263 Q200,280 220,263" fill="none" stroke="{MOUTHL}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<path d="M178,260 Q178,264 181,266 M222,260 Q222,264 219,266" fill="none" stroke="{MOUTHL}" stroke-width="2" stroke-linecap="round"/>'
        )
    if kind == "open":
        return (
            '<path d="M176,260 Q200,268 224,260 Q224,292 200,294 Q176,292 176,260 Z" fill="#8E2742" stroke="#B8406A" stroke-width="2.4" stroke-linejoin="round"/>'
            '<path d="M186,284 Q200,274 214,284 Q210,293 200,293 Q190,293 186,284 Z" fill="#FF8FA3"/>'
            '<path d="M180,262 Q200,268 220,262 L219,266 Q200,272 181,266 Z" fill="#FFFFFF" opacity="0.9"/>'
        )
    if kind == "o":
        return (
            '<ellipse cx="200" cy="274" rx="8.5" ry="10" fill="#8E2742" stroke="#B8406A" stroke-width="2.2"/>'
            '<ellipse cx="200" cy="279" rx="5" ry="3" fill="#FF8FA3"/>'
        )
    if kind == "curious":
        return (
            f'<path d="M188,268 Q201,276 214,264" fill="none" stroke="{MOUTHL}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<path d="M213,261 Q216,263 216,266" fill="none" stroke="{MOUTHL}" stroke-width="2" stroke-linecap="round"/>'
        )


def sparkle(x, y, s, c="#FFD84A"):
    return f'<path transform="translate({x},{y}) scale({s})" d="M0,-10 L2.5,-2.5 L10,0 L2.5,2.5 L0,10 L-2.5,2.5 L-10,0 L-2.5,-2.5 Z" fill="{c}"/>'


SL, SR = (148, 322), (252, 322)


def arm_l_down():
    return arm(SL, (132, 348), (124, 376), (126, 398))


def arm_r_down():
    return arm(SR, (268, 348), (276, 376), (274, 398))


def character(pose):
    o = []
    lift = -16 if pose == "cheer" else 0
    shadow_rx = 82 if pose == "cheer" else 104
    o.append(
        f'<ellipse cx="200" cy="544" rx="{shadow_rx}" ry="11" fill="#1D5A3A" opacity="0.28" filter="url(#b6)"/>'
    )
    lean = {"idle": 0, "wave": -2, "cheer": 0, "curious": 2, "surprised": 0, "proud": -2}[pose]
    o.append(f'<g transform="translate(0,{lift}) rotate({lean} 200 530)">')
    o.append(body_lower())
    back = []
    front = []
    if pose == "idle":
        back = arm_l_down() + arm_r_down()
        face = ("open", "open", 0, 0, "normal", "smile", -3, False)
    elif pose == "wave":
        back = arm_l_down() + arm(SR, (284, 318), (300, 296), (306, 264), "palm")
        face = ("smiling", "smiling", 0, 0, "happy", "open", -6, True)
    elif pose == "cheer":
        back = arm(SL, (120, 310), (104, 286), (100, 256), "palm") + arm(
            SR, (280, 310), (296, 286), (300, 256), "palm"
        )
        face = ("happy", "happy", 0, 0, "up", "open", 3, True)
    elif pose == "curious":
        back = arm_l_down()
        front = arm(SR, (286, 380), (262, 376), (244, 330), "fist", -24)
        face = ("open", "open", 7, -8, "curious", "curious", 8, False)
    elif pose == "surprised":
        front = arm(SL, (112, 330), (96, 304), (98, 276), "palm", 18) + arm(
            SR, (288, 330), (304, 304), (302, 276), "palm", -18
        )
        face = ("wide", "wide", 0, 0, "up", "o", 0, False)
    elif pose == "proud":
        back = arm_l_down()
        front = arm(SR, (290, 346), (306, 328), (302, 304), "thumb", 0)
        face = ("happy", "smiling", 0, 0, "happy", "open", -5, True)
    o.append(dress())
    o.extend(back)
    eye_l, eye_r, dx, dy, br, mo, tilt, blush = face
    o.append(f'<g transform="rotate({tilt} 200 300)">')
    o.append(head_base())
    if blush:
        o.append(
            '<ellipse cx="114" cy="246" rx="20" ry="12" fill="#FF7FA5" opacity="0.45" filter="url(#b3)"/><ellipse cx="286" cy="246" rx="20" ry="12" fill="#FF7FA5" opacity="0.45" filter="url(#b3)"/>'
        )
    o.append(brows(br))
    o.append(eye(150, "L", dx, dy, eye_l))
    o.append(eye(250, "R", dx, dy, eye_r))
    o.append(glasses())
    o.append(mouth(mo))
    o.append("</g>")
    o.extend(front)
    if pose == "cheer":
        o.append(sparkle(48, 210, 1.5))
        o.append(sparkle(356, 186, 1.2))
        o.append(sparkle(346, 340, 1.0, "#8FD3F4"))
        o.append(sparkle(54, 350, 0.9, "#FFB5A7"))
    if pose == "proud":
        o.append(sparkle(338, 262, 1.1))
    if pose == "surprised":
        o.append(
            '<path d="M330,94 L340,78 M344,110 L360,104 M60,94 L50,78" fill="none" stroke="#3B2C2A" stroke-width="3.5" stroke-linecap="round"/>'
        )
    o.append("</g>")
    return "".join(o)


POSES = [
    ("idle", "Idle"),
    ("wave", "Hi!"),
    ("cheer", "Hooray!"),
    ("curious", "Curious"),
    ("surprised", "Surprised"),
    ("proud", "Well done!"),
]
mode = sys.argv[2] if len(sys.argv) > 2 else "sheet"
if mode == "single":
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{H * 2}" viewBox="0 0 400 {H}">{DEFS}{character("idle")}</svg>'
else:
    cw, ch = 400, H + 60
    cells = []
    for i, (p, label) in enumerate(POSES):
        cx = (i % 3) * cw
        cy = (i // 3) * ch
        cells.append(
            f'<g transform="translate({cx},{cy})">{character(p)}<text x="200" y="{H + 32}" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="26" fill="#3B2C2A">{label}</text></g>'
        )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{ch * 2}" viewBox="0 0 1200 {ch * 2}">{DEFS}{"".join(cells)}</svg>'
open(OUT, "w").write(svg)
