import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import 'character_frame.dart';
import 'character_rig.dart';
import 'limb_geometry.dart';

/// Draws one [CharacterFrame] of a [CharacterRig] on a canvas, in the same
/// layer order as the drafts (`character()` in the draft scripts).
///
/// It only needs a [Canvas], so it works both in Flutter widgets
/// ([CharacterPainter]) and in Flame components.
class CharacterRenderer {
  CharacterRenderer(this.rig);

  final CharacterRig rig;

  /// Point of the scene where the body sways and squashes.
  static const Offset _feet = Offset(200, 510);

  /// Bottom of the dress: the upper body breathes from here.
  static const Offset _waist = Offset(200, 450);

  void paint(Canvas canvas, CharacterFrame f) {
    _shadow(canvas, f);
    canvas.save();
    canvas.translate(0, f.lift);
    _rotateAround(canvas, rig.leanPivot, f.lean);
    _scaleAround(canvas, _feet, 1 + f.squash, 1 - f.squash);

    canvas.save();
    _rotateAround(canvas, rig.tailRoot, f.tailAngle);
    _part(canvas, 'tail');
    canvas.restore();
    // Each leg and its foot are one piece: all the outlines, then the fills.
    final legs = [
      for (final leg in rig.legs)
        limbOutline(leg.points, leg.w0, leg.w1, bulge: leg.bulge),
    ];
    for (final path in legs) {
      _outline(canvas, path);
    }
    for (final leg in rig.legs) {
      _part(canvas, 'foot_outline', at: leg.foot);
    }
    for (final path in legs) {
      _fill(canvas, path, rig.limbFill);
    }
    for (final leg in rig.legs) {
      _part(canvas, 'foot_fill', at: leg.foot);
    }

    canvas.save();
    _scaleAround(canvas, _waist, 1 - f.breathe * 0.4, 1 + f.breathe);
    // Torso, shoulders and sleeves are one piece (D-053): torso outline,
    // all the arms, then the torso fill over the roots of the sleeves.
    _part(canvas, 'body_outline');
    for (final MapEntry(key: side, value: arm) in f.arms.entries) {
      _arm(canvas, side, arm);
    }
    _part(canvas, 'body_fill');
    _part(canvas, 'collar');
    _head(canvas, f);
    // Forearms and hands in front of the head or of their own sleeve.
    for (final MapEntry(key: side, value: arm) in f.arms.entries) {
      if (arm.front || arm.fold != null) {
        _armFront(canvas, side, arm, arm.fold ?? rig.arm.frontFrom);
      }
    }
    canvas.restore();

    _sparkles(canvas, f);
    _marks(canvas, f);
    canvas.restore();
  }

  // ------------------------------------------------------------ body

