# ROADMAP.md — Stato del progetto

> Legenda: `- [x]` fatto · `- [~]` in corso · `- [ ]` da fare
> Le fasi danno lo **stato globale**, i task lo **stato parziale**.

Ultimo aggiornamento: 2026-11-11

---

## Stato globale

| Fase | Descrizione | Stato |
|------|-------------|-------|
| 0 | Fondamenta del repository e documentazione | 🟢 completata |
| 1 | Decisioni tecniche e di design | 🟢 completata |
| 2 | Setup del progetto Flutter e test in tempo reale | 🟡 in corso |
| 3 | Motore comune (audio, animazioni, navigazione) | ⚪ da iniziare |
| 4 | Personaggi | ⚪ da iniziare |
| 5 | Hub principale | ⚪ da iniziare |
| 6 | Primo minigioco (prototipo verticale) | ⚪ da iniziare |
| 7 | Altri minigiochi | ⚪ da iniziare |
| 8 | Area genitori e impostazioni | ⚪ da iniziare |
| 9 | Rifinitura, test con la bambina, accessibilità | ⚪ da iniziare |
| 10 | Build APK e pubblicazione | ⚪ da iniziare |
| ↔ | Trasversale: smartphone, tablet e Android TV | ⚪ da iniziare |

**Prossimo passo:** Fase 2, parte sul PC del responsabile — generare `android/`, primo `flutter run` sul telefono.

---

## Fase 0 — Fondamenta del repository ✅

- [x] Repository creato su GitHub (`aptecstudio/ElidesFamily`), branch `main`
- [x] `AGENTS.md` con le regole di lavoro
- [x] `MEMORY.md` con concept, personaggi, stile e convenzioni iniziali
- [x] `ROADMAP.md` (questo file)
- [x] `README.md` pubblico
- [x] `LICENSE` GPL-3.0

## Fase 1 — Decisioni tecniche e di design ✅

- [x] Motore: Flutter + Flame (D-008)
- [x] Tecnica di animazione dei personaggi: Rive (D-007)
- [x] Orientamento schermo: solo orizzontale (D-009)
- [x] Primo minigioco: Colori (D-010)
- [x] Meccanica del minigioco Colori: ordinare + dipingere (D-011)
- [x] Voce: sintetizzata TTS (D-012)
- [x] Lingue: italiano e inglese (D-013)
- [x] Application ID Android: `com.aptecstudio.elidesfamily` (D-014)
- [x] Modalità TTS: file audio pre-generati (D-015)
- [x] Palette pastello vivace (D-016) e font Fredoka (D-017)

## Fase 2 — Setup Flutter e test in tempo reale

**Preparato senza SDK (2026-11-11):**

- [x] `pubspec.yaml` (Flame, flame_audio, Rive, shared_preferences, localizzazioni)
- [x] `analysis_options.yaml` con `flutter_lints`
- [x] `l10n.yaml` + `app_it.arb` / `app_en.arb`
- [x] Struttura delle cartelle come in `MEMORY.md`
- [x] Avvio solo orizzontale e schermo intero immersivo (`main.dart`)
- [x] `WidgetsApp`, palette, transizione tra scene, `BouncyTap`
- [x] Hub provvisorio disegnato in codice + segnaposto del minigioco Colori
- [x] Test di avvio (`test/widget_test.dart`)

