"""Exports the drawn pieces of the approved hub (D-047, D-049) for the game.

The background and the cards are drawn by Flutter (lib/hub/), but the game
icons and the parents' gear use the "puffy" SVG lighting filter, which
Flutter cannot render: they become PNG files at 3x, drawn by the same code as
the draft, so game and draft never diverge.

Usage:
    python3 export_hub.py
"""

import os

import cairo
import gi

gi.require_version("Rsvg", "2.0")
import hub_menu as hub  # noqa: E402
from gi.repository import Rsvg  # noqa: E402

OUT = os.path.join(hub.ROOT, "assets", "images", "hub")
SCALE = 3

# Cream drawing area of a card, where the icon sits (see hub_menu.card()).
ART_W, ART_H = hub.CARD_W - 36, hub.CARD_H - 52
# The icon center, relative to the drawing area.
ART_CX, ART_CY = hub.CARD_W / 2 - 18, hub.CARD_H / 2 - 8 - 20

# Box around the gear, with room for its drop shadow.
GEAR_BOX = 160

ICONS = {
    "colors": hub.art_colors,
    # Surprise cards: body and lid apart, so the lid can hop in the game.
    "gift_box": hub.art_gift_box,
    "gift_lid": hub.art_gift_lid,
}


def export(name, w, h, content):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * SCALE}" '
        f'height="{h * SCALE}" viewBox="0 0 {w} {h}">{hub.defs([])}{content}</svg>'
    )
    handle = Rsvg.Handle.new_from_data(svg.encode())
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w * SCALE, h * SCALE)
    vp = Rsvg.Rectangle()
    vp.x, vp.y, vp.width, vp.height = 0, 0, w * SCALE, h * SCALE
    handle.render_document(cairo.Context(surf), vp)
    path = os.path.join(OUT, name)
    surf.write_to_png(path)
    print(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.environ["FONTCONFIG_FILE"] = hub.font_config()
    for name, art in ICONS.items():
        export(
            f"hub_icon_{name}.png",
            ART_W,
            ART_H,
            f'<g filter="url(#puffy)"><g transform="translate({ART_CX},{ART_CY}) '
            f'scale({hub.ART_SCALE})">{art()}</g></g>',
        )
    half = GEAR_BOX // 2
    export("hub_gear.png", GEAR_BOX, GEAR_BOX, hub.gear(half, half))


if __name__ == "__main__":
    main()
