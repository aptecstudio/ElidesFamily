"""Group sheet: the four characters idle, at the same scale and on the same ground line.

Each script draws its own character (with its own gradients); here the images are
placed side by side, aligned by the feet.

Usage:
    python3 group.py group.png
"""

import base64
import os
import subprocess
import sys
import tempfile

import parts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
# The kids (Elide, Rio) are drawn at 85% of the adults (D-038).
KIDS = 0.85
# (script, scene height, ground y, scale)
CHARS = [
    ("mom.py", 580, 544, 1.0),
    ("dad.py", 580, 544, 1.0),
    ("elide.py", 540, 520, KIDS),
    ("rio.py", 540, 520, KIDS),
]
GROUND = 560
W, HTOT = 1420, 620

tmp = tempfile.mkdtemp()
items = []
x = 20
for i, (script, h, ground, k) in enumerate(CHARS):
    svg = os.path.join(tmp, f"{i}.svg")
    png = os.path.join(tmp, f"{i}.png")
    subprocess.run([sys.executable, os.path.join(HERE, script), svg, "single"], check=True)
    parts.render(svg, png)
    with open(png, "rb") as fh:
        data = base64.b64encode(fh.read()).decode()
    y = GROUND - ground * k
    items.append(
        f'<image x="{x:.0f}" y="{y:.0f}" width="{400 * k:.0f}" height="{h * k:.0f}" '
        f'href="data:image/png;base64,{data}"/>'
    )
    x += 365 * k + (20 if k < 1 else 0)

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HTOT}" viewBox="0 0 {W} {HTOT}">'
    f'<rect width="{W}" height="{HTOT}" fill="#FFF6E5"/>'
    f'<path d="M0,{GROUND} L{W},{GROUND}" stroke="#E8D8BC" stroke-width="2" stroke-dasharray="8 8"/>'
    + "".join(items)
    + "</svg>"
)
path = os.path.join(tmp, "group.svg")
with open(path, "w") as fh:
    fh.write(svg)
parts.render(path, OUT)
