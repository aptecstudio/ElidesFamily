"""Draft of Elide (white kitten), the protagonist.

Usage:
    python3 elide.py elide_poses.svg          # sheet with the 6 poses
    python3 elide.py elide_model.svg single   # idle model sheet
"""

import math
import sys

import parts

OUT = sys.argv[1]
LINE = "#9C8DB3"
LIMB = "#F1EDF8"
DLINE = "#0E7A70"
EYE = "#3B2C55"
MOUTHL = "#B8406A"

DEFS = """<defs>
<filter id="b3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>
<radialGradient id="fur" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#F1EDF7"/><stop offset="1" stop-color="#D6CDE6"/></radialGradient>
<radialGradient id="limb" cx="35%" cy="30%" r="85%"><stop offset="0" stop-color="#FCFAFE"/><stop offset="1" stop-color="#D8CFE7"/></radialGradient>
<radialGradient id="dress" cx="38%" cy="25%" r="85%"><stop offset="0" stop-color="#6FE6D9"/><stop offset="0.55" stop-color="#25BBAE"/><stop offset="1" stop-color="#15948A"/></radialGradient>
<linearGradient id="iris" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14306F"/><stop offset="0.5" stop-color="#2F6FC9"/><stop offset="1" stop-color="#8FD2FF"/></linearGradient>
<linearGradient id="nose" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9BB8"/><stop offset="1" stop-color="#D9507A"/></linearGradient>
<linearGradient id="earIn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD0DE"/><stop offset="1" stop-color="#F49DB8"/></linearGradient>
<radialGradient id="bow" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="#FF8A96"/><stop offset="0.6" stop-color="#F0475B"/><stop offset="1" stop-color="#C92A40"/></radialGradient>
<clipPath id="headC"><path d="M200,72 C276,72 322,120 324,188 C326,238 300,280 252,296 C236,302 218,304 200,304 C182,304 164,302 148,296 C100,280 74,238 76,188 C78,120 124,72 200,72 Z"/></clipPath>
<clipPath id="dressC"><path d="M156,300 Q200,292 244,300 C250,320 254,346 255,372 C261,394 267,416 274,438 Q200,458 126,438 C133,416 139,394 145,372 C146,346 150,320 156,300 Z"/></clipPath>
<clipPath id="eyeLC"><ellipse cx="150" cy="198" rx="30" ry="31"/></clipPath>
<clipPath id="eyeRC"><ellipse cx="250" cy="198" rx="30" ry="31"/></clipPath>
</defs>"""

HEADP = "M200,72 C276,72 322,120 324,188 C326,238 300,280 252,296 C236,302 218,304 200,304 C182,304 164,302 148,296 C100,280 74,238 76,188 C78,120 124,72 200,72 Z"
DRESSP = "M156,300 Q200,292 244,300 C250,320 254,346 255,372 C261,394 267,416 274,438 Q200,458 126,438 C133,416 139,394 145,372 C146,346 150,320 156,300 Z"


def tube(d, w, color=LIMB, line=LINE):
    return (
        f'<path d="{d}" fill="none" stroke="{line}" stroke-width="{w + 5}" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{w * 0.28:.1f}" stroke-linecap="round" opacity="0.7" transform="translate(-{w * 0.18:.1f},-{w * 0.1:.1f})"/>'
    )


def limb(p0, p1, p2, p3, w0, w1, bulge=3, fill="url(#limb)"):
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
    # rounded end cap
    d += " A%.1f,%.1f 0 0 1 %.1f,%.1f " % (w1 / 2, w1 / 2, right[-1][0], right[-1][1])
    d += " ".join("L%.1f,%.1f" % q for q in reversed(right)) + " Z"
    return (
        f'<path d="{d}" fill="{fill}" stroke="{LINE}" stroke-width="2.6" stroke-linejoin="round"/>'
    )


def foot(x, y):
    return (
        f'<g transform="translate({x},{y}) scale(1.25)">'
        f'<path d="M-21,4 C-23,-8 -12,-14 0,-14 C12,-14 23,-8 21,4 C21,11 12,14 0,14 C-12,14 -21,11 -21,4 Z" fill="url(#limb)" stroke="{LINE}" stroke-width="2.6"/>'
        f'<path d="M-9,3 C-10,8 -9,11 -8,13 M0,4 C0,9 0,12 0,14 M9,3 C10,8 9,11 8,13" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'
        f'<ellipse cx="-6" cy="-6" rx="7" ry="3" fill="#FFFFFF" opacity="0.8"/></g>'
    )


