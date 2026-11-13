import 'package:flutter/scheduler.dart';
import 'package:flutter/widgets.dart';

import 'character_controller.dart';
import 'character_painter.dart';
import 'character_rig.dart';

/// An animated character (D-039, D-050), e.g. `CharacterView(character: 'elide')`.
///
/// The character breathes, blinks and looks around on its own; a touch plays
/// a reaction (wave, hooray, giggle). The scene is fitted into the available
/// space with the feet on the bottom edge.
class CharacterView extends StatefulWidget {
  const CharacterView({
    required this.character,
    this.controller,
    this.reactToTouch = true,
    this.onTap,
    super.key,
  });

  /// Rig name: `assets/animations/char_<character>_rig.json`.
  final String character;

  /// Optional external controller, to trigger poses and actions from a game.
  final CharacterController? controller;

  /// Play a random reaction when touched.
  final bool reactToTouch;
  final VoidCallback? onTap;

  @override
  State<CharacterView> createState() => _CharacterViewState();
}

class _CharacterViewState extends State<CharacterView>
    with SingleTickerProviderStateMixin {
  late CharacterController _controller =
      widget.controller ?? CharacterController();
  late final Ticker _ticker = createTicker(_onTick);
  CharacterRenderer? _renderer;
  Duration _last = Duration.zero;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final rig = await CharacterRig.load(widget.character);
    if (!mounted) return;
    _controller.attach(rig);
    setState(() => _renderer = CharacterRenderer(rig));
    _ticker.start();
  }

  void _onTick(Duration elapsed) {
    // Clamp long pauses (e.g. app in background) to one smooth step.
    final dt = ((elapsed - _last).inMicroseconds / 1e6).clamp(0.0, 0.05);
    _last = elapsed;
    _controller.tick(dt);
  }

  @override
  void didUpdateWidget(CharacterView oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.controller != oldWidget.controller) {
      if (oldWidget.controller == null) _controller.dispose();
      _controller = widget.controller ?? CharacterController();
      final rig = _renderer?.rig;
      if (rig != null) _controller.attach(rig);
    }
  }

  @override
  void dispose() {
    _ticker.dispose();
    if (widget.controller == null) _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final renderer = _renderer;
    if (renderer == null) return const SizedBox.expand();
    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTap: () {
        if (widget.reactToTouch) _controller.react();
        widget.onTap?.call();
      },
      child: CustomPaint(
        size: Size.infinite,
        painter: CharacterPainter(
          renderer: renderer,
          frame: () => _controller.frame!,
          repaint: _controller,
        ),
      ),
    );
  }
}
