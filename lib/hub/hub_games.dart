import 'package:flutter/widgets.dart';

import '../app/game_colors.dart';
import '../l10n/app_localizations.dart';
import '../minigames/colors/colors_game_scene.dart';

/// A minigame shown on the hub as a card.
class HubGame {
  const HubGame({
    required this.id,
    required this.color,
    required this.name,
    required this.builder,
  });

  /// Short name, also used for the icon: `assets/images/hub/hub_icon_<id>.png`.
  final String id;

  /// Frame color of the card.
  final Color color;
  final String Function(AppLocalizations l10n) name;
  final WidgetBuilder builder;

  String get icon => 'assets/images/hub/hub_icon_$id.png';
}

/// The games on the hub, in order: the grid is filled column by column.
final hubGames = <HubGame>[
  HubGame(
    id: 'colors',
    color: GameColors.peachPink,
    name: (l10n) => l10n.gameColorsName,
    builder: (_) => const ColorsGameScene(),
  ),
];