**Da fare sul PC del responsabile (con l'SDK Flutter):**

- [ ] Generare la piattaforma Android senza toccare i file esistenti:
      `flutter create --platforms android --org com.aptecstudio --project-name elides_family .`
- [ ] Impostare `applicationId` e `namespace` a `com.aptecstudio.elidesfamily` (D-014) in `android/app/build.gradle.kts` e spostare `MainActivity.kt` nel package corrispondente
- [ ] `AndroidManifest.xml`: etichetta "Elide's Family", `android:screenOrientation="sensorLandscape"` sull'activity
- [ ] Verificare `minSdk` richiesto da Rive / Flame
- [ ] Copiare il font Fredoka (SIL OFL) in `assets/fonts/` con il file `OFL.txt` e attivarlo in `pubspec.yaml` e in `elides_family_app.dart`
- [ ] `flutter pub get` e correzione di eventuali versioni dei pacchetti
- [ ] `flutter analyze` e `flutter test` senza errori
- [ ] Test in tempo reale: `flutter run` sul telefono (USB o debug wireless) + hot reload
- [ ] Prima build APK di prova (`flutter build apk --debug`)
- [ ] Manifest pronto per Android TV: `android.hardware.touchscreen` e `android.software.leanback` con `required="false"`, intent `LEANBACK_LAUNCHER`, banner TV provvisorio (320×180)
- [ ] Emulatori di prova: smartphone, tablet 10", Android TV 1080p

## Fase 3 — Motore comune

- [ ] Servizio audio (musica, effetti, voci) con controllo volume
- [ ] Widget di feedback al tocco (rimbalzo + suono)
- [ ] Animazione di festa per il successo
- [ ] Transizioni tra scene in stile gioco
- [ ] Salvataggio locale dei progressi (offline)
- [ ] Blocco di uscite accidentali (tasto indietro gestito)
- [ ] Layout adattivo: scene che si adattano a proporzioni e dimensioni diverse (telefono, tablet, TV) senza deformarsi
- [ ] Livello di input unico: tocco/trascinamento **e** telecomando (D-pad + OK), così ogni minigioco funziona con entrambi
- [ ] Focus visibile e "giocoso" per la navigazione con telecomando (alone/rimbalzo sull'elemento selezionato)

## Fase 4 — Personaggi

- [ ] Definire il nuovo metodo per creare la grafica dei personaggi (la skill `kids-character-gen` è stata annullata, D-027)
- [~] Bozze di design: Elide, Rio, Papà, Mamma (bozze 1-4 non approvate, da riprendere più avanti — D-029)
- [ ] Approvazione del design da parte del responsabile
- [ ] Asset finali e stati animati (idle, felice, incoraggia, parla)
- [ ] Widget riutilizzabile per ogni personaggio

## Fase 5 — Hub principale

- [ ] Scena di casa illustrata con i personaggi
- [ ] Accesso ai minigiochi tramite oggetti/porte toccabili
- [ ] Musica e animazioni d'ambiente

## Fase 6 — Primo minigioco (prototipo verticale)

- [ ] Scelta del minigioco
- [ ] Meccanica, grafica, suoni, festa finale
- [ ] Variante per telecomando (Android TV) di entrambi i livelli del gioco Colori
- [ ] Test sul dispositivo con la bambina e raccolta osservazioni

## Fase 7 — Altri minigiochi

*Idee da valutare (da confermare in Fase 1):*

- [ ] Colori (es. dipingere/ordinare oggetti per colore)
- [ ] Forme (incastri)
- [ ] Numeri e conteggio (contare oggetti con Rio)
- [ ] Animali e versi
- [ ] Routine quotidiane (bagnetto, pappa, nanna con Elide)
- [ ] Puzzle semplici
- [ ] Musica (strumenti da toccare)
- [ ] Memory con i personaggi

## Fase 8 — Area genitori

- [ ] Parental gate
- [ ] Impostazioni: volume musica/effetti, lingua
- [ ] Informazioni, licenza e crediti

## Fase 9 — Rifinitura

- [ ] Test con la bambina e iterazione
- [ ] Prestazioni su dispositivi economici
- [ ] Revisione accessibilità (aree di tocco, contrasti, audio)
- [ ] Test su smartphone, tablet e Android TV reali

## Fase 10 — Build e pubblicazione

- [ ] Icona e splash definitivi
- [ ] Build APK release firmata
- [ ] Release su GitHub con APK allegato
- [ ] Icona adattiva (telefono/tablet) e banner definitivo per Android TV

## ↔ Trasversale — Smartphone, tablet e Android TV

Un solo APK per tutti e tre i tipi di dispositivo (D-024). I task operativi sono distribuiti nelle fasi 2, 3, 9 e 10; qui il riepilogo.

- [x] Deciso come si gioca con il telecomando: "seleziona e sposta", giochi riadattati (D-025)
- [ ] Manifest e banner per Android TV (Fase 2)
- [ ] Layout adattivo per telefono, tablet e TV (Fase 3)
- [ ] Input unico tocco + telecomando con focus visibile (Fase 3)
- [ ] Ogni minigioco riadattato al telecomando con una variante dedicata (Fasi 6–7)
- [ ] Interfaccia leggibile "da divano" su TV: elementi più grandi e area sicura ai bordi (Fase 5)
- [ ] Test su dispositivi reali (Fase 9)

---

## Registro sessioni

| Data | Sessione | Fatto |
|------|----------|-------|
| 2026-11-11 | Avvio | Creati AGENTS.md, MEMORY.md, ROADMAP.md, README.md, LICENSE |
| 2026-11-11 | Decisioni | Scelti Rive, Flutter + Flame, orientamento orizzontale, primo minigioco Colori |
| 2026-11-11 | Decisioni | Colori su due livelli, voce TTS, italiano + inglese, app ID com.aptecstudio.elidesfamily |
| 2026-11-11 | Decisioni | TTS pre-generato, palette pastello vivace, font Fredoka, regola sondaggi in AGENTS.md. Fase 1 chiusa |
| 2026-11-11 | Scheletro | Progetto Flutter preparato a mano (senza SDK): struttura, avvio, hub provvisorio, localizzazioni, test |
| 2026-11-11 | Dispositivi | Aggiunto in roadmap il supporto a smartphone, tablet e Android TV; giochi riadattati al telecomando (D-025), AGENTS.md aggiornato |
| 2026-11-11 | Personaggi | Bozze 1-4 dei personaggi (in sospeso); skill kids-character-gen creata e poi annullata; Elide sempre protagonista, argomenti misti |
