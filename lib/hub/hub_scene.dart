import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../app/game_colors.dart';
import '../app/game_route.dart';
import '../characters/character_view.dart';
import '../core/bouncy_tap.dart';
import '../minigames/colors/colors_game_scene.dart';

/// Main scene (hub): this is where the child picks a minigame.
///
/// Temporary Phase 2 version: a landscape drawn in code and a "bubble" for
/// the Colors minigame. The illustrated house with the characters comes in
/// Phase 5.
class HubScene extends StatelessWidget {
  const HubScene({super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(
      fit: StackFit.expand,
      children: [
        const CustomPaint(painter: _LandscapePainter()),
        // Elide on the hill: she breathes, blinks and reacts to touches.
        LayoutBuilder(
          builder: (context, box) {
            final height = box.maxHeight * 0.78;
            return Align(
              alignment: const Alignment(-0.9, 1),
              child: SizedBox(
                width: height * 400 / 540,
                height: height,
                child: const CharacterView(character: 'elide'),
              ),
            );
          },
        ),
        Center(
          child: _FloatingBubble(
            onTap: () => Navigator.of(
              context,
            ).push(GameRoute<void>(builder: (_) => const ColorsGameScene())),
            child: const _PaletteIcon(),
          ),
        ),
      ],
    );
  }
}

/// Bubble that floats gently and bounces when tapped.
class _FloatingBubble extends StatefulWidget {
  const _FloatingBubble({required this.child, required this.onTap});

  final Widget child;
  final VoidCallback onTap;

  @override
  State<_FloatingBubble> createState() => _FloatingBubbleState();
}

class _FloatingBubbleState extends State<_FloatingBubble>
    with SingleTickerProviderStateMixin {
  late final AnimationController _float = AnimationController(
    vsync: this,
    duration: const Duration(seconds: 2),
  )..repeat(reverse: true);

  @override
  void dispose() {
    _float.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _float,
      builder: (context, child) {
        final dy = math.sin(_float.value * math.pi) * -12;
        return Transform.translate(offset: Offset(0, dy), child: child);
      },
      child: BouncyTap(
        onTap: widget.onTap,
        child: Container(
          width: 180,
          height: 180,
          decoration: BoxDecoration(
            color: GameColors.cream,
            shape: BoxShape.circle,
            border: Border.all(color: GameColors.cocoa, width: 5),
            boxShadow: const [
              BoxShadow(
                color: Color(0x33000000),
                blurRadius: 12,
                offset: Offset(0, 8),
              ),
            ],
          ),
          alignment: Alignment.center,
          child: widget.child,
        ),
      ),
    );
  }
}

/// Colors minigame icon: a palette of colored drops.
class _PaletteIcon extends StatelessWidget {
  const _PaletteIcon();

  static const _drops = [
    Color(0xFFE94B4B), // red
    Color(0xFFFFC93C), // yellow
    Color(0xFF3C8DE9), // blue
    Color(0xFF4CBF5A), // green
    Color(0xFFFF8A3C), // orange
    Color(0xFF9B5DE5), // purple
  ];

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 120,
      height: 120,
      child: Stack(
        children: [
          for (var i = 0; i < _drops.length; i++)
            Align(
              alignment: Alignment(
                0.75 * math.cos(i * 2 * math.pi / _drops.length),
                0.75 * math.sin(i * 2 * math.pi / _drops.length),
              ),
              child: Container(
                width: 34,
                height: 34,
                decoration: BoxDecoration(
                  color: _drops[i],
                  shape: BoxShape.circle,
                  border: Border.all(color: GameColors.cocoa, width: 3),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

/// Background landscape: sky, sun, hills.
class _LandscapePainter extends CustomPainter {
  const _LandscapePainter();

  @override
  void paint(Canvas canvas, Size size) {
    final sky = Paint()
      ..shader = const LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [GameColors.skyBlue, GameColors.cream],
      ).createShader(Offset.zero & size);
    canvas.drawRect(Offset.zero & size, sky);

    // Sun
    canvas.drawCircle(
      Offset(size.width * 0.85, size.height * 0.18),
      size.height * 0.1,
      Paint()..color = GameColors.butterYellow,
    );

    // Hills (two layers)
    _hill(canvas, size, 0.72, GameColors.meadowGreen.withValues(alpha: 0.7));
    _hill(canvas, size, 0.8, GameColors.meadowGreen);
  }

  void _hill(Canvas canvas, Size size, double top, Color color) {
    final h = size.height;
    final w = size.width;
    final path = Path()
      ..moveTo(0, h * top)
      ..quadraticBezierTo(w * 0.25, h * (top - 0.12), w * 0.5, h * top)
      ..quadraticBezierTo(w * 0.75, h * (top + 0.1), w, h * (top - 0.04))
      ..lineTo(w, h)
      ..lineTo(0, h)
      ..close();
    canvas.drawPath(path, Paint()..color = color);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