def hem_scallops():
    pts = []
    n = 11
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * 126 + 2 * (1 - t) * t * 200 + t * t * 274
        y = (1 - t) ** 2 * 438 + 2 * (1 - t) * t * 458 + t * t * 438
        pts.append((x, y))
    d = "M%.1f,%.1f" % pts[0]
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + 9
        d += " Q%.1f,%.1f %.1f,%.1f" % (mx, my, x1, y1)
    return f'<path d="{d} L274,428 Q200,448 126,428 Z" fill="#FFFFFF" stroke="#B9AFCB" stroke-width="2" stroke-linejoin="round"/>'


def body_lower(pose):
    o = []
    o.append(
        f'<path d="M262,420 C306,420 330,386 324,350 C320,326 298,322 292,338 C288,350 302,356 306,346" fill="none" stroke="{LINE}" stroke-width="22" stroke-linecap="round"/>'
    )
    o.append(
        '<path d="M262,420 C306,420 330,386 324,350 C320,326 298,322 292,338 C288,350 302,356 306,346" fill="none" stroke="#EDE8F5" stroke-width="17" stroke-linecap="round"/>'
    )
    o.append(limb((172, 424), (171, 446), (171, 466), (172, 486), 44, 38, 2))
    o.append(limb((228, 424), (229, 446), (229, 466), (228, 486), 44, 38, 2))
    o.append(foot(170, 496))
    o.append(foot(230, 496))
    return "".join(o)


def dress():
    o = []
    o.append(f'<path d="{DRESSP}" fill="url(#dress)"/>')
    o.append(
        '<g clip-path="url(#dressC)">'
        '<ellipse cx="200" cy="302" rx="70" ry="18" fill="#0B6158" opacity="0.45" filter="url(#b6)"/>'
        '<ellipse cx="262" cy="400" rx="30" ry="70" fill="#0B6158" opacity="0.3" filter="url(#b12)"/>'
        '<ellipse cx="168" cy="360" rx="16" ry="50" fill="#BFFAF3" opacity="0.5" filter="url(#b6)"/></g>'
    )
    o.append(
        f'<path d="{DRESSP}" fill="none" stroke="{DLINE}" stroke-width="2.6" stroke-linejoin="round"/>'
    )
    o.append(hem_scallops())
    o.append(
        f'<path d="M148,362 Q200,372 252,362" fill="none" stroke="{DLINE}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>'
    )
    o.append(
        f'<path d="M168,366 L166,374 M184,369 L183,377 M216,369 L217,377 M232,366 L234,374" fill="none" stroke="{DLINE}" stroke-width="1.6" stroke-linecap="round" opacity="0.55"/>'
    )
    o.append(
        '<circle cx="200" cy="322" r="4.5" fill="#FFFFFF" stroke="#B9AFCB" stroke-width="1.5"/><circle cx="200" cy="342" r="4.5" fill="#FFFFFF" stroke="#B9AFCB" stroke-width="1.5"/>'
    )
    o.append(
        f'<path d="M222,388 L250,388 L252,412 Q237,420 222,412 Z" fill="#2ACBBE" stroke="{DLINE}" stroke-width="2" stroke-linejoin="round"/>'
    )
    o.append(
        '<path d="M224,392 L249,392" fill="none" stroke="#FFFFFF" stroke-width="1.6" stroke-dasharray="3 3"/>'
    )
    o.append(
        '<g transform="translate(237,404)"><ellipse cx="0" cy="2" rx="3.6" ry="3" fill="#FF8FB1"/><circle cx="-4.5" cy="-3" r="1.7" fill="#FF8FB1"/><circle cx="0" cy="-5" r="1.7" fill="#FF8FB1"/><circle cx="4.5" cy="-3" r="1.7" fill="#FF8FB1"/></g>'
    )
    return "".join(o)


def sleeves():
    """White collar (the sleeves now follow the arm, see parts.arm)."""
    return '<path d="M174,300 Q187,318 200,306 Q213,318 226,300 Q200,293 174,300 Z" fill="#FFFFFF" stroke="#B9AFCB" stroke-width="2.2" stroke-linejoin="round"/>'


