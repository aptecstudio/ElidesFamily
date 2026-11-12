"""Bozza di Papà (labrador bianco) — stessa testa di Elide e Rio, corpo da adulto.

Papà non è alto ed è un po' in carne: il corpo è appena più lungo di quello
dei piccoli, con la pancetta morbida. Indossa una felpa con cappuccio e i jeans.

Uso:
    python3 papa.py papa_pose.svg            # tavola con le 6 pose
    python3 papa.py papa_modello.svg single  # modello a riposo
"""
import math, sys
OUT = sys.argv[1]
LINE = "#B89C78"      # contorno pelo bianco caldo
SWL = "#4E8F36"       # contorno felpa
JL = "#2C5590"        # contorno jeans
EYE = "#3A2618"
MOUTHL = "#7A3E2A"
H = 580               # altezza della scena (i piccoli usano 540)

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
<clipPath id="torsoC"><path d="M154,302 Q200,294 246,302 C258,330 266,362 264,390 L264,412 Q200,424 136,412 L136,390 C134,362 142,330 154,302 Z"/></clipPath>
<clipPath id="eyeLC"><ellipse cx="150" cy="198" rx="30" ry="31"/></clipPath>
<clipPath id="eyeRC"><ellipse cx="250" cy="198" rx="30" ry="31"/></clipPath>
</defs>"""

HEADP = "M200,72 C276,72 322,120 324,188 C326,238 300,280 252,296 C236,302 218,304 200,304 C182,304 164,302 148,296 C100,280 74,238 76,188 C78,120 124,72 200,72 Z"
TORSOP = "M154,302 Q200,294 246,302 C258,330 266,362 264,390 L264,412 Q200,424 136,412 L136,390 C134,362 142,330 154,302 Z"


def bez(t, p0, p1, p2, p3):
    return tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d for a, b, c, d in zip(p0, p1, p2, p3))


def limb(p0, p1, p2, p3, w0, w1, bulge=3, fill="url(#limb)", line=LINE, t0=0.0):
    N = 40
    def D(t, a, b, c, d): return 3*(1-t)**2*(b-a)+6*(1-t)*t*(c-b)+3*t*t*(d-c)
    L = []; R = []
    for i in range(N+1):
        t = t0+(1-t0)*i/N
        x, y = bez(t, p0, p1, p2, p3)
        dx = D(t, p0[0], p1[0], p2[0], p3[0]); dy = D(t, p0[1], p1[1], p2[1], p3[1])
        l = math.hypot(dx, dy) or 1; nx, ny = -dy/l, dx/l
        w = (w0+(w1-w0)*t)/2+bulge*math.sin(math.pi*t)
        L.append((x+nx*w, y+ny*w)); R.append((x-nx*w, y-ny*w))
    d = "M%.1f,%.1f " % L[0]+" ".join("L%.1f,%.1f" % q for q in L[1:])
    d += " A%.1f,%.1f 0 0 1 %.1f,%.1f " % (w1/2, w1/2, R[-1][0], R[-1][1])
    d += " ".join("L%.1f,%.1f" % q for q in reversed(R))+" Z"
    return f'<path d="{d}" fill="{fill}" stroke="{line}" stroke-width="2.6" stroke-linejoin="round"/>'


def hand(x, y, rot, mirror=False, kind="open"):
    sx = -1 if mirror else 1
    if kind == "open":
        body = (f'<path d="M-12,6 C-14,-4 -13,-14 -7,-17 C-5,-21 5,-21 7,-17 C13,-14 14,-6 12,4 C11,12 6,16 0,16 C-6,16 -11,12 -12,6 Z" fill="url(#limb)" stroke="{LINE}" stroke-width="2.4" stroke-linejoin="round"/>'
                f'<path d="M-11,3 C-21,2 -24,-8 -18,-12 C-15,-9 -12,-5 -10,-2" fill="url(#limb)" stroke="{LINE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M-4,-17 L-4,-8 M2,-18 L2,-9 M7,-15 L6,-8" fill="none" stroke="{LINE}" stroke-width="1.8" stroke-linecap="round"/>'
                f'<ellipse cx="0" cy="5" rx="5.5" ry="4.5" fill="#E8A9A0" opacity="0.75"/>')
    else:  # thumb
        body = (f'<path d="M-13,-2 C-14,-12 -6,-15 2,-15 C10,-15 15,-10 14,0 C13,10 6,14 0,14 C-8,14 -13,8 -13,-2 Z" fill="url(#limb)" stroke="{LINE}" stroke-width="2.4" stroke-linejoin="round"/>'
                f'<path d="M-10,-10 C-12,-22 -8,-32 -2,-32 C3,-32 4,-26 2,-14" fill="url(#limb)" stroke="{LINE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M4,-12 Q12,-10 13,-4 M3,-4 Q12,-2 13,4 M2,4 Q10,6 11,10" fill="none" stroke="{LINE}" stroke-width="1.8" stroke-linecap="round"/>')
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f}) scale({sx*1.4},1.4)">{body}</g>'


def arm(p0, p1, p2, p3, mirror, kind="open", hand_rot=None):
    """Braccio con manica lunga del maglione, polsino a costine e mano."""
    o = [limb(p0, p1, p2, p3, 31, 25, 2, "url(#sweater)", SWL)]
    o.append(limb(p0, p1, p2, p3, 31, 27, 2, "url(#rib)", SWL, t0=0.84))
    q = bez(0.92, p0, p1, p2, p3)
    dx, dy = p3[0]-q[0], p3[1]-q[1]; l = math.hypot(dx, dy) or 1
    dx, dy = dx/l, dy/l
    rot = math.degrees(math.atan2(dy, dx))+90 if hand_rot is None else hand_rot
    o.append(hand(p3[0]+dx*16, p3[1]+dy*16, rot, mirror, kind))
    return o


def foot(x, y):
    return (f'<g transform="translate({x},{y}) scale(1.25)">'
            f'<path d="M-21,4 C-23,-8 -12,-14 0,-14 C12,-14 23,-8 21,4 C21,11 12,14 0,14 C-12,14 -21,11 -21,4 Z" fill="url(#limb)" stroke="{LINE}" stroke-width="2.6"/>'
            f'<path d="M-9,3 C-10,8 -9,11 -8,13 M0,4 C0,9 0,12 0,14 M9,3 C10,8 9,11 8,13" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'
            f'<ellipse cx="-6" cy="-6" rx="7" ry="3" fill="#FFFFFF" opacity="0.8"/></g>')


def body_lower():
    o = []
    # coda da labrador: spessa alla radice, si assottiglia e pende verso il basso
    o.append(limb((246,404),(274,412),(288,430),(290,458),24,12,1,"url(#limb)",LINE))
    # jeans: gambe corte e piene, orlo risvoltato
    for x in (174, 226):
        o.append(f'<path d="M{x-26},410 L{x-24},502 Q{x},508 {x+24},502 L{x+26},410 Z" fill="url(#jeans)" stroke="{JL}" stroke-width="2.6" stroke-linejoin="round"/>')
        o.append(f'<path d="M{x-25},492 Q{x},498 {x+25},492 L{x+25},506 Q{x},512 {x-25},506 Z" fill="#7FA9DE" stroke="{JL}" stroke-width="2.2" stroke-linejoin="round"/>')
        sx = x+11 if x < 200 else x-11
        o.append(f'<path d="M{sx},424 L{sx},486" fill="none" stroke="#E8B060" stroke-width="1.6" stroke-dasharray="4 3" opacity="0.8"/>')
    o.append(f'<path d="M140,398 L260,398 L262,428 Q244,438 226,434 L200,430 L174,434 Q156,438 138,428 Z" fill="url(#jeans)" stroke="{JL}" stroke-width="2.6" stroke-linejoin="round"/>')
    o.append(f'<path d="M200,410 L200,430" fill="none" stroke="{JL}" stroke-width="2" stroke-linecap="round"/>')
    o.append(foot(172,520)); o.append(foot(228,520))
    return "".join(o)


def torso():
    """Felpa verde prato con tasca a marsupio e bordo a costine."""
    o = []
    o.append(f'<path d="{TORSOP}" fill="url(#sweater)"/>')
    o.append('<g clip-path="url(#torsoC)">'
             '<ellipse cx="200" cy="304" rx="64" ry="16" fill="#3F7A2B" opacity="0.4" filter="url(#b6)"/>'
             '<ellipse cx="258" cy="370" rx="22" ry="60" fill="#3F7A2B" opacity="0.3" filter="url(#b12)"/>'
             '<ellipse cx="166" cy="340" rx="14" ry="40" fill="#E4FAD4" opacity="0.5" filter="url(#b6)"/>'
             f'<path d="M130,396 Q200,408 270,396 L272,430 L128,430 Z" fill="url(#rib)" stroke="{SWL}" stroke-width="2"/>'
             '</g>')
    for x in range(144, 260, 8):
        dy = 0 if abs(x-200) > 40 else 3
        o.append(f'<path d="M{x},{400+dy} L{x},{412+dy}" stroke="{SWL}" stroke-width="1.4" opacity="0.5"/>')
    # tasca a marsupio
    o.append(f'<path d="M168,356 L232,356 C238,368 244,380 250,392 Q200,400 150,392 C156,380 162,368 168,356 Z" fill="url(#sweater)" stroke="{SWL}" stroke-width="2.4" stroke-linejoin="round"/>')
    o.append(f'<path d="M168,356 C164,370 160,382 156,390 M232,356 C236,370 240,382 244,390" fill="none" stroke="{SWL}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>')
    o.append(f'<path d="{TORSOP}" fill="none" stroke="{SWL}" stroke-width="2.6" stroke-linejoin="round"/>')
    return "".join(o)


def collar():
    """Cappuccio appoggiato sulle spalle e laccetti."""
    return (f'<path d="M146,316 C134,292 156,278 200,280 C244,278 266,292 254,316 Q200,300 146,316 Z" fill="url(#sweater)" stroke="{SWL}" stroke-width="2.6" stroke-linejoin="round"/>'
            '<path d="M156,306 Q200,292 244,306" fill="none" stroke="#3F7A2B" stroke-width="5" stroke-linecap="round" opacity="0.45"/>'
            '<path d="M188,306 C186,322 188,338 185,352 M212,306 C214,322 212,338 215,352" fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round"/>'
            '<path d="M188,306 C186,322 188,338 185,352 M212,306 C214,322 212,338 215,352" fill="none" stroke="#D8D0C0" stroke-width="1" stroke-linecap="round" opacity="0.6"/>'
            '<rect x="182" y="350" width="6" height="9" rx="2" fill="#E8B060" stroke="#B88A3A" stroke-width="1.2"/>'
            '<rect x="212" y="350" width="6" height="9" rx="2" fill="#E8B060" stroke="#B88A3A" stroke-width="1.2"/>')


def ears():
    """Orecchie morbide da labrador, un po' sollevate (più espressive nelle animazioni)."""
    one = (f'<path d="M152,86 C120,70 76,76 58,102 C44,124 46,162 60,186 C70,198 84,194 90,180 C98,150 114,120 144,106 Z" fill="url(#ear)" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
           '<path d="M140,90 C112,84 84,94 70,114" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.8"/>'
           f'<path d="M138,108 C116,118 100,140 90,170" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round" opacity="0.5"/>')
    return one+f'<g transform="translate(400,0) scale(-1,1)">{one}</g>'


