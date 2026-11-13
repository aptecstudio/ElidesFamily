import 'package:flutter/gestures.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/widgets.dart';

import '../app/game_route.dart';
import '../characters/character_controller.dart';
import '../characters/character_view.dart';
import '../core/bouncy_tap.dart';
import '../l10n/app_localizations.dart';
import 'game_card.dart';
import 'hub_background.dart';
import 'hub_games.dart';

/// Main scene (hub), where the child picks a minigame (D-047..D-049).
///
/// A sky-and-meadow scene with Elide on the left, who waves when the hub
/// opens, reacts to touches and cheers when a game is chosen; the games are
/// postcards in two rows that scroll sideways; a small gear in the top-right
/// corner is the parents' entrance (D-048).
///
/// Everything is laid out in design units: the scene is [hubDesignHeight]
/// units high and as wide as the screen's aspect ratio allows, then scaled
/// to the screen.
class HubScene extends StatefulWidget {
  const HubScene({super.key});

  @override
  State<HubScene> createState() => _HubSceneState();
}

class _HubSceneState extends State<HubScene>
    with SingleTickerProviderStateMixin {
  // Layout of the approved draft (tools/menu-drafts/hub_menu.py).
  static const _rowTop = 104.0;
  static const _rowGap = 40.0;
  static const _columnGap = 40.0;
  static const _gridLeft = 450.0;
  static const _elide = Rect.fromLTWH(29, 161, 392, 529);
  static const _gearCenter = Offset(-64, 56); // from the top-right corner
  static const _gearBox = 160.0;

  final _elideController = CharacterController();
  final _time = ValueNotifier<double>(0);
  late final Ticker _ticker = createTicker(
    (elapsed) => _time.value = elapsed.inMicroseconds / 1e6,
  )..start();
  bool _opening = false;

  @override
  void dispose() {
    _ticker.dispose();
    _time.dispose();
    _elideController.dispose();
    super.dispose();
  }

  Future<void> _openGame(HubGame game) async {
    if (_opening) return;
    _opening = true;
    // TODO(phase-3): the voice reads the game name.
    await _elideController.play(CharacterAction.cheer);
    if (!mounted) return;
    await Navigator.of(context).push(GameRoute<void>(builder: game.builder));
    _opening = false;
    if (mounted) _elideController.play(CharacterAction.wave);
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    return LayoutBuilder(
      builder: (context, box) {
        final scale = box.maxHeight / hubDesignHeight;
        final width = box.maxWidth / scale;
        return FittedBox(
          fit: BoxFit.fill,
          child: SizedBox(
            width: width,
            height: hubDesignHeight,
            child: Stack(
              children: [
                Positioned.fill(
                  child: CustomPaint(
                    painter: HubBackgroundPainter(time: _time),
                  ),
                ),
                Positioned.fill(child: _grid(l10n)),
                // Elide on the hill, over the cards that scroll behind her.
                Positioned.fromRect(
                  rect: _elide,
                  child: CharacterView(
                    character: 'elide',
                    controller: _elideController,
                    onReady: () => _elideController.play(CharacterAction.wave),
                  ),
                ),
                Positioned(
                  left: width + _gearCenter.dx - _gearBox / 2,
                  top: _gearCenter.dy - _gearBox / 2,
                  width: _gearBox,
                  height: _gearBox,
                  child: Center(
                    child: BouncyTap(
                      // TODO(phase-8): open the parental gate (D-048).
                      onTap: () {},
                      child: const SizedBox.square(
                        dimension: 96,
                        child: OverflowBox(
                          maxWidth: _gearBox,
                          maxHeight: _gearBox,
                          child: Image(
                            image: AssetImage('assets/images/hub/hub_gear.png'),
                            width: _gearBox,
                            height: _gearBox,
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _grid(AppLocalizations l10n) {
    final columns = <Widget>[];
    for (var i = 0; i < hubGames.length; i += 2) {
      columns.add(
        Padding(
          padding: const EdgeInsets.only(right: _columnGap),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              for (final game in hubGames.skip(i).take(2))
                Padding(
                  padding: const EdgeInsets.only(bottom: _rowGap),
                  child: GameCard(
                    color: game.color,
                    icon: game.icon,
                    name: game.name(l10n),
                    onTap: () => _openGame(game),
                  ),
                ),
            ],
          ),
        ),
      );
    }
    return ScrollConfiguration(
      // Also scroll with a mouse drag (desktop and emulator).
      behavior: const ScrollBehavior().copyWith(
        dragDevices: PointerDeviceKind.values.toSet(),
        scrollbars: false,
      ),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        physics: const BouncingScrollPhysics(),
        clipBehavior: Clip.none,
        padding: const EdgeInsets.only(
          left: _gridLeft,
          top: _rowTop,
          right: 40,
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: columns,
        ),
      ),
    );
  }
}
