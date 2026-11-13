import 'dart:io';
import 'dart:ui' as ui;

import 'package:elides_family/characters/character_controller.dart';
import 'package:elides_family/characters/character_frame.dart';
import 'package:elides_family/characters/character_painter.dart';
import 'package:elides_family/characters/character_rig.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';

/// Renders [frame] to an image of the 400×540 scene at 2x.
Future<ui.Image> _render(CharacterRig rig, CharacterFrame frame) {
  final recorder = ui.PictureRecorder();
  final canvas = Canvas(recorder)..scale(2);
  canvas.drawRect(
    const Rect.fromLTWH(0, 0, 400, 540),
    Paint()..color = const Color(0xFFFFF6E5),
  );
  CharacterRenderer(rig).paint(canvas, frame);
  return recorder.endRecording().toImage(800, 1080);
}

/// Number of pixels that differ from the cream background.
Future<int> _inked(ui.Image image) async {
  final data = (await image.toByteData())!;
  var count = 0;
  for (var i = 0; i < data.lengthInBytes; i += 4 * 97) {
    if (data.getUint8(i) != 0xFF || data.getUint8(i + 2) != 0xE5) count++;
  }
  return count;
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  // Set CHARACTER_PREVIEW_DIR to save the rendered poses as PNG files.
  final previewDir = Platform.environment['CHARACTER_PREVIEW_DIR'];

  test('Elide rig loads with all its parts and poses', () async {
    final rig = await CharacterRig.load('elide');
    expect(rig.images.length, rig.parts.length);
    expect(
      rig.poses.keys,
      containsAll(['idle', 'wave', 'cheer', 'curious', 'surprised', 'proud']),
    );
  });

  for (final name in ['elide', 'rio']) {
    test('every pose of $name is drawn', () async {
      final rig = await CharacterRig.load(name);
      for (final pose in rig.poses.keys) {
        final image = await _render(
          rig,
          CharacterFrame.fromPose(rig.poses[pose]!),
        );
        expect(await _inked(image), greaterThan(500), reason: pose);
        if (previewDir != null) {
          final png = await image.toByteData(format: ui.ImageByteFormat.png);
          File(
            '$previewDir/${name}_$pose.png',
          ).writeAsBytesSync(png!.buffer.asUint8List());
        }
      }
    });
  }

  test('actions play and the character goes back to rest', () async {
    final rig = await CharacterRig.load('elide');
    final controller = CharacterController()..attach(rig);
    for (final action in CharacterAction.values) {
      final done = controller.play(action);
      expect(controller.isBusy, isTrue);
      for (var i = 0; i < 200 && controller.isBusy; i++) {
        controller.tick(1 / 60);
        await _render(rig, controller.frame!);
      }
      await done;
      expect(controller.isBusy, isFalse, reason: action.name);
    }
    expect(controller.pose, 'idle');
  });
}
