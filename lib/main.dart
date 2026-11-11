import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import 'app/elides_family_app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Solo orizzontale (D-009).
  await SystemChrome.setPreferredOrientations(const [
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);

  // Schermo intero immersivo: niente barre di sistema durante il gioco.
  await SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);

  runApp(const ElidesFamilyApp());
}