def bow():
    return (
        '<g transform="rotate(-18 132 92)">'
        '<path d="M120,98 L106,128 L116,124 L120,134 L130,102 Z" fill="url(#bow)" stroke="#A81F33" stroke-width="2.2" stroke-linejoin="round"/>'
        '<path d="M144,98 L158,128 L148,124 L144,134 L134,102 Z" fill="url(#bow)" stroke="#A81F33" stroke-width="2.2" stroke-linejoin="round"/>'
        '<path d="M132,92 C118,72 88,66 84,86 C80,108 112,112 132,92 Z" fill="url(#bow)" stroke="#A81F33" stroke-width="2.4" stroke-linejoin="round"/>'
        '<path d="M132,92 C146,72 176,66 180,86 C184,108 152,112 132,92 Z" fill="url(#bow)" stroke="#A81F33" stroke-width="2.4" stroke-linejoin="round"/>'
        '<path d="M124,90 C112,82 98,80 94,86 M140,90 C152,82 166,80 170,86" fill="none" stroke="#B8243A" stroke-width="2" stroke-linecap="round" opacity="0.8"/>'
        '<ellipse cx="102" cy="82" rx="7" ry="3.5" fill="#FFFFFF" opacity="0.55" transform="rotate(-15 102 82)"/>'
        '<rect x="123" y="82" width="18" height="21" rx="7" fill="url(#bow)" stroke="#A81F33" stroke-width="2.4"/>'
        '<ellipse cx="129" cy="88" rx="3" ry="2" fill="#FFFFFF" opacity="0.7"/></g>'
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
        '<g clip-path="url(#headC)"><ellipse cx="200" cy="300" rx="130" ry="30" fill="#B3A6CC" opacity="0.45" filter="url(#b12)"/>'
        '<ellipse cx="318" cy="200" rx="18" ry="90" fill="#BDB0D4" opacity="0.4" filter="url(#b12)"/>'
        '<ellipse cx="170" cy="112" rx="56" ry="24" fill="#FFFFFF" opacity="0.95" filter="url(#b6)"/></g>'
    )
    o.append(
        f'<path d="{HEADP}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
    )
    o.append(
        f'<path d="M80,206 L66,212 L80,220 L70,230 L86,232 M320,206 L334,212 L320,220 L330,230 L314,232" fill="url(#fur)" stroke="{LINE}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>'
    )
    o.append(
        f'<path d="M162,90 C170,60 210,48 240,66 C224,66 212,74 206,86 C196,76 178,76 162,90 Z" fill="url(#fur)" stroke="{LINE}" stroke-width="2.8" stroke-linejoin="round"/>'
    )
    o.append(
        '<path d="M186,80 Q200,70 214,72" fill="none" stroke="#D6CDE6" stroke-width="2" stroke-linecap="round"/>'
    )
    o.append(
        '<path d="M200,224 C238,224 264,244 264,268 C264,290 236,300 200,300 C164,300 136,290 136,268 C136,244 162,224 200,224 Z" fill="#FFFFFF" stroke="#DCD3E8" stroke-width="2"/>'
    )
    o.append(
        '<ellipse cx="112" cy="250" rx="18" ry="11" fill="#FF8DB0" opacity="0.5" filter="url(#b3)"/><ellipse cx="288" cy="250" rx="18" ry="11" fill="#FF8DB0" opacity="0.5" filter="url(#b3)"/>'
    )
    o.append(
        '<path d="M187,236 Q200,231 213,236 Q209,249 200,253 Q191,249 187,236 Z" fill="url(#nose)" stroke="#B8406A" stroke-width="2" stroke-linejoin="round"/><ellipse cx="196" cy="237" rx="4" ry="2" fill="#FFFFFF" opacity="0.9"/>'
    )
    o.append(
        f'<path d="M200,253 L200,259" fill="none" stroke="{MOUTHL}" stroke-width="2.2" stroke-linecap="round"/>'
    )
    o.append(bow())
    return "".join(o)


