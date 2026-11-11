import 'package:flutter/widgets.dart';

/// Rende toccabile qualsiasi elemento della scena con un feedback "morbido":
/// si schiaccia al tocco e rimbalza al rilascio.
///
/// Ogni elemento interattivo del gioco deve passare da qui, così il
/// feedback al tocco è uguale ovunque (AGENTS.md, principio 3).
// TODO(fase-3): aggiungere il suono del tocco tramite il servizio audio.
class BouncyTap extends StatefulWidget {
  const BouncyTap({required this.child, this.onTap, super.key});

  final Widget child;
  final VoidCallback? onTap;

  @override
  State<BouncyTap> createState() => _BouncyTapState();
}

class _BouncyTapState extends State<BouncyTap>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 90),
    reverseDuration: const Duration(milliseconds: 500),
    value: 0,
  );

  late final Animation<double> _scale = Tween<double>(begin: 1, end: 0.86)
      .animate(
        CurvedAnimation(
          parent: _controller,
          curve: Curves.easeOut,
          reverseCurve: Curves.elasticIn,
        ),
      );

  void _press() => _controller.forward();

  void _release() {
    _controller.reverse();
    widget.onTap?.call();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTapDown: (_) => _press(),
      onTapUp: (_) => _release(),
      onTapCancel: () => _controller.reverse(),
      child: ScaleTransition(scale: _scale, child: widget.child),
    );
  }
}