def head_base():
    o = []
    o.append(f'<path d="{HEADP}" fill="url(#fur)"/>')
    o.append('<g clip-path="url(#headC)"><ellipse cx="200" cy="300" rx="130" ry="30" fill="#CDB892" opacity="0.45" filter="url(#b12)"/>'
             '<ellipse cx="318" cy="200" rx="18" ry="90" fill="#D6C29E" opacity="0.4" filter="url(#b12)"/>'
             '<ellipse cx="170" cy="112" rx="56" ry="24" fill="#FFFFFF" opacity="0.95" filter="url(#b6)"/></g>')
    o.append(f'<path d="{HEADP}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>')
    o.append(ears())
    # musetto da labrador, un po' allungato
    o.append(f'<path d="M200,218 C244,218 270,242 270,268 C270,294 240,306 200,306 C160,306 130,294 130,268 C130,242 156,218 200,218 Z" fill="url(#muzzle)" stroke="#D8C6A6" stroke-width="2"/>')
    o.append('<ellipse cx="112" cy="252" rx="17" ry="10" fill="#FF9D8A" opacity="0.4" filter="url(#b3)"/><ellipse cx="288" cy="252" rx="17" ry="10" fill="#FF9D8A" opacity="0.4" filter="url(#b3)"/>')
    for (x, y) in ((160,262),(152,272),(164,276),(240,262),(248,272),(236,276)):
        o.append(f'<circle cx="{x}" cy="{y}" r="1.8" fill="#C9B08A"/>')
    o.append('<path d="M180,230 Q200,222 220,230 Q223,245 208,252 L192,252 Q177,245 180,230 Z" fill="url(#nose)" stroke="#2A1A16" stroke-width="2" stroke-linejoin="round"/>')
    o.append('<ellipse cx="193" cy="232" rx="6.5" ry="2.8" fill="#FFFFFF" opacity="0.85"/>')
    o.append('<path d="M193,243 Q196,246 197,243 M203,243 Q204,246 207,243" fill="none" stroke="#1E120F" stroke-width="1.8" stroke-linecap="round"/>')
    return "".join(o)


