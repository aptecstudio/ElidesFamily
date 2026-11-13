import 'dart:io';
import 'dart:ui' as ui;

import 'package:elides_family/app/elides_family_app.dart';
import 'package:elides_family/hub/game_card.dart';
import 'package:elides_family/minigames/colors/colors_game_scene.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';

Future<void> _loadFont() async {
  final font = rootBundle.load('assets/fonts/fredoka_variable.ttf');
  await (FontLoader('Fredoka')..addFont(font)).load();
}

/// Lets the rig and the images load (real asynchronous work).
Future<void> _settle(WidgetTester tester) async {
  for (var i = 0; i < 5; i++) {
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 100)),
    );
    await tester.pump(const Duration(milliseconds: 100));
  }
}

void main() {
  // Set CHARACTER_PREVIEW_DIR to save a picture of the hub.
  final previewDir = Platform.environment['CHARACTER_PREVIEW_DIR'];

  // One test for all the screens: the character rigs are cached, and a rig
  // loaded in one test cannot be awaited from the next one.
  testWidgets('a card opens its game after Elide cheers', (tester) async {
    await _loadFont();
    addTearDown(tester.view.reset);
    tester.view.devicePixelRatio = 1;
    // Phone 20:9, tablet 16:10, TV 16:9.
    for (final size in const [
      Size(1600, 720),
      Size(1152, 720),
      Size(1280, 720),
    ]) {
      tester.view.physicalSize = size;
      await tester.pumpWidget(ElidesFamilyApp(key: ValueKey(size)));
      await _settle(tester);
      // Elide's welcome wave.
      await tester.pump(const Duration(seconds: 3));
      await _settle(tester);

      if (previewDir != null) {
        final boundary = tester.renderObject<RenderRepaintBoundary>(
          find.byType(RepaintBoundary).first,
        );
        final image = await tester.runAsync(() => boundary.toImage());
        final png = await tester.runAsync(
          () => image!.toByteData(format: ui.ImageByteFormat.png),
        );
        File(
          '$previewDir/hub_${size.width.round()}.png',
        ).writeAsBytesSync(png!.buffer.asUint8List());
      }

      await tester.tap(find.byType(GameCard).first);
      for (var i = 0; i < 40; i++) {
        await tester.pump(const Duration(milliseconds: 100));
      }
      expect(find.byType(ColorsGameScene), findsOneWidget, reason: '$size');
    }
  });
}
