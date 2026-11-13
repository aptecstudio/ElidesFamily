import 'package:flutter/widgets.dart';

import '../app/game_colors.dart';
import '../core/bouncy_tap.dart';
import 'hub_background.dart';

/// Size of a card in design units, without the "cushion" and the badge
/// that sticks out below (D-047, `card()` in `hub_menu.py`).
const Size cardSize = Size(230, 200);

/// Total height taken by a card, badge included.
const double cardExtent = 232;

const double _radius = 40;
const double _depth = 12;
const double _badgeHeight = 50;
const double _line = 7;

/// Soft drop shadow of cards and badges (the draft's `soft` filter).
const _soft = BoxShadow(
  color: Color(0x473E5A2E),
  offset: Offset(0, 10),
  blurRadius: 15,
);

/// A straight rounded postcard with volume (D-047, D-049): a darker cushion
/// underneath, a gradient frame with a glossy top, a cream drawing area with
/// an inner shadow and the game name on a cream badge across the bottom edge.
class GameCard extends StatelessWidget {
  const GameCard({
    required this.color,
    required this.icon,
    required this.name,
    required this.onTap,
    super.key,
  });

  final Color color;

  /// Asset of the game icon, exported by `tools/menu-drafts/export_hub.py`.
  final String icon;
  final String name;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return BouncyTap(
      onTap: onTap,
      child: SizedBox(
        width: cardSize.width,
        height: cardExtent,
        child: Stack(
          clipBehavior: Clip.none,
          children: [
            // Cushion.
            Positioned(
              top: _depth,
              width: cardSize.width,
              height: cardSize.height,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  color: darker(color, 0.35),
                  borderRadius: BorderRadius.circular(_radius),
                  border: Border.all(
                    color: GameColors.cocoa,
                    width: _line,
                    strokeAlign: BorderSide.strokeAlignCenter,
                  ),
                  boxShadow: const [_soft],
                ),
              ),
            ),
            // Frame.
            Positioned(
              top: 0,
              width: cardSize.width,
              height: cardSize.height,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [lighter(color, 0.35), color, darker(color, 0.1)],
                  ),
                  borderRadius: BorderRadius.circular(_radius),
                  border: Border.all(
                    color: GameColors.cocoa,
                    width: _line,
                    strokeAlign: BorderSide.strokeAlignCenter,
                  ),
                ),
              ),
            ),
            // Glossy highlight on the top edge.
            const Positioned(
              left: 26,
              top: 7,
              width: 230 - 52,
              height: 14,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(7)),
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [Color(0xBFFFFFFF), Color(0x00FFFFFF)],
                  ),
                ),
              ),
            ),
            // Cream drawing area with the icon.
            Positioned(
              left: 18,
              top: 20,
              width: cardSize.width - 36,
              height: cardSize.height - 52,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(_radius - 16),
                  border: Border.all(
                    color: darker(color, 0.2),
                    width: 3,
                    strokeAlign: BorderSide.strokeAlignCenter,
                  ),
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [
                      darker(GameColors.cream, 0.12),
                      GameColors.cream,
                      lighter(GameColors.cream, 0.4),
                    ],
                    stops: const [0, 0.16, 1],
                  ),
                ),
                child: OverflowBox(
                  maxWidth: double.infinity,
                  maxHeight: double.infinity,
                  child: Image.asset(
                    icon,
                    width: cardSize.width - 36,
                    height: cardSize.height - 52,
                    filterQuality: FilterQuality.medium,
                  ),
                ),
              ),
            ),
            // Name badge.
            Positioned(
              left: 0,
              right: 0,
              top: cardSize.height - _badgeHeight / 2 + 6,
              height: _badgeHeight,
              child: Center(child: _Badge(name)),
            ),
          ],
        ),
      ),
    );
  }
}

class _Badge extends StatelessWidget {
  const _Badge(this.name);

  final String name;

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          height: _badgeHeight,
          // 3 + 6 + 32 + 6 + 3 = 50 (6: half of the border inside).
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 6),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(_badgeHeight / 2),
            border: Border.all(
              color: GameColors.cocoa,
              width: 6,
              strokeAlign: BorderSide.strokeAlignCenter,
            ),
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [const Color(0xFFFFFFFF), darker(GameColors.cream, 0.08)],
            ),
            boxShadow: const [_soft],
          ),
          child: Text(
            name,
            maxLines: 1,
            style: const TextStyle(
              fontSize: 32,
              height: 1,
              color: GameColors.cocoa,
            ),
          ),
        ),
        // Glossy streak along the top of the badge.
        Positioned(
          left: 16,
          right: 16,
          top: 6,
          height: 10,
          child: DecoratedBox(
            decoration: BoxDecoration(
              color: const Color(0xFFFFFFFF).withValues(alpha: 0.8),
              borderRadius: BorderRadius.circular(5),
            ),
          ),
        ),
      ],
    );
  }
}
