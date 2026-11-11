import 'package:flutter/widgets.dart';

/// Transizione tra scene in stile gioco: la nuova scena "sboccia"
/// con una dissolvenza e un leggero ingrandimento elastico.
class GameRoute<T> extends PageRouteBuilder<T> {
  GameRoute({required WidgetBuilder builder, super.settings})
      : super(
          transitionDuration: const Duration(milliseconds: 450),
          reverseTransitionDuration: const Duration(milliseconds: 300),
          pageBuilder: (context, _, __) => builder(context),
          transitionsBuilder: (context, animation, _, child) {
            final scale = Tween<double>(begin: 0.92, end: 1).animate(
              CurvedAnimation(parent: animation, curve: Curves.easeOutBack),
            );
            return FadeTransition(
              opacity: animation,
              child: ScaleTransition(scale: scale, child: child),
            );
          },
        );
}