def eye(cx, side, dx=0, dy=0, kind="open"):
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
            f'<g clip-path="url(#{clip})"><circle cx="{ix}" cy="{iy}" r="{r}" fill="url(#iris)"/><circle cx="{ix}" cy="{iy + 1}" r="{pr}" fill="#0E1330"/>'
            f'<ellipse cx="{ix + 8}" cy="{iy - 10}" rx="7.5" ry="8.5" fill="#FFFFFF"/><circle cx="{ix - 9}" cy="{iy + 10}" r="3.4" fill="#FFFFFF" opacity="0.9"/>'
        )
        if kind == "smiling":
            o.append(
                f'<path d="M{cx - 34},232 Q{cx},210 {cx + 34},232 L{cx + 34},240 L{cx - 34},240 Z" fill="#F2EEF8"/>'
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
        f'<path d="{d}" fill="none" stroke="#B2A3C8" stroke-width="4.2" stroke-linecap="round"/>'
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


SL, SR = (150, 316), (250, 316)
SLEEVE = dict(
    fill="url(#dress)", line=DLINE, t1=0.3, w0=44, w1=36, trim="#FFFFFF", trim_line="#B9AFCB"
)


def arm(p0, p1, p2, p3, kind="back", hand_rot=None):
    return parts.arm(p0, p1, p2, p3, "url(#limb)", LINE, kind, hand_rot, SLEEVE)


def arm_l_down():
    return arm(SL, (134, 340), (120, 372), (114, 400))


def arm_r_down():
    return arm(SR, (266, 340), (280, 372), (286, 400))


def character(pose):
    o = []
    lift = -16 if pose == "cheer" else 0
    shadow_rx = 82 if pose == "cheer" else 106
    o.append(
        f'<ellipse cx="200" cy="520" rx="{shadow_rx}" ry="11" fill="#1D5A3A" opacity="0.28" filter="url(#b6)"/>'
    )
    lean = {"idle": 0, "wave": -2, "cheer": 0, "curious": 2, "surprised": 0, "proud": -2}[pose]
    o.append(f'<g transform="translate(0,{lift}) rotate({lean} 200 500)">')
    o.append(body_lower(pose))
    back = []
    front = []
    if pose == "idle":
        back = arm_l_down() + arm_r_down()
        face = ("open", "open", 0, 0, "normal", "smile", -3, False)
    elif pose == "wave":
        back = arm_l_down() + arm(SR, (284, 330), (310, 318), (318, 290), "palm")
        face = ("smiling", "smiling", 0, 0, "happy", "open", -6, True)
    elif pose == "cheer":
        back = arm(SL, (118, 318), (96, 300), (90, 276), "palm") + arm(
            SR, (282, 318), (304, 300), (310, 276), "palm"
        )
        face = ("happy", "happy", 0, 0, "up", "open", 3, True)
    elif pose == "curious":
        back = arm_l_down()
        front = arm(SR, (298, 372), (268, 376), (250, 330), "fist", -24)
        face = ("open", "open", 7, -8, "curious", "curious", 8, False)
    elif pose == "surprised":
        front = arm(SL, (104, 334), (88, 314), (92, 290), "palm", 18) + arm(
            SR, (296, 334), (312, 314), (308, 290), "palm", -18
        )
        face = ("wide", "wide", 0, 0, "up", "o", 0, False)
    elif pose == "proud":
        back = arm_l_down()
        front = arm(SR, (300, 356), (318, 338), (308, 312), "thumb", 0)
        face = ("happy", "smiling", 0, 0, "happy", "open", -5, True)
    o.append(dress())
    o.extend(back)
    o.append(sleeves())
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
    o.append(mouth(mo))
    o.append("</g>")
    o.extend(front)
    if pose == "cheer":
        o.append(sparkle(52, 210, 1.5))
        o.append(sparkle(352, 186, 1.2))
        o.append(sparkle(344, 322, 1.0, "#7EEADF"))
        o.append(sparkle(60, 334, 0.9, "#FF9BB8"))
    if pose == "proud":
        o.append(sparkle(338, 262, 1.1))
    if pose == "surprised":
        o.append(
            '<path d="M330,94 L340,78 M344,110 L360,104 M60,94 L50,78" fill="none" stroke="#3B2C55" stroke-width="3.5" stroke-linecap="round"/>'
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
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="1080" viewBox="0 0 400 540">{DEFS}{character("idle")}</svg>'
else:
    cw, ch = 400, 600
    cells = []
    for i, (p, label) in enumerate(POSES):
        cx = (i % 3) * cw
        cy = (i // 3) * ch
        cells.append(
            f'<g transform="translate({cx},{cy})">{character(p)}<text x="200" y="572" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="26" fill="#3B2C55">{label}</text></g>'
        )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200">{DEFS}{"".join(cells)}</svg>'
open(OUT, "w").write(svg)
