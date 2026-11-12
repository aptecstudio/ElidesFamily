"""Temporary Android TV banner (320x180) built from the group sheet.

The final banner comes in Phase 10; this one only makes the app recognizable
in the TV launcher.

Usage:
    python3 tv_banner.py ../../android/app/src/main/res/drawable-xhdpi/tv_banner.png
"""

import base64
import os
import sys
import tempfile

import parts

HERE = os.path.dirname(os.path.abspath(__file__))
GROUP = os.path.join(HERE, "..", "..", "docs", "characters", "group.png")
W, H = 320, 180

with open(GROUP, "rb") as fh:
    data = base64.b64encode(fh.read()).decode()

# The group sheet is 1420x620: fit its width and sit the family on a meadow.
img_h = 620 * W / 1420
svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#8FD3F4"/><stop offset="1" stop-color="#FFF6E5"/>'
    "</linearGradient></defs>"
    f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    f'<ellipse cx="{W / 2}" cy="{H + 40}" rx="{W * 0.8}" ry="70" fill="#9BDB7C"/>'
    f'<image x="0" y="{H - img_h - 8:.1f}" width="{W}" height="{img_h:.1f}" '
    f'href="data:image/png;base64,{data}"/>'
    "</svg>"
)
tmp = os.path.join(tempfile.mkdtemp(), "tv_banner.svg")
with open(tmp, "w") as fh:
    fh.write(svg)
parts.render(tmp, sys.argv[1])
