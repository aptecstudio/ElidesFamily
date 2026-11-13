import 'package:flutter/widgets.dart';

import '../app/game_colors.dart';
import '../l10n/app_localizations.dart';
import 'parental_gate.dart';

/// The protected adults' area, reached through the parental gate (D-057).
///
/// Phase 8 placeholder: languages, sound and the other settings come later.
class ParentsAreaScene extends StatelessWidget {
  const ParentsAreaScene({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    return ColoredBox(
      color: GameColors.cream,
      child: Stack(
        children: [
          Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  l10n.parentsAreaTitle,
                  style: const TextStyle(fontSize: 44),
                ),
                const SizedBox(height: 16),
                Text(l10n.comingSoon),
              ],
            ),
          ),
          Positioned(
            top: 24,
            left: 24,
            child: GateKey(
              label: '‹',
              size: 88,
              color: GameColors.butterYellow,
              autofocus: true,
              onPressed: () => Navigator.of(context).pop(),
            ),
          ),
        ],
      ),
    );
  }
}