  void _shadow(Canvas canvas, CharacterFrame f) {
    final s = rig.shadow;
    // The shadow shrinks and fades while the character is in the air.
    final air = (-f.lift / 60).clamp(0.0, 0.6);
    final paint = Paint()
      ..color = s.color.withValues(alpha: s.color.a * (1 - air * 0.6))
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 6);
    canvas.drawOval(
      Rect.fromCenter(
        center: s.center,
        width: 2 * f.shadow * (1 - air * 0.4),
        height: 2 * s.ry,
      ),
      paint,
    );
  }

  /// An arm with its sleeve and hand. Arm and hand are one piece: their
  /// outlines are drawn first and the fills on top, so no line shows at the
  /// wrist (as in `parts.arm()`).
  void _arm(Canvas canvas, String side, ArmFrame a) {
    final p = a.points;
    final style = rig.arm;
    final armPath = limbOutline(p, style.w0, style.w1, bulge: style.bulge);

    void hand(String layer) => _hand(canvas, side, a, layer);

    _outline(canvas, armPath);
    hand('outline');
    _fill(canvas, armPath, rig.limbFill);

    final sl = rig.sleeve;
    final t1 = sl.t1;
    final tan = bezierTangent(p, t1);
    final angle = math.atan2(tan.dy, tan.dx);
    if (!sl.long) {
      // Soft shadow where the arm comes out of the sleeve.
      final c = bezierAt(p, math.min(t1 + 0.06, 1));
      canvas.save();
      canvas.clipPath(armPath);
      canvas.translate(c.dx, c.dy);
      canvas.rotate(angle);
      canvas.drawOval(
        Rect.fromCenter(center: Offset.zero, width: 18, height: 44),
        Paint()
          ..color = const Color(0x21000000)
          ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 3),
      );
      canvas.restore();
    }
    final sleevePath = limbOutline(
      p,
      sl.w0,
      sl.w1,
      bulge: 4,
      t1: t1,
      capEnd: false,
      capStart: true,
    );
    _fill(canvas, sleevePath, sl.fill);
    _stroke(canvas, sleevePath, sl.line, 2.6);

    // Cuff: perpendicular to the arm, so it follows every pose.
    final c = bezierAt(p, t1);
    final hw = (sl.w0 + (sl.w1 - sl.w0) * t1) / 2 + 4 * math.sin(math.pi * t1);
    canvas.save();
    canvas.translate(c.dx, c.dy);
    canvas.rotate(angle);
    if (sl.trim != null) {
      final cuff = Rect.fromCenter(
        center: Offset.zero,
        width: 10,
        height: 2 * hw,
      );
      canvas.drawOval(cuff, Paint()..color = sl.trim!);
      canvas.drawOval(
        cuff,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2
          ..color = sl.trimLine,
      );
    } else {
      canvas.drawArc(
        Rect.fromCenter(center: Offset.zero, width: 6, height: 2 * hw),
        -math.pi / 2,
        math.pi,
        false,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2
          ..strokeCap = StrokeCap.round
          ..color = sl.line.withValues(alpha: 0.6),
      );
    }
    canvas.restore();

    hand('fill');
  }

  /// Forearm (from [t0]) and hand drawn again over the arm: in front of the
  /// head, or over its own sleeve. Only its sides and tip are outlined, so it
  /// starts seamlessly from the arm underneath (`parts.arm_front()`).
  void _armFront(Canvas canvas, String side, ArmFrame a, double t0) {
    final p = a.points;
    final style = rig.arm;
    final edge = limbOutline(
      p,
      style.w0,
      style.w1,
      bulge: style.bulge,
      t0: t0,
      closed: false,
    );
    _stroke(canvas, edge, rig.line, 2 * rig.limbStroke);
    _hand(canvas, side, a, 'outline');
    final piece = limbOutline(
      p,
      style.w0,
      style.w1,
      bulge: style.bulge,
      t0: t0,
    );
    _fill(canvas, piece, rig.limbFill);
    _hand(canvas, side, a, 'fill');
  }

  /// One layer (`outline` or `fill`) of the hand at the end of an arm,
  /// turned along it.
  void _hand(Canvas canvas, String side, ArmFrame a, String layer) {
    final p = a.points;
    final q = bezierAt(p, 0.92);
    var dir = p[3] - q;
    dir = dir / (dir.distance == 0 ? 1 : dir.distance);
    final rotDeg = a.handRot ?? math.atan2(dir.dy, dir.dx) * 180 / math.pi + 90;
    final pos = p[3] + dir * rig.arm.handOffset;
    canvas.save();
    canvas.translate(pos.dx, pos.dy);
    canvas.rotate(rad(rotDeg));
    canvas.scale(thumbMirror(a.kind, side), 1);
    _part(canvas, 'hand_${a.kind}_$layer');
    canvas.restore();
  }

  // ------------------------------------------------------------ head

  void _head(Canvas canvas, CharacterFrame f) {
    canvas.save();
    canvas.translate(0, f.headBob);
    _rotateAround(canvas, rig.headPivot, f.tilt);
    _part(canvas, 'head');
    if (f.blush > 0.01) _part(canvas, 'blush', opacity: f.blush);
    _crossFade(canvas, 'brows', f.browsFrom, f.browsTo, f.browsT);
    for (var i = 0; i < 2; i++) {
      _eye(canvas, i, f.eyes[i], f.look);
    }
    _crossFade(canvas, 'mouth', f.mouthFrom, f.mouthTo, f.mouthT);
    canvas.restore();
  }

  void _eye(Canvas canvas, int index, String kind, Offset look) {
    final e = rig.eyes;
    final side = index == 0 ? 'l' : 'r';
    final geometry = e.geometry[kind];
    if (e.open.contains(kind) && geometry != null) {
      final cx = e.x[index];
      final white = Rect.fromCenter(
        center: Offset(cx, e.cy),
        width: 2 * e.rx,
        height: 2 * e.ry,
      );
      canvas.drawOval(white, Paint()..color = const Color(0xFFFFFFFF));
      canvas.drawOval(
        white,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = e.lineWidth
          ..color = e.line,
      );
      canvas.save();
      canvas.clipPath(Path()..addOval(white));
      final ix = cx + (index == 0 ? geometry.x : -geometry.x) + look.dx;
      final iy = geometry.y + look.dy;
      final iris = Rect.fromCircle(center: Offset(ix, iy), radius: geometry.r);
      canvas.drawOval(
        iris,
        Paint()..shader = rig.gradients[e.iris]!.shader(iris),
      );
      canvas.drawCircle(
        Offset(ix, iy + 1),
        geometry.pupil,
        Paint()..color = e.pupil,
      );
      const highlight = Color(0xFFFFFFFF);
      canvas.drawOval(
        Rect.fromCenter(center: Offset(ix + 8, iy - 10), width: 15, height: 17),
        Paint()..color = highlight,
      );
      canvas.drawCircle(
        Offset(ix - 9, iy + 10),
        3.4,
        Paint()..color = highlight.withValues(alpha: 0.9),
      );
      canvas.restore();
    }
    _part(canvas, 'eye_${side}_$kind');
  }

  void _crossFade(
    Canvas canvas,
    String prefix,
    String from,
    String to,
    double t,
  ) {
    if (from == to || t >= 0.99) {
      _part(canvas, '${prefix}_$to');
    } else if (t <= 0.01) {
      _part(canvas, '${prefix}_$from');
    } else {
      _part(canvas, '${prefix}_$from', opacity: 1 - t);
      _part(canvas, '${prefix}_$to', opacity: t);
    }
  }

  // ------------------------------------------------------------ effects

  void _sparkles(Canvas canvas, CharacterFrame f) {
    for (final (i, s) in f.sparkles.indexed) {
      final twinkle = 1 + 0.18 * math.sin(f.time * 5 + i * 1.7);
      canvas.save();
      canvas.translate(s.data.position.dx, s.data.position.dy);
      canvas.scale(s.data.scale * twinkle);
      canvas.rotate(0.15 * math.sin(f.time * 2 + i));
      canvas.drawPath(
        rig.sparklePath,
        Paint()..color = s.data.color.withValues(alpha: s.opacity),
      );
      canvas.restore();
    }
  }

  void _marks(Canvas canvas, CharacterFrame f) {
    if (f.marks <= 0.01) return;
    canvas.drawPath(
      rig.marksPath,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = rig.marksWidth
        ..strokeCap = StrokeCap.round
        ..color = rig.marksColor.withValues(alpha: f.marks),
    );
  }

  // ------------------------------------------------------------ helpers

  void _part(
    Canvas canvas,
    String key, {
    Offset at = Offset.zero,
    double opacity = 1,
  }) {
    final image = rig.images[key];
    final rect = rig.parts[key];
    if (image == null || rect == null) return;
    canvas.drawImageRect(
      image,
      Rect.fromLTWH(0, 0, image.width.toDouble(), image.height.toDouble()),
      rect.shift(at),
      Paint()
        ..filterQuality = FilterQuality.medium
        ..color = Color.fromRGBO(0, 0, 0, opacity),
    );
  }

  /// Outline pass of a shape that merges with its neighbours: a stroke twice
  /// as wide, half of which is then covered by the fill.
  void _outline(Canvas canvas, Path path) {
    canvas.drawPath(path, Paint()..color = rig.line);
    _stroke(canvas, path, rig.line, 2 * rig.limbStroke);
  }

  void _fill(Canvas canvas, Path path, String gradient) {
    canvas.drawPath(
      path,
      Paint()..shader = rig.gradients[gradient]!.shader(path.getBounds()),
    );
  }

  void _stroke(Canvas canvas, Path path, Color color, double width) {
    canvas.drawPath(
      path,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = width
        ..strokeJoin = StrokeJoin.round
        ..strokeCap = StrokeCap.round
        ..color = color,
    );
  }

  static void _rotateAround(Canvas canvas, Offset pivot, double degrees) {
    if (degrees == 0) return;
    canvas.translate(pivot.dx, pivot.dy);
    canvas.rotate(rad(degrees));
    canvas.translate(-pivot.dx, -pivot.dy);
  }

  static void _scaleAround(Canvas canvas, Offset pivot, double sx, double sy) {
    if (sx == 1 && sy == 1) return;
    canvas.translate(pivot.dx, pivot.dy);
    canvas.scale(sx, sy);
    canvas.translate(-pivot.dx, -pivot.dy);
  }
}

