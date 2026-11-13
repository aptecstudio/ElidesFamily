import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../app/game_colors.dart';
import '../core/bouncy_tap.dart';
import '../hub/hub_background.dart';
import '../l10n/app_localizations.dart';

/// Shows the parental gate (D-057) over the current scene and completes with
/// true only when the multiplication is answered right.
///
/// A wrong answer closes the gate gently, with no error sound or message: it
/// is usually the child tapping at random.
Future<bool> showParentalGate(
  BuildContext context, {
  math.Random? random,
}) async {
  final passed = await Navigator.of(context).push<bool>(
    PageRouteBuilder<bool>(
      opaque: false,
      barrierDismissible: true,
      barrierLabel: 'close',
      barrierColor: const Color(0x663E5A2E),
      transitionDuration: const Duration(milliseconds: 350),
      reverseTransitionDuration: const Duration(milliseconds: 250),
      pageBuilder: (context, _, _) => ParentalGate(random: random),
      transitionsBuilder: (context, animation, _, child) => FadeTransition(
        opacity: animation,
        child: ScaleTransition(
          scale: Tween<double>(begin: 0.85, end: 1).animate(
            CurvedAnimation(parent: animation, curve: Curves.easeOutBack),
          ),
          child: child,
        ),
      ),
    ),
  );
  return passed ?? false;
}

/// The gate panel: "How much is 7 × 4?", the typed digits and a drawn
/// number pad. Keys work with touch and with the TV remote (arrows and OK).
class ParentalGate extends StatefulWidget {
  const ParentalGate({this.random, super.key});

  /// Source of the factors (tests pass a seeded one).
  final math.Random? random;

  @override
  State<ParentalGate> createState() => _ParentalGateState();
}

class _ParentalGateState extends State<ParentalGate> {
  // Design size of the panel, in the hub's design units (720 high).
  static const _panel = Size(760, 520);
  static const _keySize = 96.0;

  late final math.Random _random = widget.random ?? math.Random();
  // Factors from 3 to 9: the answer always has two digits.
  late final int _a = 3 + _random.nextInt(7);
  late final int _b = 3 + _random.nextInt(7);
  String _typed = '';

  String get _answer => '${_a * _b}';

  void _type(int digit) {
    if (_typed.length >= _answer.length) return;
    setState(() => _typed += '$digit');
    if (_typed.length == _answer.length) {
      final right = _typed == _answer;
      // A short pause so the last digit is seen before the gate closes.
      Future<void>.delayed(const Duration(milliseconds: 250), () {
        if (mounted) Navigator.of(context).pop(right);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    return LayoutBuilder(
      builder: (context, box) {
        final scale = box.maxHeight / hubDesignHeight;
        return Center(
          child: SizedBox(
            width: _panel.width * scale,
            height: _panel.height * scale,
            child: FittedBox(
              child: SizedBox.fromSize(size: _panel, child: _body(l10n)),
            ),
          ),
        );
      },
    );
  }

  Widget _body(AppLocalizations l10n) {
    return Stack(
      clipBehavior: Clip.none,
      children: [
        Positioned.fill(
          child: DecoratedBox(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(48),
              border: Border.all(
                color: GameColors.cocoa,
                width: 7,
                strokeAlign: BorderSide.strokeAlignCenter,
              ),
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  const Color(0xFFFFFFFF),
                  darker(GameColors.cream, 0.06),
                ],
              ),
              boxShadow: const [
                BoxShadow(
                  color: Color(0x473E5A2E),
                  offset: Offset(0, 12),
                  blurRadius: 20,
                ),
              ],
            ),
          ),
        ),
        Positioned.fill(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(40, 30, 40, 36),
            child: Column(
              children: [
                Text(
                  l10n.parentsGateTitle,
                  style: TextStyle(
                    fontSize: 26,
                    color: GameColors.cocoa.withValues(alpha: 0.7),
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  l10n.parentsGateQuestion(_a, _b),
                  style: const TextStyle(fontSize: 44),
                ),
                const SizedBox(height: 18),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [for (var i = 0; i < _answer.length; i++) _slot(i)],
                ),
                const Spacer(),
                for (final row in const [
                  [1, 2, 3, 4, 5],
                  [6, 7, 8, 9, 0],
                ])
                  Padding(
                    padding: const EdgeInsets.only(top: 14),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        for (final d in row)
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 8),
                            child: GateKey(
                              label: '$d',
                              size: _keySize,
                              autofocus: d == 1,
                              onPressed: () => _type(d),
                            ),
                          ),
                      ],
                    ),
                  ),
              ],
            ),
          ),
        ),
        // Close: a small drawn cross in the corner.
        Positioned(
          right: -18,
          top: -18,
          child: GateKey(
            label: '×',
            size: 64,
            labelScale: 0.9,
            color: GameColors.peachPink,
            onPressed: () => Navigator.of(context).pop(false),
          ),
        ),
      ],
    );
  }

  Widget _slot(int i) {
    final digit = i < _typed.length ? _typed[i] : '';
    return Container(
      width: 72,
      height: 84,
      margin: const EdgeInsets.symmetric(horizontal: 6),
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: GameColors.cream,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: darker(GameColors.lavender, 0.3),
          width: 4,
          strokeAlign: BorderSide.strokeAlignCenter,
        ),
      ),
      child: Text(digit, style: const TextStyle(fontSize: 52, height: 1)),
    );
  }
}

/// A round drawn key of the gate, focusable with the TV remote: the focused
/// key gets a butter-yellow halo and grows a little (D-025).
class GateKey extends StatefulWidget {
  const GateKey({
    required this.label,
    required this.onPressed,
    this.size = 96,
    this.color = GameColors.lavender,
    this.autofocus = false,
    this.labelScale = 0.5,
    super.key,
  });

  /// Label size, as a fraction of the key size.
  final double labelScale;

  final String label;
  final VoidCallback onPressed;
  final double size;
  final Color color;
  final bool autofocus;

  @override
  State<GateKey> createState() => _GateKeyState();
}

class _GateKeyState extends State<GateKey> {
  bool _focused = false;

  @override
  Widget build(BuildContext context) {
    final s = widget.size;
    return FocusableActionDetector(
      autofocus: widget.autofocus,
      onShowFocusHighlight: (v) => setState(() => _focused = v),
      actions: {
        ActivateIntent: CallbackAction<ActivateIntent>(
          onInvoke: (_) {
            widget.onPressed();
            return null;
          },
        ),
      },
      child: AnimatedScale(
        scale: _focused ? 1.1 : 1,
        duration: const Duration(milliseconds: 150),
        child: BouncyTap(
          onTap: widget.onPressed,
          child: Container(
            width: s,
            height: s,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(
                color: GameColors.cocoa,
                width: s * 0.06,
                strokeAlign: BorderSide.strokeAlignCenter,
              ),
              gradient: RadialGradient(
                center: const Alignment(-0.35, -0.4),
                radius: 0.9,
                colors: [
                  lighter(widget.color, 0.55),
                  widget.color,
                  darker(widget.color, 0.15),
                ],
                stops: const [0, 0.6, 1],
              ),
              boxShadow: [
                if (_focused)
                  const BoxShadow(
                    color: GameColors.butterYellow,
                    spreadRadius: 9,
                  ),
                const BoxShadow(
                  color: Color(0x403E5A2E),
                  offset: Offset(0, 6),
                  blurRadius: 8,
                ),
              ],
            ),
            child: Text(
              widget.label,
              style: TextStyle(fontSize: s * widget.labelScale, height: 1),
            ),
          ),
        ),
      ),
    );
  }
}