def eye(cx, side, dx=0, dy=0, kind="open"):
    o = []
    clip = "eyeLC" if side == "L" else "eyeRC"
    L = side == "L"
    if kind in ("open", "wide", "smiling"):
        o.append(f'<ellipse cx="{cx}" cy="198" rx="30" ry="31" fill="#FFFFFF" stroke="{EYE}" stroke-width="2.2"/>')
        r = 25 if kind != "wide" else 21
        pr = 11.5 if kind != "wide" else 8
        ix = cx + (1 if L else -1) + dx
        iy = 201 + dy + (0 if kind != "wide" else -3)
        o.append(f'<g clip-path="url(#{clip})"><circle cx="{ix}" cy="{iy}" r="{r}" fill="url(#iris)"/><circle cx="{ix}" cy="{iy+1}" r="{pr}" fill="#140A05"/>'
                 f'<ellipse cx="{ix+8}" cy="{iy-10}" rx="7.5" ry="8.5" fill="#FFFFFF"/><circle cx="{ix-9}" cy="{iy+10}" r="3.4" fill="#FFFFFF" opacity="0.9"/>')
        if kind == "smiling":
            o.append(f'<path d="M{cx-34},232 Q{cx},210 {cx+34},232 L{cx+34},240 L{cx-34},240 Z" fill="#FFF6E5"/>')
        o.append('</g>')
        if kind == "smiling":
            o.append(f'<path d="M{cx-26},222 Q{cx},212 {cx+26},222" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>')
        lift = -5 if kind == "wide" else 0
        if L:
            o.append(f'<path d="M121,{193+lift} Q150,{164+lift} 179,{191+lift}" fill="none" stroke="{EYE}" stroke-width="4" stroke-linecap="round"/>')
        else:
            o.append(f'<path d="M221,{191+lift} Q250,{164+lift} 279,{193+lift}" fill="none" stroke="{EYE}" stroke-width="4" stroke-linecap="round"/>')
    elif kind == "happy":
        o.append(f'<path d="M{cx-25},206 Q{cx},182 {cx+25},206" fill="none" stroke="{EYE}" stroke-width="4.6" stroke-linecap="round"/>')
    return "".join(o)