/// Horizontal flip of a hand so the thumb is on the right side: it only
/// depends on which hand it is ([side] `L` is the one on the viewer's left)
/// and on whether the palm side is shown; the hand rotation does the rest.
/// Same rule as `thumb_mirror()` in `tools/character-drafts/parts.py`.
double thumbMirror(String kind, String side) {
  final palmSide = kind != 'back';
  return (palmSide ? -1.0 : 1.0) * (side == 'L' ? 1.0 : -1.0);
}

/// [CustomPainter] that fits the 400×540 character scene into the widget,
/// with the feet on the bottom edge.
class CharacterPainter extends CustomPainter {
  CharacterPainter({
    required this.renderer,
    required this.frame,
    super.repaint,
  });

  final CharacterRenderer renderer;
  final CharacterFrame Function() frame;

  @override
  void paint(Canvas canvas, Size size) {
    final scene = renderer.rig.size;
    final scale = math.min(
      size.width / scene.width,
      size.height / scene.height,
    );
    canvas.save();
    canvas.translate(
      (size.width - scene.width * scale) / 2,
      size.height - scene.height * scale,
    );
    canvas.scale(scale);
    renderer.paint(canvas, frame());
    canvas.restore();
  }

  @override
  bool shouldRepaint(CharacterPainter oldDelegate) =>
      oldDelegate.renderer != renderer;
}
