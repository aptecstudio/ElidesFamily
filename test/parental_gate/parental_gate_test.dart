import 'dart:io';
import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:elides_family/l10n/app_localizations.dart';
import 'package:elides_family/parental_gate/parental_gate.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';

/// Opens the gate from a button and records its result.
class _Host extends StatelessWidget {
  const _Host({required this.seed, required this.result});

  final int seed;
  final ValueNotifier<bool?> result;

  @override
  Widget build(BuildContext context) {
    return WidgetsApp(
      color: const Color(0xFF8FD3F4),
      locale: const Locale('it'),
      debugShowCheckedModeBanner: false,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      textStyle: const TextStyle(
        fontFamily: 'Fredoka',
        color: Color(0xFF5A3E36),
      ),
      pageRouteBuilder: <T>(settings, builder) => PageRouteBuilder<T>(
        settings: settings,
        pageBuilder: (c, _, _) => builder(c),
      ),
      home: Builder(
        builder: (context) => GestureDetector(
          onTap: () async => result.value = await showParentalGate(
            context,
            random: math.Random(seed),
          ),
          child: const ColoredBox(color: Color(0xFF8FD3F4)),
        ),
      ),
    );
  }
}

/// The answer the gate asks for with [seed] (same draws as the gate).
String _answer(int seed) {
  final r = math.Random(seed);
  final a = 3 + r.nextInt(7);
  final b = 3 + r.nextInt(7);
  return '${a * b}';
}

Future<void> _open(
  WidgetTester tester,
  int seed,
  ValueNotifier<bool?> result,
) async {
  tester.view.physicalSize = const Size(1600, 720);
  tester.view.devicePixelRatio = 1;
  await tester.pumpWidget(_Host(seed: seed, result: result));
  await tester.tapAt(const Offset(20, 20));
  await tester.pumpAndSettle();
  expect(find.byType(ParentalGate), findsOneWidget);
}

Future<void> _type(WidgetTester tester, String digits) async {
  for (final d in digits.split('')) {
    await tester.tap(find.widgetWithText(GateKey, d));
    await tester.pump(const Duration(milliseconds: 50));
  }
  // The gate closes a moment after the last digit.
  await tester.pump(const Duration(milliseconds: 300));
  await tester.pumpAndSettle();
}

void main() {
  final previewDir = Platform.environment['CHARACTER_PREVIEW_DIR'];

  testWidgets('the right answer opens the gate', (tester) async {
    // Load the font for real, then let its font-change notice reach a frame,
    // so no frame callback is left pending at the end of the test.
    await tester.runAsync(() async {
      final font = rootBundle.load('assets/fonts/fredoka_variable.ttf');
      await (FontLoader('Fredoka')..addFont(font)).load();
      await Future<void>.delayed(const Duration(milliseconds: 50));
    });
    await tester.pump();
    addTearDown(tester.view.reset);
    final result = ValueNotifier<bool?>(null);
    await _open(tester, 1, result);
    final answer = _answer(1);
    await _type(tester, answer[0]);
    if (previewDir != null) {
      // The whole screen, gate route included.
      final layer = tester.binding.renderViews.first.debugLayer! as OffsetLayer;
      final image = await tester.runAsync(
        () => layer.toImage(const Offset(0, 0) & const Size(1600, 720)),
      );
      final png = await tester.runAsync(
        () => image!.toByteData(format: ui.ImageByteFormat.png),
      );
      File('$previewDir/gate.png').writeAsBytesSync(png!.buffer.asUint8List());
    }
    await _type(tester, answer.substring(1));
    expect(find.byType(ParentalGate), findsNothing);
    expect(result.value, isTrue);
  });

  testWidgets('a wrong answer closes the gate', (tester) async {
    addTearDown(tester.view.reset);
    final result = ValueNotifier<bool?>(null);
    await _open(tester, 2, result);
    final answer = _answer(2);
    final wrong = answer == '11' ? '22' : '11';
    await _type(tester, wrong);
    expect(find.byType(ParentalGate), findsNothing);
    expect(result.value, isFalse);
  });

  testWidgets('the remote can answer with arrows and OK', (tester) async {
    addTearDown(tester.view.reset);
    final result = ValueNotifier<bool?>(null);
    await _open(tester, 3, result);
    // Focus starts on "1"; the keys are 1-5 on top and 6-9, 0 below.
    const order = '1234567890';
    var at = 0;
    for (final d in _answer(3).split('')) {
      final to = order.indexOf(d);
      while (at % 5 < to % 5) {
        await tester.sendKeyEvent(LogicalKeyboardKey.arrowRight);
        at++;
      }
      while (at % 5 > to % 5) {
        await tester.sendKeyEvent(LogicalKeyboardKey.arrowLeft);
        at--;
      }
      if (at < 5 && to >= 5) {
        await tester.sendKeyEvent(LogicalKeyboardKey.arrowDown);
        at += 5;
      } else if (at >= 5 && to < 5) {
        await tester.sendKeyEvent(LogicalKeyboardKey.arrowUp);
        at -= 5;
      }
      await tester.sendKeyEvent(LogicalKeyboardKey.select);
      await tester.pump(const Duration(milliseconds: 50));
    }
    await tester.pump(const Duration(milliseconds: 300));
    await tester.pumpAndSettle();
    expect(result.value, isTrue);
  });
}
