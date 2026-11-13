import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import 'game_card.dart';

/// Card of a game still to come (D-056): a closed gift that wiggles and
/// lifts its lid a little when touched, but never opens.
class SurpriseCard extends StatefulWidget {
  const SurpriseCard({required this.color, this.onTap, super.key});

  final Color color;
  final VoidCallback? onTap;

  @override
  State<SurpriseCard> createState() => _SurpriseCardState();
}

class _SurpriseCardState extends State<SurpriseCard>
    with SingleTickerProviderStateMixin {
  late final AnimationController _shake = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 900),
  );

  @override
  void dispose() {
    _shake.dispose();
    super.dispose();
  }

  void _tap() {
    _shake.forward(from: 0);
    widget.onTap?.call();
  }

  @override
  Widget build(BuildContext context) {
    return GameCard(
      color: widget.color,
      name: '?',
      onTap: _tap,
      art: AnimatedBuilder(
        animation: _shake,
        builder: (context, _) {
          final t = _shake.value;
          // Three wiggles that fade out, and the lid hops twice.
          final wiggle = math.sin(t * math.pi * 6) * 0.12 * (1 - t);
          final hop = -math.sin(t * math.pi * 2).abs() * 14 * (1 - t);
          return Transform.rotate(
            angle: wiggle,
            alignment: const Alignment(0, 0.8),
            child: Stack(
              clipBehavior: Clip.none,
              children: [
                cardIcon('assets/images/hub/hub_icon_gift_box.png'),
                Transform.translate(
                  offset: Offset(0, hop),
                  child: cardIcon('assets/images/hub/hub_icon_gift_lid.png'),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
