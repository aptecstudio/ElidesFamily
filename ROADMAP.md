# ROADMAP.md — Project status

> Legend: `- [x]` done · `- [~]` in progress · `- [ ]` to do
> Phases give the **global status**, tasks the **partial status**.

Last update: 2026-11-13

---

## Global status

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Repository foundations and documentation | 🟢 completed |
| 1 | Technical and design decisions | 🟢 completed |
| 2 | Flutter project setup and live testing | 🟡 in progress |
| 3 | Shared engine (audio, animations, navigation) | ⚪ not started |
| 4 | Characters | 🟡 in progress |
| 5 | Main hub | ⚪ not started |
| 6 | First minigame (vertical prototype) | ⚪ not started |
| 7 | More minigames | ⚪ not started |
| 8 | Parents' area and settings | ⚪ not started |
| 9 | Polish, testing with the child, accessibility | ⚪ not started |
| 10 | APK build and release | ⚪ not started |
| ↔ | Cross-cutting: smartphone, tablet and Android TV | ⚪ not started |

**Next step (next session):** on the new PC, finish the first debug build, install it on the emulators and on the owner's phone and check the landscape start, then `flutter run` with hot reload (Phase 2); design approval of the updated drafts (Phase 4); menu graphics (Phase 5).

**Previous step:** Android platform generated and configured (app ID, landscape, Android TV manifest and banner); the first build stopped because the disk was full.

---

## Phase 0 — Repository foundations ✅

- [x] Repository created on GitHub (`aptecstudio/ElidesFamily`), branch `main`
- [x] `AGENTS.md` with the working rules
- [x] `MEMORY.md` with concept, characters, style and initial conventions
- [x] `ROADMAP.md` (this file)
- [x] Public `README.md`
- [x] GPL-3.0 `LICENSE`

## Phase 1 — Technical and design decisions ✅

- [x] Engine: Flutter + Flame (D-008)
- [x] ~~Character animation technique: Rive (D-007)~~ → animation by code (D-039)
- [x] Screen orientation: landscape only (D-009)
- [x] First minigame: Colors (D-010)
- [x] Colors minigame mechanics: sort + paint (D-011)
- [x] Voice: TTS synthesis (D-012)
- [x] Languages: Italian and English (D-013)
- [x] Android application ID: `com.aptecstudio.elidesfamily` (D-014)
- [x] TTS mode: pre-generated audio files (D-015)
- [x] Vivid pastel palette (D-016) and Fredoka font (D-017)

## Phase 2 — Flutter setup and live testing

**Prepared without the SDK (2026-11-11):**

- [x] `pubspec.yaml` (Flame, flame_audio, shared_preferences, localizations)
- [x] `analysis_options.yaml` with `flutter_lints`
- [x] `l10n.yaml` + `app_en.arb` (template) / `app_it.arb`
- [x] Folder structure as in `MEMORY.md`
- [x] Landscape-only start and immersive full screen (`main.dart`)
- [x] `WidgetsApp`, palette, scene transition, `BouncyTap`
- [x] Temporary hub drawn in code + Colors minigame placeholder
- [x] Startup test (`test/widget_test.dart`)

**To do on the owner's PC (with the Flutter SDK):**

- [x] Generate the Android platform without touching the existing files:
      `flutter create --platforms android --org com.aptecstudio --project-name elides_family .`