def brows(kind="normal"):
    shapes = {
        "normal": ("M128,156 Q145,148 163,153", "M237,153 Q255,148 272,156"),
        "happy":  ("M128,152 Q146,140 164,148", "M236,148 Q254,140 272,152"),
        "up":     ("M128,142 Q146,128 164,138", "M236,138 Q254,128 272,142"),
        "curious": ("M128,156 Q145,150 163,155", "M236,140 Q256,128 274,140"),
    }[kind]
    return "".join(f'<path d="{d}" fill="none" stroke="#C9AE86" stroke-width="5" stroke-linecap="round"/>' for d in shapes)


def lips():
    return (f'<path d="M200,252 L200,262 M200,262 Q190,270 178,266 M200,262 Q210,270 222,266" fill="none" stroke="{MOUTHL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')


def mouth(kind="smile"):
    if kind == "smile":
        return lips()+f'<path d="M180,272 Q200,286 220,272" fill="none" stroke="{MOUTHL}" stroke-width="2.4" stroke-linecap="round"/>'
    if kind == "open":
        return ('<path d="M176,266 Q200,274 224,266 Q224,294 200,296 Q176,294 176,266 Z" fill="#6E2A2A" stroke="#7A3E2A" stroke-width="2.4" stroke-linejoin="round"/>'
                '<path d="M186,284 Q200,276 214,284 Q212,296 200,297 Q188,296 186,284 Z" fill="#FF8FA3"/>'
                + lips())
    if kind == "o":
        return lips()+('<ellipse cx="200" cy="280" rx="8.5" ry="9" fill="#6E2A2A" stroke="#7A3E2A" stroke-width="2.2"/>'
                       '<ellipse cx="200" cy="284" rx="5" ry="3" fill="#FF8FA3"/>')
    if kind == "curious":
        return (f'<path d="M200,252 L200,262 M200,262 Q190,270 178,268 M200,262 Q212,268 222,262" fill="none" stroke="{MOUTHL}" stroke-width="2.4" stroke-linecap="round"/>'
                f'<path d="M222,262 Q226,262 227,258" fill="none" stroke="{MOUTHL}" stroke-width="2" stroke-linecap="round"/>')


