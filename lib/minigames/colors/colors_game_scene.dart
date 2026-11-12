import 'package:flutter/widgets.dart';

import '../../app/game_colors.dart';
import '../../core/bouncy_tap.dart';
import '../../l10n/app_localizations.dart';

/// Colors minigame (D-010, D-011).
///
/// Phase 2 placeholder: the mechanics (level 1 "sort into the baskets",
/// level 2 "paint") will be built with Flame in Phase 6.
class ColorsGameScene extends StatelessWidget {
  const ColorsGameScene({super.key});

  @override
  Widget build(BuildContext context) {
    return ColoredBox(
      color: GameColors.lavender,
      child: Stack(
        children: [
          Center(child: Text(AppLocalizations.of(context).comingSoon)),
          Positioned(
            top: 24,
            left: 24,
            child: BouncyTap(
              onTap: () => Navigator.of(context).pop(),
              child: Container(
                width: 88,
                height: 88,
                decoration: BoxDecoration(
                  color: GameColors.butterYellow,
                  shape: BoxShape.circle,
                  border: Border.all(color: GameColors.cocoa, width: 4),
                ),
                child: const CustomPaint(painter: _HomeIconPainter()),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

/// Drawn little house: the "back home" button is an icon, not a label.
class _HomeIconPainter extends CustomPainter {
  const _HomeIconPainter();

  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;
    final fill = Paint()..color = GameColors.peachPink;
    final stroke = Paint()
      ..color = GameColors.cocoa
      ..style = PaintingStyle.stroke
      ..strokeWidth = 4
      ..strokeJoin = StrokeJoin.round;

    final house = Path()
      ..moveTo(w * 0.5, h * 0.24)
      ..lineTo(w * 0.76, h * 0.48)
      ..lineTo(w * 0.7, h * 0.48)
      ..lineTo(w * 0.7, h * 0.74)
      ..lineTo(w * 0.3, h * 0.74)
      ..lineTo(w * 0.3, h * 0.48)
      ..lineTo(w * 0.24, h * 0.48)
      ..close();
    canvas
      ..drawPath(house, fill)
      ..drawPath(house, stroke);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