- [x] Set `applicationId` and `namespace` to `com.aptecstudio.elidesfamily` (D-014) in `android/app/build.gradle.kts` and move `MainActivity.kt` to the matching package
- [x] `AndroidManifest.xml`: label "Elide's Family", `android:screenOrientation="sensorLandscape"` on the activity
- [ ] Check the `minSdk` required by Flame (Flutter's default is 24)
- [ ] Copy the Fredoka font (SIL OFL) into `assets/fonts/` with the `OFL.txt` file and enable it in `pubspec.yaml` and `elides_family_app.dart`
- [x] Flutter SDK, JDK 17 and Android SDK (platform 36, build-tools 36.0.0) installed on the owner's PC (D-044)
- [x] `flutter pub get` (versions resolved, `pubspec.lock` committed)
- [x] `flutter analyze` and `flutter test` with no errors
- [ ] Live test: `flutter run` on the phone (USB or wireless debugging) + hot reload
- [ ] First test APK build (`flutter build apk --debug`)
- [x] Manifest ready for Android TV: `android.hardware.touchscreen` and `android.software.leanback` with `required="false"`, `LEANBACK_LAUNCHER` intent, temporary TV banner (320×180, `tools/character-drafts/tv_banner.py`)
- [x] Test emulators: smartphone (`ef_phone`), tablet (`ef_tablet`), Android TV 1080p (`ef_tv`) on the new PC (D-045)

## Phase 3 — Shared engine

- [ ] Audio service (music, effects, voices) with volume control
- [ ] Touch feedback widget (bounce + sound)
- [ ] Celebration animation for success
- [ ] Game-style scene transitions
- [ ] Local progress storage (offline)
- [ ] Accidental exit blocking (back button handled)
- [ ] Adaptive layout: scenes that adapt to different aspect ratios and sizes (phone, tablet, TV) without stretching
- [ ] Single input layer: touch/drag **and** remote control (D-pad + OK), so every minigame works with both
- [ ] Visible, "playful" focus for remote navigation (halo/bounce on the selected element)

## Phase 4 — Characters

- [x] Shared art direction for the characters (`docs/characters/README.md`, D-030)
- [x] Draft method: script → SVG → PNG (`tools/character-drafts/`, D-032)
- [x] ~~Animation pipeline: Rive with bones and deformable meshes (D-031)~~ → animation by code from layered SVG parts (D-039)
- [x] Draft of Elide and 6 poses (provisionally approved, to be refined)
- [x] **Rio**: sheet, model, 6 poses and expressions (provisionally approved, D-034)
- [x] **Dad**: sheet, model, 6 poses and expressions (provisionally approved, D-036)
- [x] **Mom**: sheet, model, 6 poses and expressions (provisionally approved, D-037)
- [x] Group sheet: the four characters together, kids at 85% (D-038)
- [~] Final optimization of the drafts
  - [x] Shared parts module `parts.py` with in-project PNG rendering (D-041)
  - [x] New hands: thumb on the right side, readable palm, fist and thumbs up (all four)
  - [x] Sleeves that follow the arm, with no visible joint (all four)
  - [x] Port Rio, Dad and Mom to `parts.py` (hands and sleeves)
  - [x] Regenerate every model, pose sheet and the group sheet
- [ ] Design approval by the owner
- [ ] Final layered illustrations (head, eyes, mouths, limbs, clothes) exported as SVG parts
- [ ] Flutter character renderer: layered parts + Bezier limbs recomputed every frame (D-039)
- [ ] Layered animation controller: body, face, eyes, mouth (D-033)
- [ ] Idle animations: breathing, blinking, looking around, waiting, sitting
- [ ] Movement: walking (front and side), running, turning, entering/leaving, jumps
- [ ] Happiness: smile, hop, hooray, clapping, laughing, thumbs up, hug
- [ ] Dances: at least 3 looping
- [ ] Gentle disapproval: head shake, wagging finger, pout, crossed arms, shoulders down, slightly sad
- [ ] Thinking and surprise: curious, confused, surprised, small funny fright
- [ ] Interaction: wave, beckon, point, take/hand over, reaction to touch
- [ ] Routines: eating, drinking, washing, yawning, sleeping
- [ ] Viseme lip sync for the TTS voices
- [ ] Complete suite for all four characters
- [ ] Reusable widget for every character

## Phase 5 — Main hub

**Choosing the in-game menu graphics** (with polls for the owner):

- [ ] Hub layout: illustrated scene with an animated Elide and the minigame tiles
- [ ] Tile style: frames, illustrations, game name, "new" marker
- [ ] Buttons for adults (parents, languages, settings) and their position
- [ ] Animated loading screen with a character
- [ ] Buttons inside the minigames: back to the games, exit protected by dragging
- [ ] Item bar inside the minigames (tray to drag from)
- [ ] Transitions between menus and minigames
- [ ] Android TV variant with remote focus
- [ ] Menu design sheet approved and saved in `docs/`

- [ ] Illustrated house scene with the characters
- [ ] Access to the minigames through tappable objects/doors
- [ ] Music and ambient animations

## Phase 6 — First minigame (vertical prototype)

- [ ] Choice of the minigame
- [ ] Mechanics, graphics, sounds, final celebration
- [ ] Remote-control variant (Android TV) of both levels of the Colors game
- [ ] On-device test with the child and collection of observations

## Phase 7 — More minigames

*Ideas to evaluate (to be confirmed in Phase 1):*

- [ ] Colors (e.g. painting/sorting objects by color)
- [ ] Shapes (shape sorter)
- [ ] Numbers and counting (counting objects with Rio)
- [ ] Animals and their sounds
- [ ] Daily routines (bath, meal, bedtime with Elide)
- [ ] Simple puzzles
- [ ] Music (instruments to touch)
- [ ] Memory game with the characters

## Phase 8 — Parents' area

- [ ] Parental gate
- [ ] Settings: music/effects volume, language
- [ ] Information, license and credits

## Phase 9 — Polish

- [ ] Testing with the child and iteration
- [ ] Performance on low-end devices
- [ ] Accessibility review (touch areas, contrast, audio)
- [ ] Testing on real smartphones, tablets and Android TV

## Phase 10 — Build and release

- [ ] Final icon and splash
- [ ] Signed release APK
- [ ] GitHub release with the APK attached
- [ ] Adaptive icon (phone/tablet) and final Android TV banner

## ↔ Cross-cutting — Smartphone, tablet and Android TV

A single APK for all three device types (D-024). The operational tasks are spread over phases 2, 3, 9 and 10; here is the summary.

- [x] Decided how to play with the remote: "select and move", games adapted (D-025)
- [ ] Manifest and banner for Android TV (Phase 2)
- [ ] Adaptive layout for phone, tablet and TV (Phase 3)
- [ ] Single touch + remote input with visible focus (Phase 3)
- [ ] Every minigame adapted to the remote with a dedicated variant (Phases 6–7)
- [ ] Interface readable "from the couch" on TV: bigger elements and a safe area at the edges (Phase 5)
- [ ] Testing on real devices (Phase 9)

---

## Session log

| Date | Session | Done |
|------|---------|------|
| 2026-11-11 | Kick-off | Created AGENTS.md, MEMORY.md, ROADMAP.md, README.md, LICENSE |
| 2026-11-11 | Decisions | Chose Rive, Flutter + Flame, landscape orientation, Colors as the first minigame |
| 2026-11-11 | Decisions | Colors on two levels, TTS voice, Italian + English, app ID com.aptecstudio.elidesfamily |
| 2026-11-11 | Decisions | Pre-generated TTS, vivid pastel palette, Fredoka font, polls rule in AGENTS.md. Phase 1 closed |
| 2026-11-11 | Skeleton | Flutter project prepared by hand (without the SDK): structure, startup, temporary hub, localizations, test |
| 2026-11-11 | Devices | Added smartphone, tablet and Android TV support to the roadmap; games adapted to the remote (D-025), AGENTS.md updated |
| 2026-11-11 | Characters | Character drafts 1-4 (on hold); kids-character-gen skill created and then cancelled; Elide always the protagonist, mixed topics |
| 2026-11-12 | Characters | New art direction from the reference video; draft of Elide and 6 poses provisionally approved; Rive pipeline with deformable meshes |
| 2026-11-12 | Animations | Defined the complete animation suite for every character (D-033) |
| 2026-11-12 | Planning | Added the creation of Rio, Dad and Mom and the menu graphics choice to the roadmap; end of session |
| 2026-11-12 | Characters | Created Rio (sheet, model, 6 poses) with `tools/character-drafts/rio.py`; right/left from the character's point of view (D-035) |
| 2026-11-12 | Characters | Created Dad (sheet, model, 6 poses) with `tools/character-drafts/dad.py`: shorter, chubby, hoodie |
| 2026-11-12 | Characters | Created Mom (sheet, model, 6 poses) with `tools/character-drafts/mom.py`; group sheet with the kids at 85% (D-038) |
| 2026-11-12 | Optimization | Animation by code instead of Rive (D-039); shared `parts.py` with new hands and sleeves following the arm, applied to Elide (D-041) |
| 2026-11-12 | Conventions | AGENTS.md: English code and docs, Italian chat, English commits, per-language style (D-040); whole project translated, files renamed (D-043), ARB template in English (D-042), PEP 8 with ruff |
| 2026-11-12 | Optimization | Rio, Dad and Mom ported to `parts.py` (new hands, sleeves following the arm); all models, pose sheets and the group sheet regenerated |
| 2026-11-12 | Setup | Flutter 3.50 (snap), JDK 17 and Android SDK installed on the owner's PC; `pub get`, `analyze` and `test` pass (D-044) |
| 2026-11-12 | Setup | Android platform generated and configured; first debug build stopped with a full disk, to be resumed after freeing space. End of session |
