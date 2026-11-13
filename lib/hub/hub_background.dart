import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../app/game_colors.dart';

/// Height of the hub design, in design units: the hub is drawn in a scene
/// 720 units high and as wide as the screen allows (1600 on a 20:9 phone).
const double hubDesignHeight = 720;

/// Width of the approved draft (`tools/menu-drafts/hub_menu.py`).
const double hubDraftWidth = 1600;

/// Blend of two colors, like `mix()` in the draft: t=0 gives [a], t=1 [b].
Color mix(Color a, Color b, double t) => Color.lerp(a, b, t)!;

Color lighter(Color c, double t) => mix(c, const Color(0xFFFFFFFF), t);

Color darker(Color c, double t) => mix(c, GameColors.cocoa, t);

/// Sky-and-meadow background of the hub (D-047), a port of `background()` in
/// the draft. The clouds drift and the sun's rays turn slowly ([time], in
/// seconds). The hills stretch sideways with the screen; bushes, flowers and
/// tufts keep their shape and only move.
class HubBackgroundPainter extends CustomPainter {
  HubBackgroundPainter({required this.time}) : super(repaint: time);

  final ValueNotifier<double> time;

  @override
  void paint(Canvas canvas, Size size) {
    final t = time.value;
    final w = size.width;
    final sx = w / hubDraftWidth;
    final all = Offset.zero & size;

    canvas.drawRect(
      all,
      Paint()
        ..shader = LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            mix(GameColors.skyBlue, const Color(0xFF5BB8E6), 0.5),
            GameColors.skyBlue,
            const Color(0xFFEAF7FC),
          ],
          stops: const [0, 0.55, 1],
        ).createShader(all),
    );

    _sun(canvas, const Offset(372, 76), t);

    // Clouds drift to the right and come back in from the left.
    const clouds = [
      (200.0, 96.0, 1.0),
      (790.0, 54.0, 0.75),
      (1100.0, 70.0, 0.6),
    ];
    for (final (x, y, k) in clouds) {
      final span = w + 320;
      final cx = (x * sx + 160 + t * 6 * k) % span - 160;
      _cloud(canvas, Offset(cx, y), k);
    }

    Path hill(List<double> d) {
      // d: start point, then cubic segments (6 numbers each), in draft units.
      final p = Path()..moveTo(d[0] * sx, d[1]);
      for (var i = 2; i + 5 < d.length; i += 6) {
        p.cubicTo(
          d[i] * sx,
          d[i + 1],
          d[i + 2] * sx,
          d[i + 3],
          d[i + 4] * sx,
          d[i + 5],
        );
      }
      return p;
    }

    void ground(Path ridge, List<Color> colors, {double rim = 0}) {
      final area = Path.from(ridge)
        ..lineTo(w, hubDesignHeight)
        ..lineTo(0, hubDesignHeight)
        ..close();
      canvas.drawPath(area, _vertical(area.getBounds(), colors));
      if (rim > 0) {
        canvas.drawPath(
          ridge,
          Paint()
            ..style = PaintingStyle.stroke
            ..strokeWidth = 5
            ..color = const Color(0xFFFFFFFF).withValues(alpha: rim),
        );
      }
    }

    ground(
      hill(const [
        0, 500, 220, 440, 460, 450, 640, 500, 860, 560, 1120, 470, 1360, 470, //
        1460, 470, 1540, 490, 1600, 505,
      ]),
      const [Color(0xFFBFE6C4), Color(0xFFA7D9B5)],
    );
    ground(
      hill(const [
        0,
        560,
        300,
        500,
        620,
        510,
        900,
        560,
        1150,
        605,
        1400,
        590,
        1600,
        540,
      ]),
      const [Color(0xFFC4ECA8), Color(0xFF9CD483)],
      rim: 0.45,
    );
    _bush(canvas, Offset(60 * sx, 560), 0.9);
    _bush(canvas, Offset(1540 * sx, 548), 0.8);
    ground(
      hill(const [
        0,
        620,
        350,
        575,
        700,
        585,
        1000,
        630,
        1250,
        665,
        1450,
        650,
        1600,
        615,
      ]),
      [lighter(GameColors.meadowGreen, 0.25), const Color(0xFF7CC25E)],
      rim: 0.4,
    );
    const tufts = [
      (380.0, 660.0),
      (640.0, 690.0),
      (1040.0, 680.0),
      (1320.0, 700.0),
      (1560.0, 670.0),
      (40.0, 700.0),
    ];
    for (final (x, y) in tufts) {
      _tuft(canvas, Offset(x * sx, y));
    }
    final flowers = [
      (100.0, 650.0, GameColors.peachPink, 1.0),
      (1180.0, 668.0, GameColors.lavender, 1.0),
      (1480.0, 650.0, GameColors.butterYellow, 1.0),
      (900.0, 692.0, GameColors.peachPink, 0.9),
      (720.0, 640.0, GameColors.butterYellow, 0.7),
    ];
    for (final (i, (x, y, c, k)) in flowers.indexed) {
      // A gentle sway, each flower with its own phase.
      final sway = math.sin(t * 1.3 + i * 1.7) * 0.06;
      _flower(canvas, Offset(x * sx, y), c, k, sway);
    }

    // Soft patch of shade on the grass under Elide.
    canvas.drawOval(
      Rect.fromCenter(center: const Offset(225, 676), width: 240, height: 32),
      Paint()..color = const Color(0x473E7A2E),
    );
  }

  static Paint _vertical(Rect r, List<Color> colors, [List<double>? stops]) =>
      Paint()
        ..shader = LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: colors,
          stops: stops,
        ).createShader(r);

  static void _sun(Canvas canvas, Offset c, double t) {
    canvas.save();
    canvas.translate(c.dx, c.dy);
    const glow = Rect.fromLTRB(-120, -120, 120, 120);
    canvas.drawCircle(
      Offset.zero,
      120,
      Paint()
        ..shader = RadialGradient(
          colors: [
            const Color(0xFFFFF3C4).withValues(alpha: 0.9),
            const Color(0x00FFF3C4),
          ],
        ).createShader(glow),
    );
    canvas.save();
    canvas.rotate(t * 0.08);
    final ray = Paint()
      ..color = const Color(0xFFFFD66B).withValues(alpha: 0.85);
    for (var i = 0; i < 12; i++) {
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          const Rect.fromLTWH(-5, -58, 10, 18),
          const Radius.circular(5),
        ),
        ray,
      );
      canvas.rotate(math.pi / 6);
    }
    canvas.restore();
    const body = Rect.fromLTRB(-34, -34, 34, 34);
    canvas.drawCircle(
      Offset.zero,
      34,
      Paint()
        ..shader = const RadialGradient(
          center: Alignment(-0.24, -0.3),
          radius: 0.7,
          colors: [Color(0xFFFFF6CF), Color(0xFFFFE08A), Color(0xFFF7C75A)],
          stops: [0, 0.6, 1],
        ).createShader(body),
    );
    canvas.drawCircle(
      Offset.zero,
      34,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 3
        ..color = const Color(0xFFF2B84B),
    );
    canvas.drawOval(
      Rect.fromCenter(center: const Offset(-11, -13), width: 20, height: 12),
      Paint()..color = const Color(0xB3FFFFFF),
    );
    canvas.restore();
  }

  static void _cloud(Canvas canvas, Offset c, double k) {
    canvas.save();
    canvas.translate(c.dx, c.dy);
    canvas.scale(k);
    canvas.drawOval(
      Rect.fromCenter(center: const Offset(0, 18), width: 148, height: 60),
      Paint()..color = const Color(0x80BFDDEE),
    );
    final puffs = [
      Rect.fromCenter(center: const Offset(0, 10), width: 144, height: 60),
      Rect.fromCircle(center: const Offset(-32, -2), radius: 32),
      Rect.fromCircle(center: const Offset(16, -16), radius: 42),
      Rect.fromCircle(center: const Offset(52, 6), radius: 27),
    ];
    for (final r in puffs) {
      canvas.drawOval(
        r,
        _vertical(r, const [Color(0xFFFFFFFF), Color(0xFFD6EBF6)], [0.35, 1]),
      );
    }
    canvas.drawOval(
      Rect.fromCenter(center: const Offset(4, -34), width: 44, height: 18),
      Paint()..color = const Color(0xE6FFFFFF),
    );
    canvas.restore();
  }

  static void _bush(Canvas canvas, Offset c, double k) {
    canvas.save();
    canvas.translate(c.dx, c.dy);
    canvas.scale(k);
    final line = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3
      ..color = const Color(0xFF5A9A45);
    for (final (x, y, r) in const [
      (-34.0, -10.0, 30.0),
      (34.0, -8.0, 28.0),
      (0.0, -28.0, 38.0),
    ]) {
      final rect = Rect.fromCircle(center: Offset(x, y), radius: r);
      canvas.drawOval(
        rect,
        _vertical(rect, const [Color(0xFF8FD474), Color(0xFF5FA94A)]),
      );
      canvas.drawOval(rect, line);
    }
    canvas.drawOval(
      Rect.fromCenter(center: const Offset(-12, -48), width: 32, height: 14),
      Paint()..color = const Color(0x59FFFFFF),
    );
    canvas.restore();
  }

  static void _tuft(Canvas canvas, Offset c) {
    final x = c.dx;
    final y = c.dy;
    final p = Path()
      ..moveTo(x - 10, y)
      ..quadraticBezierTo(x - 8, y - 16, x - 2, y - 22)
      ..quadraticBezierTo(x, y - 10, x + 2, y)
      ..quadraticBezierTo(x + 6, y - 14, x + 12, y - 18)
      ..quadraticBezierTo(x + 8, y - 6, x + 10, y)
      ..close();
    canvas.drawPath(p, Paint()..color = const Color(0xFF6DB553));
  }

  static void _flower(
    Canvas canvas,
    Offset c,
    Color color,
    double k,
    double sway,
  ) {
    canvas.save();
    canvas.translate(c.dx, c.dy);
    canvas.scale(k);
    canvas.drawPath(
      Path()
        ..moveTo(0, 4)
        ..cubicTo(2, 16, 0, 26, -2, 34),
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 4
        ..color = const Color(0xFF5FA94A),
    );
    // The head sways around the top of the stem.
    canvas.translate(0, 4);
    canvas.rotate(sway);
    canvas.translate(0, -4);
    final petal = Paint()..color = color;
    final edge = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5
      ..color = darker(color, 0.25);
    const oval = Rect.fromLTRB(-8, -21, 8, 1);
    for (var i = 0; i < 5; i++) {
      canvas.drawOval(oval, petal);
      canvas.drawOval(oval, edge);
      canvas.rotate(2 * math.pi / 5);
    }
    canvas.drawCircle(Offset.zero, 7, Paint()..color = GameColors.butterYellow);
    canvas.drawCircle(
      Offset.zero,
      7,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2
        ..color = GameColors.honey,
    );
    canvas.drawCircle(
      const Offset(-2, -2),
      2.5,
      Paint()..color = const Color(0xCCFFFFFF),
    );
    canvas.restore();
  }

  @override
  bool shouldRepaint(HubBackgroundPainter oldDelegate) =>
      oldDelegate.time != time;
}
