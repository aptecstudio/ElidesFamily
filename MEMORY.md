# MEMORY.md — Project memory

> Log of the **choices** (with their reasons), the graphic and sound **style traits**, the **code structure** and the **conventions**.
> Superseded decisions are not deleted: they are marked with ~~strikethrough~~ and point to the new one.

Last update: 2026-11-13

---

## 1. Decisions

| ID | Date | Decision | Reason | Status |
|----|------|----------|--------|--------|
| D-001 | 2026-11-11 | Framework **Flutter**, target **Android (APK)**. | Requested by the owner; a single codebase, great graphics performance, hot reload for live testing. | ✅ active |
| D-002 | 2026-11-11 | Live testing through `flutter run` on a physical Android device (USB or wireless debugging) with **hot reload**. | The game has to be tried by touching it, on the device the child will use. | ✅ active |
| D-003 | 2026-11-11 | **GPL-3.0** license. | Requested by the owner; public repository. | ✅ active |
| D-004 | 2026-11-11 | A single branch: **`main`**. | Hobby project, simple workflow. | ✅ active |
| D-005 | 2026-11-11 | Structure: **central hub + independent minigames**. | Each minigame is developed and tested on its own; more can be added over time without touching the others. | ✅ active |
| D-006 | 2026-11-11 | **Non-app-like** interface: no visible Material widgets (AppBar, Card, ListTile, standard buttons). | The experience must be that of an illustrated game, not of an application. | ✅ active |
| ~~D-007~~ | 2026-11-11 | ~~Characters animated with **Rive** (state machine: idle, happy, encourage, talk). Refined by D-031.~~ Superseded by D-039. | Vector-based and lightweight, multiple states driven by code, suited to touch reactions. | ❌ superseded |
| D-008 | 2026-11-11 | Engine: **Flutter** for hub, navigation and parents' area; **Flame** for the minigames. | Flutter is ideal for scenes and transitions, Flame for game loop, movement and dragging. | ✅ active |
| D-009 | 2026-11-11 | **Landscape only**, immersive full screen. | More room for the scenes, typical of games for children. | ✅ active |
| D-010 | 2026-11-11 | First minigame (prototype): **Colors**. | The owner's choice. | ✅ active |
| D-011 | 2026-11-11 | Colors minigame with **two levels**: 1) sort the objects by dragging them into the basket of the right color; 2) paint a drawing by tapping a color and then an area. | The owner's choice: it covers color recognition and fine motor skills. | ✅ active |
| D-012 | 2026-11-11 | Voice instructions with a **synthesized voice (TTS)**. | The owner's choice: faster to produce and to translate. | ✅ active |
| D-013 | 2026-11-11 | Languages: **Italian and English**, with a localization system from the start. | The owner's choice; in-game texts and lines are never hard-coded. | ✅ active |
| D-014 | 2026-11-11 | Android application ID: **`com.aptecstudio.elidesfamily`**. | The owner's choice. | ✅ active |
| D-015 | 2026-11-11 | TTS voice **pre-generated** as audio files bundled in the app (`assets/audio/voice/<language>/`). | Same voice on every phone, controlled quality, always offline. | ✅ active |
| D-016 | 2026-11-11 | **Vivid pastel** palette (see §3). | Warm, saturated but soft tones, suited to the age. | ✅ active |
| D-017 | 2026-11-11 | **Fredoka** font (SIL OFL 1.1 license), bundled in the assets. | Round and playful; compatible license; bundled so it works offline. | ✅ active |
| D-018 | 2026-11-11 | AGENTS.md updated (with the owner's authorization): questions are **always asked through interactive polls**. | Requested by the owner. | ✅ active |
| D-019 | 2026-11-11 | App root with **`WidgetsApp`** (not `MaterialApp`), `uses-material-design: false`. | No "app-like" look (D-006): themes, transitions and controls are all ours. | ✅ active |
| D-020 | 2026-11-11 | Every tappable element goes through the shared **`BouncyTap`** widget (`lib/core/`). | The same touch feedback everywhere (squash + bounce, then sound). | ✅ active |
| D-021 | 2026-11-11 | Interface icons are **drawn** (CustomPainter or assets), never written. | 3-year-olds cannot read. | ✅ active |
| D-022 | 2026-11-11 | Localization with **`flutter gen-l10n`**: ARB files in `lib/l10n/` ~~(`app_it.arb` is the template)~~ (template changed by D-042); generated files are not versioned. | Italian + English (D-013) with no hard-coded texts. | ✅ active |
| D-023 | 2026-11-11 | The `android/` folder is generated with `flutter create` **on the owner's PC**, then adapted. | The AI development environment has no Flutter SDK: generating it with the official tool avoids wrong Gradle/AGP versions. | ✅ active |
| D-024 | 2026-11-11 | Supported devices: **smartphones, tablets and Android TV**, with **a single APK**. | Requested by the owner. A single APK makes build and distribution simpler; the game adapts to screen and input type. | ✅ active |
| D-025 | 2026-11-11 | On Android TV the minigames are **adapted to the remote control**, not just "ported": **select and move** mode (arrows to choose the object, OK to pick it up, arrows to carry it, OK to drop it). | Requested by the owner: the remote is a different input and every game must feel natural with it too. | ✅ active |
| D-026 | 2026-11-11 | AGENTS.md, principle 1, updated with the owner's authorization: it includes the remote control on Android TV. | Consistency with D-024 and D-025. | ✅ active |
| ~~D-027~~ | 2026-11-11 | ~~Project skill `kids-character-gen` to generate the characters.~~ **Cancelled** on 2026-11-11: the skill was removed; the graphics for children will be produced another way. | Requested by the owner. | ❌ superseded |
| D-028 | 2026-11-11 | No character has a fixed "subject": the educational topics are **mixed**. In minigames with **a single character** it is always **Elide**; in those with more characters the others **take turns** next to her. **Elide is always the protagonist.** | Requested by the owner. | ✅ active |
| ~~D-029~~ | 2026-11-11 | ~~Character design (drafts 1-4) not approved, to be resumed later.~~ Superseded by D-030. | Requested by the owner. | ❌ superseded |
| D-030 | 2026-11-12 | New art direction for the characters derived from the reference video: outlines colored in tone, head half of the height, round eyes set wide apart, large light muzzle, chubby limbs, hands with a thumb and feet with toes. Rules in `docs/characters/README.md`. **Elide** (draft, light blue eyes, red bow, turquoise dress) and her 6 poses are **provisionally approved** and to be refined later. | Requested by the owner: the drafts are the working base and remain the reference. | ✅ active |
| ~~D-031~~ | 2026-11-12 | ~~Animated character pipeline: **final layered illustration → Rive with bones and deformable meshes** (vertex weights), state machine for poses and expressions, `rive` runtime in Flutter. Spine discarded.~~ Superseded by D-039. | Requested by the owner: smooth animations, without it being visible that the body is made of pieces. The Rive runtime is MIT, compatible with GPL-3.0; Spine's has a proprietary license. | ❌ superseded |
| D-032 | 2026-11-12 | Character drafts are generated with Python scripts → SVG → PNG (`tools/character-drafts/`), so all poses share the same construction. | Guaranteed consistency between poses and characters; easy to retouch. | ✅ active |
| D-033 | 2026-11-12 | **Complete animation suite**, the same for every character: idle, walking, running, jumps, dances, happiness, gentle disapproval, thinking and surprise, interaction, routines, viseme lip sync. Separate combinable layers (body, face, eyes, mouth). List in `docs/characters/README.md`. | Requested by the owner: the suite must be complete. Separate layers allow combining movement, expression and speech. | ✅ active |
| D-034 | 2026-11-12 | **Rio** (draft) and his 6 poses **provisionally approved**: honey French bulldog standing on two legs, right ear bat-like and left ear soft (his trademark), white blaze from forehead to muzzle and white chest, hazel eyes without eyelashes, sky-blue overalls with a butter-yellow striped T-shirt. Sheet in `docs/characters/rio/`. | The owner's choices through polls. Same construction as Elide (D-032) for consistency. | ✅ active |
| D-035 | 2026-11-12 | A character's **right and left** are always meant **from their own point of view**, not the viewer's. Elide's sheet was fixed accordingly (bow on her right ear). | Requested by the owner. | ✅ active |
| D-036 | 2026-11-12 | **Dad** (Papà, draft) and his 6 poses **provisionally approved**: white Labrador, not tall and a bit chubby, soft slightly raised ears, dark brown eyes without eyelashes, no accessories; plain meadow-green hoodie with hood, drawstrings and kangaroo pocket, jeans with a rolled-up hem. Sheet in `docs/characters/dad/`. The adults have the same head as the kids and a taller scene (580 instead of 540). | The owner's choices through polls (a first version with a sweater, taller and slimmer, was discarded). | ✅ active |
| D-037 | 2026-11-12 | **Mom** (Mamma, draft) and her 6 poses **provisionally approved**: honey cat with white muzzle, chest and paws, head built like Elide's (pointed ears, eyelashes, pink nose), green eyes, dark-lavender **round glasses**, knee-length lavender dress with short sleeves, belt and little bow; same build as Dad. Sheet in `docs/characters/mom/`. | The owner's choices through polls (a headband and then a bun were tried and discarded). | ✅ active |
| D-038 | 2026-11-12 | In scenes the **kids** (Elide, Rio) are drawn at **85%** of the adults. Group sheet in `docs/characters/group.png` (`tools/character-drafts/group.py`). | With the same head for everyone, at full scale the parents looked barely taller than the kids; the owner's choice. | ✅ active |
| D-039 | 2026-11-12 | Characters are **animated by code** in Flutter/Flame, starting from **layered SVG parts** (format of the parts refined by D-050) (head, eyes, mouths, arms, legs, clothes) produced by the draft scripts. No Rive rig: the `rive` dependency was removed. Arms and legs stay smooth curves (Bezier "limbs") recomputed every frame, so they bend without visible joints. | The owner's choice: the Rive rig can only be done by hand in the Rive editor, while code animation can be done entirely within the project. Drawing the limbs as curves keeps the goal of D-031 (no visible joints). | ✅ active |
| D-040 | 2026-11-12 | AGENTS.md updated on the owner's request: all **source code and documentation in English**, **chat with the owner in Italian**; **commits in English**; every language follows **its own standard conventions** (Dart: Effective Dart + `dart format` + `flutter_lints`; Python: PEP 8 checked with `ruff`, config in `ruff.toml`). Existing docs, comments and file names were translated. | Requested by the owner. | ✅ active |
| D-041 | 2026-11-12 | Shared draft parts in `tools/character-drafts/parts.py`: `limb()`, `arm()` with a **sleeve that follows the arm** (puffy sleeve along the arm curve, cuff perpendicular to the arm, soft shadow where the arm comes out), `paw()` with an **automatic thumb side** (back of the hand at rest with the thumb towards the body; palm shown with the thumb outwards), and `render()` SVG → PNG through librsvg (PyGObject), so `rsvg-convert` is no longer required. | Optimization of the drafts requested by the owner: the resting hands looked inside out and the arm looked like a tube attached under a fixed sleeve. | ✅ active |
| D-042 | 2026-11-12 | The ARB template is now **`app_en.arb`** (it holds the `@` descriptions); `app_it.arb` only holds the Italian translations. | Consequence of D-040: descriptions are documentation and must be in English. | ✅ active |
| D-043 | 2026-11-12 | File and folder names in English: `dad`/`mom` (Papà/Mamma), `*_model.png`, `*_poses.png`, `group.png`, pose ids `idle`, `wave`, `cheer`, `curious`, `surprised`, `proud`. In English documentation Papà and Mamma are called **Dad** and **Mom**. | Consequence of D-040. | ✅ active |
| D-044 | 2026-11-12 | Development toolchain on the owner's PC: **Flutter stable via snap** (3.50, Dart 3.14), **Temurin JDK 17** and the **Android SDK** command-line tools (platform 36, build-tools 36.0.0, platform-tools), installed in the user's home and linked with `flutter config`. ~~No emulators for now; tests run on the owner's physical phone.~~ (emulators added by D-045) `pubspec.lock` is versioned. Supersedes the "no SDK" limitation of D-023: `android/` can now be generated directly. | Requested by the owner. Limited free disk space, so only what is needed for Android builds was installed. `pubspec.lock` keeps builds reproducible for an app. | ✅ active |
| D-045 | 2026-11-13 | Work moved to a new PC with more disk space (project on an NTFS partition, SDKs in the home on ext4; git needs a `safe.directory` exception). **Android emulators** added with KVM: `ef_phone` (Pixel 8), `ef_tablet` (Pixel Tablet), both on `android-36;google_apis;x86_64`, and `ef_tv` (TV 1080p, `android-36;android-tv;x86_64`), with a hardware keyboard enabled to simulate the remote. JDK in `~/jdk/jdk-17.0.21+9`. The physical phone remains the reference for the final touch test. | Requested by the owner: test without being physically connected to the phone. Covers the three device types of D-024. | ✅ active |
| D-046 | 2026-11-13 | **Design of the four characters approved** (Elide, Rio, Dad, Mom) in the optimized drafts (new hands, sleeves that follow the arm, D-041). The sheets in `docs/characters/` are now the final reference for the layered SVG parts to animate by code (D-039). Supersedes the "provisionally approved" status of D-030, D-034, D-036 and D-037. | The owner's choice through a poll. | ✅ active |
| D-047 | 2026-11-13 | **Main menu (hub)**: sky-and-meadow scene (far hill, meadow, bushes, flowers, drifting clouds, sun with a glow); **Elide on the left** who breathes, blinks and **reacts** to touches (waves, laughs) and cheers when a game is chosen; the games are **straight rounded postcards in two rows** that **scroll sideways**, filled column by column; each card has a pastel frame, a cream drawing area and the game **name on a cream badge** across the bottom edge (small Fredoka text, read aloud by the voice on touch). Draft: `docs/menu/hub_menu.png` (`tools/menu-drafts/hub_menu.py`). | The owner's choices through polls; the first drafts (tilted cards in one row, then a flat look) were discarded. | ✅ active |
| D-048 | 2026-11-13 | **Parents' entrance**: a small, low-contrast **drawn gear** in the top-right corner, leading to the parental gate. | The owner's choice: easy for adults to find, not attractive for the child. | ✅ active |
| D-049 | 2026-11-13 | **Graphics with volume**, not flat: soft gradients, glossy highlights, drop shadows, cards with a darker "cushion" edge, and a **"puffy" lighting filter** (specular light from the top left) on drawn icons, in the same style as the characters. | The owner rejected a flat version of the menu as "too flat". | ✅ active |
| D-050 | 2026-11-13 | **Character rig pipeline**: `tools/character-drafts/export_rig.py <name>` exports, from the same draft code, (1) the parts with soft shading (head, dress, collar, tail, feet, hands, brows, mouths, eye lids) as cropped **PNG layers at 3x** in `assets/images/characters/<name>/`, (2) the **vector data** of what moves every frame (arms with sleeves, legs, irises, shadow, sparkles) and (3) the **poses** (`POSE_DATA`) in `assets/animations/char_<name>_rig.json`. In Flutter, `lib/characters/` draws it: `CharacterRig` (loading), `CharacterRenderer`/`CharacterPainter` (drawing, also usable from Flame), `CharacterFrame` (blendable state), `CharacterController` (pose blending, breathing, blinking, gaze, tail, actions wave/cheer/giggle/surprise) and `CharacterView` (widget that reacts to touch). The draft scripts keep their poses as data (`POSE_DATA`) so sheets and game never diverge; refactors are checked by comparing the generated SVGs byte by byte. New pieces not on the sheets (blink "closed" eyes, "giggle" pose) are built from approved shapes. | Flutter's SVG support does not render blur filters, which the drafts use for their soft shading: PNG layers keep the approved look exactly, while code-drawn limbs still bend without visible joints (goal of D-039). | ✅ active |
| D-051 | 2026-11-13 | **Hands, feet and arms fixed** after the owner's review: (1) the thumb side follows the hand's **handedness** (`thumb_mirror()` in `parts.py`, `thumbMirror()` in Dart): with the palm side shown and the fingers up the thumb points towards the body (the old rule "palm → thumb outwards" was wrong); (2) hands and feet are **merged with the limbs**: all outlines are drawn first (stroke twice as wide) and the fills on top, so only the outer silhouette is outlined; hands and feet are exported in `_outline` and `_fill` layers; (3) arms always **visible**: Elide's cheer, curious, surprised and proud arms were redrawn, and an arm can `fold` (the forearm is drawn again in front of the upper arm and the sleeve, outlining only its sides). Sheets of all four characters regenerated. | Requested by the owner: wrong thumbs, hidden limbs, a visible line between paws and limbs. | ✅ active |

### Rules for the minigames on Android TV (D-025)

- Every minigame has a **remote-control variant** designed together with the touch one: mechanics, distances and pace can be simplified.
- The selected element is always obvious (colored halo and a small bounce) and comes with a sound.
- "Picked up" objects follow the arrows with soft steps between predefined positions, not pixel by pixel.
- No action requires keys other than arrows, OK and Back.

### Open decisions

- *(none)*

---

## 2. Game concept

- **Name**: Elide's Family.
- **Audience**: children aged 3 and up.
- **Format**: a collection of minigames that help growth and learning (colors, shapes, numbers, animals, sounds, daily routines, fine motor skills…).
- **Style reference** (internal, not to be mentioned in the README): gameplay and graphics in the style of *Baby Games: Lucas & Friends* — soft, rounded animal characters, colorful scenes, immediate feedback. Only the **style** is taken as inspiration; all assets are original.

### Characters

| Character | Who they are | Look |
|-----------|--------------|------|
| **Elide** | The protagonist, the little one in the family | Little **white** kitten |
| **Rio** | The four-legged friend | **Honey**-colored **French bulldog** |
| **Dad** (Papà) | The dad | **White Labrador** |
| **Mom** (Mamma) | The mom | **Honey**-colored cat with **white patches** |

- Not every character appears in every minigame: they are chosen according to the context.
- **Elide is always there**: she is the only one in single-character minigames; in the others Rio, Dad and Mom join her in turn (D-028).
- No character is tied to a specific educational topic (D-028).
- Art direction and sheets: `docs/characters/` (D-030). States of every character: idle, hi, hooray, curious, surprised, well done.
- "Baby" proportions: big head, small round body, big shiny eyes, soft outlines, no sharp corners.
- Every character has a minimum set of animated states: **idle** (breathing/blinking), **happy/celebrate**, **encourage**, **talk**.

---

## 3. Graphic and sound style

- **Colors**: vivid but soft palette (saturated pastel tints), bright illustrated backgrounds.
- **Shapes**: everything rounded; large, well-spaced interactive elements (minimum touch area ~64 dp).
- **Typography**: almost absent (3-year-olds cannot read); where needed, a large round font.
- **Feedback**: every touch produces an animation (bounce, squash, sparkles) and a sound.
- **Success**: celebration with confetti/stars, a jumping character, a cheerful sound.
- **Mistake**: never punishing — the object softly goes back to its place, the character encourages.
- **Audio**: light background music at low volume, short and gentle effects, clear voices.

### "Vivid pastel" palette (D-016)

| Name | Hex | Main use |
|------|-----|----------|
| `skyBlue` | `#8FD3F4` | sky, open backgrounds |
| `butterYellow` | `#FFE08A` | light, stars, highlights |
| `meadowGreen` | `#9BDB7C` | meadows, confirmations |
| `peachPink` | `#FFB5A7` | warm details, cheeks |
| `lavender` | `#C7B8F5` | magical elements, hub area |
| `honey` | `#E8B060` | Rio and Mom, wood |
| `cream` | `#FFF6E5` | indoor backgrounds, Elide and Dad (warm white) |
| `cocoa` | `#5A3E36` | soft outlines and text (instead of black) |

- No pure black: outlines use `cocoa`.
- The Colors minigame uses **pure, clearly distinct** colors (red, yellow, blue, green, orange, purple), defined separately inside the minigame.

### Font (D-017)

- **Fredoka** (SIL OFL 1.1), variable font in `assets/fonts/fredoka_variable.ttf` with `OFL.txt`; default text style in `elides_family_app.dart` (weight 600 via `fontWeight` and `FontVariation.weight`).

*(The sound effect set will be recorded here once decided.)*

---

## 4. Code structure (planned)

```
lib/
├── main.dart                     # startup: landscape only, immersive full screen
├── app/
│   ├── elides_family_app.dart    # WidgetsApp, localizations, text style
│   ├── game_colors.dart          # palette (D-016)
│   └── game_route.dart           # transition between scenes
├── core/
│   └── bouncy_tap.dart           # shared touch feedback (D-020)
├── characters/                   # rig loading, renderer, controller, CharacterView (D-039, D-050)
├── hub/
│   └── hub_scene.dart            # main scene (temporary)
├── parental_gate/                # protected adults' area
├── l10n/                         # app_en.arb (template), app_it.arb (+ generated files, not versioned)
└── minigames/
    └── colors/
        └── colors_game_scene.dart  # placeholder of the Colors minigame
assets/
├── images/
│   └── characters/<name>/        # rig PNG layers (D-050)
├── animations/                   # char_<name>_rig.json (D-050)
├── audio/
│   ├── music/
│   ├── sfx/
│   └── voice/{it,en}/            # pre-generated TTS voices (D-015)
└── fonts/                        # Fredoka (D-017)
test/
└── widget_test.dart
tools/
├── character-drafts/             # Python draft scripts (D-032): parts.py, elide.py, rio.py, dad.py, mom.py, group.py, export_rig.py
└── menu-drafts/                  # menu design drafts (hub_menu.py, D-047)
docs/
├── characters/                   # art direction, sheets and draft images
└── menu/                         # menu design sheets (hub_menu.png)
```

Empty folders contain a `.gitkeep`, to be removed when they get their first file.

---

## 5. Conventions

- **Language**: identifiers, comments, documentation and commits in English; chat with the owner in Italian (D-040).
- **Dart**: Effective Dart style (`dart format`), `flutter_lints` rules plus those in `analysis_options.yaml`.
- **Python**: PEP 8, formatted and checked with `ruff` (`ruff format`, `ruff check`; config in `ruff.toml`).
- **Naming**: Dart files `snake_case.dart`, classes `PascalCase`, variables/methods `camelCase`, constants `lowerCamelCase`; Python modules, functions and variables `snake_case`, constants `UPPER_CASE`.
- **Assets**: `snake_case`, with a category prefix (e.g. `char_elide_idle.svg`, `sfx_pop.ogg`, `bg_kitchen.png`).
- **Minigames**: folder `lib/minigames/<name>/`; Flutter entry scene `<Name>GameScene`, Flame game `<Name>Game`.
- **Texts and voices**: ARB keys in `camelCase` (e.g. `gameColorsName`); the matching voice file is named `voice_<key_in_snake_case>` in the language folder (e.g. `assets/audio/voice/it/voice_game_colors_name.ogg`).
- **Colors**: only from the `GameColors` constants, never scattered hex values (exception: the colors "to learn" defined inside the Colors minigame).
- **Commits**: conventional prefix, in English (see `AGENTS.md`).

---

## 6. Third-party assets

| Asset | Source | License | Notes |
|-------|--------|---------|-------|
| Fredoka (variable font, `wdth` 75–125, `wght` 300–700) → `assets/fonts/fredoka_variable.ttf` | Google Fonts repository (`google/fonts`, `ofl/fredoka`), by Milena Brandão / Hafontia | SIL OFL 1.1 (`assets/fonts/OFL.txt`) | Copyright 2016 The Fredoka Project Authors. Added 2026-11-13. Being a variable font, the weight is also set with `FontVariation.weight`. |
