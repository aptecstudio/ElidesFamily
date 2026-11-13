"""Poses and drawing order shared by the character drafts (D-032, D-050).

The poses are data: the draft sheets draw them and export_rig.py writes them
into the animation rig, so the game animates exactly the approved poses.
The kids (Elide, Rio) have the same body, so they share the same pose table.

A character module using character() / main() provides: DEFS, EYE_X,
SURPRISE_MARKS, MARKS_COLOR, POSE_DATA and the functions body_lower(), body(),
arm(), collar(), head_base(), blush_cheeks(), brows(), eye(), mouth(),
sparkle().
"""

import sys

SPARKLE = "#FFD84A"


def arm_pose(shoulder, side, p1, p2, p3, kind="back", hand_rot=None, layer="back", fold=None):
    """One arm of a pose: Bezier from the shoulder, hand kind and rotation,
    drawn behind ("back") or in front of ("front") the head; fold as in
    parts.arm, for a forearm that crosses in front of the upper arm."""
    return dict(
        side=side,
        points=(shoulder, p1, p2, p3),
        kind=kind,
        hand_rot=hand_rot,
        layer=layer,
        fold=fold,
    )


def face(eyes, look, brows_kind, mouth_kind, tilt, blush):
    return dict(eyes=eyes, look=look, brows=brows_kind, mouth=mouth_kind, tilt=tilt, blush=blush)


def kid_poses(sl, sr, accents):
    """Pose table of the kids. accents: two colors for the cheer sparkles."""

    def left(*a, **k):
        return arm_pose(sl, "L", *a, **k)

    def right(*a, **k):
        return arm_pose(sr, "R", *a, **k)

    arm_l_down = left((134, 340), (120, 372), (114, 400))
    arm_r_down = right((266, 340), (280, 372), (286, 400))
    return {
        "idle": dict(
            lift=0,
            lean=0,
            shadow=106,
            arms=(arm_l_down, arm_r_down),
            face=face(("open", "open"), (0, 0), "normal", "smile", -3, False),
        ),
        "wave": dict(
            lift=0,
            lean=-2,
            shadow=106,
            arms=(arm_l_down, right((284, 330), (310, 318), (318, 290), "palm")),
            face=face(("smiling", "smiling"), (0, 0), "happy", "open", -6, True),
        ),
        "cheer": dict(
            lift=-16,
            lean=0,
            shadow=82,
            arms=(
                left((110, 326), (66, 304), (54, 260), "palm"),
                right((290, 326), (334, 304), (346, 260), "palm"),
            ),
            face=face(("happy", "happy"), (0, 0), "up", "open", 3, True),
            sparkles=(
                (52, 210, 1.5, SPARKLE),
                (352, 186, 1.2, SPARKLE),
                (344, 322, 1.0, accents[0]),
                (60, 334, 0.9, accents[1]),
            ),
        ),
        "curious": dict(
            lift=0,
            lean=2,
            shadow=106,
            arms=(
                arm_l_down,
                right((312, 392), (286, 412), (248, 340), "fist", -24, "front", 0.5),
            ),
            face=face(("open", "open"), (7, -8), "curious", "curious", 8, False),
        ),
        "surprised": dict(
            lift=0,
            lean=0,
            shadow=106,
            arms=(
                left((98, 350), (62, 330), (78, 292), "palm", 18, "front"),
                right((302, 350), (338, 330), (322, 292), "palm", -18, "front"),
            ),
            face=face(("wide", "wide"), (0, 0), "up", "o", 0, False),
            marks=True,
        ),
        "proud": dict(
            lift=0,
            lean=-2,
            shadow=106,
            arms=(arm_l_down, right((306, 378), (346, 370), (338, 324), "thumb", 0, "front")),
            face=face(("happy", "smiling"), (0, 0), "happy", "open", -5, True),
            sparkles=((338, 262, 1.1, SPARKLE),),
        ),
        # Not on the draft sheet: built from approved pieces for the touch reaction.
        "giggle": dict(
            lift=0,
            lean=0,
            shadow=106,
            arms=(arm_l_down, arm_r_down),
            face=face(("happy", "happy"), (0, 0), "happy", "open", 0, True),
        ),
    }


# Poses on the draft sheet, with their labels.
SHEET = [
    ("idle", "Idle"),
    ("wave", "Hi!"),
    ("cheer", "Hooray!"),
    ("curious", "Curious"),
    ("surprised", "Surprised"),
    ("proud", "Well done!"),
]


def character(ch, pose):
    """SVG of character module ch in pose, in the 400×540 scene."""
    o = []
    data = ch.POSE_DATA[pose]
    o.append(
        f'<ellipse cx="200" cy="520" rx="{data["shadow"]}" ry="11" fill="#1D5A3A" opacity="0.28" filter="url(#b6)"/>'
    )
    o.append(f'<g transform="translate(0,{data["lift"]}) rotate({data["lean"]} 200 500)">')
    o.append(ch.body_lower())
    back = []
    front = []
    for a in data["arms"]:
        drawn = ch.arm(*a["points"], a["kind"], a["hand_rot"], a["fold"])
        (front if a["layer"] == "front" else back).extend(drawn)
    o.append(ch.body())
    o.extend(back)
    o.append(ch.collar())
    f = data["face"]
    eye_l, eye_r = f["eyes"]
    dx, dy = f["look"]
    o.append(f'<g transform="rotate({f["tilt"]} 200 300)">')
    o.append(ch.head_base())
    if f["blush"]:
        o.append(ch.blush_cheeks())
    o.append(ch.brows(f["brows"]))
    o.append(ch.eye(ch.EYE_X[0], "L", dx, dy, eye_l))
    o.append(ch.eye(ch.EYE_X[1], "R", dx, dy, eye_r))
    o.append(ch.mouth(f["mouth"]))
    o.append("</g>")
    o.extend(front)
    for x, y, k, c in data.get("sparkles", ()):
        o.append(ch.sparkle(x, y, k, c))
    if data.get("marks"):
        o.append(
            f'<path d="{ch.SURPRISE_MARKS}" fill="none" stroke="{ch.MARKS_COLOR}" stroke-width="3.5" stroke-linecap="round"/>'
        )
    o.append("</g>")
    return "".join(o)


def main(ch, label_color):
    """Command line of the draft scripts:
    script.py out.svg [single [pose]]"""
    out = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "sheet"
    if mode == "single":
        pose = sys.argv[3] if len(sys.argv) > 3 else "idle"
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="1080" viewBox="0 0 400 540">{ch.DEFS}{character(ch, pose)}</svg>'
    else:
        cw, chh = 400, 600
        cells = []
        for i, (p, label) in enumerate(SHEET):
            cx = (i % 3) * cw
            cy = (i // 3) * chh
            cells.append(
                f'<g transform="translate({cx},{cy})">{character(ch, p)}<text x="200" y="572" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="26" fill="{label_color}">{label}</text></g>'
            )
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200">{ch.DEFS}{"".join(cells)}</svg>'
    with open(out, "w") as fh:
        fh.write(svg)
