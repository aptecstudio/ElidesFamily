import 'dart:math' as math;
import 'dart:ui';

/// Point of the cubic Bezier [p] (four control points) at [t].
Offset bezierAt(List<Offset> p, double t) {
  final u = 1 - t;
  return p[0] * (u * u * u) +
      p[1] * (3 * u * u * t) +
      p[2] * (3 * u * t * t) +
      p[3] * (t * t * t);
}

/// Derivative of the cubic Bezier [p] at [t].
Offset bezierTangent(List<Offset> p, double t) {
  final u = 1 - t;
  return (p[1] - p[0]) * (3 * u * u) +
      (p[2] - p[1]) * (6 * u * t) +
      (p[3] - p[2]) * (3 * t * t);
}

/// Closed outline of a chubby limb along the Bezier [p]: the width goes from
/// [w0] at the root to [w1] at the tip, swelling by [bulge] in the middle.
///
/// Port of `limb_outline()` in `tools/character-drafts/parts.py`, so arms and
/// legs look exactly like the drafts, but are recomputed every frame.
Path limbOutline(
  List<Offset> p,
  double w0,
  double w1, {
  double bulge = 3,
  double t0 = 0,
  double t1 = 1,
  bool capEnd = true,
  bool capStart = false,
}) {
  const steps = 40;
  final left = <Offset>[];
  final right = <Offset>[];
  for (var i = 0; i <= steps; i++) {
    final t = t0 + (t1 - t0) * i / steps;
    final c = bezierAt(p, t);
    final n = _normal(bezierTangent(p, t));
    final w = (w0 + (w1 - w0) * t) / 2 + bulge * math.sin(math.pi * t);
    left.add(c + n * w);
    right.add(c - n * w);
  }

  List<Offset> cap(Offset a, Offset b, double t, double sign) {
    final c = (a + b) / 2;
    final r = (a - c).distance;
    final tan = bezierTangent(p, t);
    final len = tan.distance == 0 ? 1.0 : tan.distance;
    final tx = tan / len * sign;
    final u = r == 0 ? Offset.zero : (a - c) / r;
    return [
      for (var k = 1; k < 12; k++)
        c +
            u * (r * math.cos(math.pi * k / 12)) +
            tx * (r * math.sin(math.pi * k / 12)),
    ];
  }

  final points = <Offset>[...left];
  if (capEnd) points.addAll(cap(left.last, right.last, t1, 1));
  points.addAll(right.reversed);
  if (capStart) points.addAll(cap(right.first, left.first, t0, -1));
  return Path()..addPolygon(points, true);
}

Offset _normal(Offset tangent) {
  final len = tangent.distance == 0 ? 1.0 : tangent.distance;
  return Offset(-tangent.dy / len, tangent.dx / len);
}
