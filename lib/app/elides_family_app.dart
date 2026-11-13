import 'package:flutter/widgets.dart';

import '../hub/hub_scene.dart';
import '../l10n/app_localizations.dart';
import 'game_colors.dart';
import 'game_route.dart';

/// Root of the app.
///
/// Uses [WidgetsApp] instead of MaterialApp: no "app-like" look (D-006);
/// every screen is a game scene that we draw ourselves.
class ElidesFamilyApp extends StatelessWidget {
  const ElidesFamilyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return WidgetsApp(
      color: GameColors.skyBlue,
      debugShowCheckedModeBanner: false,
      onGenerateTitle: (context) => AppLocalizations.of(context).appTitle,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      textStyle: const TextStyle(
        fontFamily: 'Fredoka',
        color: GameColors.cocoa,
        fontSize: 28,
        fontWeight: FontWeight.w600,
        // Fredoka is a variable font: the weight is set on its axis too.
        fontVariations: [FontVariation.weight(600)],
      ),
      pageRouteBuilder: <T>(RouteSettings settings, WidgetBuilder builder) =>
          GameRoute<T>(settings: settings, builder: builder),
      home: const HubScene(),
    );
  }
}
