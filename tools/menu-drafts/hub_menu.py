"""Design draft of the main menu (hub): a scrolling grid of game postcards.

Owner's choices (D-047): sky-and-meadow background, Elide on the left who waves
and reacts, straight rounded postcards in two rows with the name on a cream
badge, a gear for the parents in the top corner. The look has volume (soft
gradients, highlights, a "puffy" lighting filter on the drawings), in the same
glossy style as the characters. Only "Colors" exists today: the other cards are
examples that show how the grid grows and scrolls.

Usage:
    python3 hub_menu.py hub_menu.png
"""

import base64
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
DRAFTS = os.path.join(ROOT, "tools", "character-drafts")
sys.path.insert(0, DRAFTS)

import parts  # noqa: E402

# Phone landscape, 20:9.
W, H = 1600, 720

# Palette (D-016).
SKY = "#8FD3F4"
BUTTER = "#FFE08A"
MEADOW = "#9BDB7C"
PEACH = "#FFB5A7"
LAVENDER = "#C7B8F5"
HONEY = "#E8B060"
CREAM = "#FFF6E5"
COCOA = "#5A3E36"

# Pure colors of the Colors minigame.
RED, YELLOW, BLUE = "#E94B4B", "#FFC93C", "#3D8EE8"
GREEN, ORANGE, PURPLE = "#4CBF5A", "#FF8A3D", "#9B5DE5"

# Two rows of straight cards; the grid scrolls sideways.
CARD_W, CARD_H, CARD_R = 230, 200, 40
DEPTH = 12  # thickness of the card "cushion"
ROW_Y = (104, 376)
CARD_X0, CARD_GAP = 450, 40
# The drawings are designed for a ~210 px box and shrunk to fit the card.
ART_SCALE = 0.68
BADGE_H = 50


