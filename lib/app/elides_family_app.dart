import 'package:flutter/widgets.dart';

import '../hub/hub_scene.dart';
import '../l10n/app_localizations.dart';
import 'game_colors.dart';
import 'game_route.dart';

/// Radice dell'app.
///
/// Si usa [WidgetsApp] e non MaterialApp: nessun aspetto "da app" (D-006),
/// ogni schermata è una scena di gioco disegnata da noi.
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
        // Diventerà 'Fredoka' quando il font sarà negli asset (D-017).
        color: GameColors.cocoa,
        fontSize: 28,
        fontWeight: FontWeight.w600,
      ),
      pageRouteBuilder: <T>(RouteSettings settings, WidgetBuilder builder) =>
          GameRoute<T>(settings: settings, builder: builder),
      home: const HubScene(),
    );
  }
}