def sparkle(x, y, s, c="#FFD84A"):
    return f'<path transform="translate({x},{y}) scale({s})" d="M0,-10 L2.5,-2.5 L10,0 L2.5,2.5 L0,10 L-2.5,2.5 L-10,0 L-2.5,-2.5 Z" fill="{c}"/>'


SL, SR = (148,322), (252,322)
def armL_down(): return arm(SL,(132,348),(124,376),(126,398),True)
def armR_down(): return arm(SR,(268,348),(276,376),(274,398),False)


def character(pose):
    o = []
    lift = -16 if pose == "festa" else 0
    shadow_rx = 82 if pose == "festa" else 100
    o.append(f'<ellipse cx="200" cy="544" rx="{shadow_rx}" ry="11" fill="#1D5A3A" opacity="0.28" filter="url(#b6)"/>')
    lean = {"neutra":0,"saluto":-2,"festa":0,"curiosa":2,"sorpresa":0,"brava":-2}[pose]
    o.append(f'<g transform="translate(0,{lift}) rotate({lean} 200 530)">')
    o.append(body_lower())
    back = []; front = []
    if pose == "neutra":
        back = armL_down()+armR_down(); face = ("open","open",0,0,"normal","smile",-3,False)
    elif pose == "saluto":
        back = armL_down()+arm(SR,(284,318),(300,296),(306,264),False)
        face = ("smiling","smiling",0,0,"happy","open",-6,True)
    elif pose == "festa":
        back = arm(SL,(120,310),(104,286),(100,256),True)+arm(SR,(280,310),(296,286),(300,256),False)
        face = ("happy","happy",0,0,"up","open",3,True)
    elif pose == "curiosa":
        back = armL_down()
        front = arm(SR,(286,380),(262,376),(244,330),False,hand_rot=-24)
        face = ("open","open",7,-8,"curious","curious",8,False)
    elif pose == "sorpresa":
        front = arm(SL,(112,330),(96,304),(98,276),True,hand_rot=18)+arm(SR,(288,330),(304,304),(302,276),False,hand_rot=-18)
        face = ("wide","wide",0,0,"up","o",0,False)
    elif pose == "brava":
        back = armL_down()
        front = arm(SR,(290,346),(306,328),(302,304),False,"thumb",0)
        face = ("happy","smiling",0,0,"happy","open",-5,True)
    o.append(torso())
    o.extend(back)
    o.append(collar())
    eL, eR, dx, dy, br, mo, tilt, blush = face
    o.append(f'<g transform="rotate({tilt} 200 300)">')
    o.append(head_base())
    if blush:
        o.append('<ellipse cx="114" cy="248" rx="20" ry="12" fill="#FF8D7A" opacity="0.4" filter="url(#b3)"/><ellipse cx="286" cy="248" rx="20" ry="12" fill="#FF8D7A" opacity="0.4" filter="url(#b3)"/>')
    o.append(brows(br))
    o.append(eye(150,"L",dx,dy,eL)); o.append(eye(250,"R",dx,dy,eR))
    o.append(mouth(mo))
    o.append('</g>')
    o.extend(front)
    if pose == "festa":
        o.append(sparkle(48,210,1.5)); o.append(sparkle(356,186,1.2)); o.append(sparkle(346,340,1.0,"#8FD3F4")); o.append(sparkle(54,350,0.9,"#FFB5A7"))
    if pose == "brava":
        o.append(sparkle(338,262,1.1))
    if pose == "sorpresa":
        o.append('<path d="M330,94 L340,78 M344,110 L360,104 M60,94 L50,78" fill="none" stroke="#3A2618" stroke-width="3.5" stroke-linecap="round"/>')
    o.append('</g>')
    return "".join(o)


POSES = [("neutra","A riposo"),("saluto","Ciao!"),("festa","Evviva!"),("curiosa","Curioso"),("sorpresa","Sorpreso"),("brava","Bravo!")]
mode = sys.argv[2] if len(sys.argv) > 2 else "sheet"
if mode == "single":
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{H*2}" viewBox="0 0 400 {H}">{DEFS}{character("neutra")}</svg>'
else:
    cw, ch = 400, H+60
    parts = []
    for i, (p, label) in enumerate(POSES):
        cx = (i % 3)*cw; cy = (i//3)*ch
        parts.append(f'<g transform="translate({cx},{cy})">{character(p)}<text x="200" y="{H+32}" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="26" fill="#3A2618">{label}</text></g>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{ch*2}" viewBox="0 0 1200 {ch*2}">{DEFS}{"".join(parts)}</svg>'
open(OUT, "w").write(svg)