def mix(color, other, t):
    """Blend two #RRGGBB colors: t=0 gives color, t=1 gives other."""
    a = [int(color[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(other[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b, strict=True))


def lighter(color, t):
    return mix(color, "#FFFFFF", t)


def darker(color, t):
    return mix(color, COCOA, t)


def font_config():
    """Fontconfig file that also sees the bundled Fredoka font."""
    tmp = tempfile.mkdtemp()
    conf = os.path.join(tmp, "fonts.conf")
    fonts = os.path.abspath(os.path.join(ROOT, "assets", "fonts"))
    with open(conf, "w") as fh:
        fh.write(
            '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">'
            "<fontconfig><include ignore_missing='yes'>/etc/fonts/fonts.conf</include>"
            f"<dir>{fonts}</dir></fontconfig>"
        )
    return conf


def elide_png(pose):
    tmp = tempfile.mkdtemp()
    svg = os.path.join(tmp, "elide.svg")
    png = os.path.join(tmp, "elide.png")
    subprocess.run(
        [sys.executable, os.path.join(DRAFTS, "elide.py"), svg, "single", pose],
        check=True,
    )
    parts.render(svg, png)
    with open(png, "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def defs(card_colors):
    o = [
        "<defs>",
        # Sky: deeper at the top, hazy near the horizon.
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{mix(SKY, "#5BB8E6", 0.5)}"/>'
        f'<stop offset="0.55" stop-color="{SKY}"/>'
        '<stop offset="1" stop-color="#EAF7FC"/></linearGradient>',
        '<radialGradient id="sunglow"><stop offset="0" stop-color="#FFF3C4" stop-opacity="0.9"/>'
        '<stop offset="1" stop-color="#FFF3C4" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="sun" cx="0.38" cy="0.35" r="0.7">'
        '<stop offset="0" stop-color="#FFF6CF"/><stop offset="0.6" stop-color="#FFE08A"/>'
        '<stop offset="1" stop-color="#F7C75A"/></radialGradient>',
        '<linearGradient id="cloud" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0.35" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D6EBF6"/>'
        "</linearGradient>",
        '<linearGradient id="hillfar" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#BFE6C4"/><stop offset="1" stop-color="#A7D9B5"/>'
        "</linearGradient>",
        '<linearGradient id="hillmid" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#C4ECA8"/><stop offset="1" stop-color="#9CD483"/>'
        "</linearGradient>",
        '<linearGradient id="hillnear" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{lighter(MEADOW, 0.25)}"/>'
        '<stop offset="1" stop-color="#7CC25E"/></linearGradient>',
        '<linearGradient id="bush" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#8FD474"/><stop offset="1" stop-color="#5FA94A"/>'
        "</linearGradient>",
        # Cream drawing area: a soft inner shadow under the top edge.
        '<linearGradient id="inner" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{darker(CREAM, 0.12)}"/>'
        f'<stop offset="0.16" stop-color="{CREAM}"/>'
        f'<stop offset="1" stop-color="{lighter(CREAM, 0.4)}"/></linearGradient>',
        '<linearGradient id="badge" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF"/>'
        f'<stop offset="1" stop-color="{darker(CREAM, 0.08)}"/></linearGradient>',
        '<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.75"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>',
        # Soft drop shadow of cards and badges.
        '<filter id="soft" x="-20%" y="-20%" width="140%" height="160%">'
        '<feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#3E5A2E" flood-opacity="0.28"/>'
        "</filter>",
        # "Puffy" look for the drawings: a specular highlight from the top left,
        # computed on the blurred shape so every drawing looks rubbery and round.
        '<filter id="puffy" x="-15%" y="-15%" width="130%" height="130%">'
        '<feGaussianBlur in="SourceAlpha" stdDeviation="5" result="b"/>'
        '<feSpecularLighting in="b" surfaceScale="5" specularConstant="0.85" '
        'specularExponent="24" lighting-color="#FFFFFF" result="s">'
        '<feDistantLight azimuth="225" elevation="48"/></feSpecularLighting>'
        '<feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>'
        '<feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3="0.5" k4="0"/>'
        "</filter>",
    ]
    for i, c in enumerate(card_colors):
        o.append(
            f'<linearGradient id="frame{i}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{lighter(c, 0.35)}"/>'
            f'<stop offset="0.5" stop-color="{c}"/>'
            f'<stop offset="1" stop-color="{darker(c, 0.1)}"/></linearGradient>'
        )
    o.append("</defs>")
    return "".join(o)


def cloud(cx, cy, k):
    return (
        f'<g transform="translate({cx},{cy}) scale({k})">'
        '<g fill="#BFDDEE" opacity="0.5" transform="translate(0,8)">'
        '<ellipse cx="0" cy="10" rx="74" ry="30"/></g>'
        '<g fill="url(#cloud)"><ellipse cx="0" cy="10" rx="72" ry="30"/>'
        '<circle cx="-32" cy="-2" r="32"/><circle cx="16" cy="-16" r="42"/>'
        '<circle cx="52" cy="6" r="27"/></g>'
        '<ellipse cx="4" cy="-34" rx="22" ry="9" fill="#FFFFFF" opacity="0.9"/></g>'
    )


def flower(x, y, c, k=1.0):
    o = [f'<g transform="translate({x},{y}) scale({k})">']
    o.append('<path d="M0,4 C2,16 0,26 -2,34" stroke="#5FA94A" stroke-width="4" fill="none"/>')
    for i in range(5):
        o.append(
            f'<ellipse cx="0" cy="-10" rx="8" ry="11" fill="{c}" stroke="{darker(c, 0.25)}" '
            f'stroke-width="1.5" transform="rotate({i * 72})"/>'
        )
    o.append(f'<circle r="7" fill="{BUTTER}" stroke="{HONEY}" stroke-width="2"/>')
    o.append('<circle cx="-2" cy="-2" r="2.5" fill="#FFFFFF" opacity="0.8"/></g>')
    return "".join(o)


def bush(x, y, k=1.0):
    return (
        f'<g transform="translate({x},{y}) scale({k})">'
        '<g fill="url(#bush)" stroke="#5A9A45" stroke-width="3">'
        '<circle cx="-34" cy="-10" r="30"/><circle cx="34" cy="-8" r="28"/>'
        '<circle cx="0" cy="-28" r="38"/></g>'
        '<ellipse cx="-12" cy="-48" rx="16" ry="7" fill="#FFFFFF" opacity="0.35"/></g>'
    )


def tuft(x, y):
    return (
        f'<path d="M{x - 10},{y} Q{x - 8},{y - 16} {x - 2},{y - 22} Q{x},{y - 10} {x + 2},{y} '
        f'Q{x + 6},{y - 14} {x + 12},{y - 18} Q{x + 8},{y - 6} {x + 10},{y} Z" fill="#6DB553"/>'
    )


def background():
    o = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    # Sun with a warm glow and soft rays.
    o.append('<g transform="translate(372,76)">')
    o.append('<circle r="120" fill="url(#sunglow)"/>')
    for i in range(12):
        o.append(
            f'<rect x="-5" y="-58" width="10" height="18" rx="5" fill="#FFD66B" '
            f'opacity="0.85" transform="rotate({i * 30})"/>'
        )
    o.append('<circle r="34" fill="url(#sun)" stroke="#F2B84B" stroke-width="3"/>')
    o.append('<ellipse cx="-11" cy="-13" rx="10" ry="6" fill="#FFFFFF" opacity="0.7"/></g>')
    # Clouds (they drift slowly in the game).
    for cx, cy, k in ((200, 96, 1.0), (790, 54, 0.75), (1100, 70, 0.6)):
        o.append(cloud(cx, cy, k))
    # Far hill, middle hill, near meadow.
    o.append(
        '<path d="M0,500 C220,440 460,450 640,500 C860,560 1120,470 1360,470 '
        'C1460,470 1540,490 1600,505 L1600,720 L0,720 Z" fill="url(#hillfar)"/>'
    )
    o.append(
        '<path d="M0,560 C300,500 620,510 900,560 C1150,605 1400,590 1600,540 '
        'L1600,720 L0,720 Z" fill="url(#hillmid)"/>'
    )
    o.append(
        '<path d="M0,560 C300,500 620,510 900,560 C1150,605 1400,590 1600,540" '
        'fill="none" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="5"/>'
    )
    o.append(bush(60, 560, 0.9))
    o.append(bush(1540, 548, 0.8))
    o.append(
        '<path d="M0,620 C350,575 700,585 1000,630 C1250,665 1450,650 1600,615 '
        'L1600,720 L0,720 Z" fill="url(#hillnear)"/>'
    )
    o.append(
        '<path d="M0,620 C350,575 700,585 1000,630 C1250,665 1450,650 1600,615" '
        'fill="none" stroke="#FFFFFF" stroke-opacity="0.4" stroke-width="5"/>'
    )
    for x, y in ((380, 660), (640, 690), (1040, 680), (1320, 700), (1560, 670), (40, 700)):
        o.append(tuft(x, y))
    for fx, fy, c, k in (
        (100, 650, PEACH, 1.0),
        (1180, 668, LAVENDER, 1.0),
        (1480, 650, BUTTER, 1.0),
        (900, 692, PEACH, 0.9),
        (720, 640, BUTTER, 0.7),
    ):
        o.append(flower(fx, fy, c, k))
    return "".join(o)


def card(i, x, y, color, art, name):
    """A straight rounded postcard with volume: a darker "cushion" underneath,
    a gradient frame with a glossy top, a cream drawing area with an inner
    shadow and a cream name badge across the bottom edge."""
    cx, cy = x + CARD_W / 2, y + CARD_H / 2 - 8
    badge_w = 34 + 19 * len(name)
    by = y + CARD_H - BADGE_H / 2 + 6
    edge = darker(color, 0.35)
    return (
        '<g filter="url(#soft)">'
        f'<rect x="{x}" y="{y + DEPTH}" width="{CARD_W}" height="{CARD_H}" rx="{CARD_R}" '
        f'fill="{edge}" stroke="{COCOA}" stroke-width="7"/>'
        "</g>"
        f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="{CARD_R}" '
        f'fill="url(#frame{i})" stroke="{COCOA}" stroke-width="7"/>'
        f'<rect x="{x + 26}" y="{y + 7}" width="{CARD_W - 52}" height="14" rx="7" fill="url(#gloss)"/>'
        f'<rect x="{x + 18}" y="{y + 20}" width="{CARD_W - 36}" height="{CARD_H - 52}" '
        f'rx="{CARD_R - 16}" fill="url(#inner)" stroke="{darker(color, 0.2)}" stroke-width="3"/>'
        f'<g filter="url(#puffy)"><g transform="translate({cx},{cy}) scale({ART_SCALE})">{art}</g></g>'
        '<g filter="url(#soft)">'
        f'<rect x="{cx - badge_w / 2}" y="{by}" width="{badge_w}" height="{BADGE_H}" '
        f'rx="{BADGE_H / 2}" fill="url(#badge)" stroke="{COCOA}" stroke-width="6"/></g>'
        f'<rect x="{cx - badge_w / 2 + 16}" y="{by + 6}" width="{badge_w - 32}" height="10" '
        'rx="5" fill="#FFFFFF" opacity="0.8"/>'
        f'<text x="{cx}" y="{by + 36}" text-anchor="middle" font-family="Fredoka" '
        f'font-weight="600" font-size="32" fill="{COCOA}">{name}</text>'
    )


def art_colors():
    dots = (
        (-42, -48, ORANGE),
        (42, -48, PURPLE),
        (-80, 10, GREEN),
        (80, 10, RED),
        (-42, 66, BLUE),
        (42, 66, YELLOW),
    )
    return "".join(
        f'<circle cx="{x}" cy="{y - 8}" r="34" fill="{c}" stroke="{COCOA}" stroke-width="6"/>'
        for x, y, c in dots
    )


def art_shapes():
    s = f'stroke="{COCOA}" stroke-width="6" stroke-linejoin="round"'
    return (
        f'<circle cx="-56" cy="-34" r="40" fill="{RED}" {s}/>'
        f'<path d="M58,-82 L104,0 L12,0 Z" fill="{YELLOW}" {s}/>'
        f'<rect x="-34" y="18" width="76" height="76" rx="12" fill="{BLUE}" {s}/>'
    )


def art_numbers():
    o = []
    for i, (n, c) in enumerate((("1", GREEN), ("2", ORANGE), ("3", PURPLE))):
        x = -98 + i * 66
        y = 20 - i * 34
        o.append(
            f'<rect x="{x}" y="{y}" width="64" height="64" rx="14" fill="{c}" stroke="{COCOA}" stroke-width="6"/>'
            f'<text x="{x + 32}" y="{y + 48}" text-anchor="middle" font-family="Fredoka" font-weight="700" '
            f'font-size="44" fill="{CREAM}">{n}</text>'
        )
    return "".join(o)


def art_animals():
    toes = ((-44, -44), (-14, -68), (20, -68), (50, -44))
    o = [
        f'<ellipse cx="3" cy="22" rx="52" ry="46" fill="{HONEY}" stroke="{COCOA}" stroke-width="6"/>'
    ]
    o += [
        f'<ellipse cx="{x}" cy="{y}" rx="18" ry="22" fill="{HONEY}" stroke="{COCOA}" stroke-width="6"/>'
        for x, y in toes
    ]
    return "".join(o)


def art_music():
    s = f'stroke="{COCOA}" stroke-width="6" stroke-linejoin="round"'
    return (
        f'<path d="M-40,40 L-40,-60 L60,-80 L60,20" fill="none" {s} stroke-linecap="round"/>'
        f'<path d="M-40,-60 L60,-80 L60,-52 L-40,-32 Z" fill="{PURPLE}" {s}/>'
        f'<ellipse cx="-62" cy="44" rx="28" ry="22" fill="{BLUE}" {s}/>'
        f'<ellipse cx="38" cy="24" rx="28" ry="22" fill="{RED}" {s}/>'
    )


def art_puzzle():
    piece = (
        "M-40,-40 L-10,-40 C-14,-56 14,-56 10,-40 L40,-40 L40,-10 "
        "C56,-14 56,14 40,10 L40,40 L-40,40 Z"
    )
    return (
        f'<path d="{piece}" transform="translate(-30,0)" fill="{GREEN}" '
        f'stroke="{COCOA}" stroke-width="6" stroke-linejoin="round"/>'
        f'<path d="{piece}" transform="translate(52,-6) rotate(12)" fill="{ORANGE}" '
        f'stroke="{COCOA}" stroke-width="6" stroke-linejoin="round"/>'
    )


def art_fruit():
    s = f'stroke="{COCOA}" stroke-width="6" stroke-linejoin="round"'
    return (
        f'<path d="M-4,-50 C-4,-70 6,-82 18,-86" fill="none" {s} stroke-linecap="round"/>'
        f'<path d="M2,-62 C20,-84 46,-76 50,-60 C30,-52 12,-54 2,-62 Z" fill="{GREEN}" {s}/>'
        f'<path d="M0,-44 C-30,-64 -78,-50 -76,0 C-74,50 -36,82 0,66 '
        f'C36,82 74,50 76,0 C78,-50 30,-64 0,-44 Z" fill="{RED}" {s}/>'
    )


def art_clothes():
    return (
        '<path d="M-36,-70 C-24,-56 24,-56 36,-70 L86,-42 L66,0 L44,-10 L44,74 L-44,74 '
        'L-44,-10 L-66,0 L-86,-42 Z" '
        f'fill="{YELLOW}" stroke="{COCOA}" stroke-width="6" stroke-linejoin="round"/>'
        f'<circle cx="0" cy="18" r="20" fill="{RED}" stroke="{COCOA}" stroke-width="5"/>'
    )


def gear(x, y):
    """Small, low-contrast gear for the parents (D-048): it must not attract the child."""
    o = [f'<g transform="translate({x},{y})" opacity="0.9">']
    o.append(
        f'<g filter="url(#soft)"><circle r="40" fill="url(#badge)" stroke="{COCOA}" stroke-width="5"/></g>'
    )
    o.append('<g filter="url(#puffy)">')
    for i in range(8):
        o.append(
            f'<rect x="-6" y="-28" width="12" height="13" rx="3" fill="{LAVENDER}" transform="rotate({i * 45})"/>'
        )
    o.append(f'<circle r="19" fill="{LAVENDER}"/></g><circle r="8" fill="{CREAM}"/>')
    o.append("</g>")
    return "".join(o)


def main(out):
    os.environ["FONTCONFIG_FILE"] = font_config()
    elide = elide_png("wave")

    # Filled column by column, so the grid grows sideways; the fifth column is
    # cut by the screen edge to suggest scrolling.
    cards = [
        (PEACH, art_colors(), "Colori"),
        (BUTTER, art_music(), "Musica"),
        (SKY, art_shapes(), "Forme"),
        (PEACH, art_puzzle(), "Puzzle"),
        (MEADOW, art_numbers(), "Numeri"),
        (LAVENDER, art_fruit(), "Frutta"),
        (LAVENDER, art_animals(), "Animali"),
        (SKY, art_clothes(), "Vestiti"),
        (MEADOW, art_shapes(), "Forme"),
        (BUTTER, art_colors(), "Colori"),
    ]
    grid = "".join(
        card(i, CARD_X0 + (i // 2) * (CARD_W + CARD_GAP), ROW_Y[i % 2], c, a, n)
        for i, (c, a, n) in enumerate(cards)
    )
    # Elide stands on the hill on the left, kid scale.
    ew, eh = 400 * 0.98, 540 * 0.98
    elide_img = (
        '<ellipse cx="225" cy="676" rx="120" ry="16" fill="#3E7A2E" opacity="0.28"/>'
        f'<image x="{225 - ew / 2:.0f}" y="{690 - eh:.0f}" width="{ew:.0f}" height="{eh:.0f}" '
        f'href="data:image/png;base64,{elide}"/>'
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        + defs([c for c, _, _ in cards])
        + background()
        + grid
        + elide_img
        + gear(W - 64, 56)
        + "</svg>"
    )
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "hub.svg")
    with open(path, "w") as fh:
        fh.write(svg)
    parts.render(path, out)


if __name__ == "__main__":
    main(sys.argv[1])
