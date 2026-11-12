"""Tavola di gruppo: i quattro personaggi a riposo, alla stessa scala e sullo stesso piano.

Ogni script disegna il proprio personaggio (con i propri gradienti); qui le immagini
vengono affiancate allineando i piedi. Richiede rsvg-convert.

Uso:
    python3 gruppo.py gruppo.png
"""
import base64, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
# (script, altezza della scena, y del terreno, scala)
# I piccoli (Elide, Rio) stanno in scena all'85% degli adulti (D-038).
KIDS = 0.85
CHARS = [("mamma.py", 580, 544, 1.0), ("papa.py", 580, 544, 1.0), ("elide.py", 540, 520, KIDS), ("rio.py", 540, 520, KIDS)]
GROUND = 560
W, HTOT = 1420, 620

tmp = tempfile.mkdtemp()
items = []
x = 20
for i, (script, h, ground, k) in enumerate(CHARS):
    svg = os.path.join(tmp, f"{i}.svg"); png = os.path.join(tmp, f"{i}.png")
    subprocess.run([sys.executable, os.path.join(HERE, script), svg, "single"], check=True)
    subprocess.run(["rsvg-convert", svg, "-o", png], check=True)
    data = base64.b64encode(open(png, "rb").read()).decode()
    y = GROUND - ground*k
    items.append(f'<image x="{x:.0f}" y="{y:.0f}" width="{400*k:.0f}" height="{h*k:.0f}" href="data:image/png;base64,{data}"/>')
    x += 365*k + (20 if k < 1 else 0)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HTOT}" viewBox="0 0 {W} {HTOT}">'
       f'<rect width="{W}" height="{HTOT}" fill="#FFF6E5"/>'
       f'<path d="M0,{GROUND} L{W},{GROUND}" stroke="#E8D8BC" stroke-width="2" stroke-dasharray="8 8"/>'
       + "".join(items) + "</svg>")
path = os.path.join(tmp, "gruppo.svg")
open(path, "w").write(svg)
subprocess.run(["rsvg-convert", path, "-o", OUT], check=True)
