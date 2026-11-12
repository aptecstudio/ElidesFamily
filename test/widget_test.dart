import 'package:elides_family/app/elides_family_app.dart';
import 'package:elides_family/hub/hub_scene.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('the app starts on the hub scene', (tester) async {
    await tester.pumpWidget(const ElidesFamilyApp());
    await tester.pump();

    expect(find.byType(HubScene), findsOneWidget);
  });
}
