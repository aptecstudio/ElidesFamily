# MEMORY.md — Memoria del progetto

> Registro delle **scelte** (con motivazione), dei **tratti stilistici** grafici e sonori, della **struttura del codice** e delle **convenzioni**.
> Le decisioni superate non si cancellano: si marcano con ~~barrato~~ e si rimanda a quella nuova.

Ultimo aggiornamento: 2026-11-11

---

## 1. Decisioni

| ID | Data | Decisione | Motivazione | Stato |
|----|------|-----------|-------------|-------|
| D-001 | 2026-11-11 | Framework **Flutter**, target **Android (APK)**. | Richiesto dal responsabile; un'unica base di codice, ottime prestazioni grafiche, hot reload per il test in tempo reale. | ✅ attiva |
| D-002 | 2026-11-11 | Test in tempo reale tramite `flutter run` su dispositivo Android fisico (USB o debug wireless) con **hot reload**. | Il gioco va provato toccandolo, sul dispositivo che userà la bambina. | ✅ attiva |
| D-003 | 2026-11-11 | Licenza **GPL-3.0**. | Richiesta del responsabile; repository pubblico. | ✅ attiva |
| D-004 | 2026-11-11 | Un solo branch: **`main`**. | Progetto hobbistico, flusso semplice. | ✅ attiva |
| D-005 | 2026-11-11 | Struttura: **hub centrale + minigiochi indipendenti**. | Ogni minigioco si sviluppa e si testa da solo; se ne possono aggiungere nel tempo senza toccare gli altri. | ✅ attiva |
| D-006 | 2026-11-11 | Interfaccia **non in stile app**: niente widget Material visibili (AppBar, Card, ListTile, pulsanti standard). | L'esperienza deve essere quella di un gioco illustrato, non di un'applicazione. | ✅ attiva |
| D-007 | 2026-11-11 | Personaggi animati con **Rive** (state machine: idle, felice, incoraggia, parla). | Vettoriale e leggero, stati multipli guidati dal codice, adatto a reazioni al tocco. | ✅ attiva |
| D-008 | 2026-11-11 | Motore: **Flutter** per hub, navigazione e area genitori; **Flame** per i minigiochi. | Flutter è ideale per scene e transizioni, Flame per game loop, movimento e trascinamenti. | ✅ attiva |
| D-009 | 2026-11-11 | Orientamento **solo orizzontale**, schermo intero immersivo. | Più spazio per le scene, tipico dei giochi per bambini. | ✅ attiva |
| D-010 | 2026-11-11 | Primo minigioco (prototipo): **Colori**. | Scelta del responsabile. | ✅ attiva |
| D-011 | 2026-11-11 | Minigioco Colori con **due livelli**: 1) ordinare gli oggetti trascinandoli nel cesto del colore giusto; 2) dipingere un disegno toccando un colore e poi una zona. | Scelta del responsabile: copre riconoscimento dei colori e motricità fine. | ✅ attiva |
| D-012 | 2026-11-11 | Istruzioni vocali con **voce sintetizzata (TTS)**. | Scelta del responsabile: più veloce da produrre e da tradurre. | ✅ attiva |
| D-013 | 2026-11-11 | Lingue: **italiano e inglese**, con sistema di localizzazione fin dall'inizio. | Scelta del responsabile; i testi/frasi non vanno mai scritti "a mano" nel codice. | ✅ attiva |
| D-014 | 2026-11-11 | Application ID Android: **`com.aptecstudio.elidesfamily`**. | Scelta del responsabile. | ✅ attiva |

| D-015 | 2026-11-11 | Voce TTS **pre-generata** come file audio inclusi nell'app (`assets/audio/voice/<lingua>/`). | Stessa voce su ogni telefono, qualità controllata, sempre offline. | ✅ attiva |
| D-016 | 2026-11-11 | Palette **pastello vivace** (vedi §3). | Toni caldi e saturi ma morbidi, adatti all'età. | ✅ attiva |
| D-017 | 2026-11-11 | Font **Fredoka** (licenza SIL OFL 1.1), incluso negli asset. | Tondo e giocoso; licenza compatibile; incluso per funzionare offline. | ✅ attiva |
| D-018 | 2026-11-11 | AGENTS.md aggiornato (con autorizzazione del responsabile): le domande si fanno **sempre con sondaggi interattivi**. | Richiesta del responsabile. | ✅ attiva |

| D-019 | 2026-11-11 | Radice dell'app con **`WidgetsApp`** (non `MaterialApp`), `uses-material-design: false`. | Nessun aspetto "da app" (D-006): temi, transizioni e controlli sono tutti nostri. | ✅ attiva |
| D-020 | 2026-11-11 | Ogni elemento toccabile passa dal widget comune **`BouncyTap`** (`lib/core/`). | Feedback al tocco uguale ovunque (schiacciamento + rimbalzo, poi suono). | ✅ attiva |
| D-021 | 2026-11-11 | Le icone dell'interfaccia sono **disegnate** (CustomPainter o asset), mai scritte. | I bambini di 3 anni non leggono. | ✅ attiva |
| D-022 | 2026-11-11 | Localizzazione con **`flutter gen-l10n`**: ARB in `lib/l10n/` (`app_it.arb` è il modello); i file generati non si versionano. | Italiano + inglese (D-013) senza testi scritti nel codice. | ✅ attiva |
| D-023 | 2026-11-11 | Cartella `android/` generata con `flutter create` **sul PC del responsabile**, poi adattata. | L'ambiente di sviluppo AI non ha l'SDK Flutter: generarla con lo strumento ufficiale evita versioni Gradle/AGP sbagliate. | ✅ attiva |

| D-024 | 2026-11-11 | Dispositivi supportati: **smartphone, tablet e Android TV**, con **un solo APK**. | Richiesta del responsabile. Un APK unico semplifica build e distribuzione; il gioco si adatta a schermo e tipo di input. | ✅ attiva |

| D-025 | 2026-11-11 | Su Android TV i minigiochi sono **riadattati al telecomando**, non solo "portati": modalità **seleziona e sposta** (frecce per scegliere l'oggetto, OK per prenderlo, frecce per portarlo, OK per lasciarlo). | Richiesta del responsabile: il telecomando è un input diverso e ogni gioco deve risultare naturale anche così. | ✅ attiva |
| D-026 | 2026-11-11 | AGENTS.md, principio 1, aggiornato con autorizzazione del responsabile: include il telecomando su Android TV. | Coerenza con D-024 e D-025. | ✅ attiva |

### Regole per i minigiochi su Android TV (D-025)

- Ogni minigioco ha una **variante per telecomando** progettata insieme a quella touch: meccanica, distanze e ritmo si possono semplificare.
- L'elemento selezionato è sempre evidente (alone colorato e piccolo rimbalzo) e accompagnato da un suono.
- Gli oggetti "presi" seguono le frecce a scatti morbidi fra posizioni prestabilite, non a pixel.
- Nessuna azione richiede tasti diversi da frecce, OK e Indietro.

### Decisioni ancora aperte

- *(nessuna)*

---

## 2. Concept del gioco

- **Nome**: Elide's Family.
- **Pubblico**: bambini dai 3 anni in su.
- **Formato**: raccolta di minigiochi che aiutano crescita e apprendimento (colori, forme, numeri, animali, suoni, routine quotidiane, motricità fine…).
- **Riferimento di stile** (interno, da non citare nel README): modalità di gioco e grafica sullo stile di *Baby Games: Lucas & Friends* — personaggi animali morbidi e tondeggianti, scene colorate, feedback immediato. Si prende ispirazione dallo **stile**, gli asset sono tutti originali.

### Personaggi

| Personaggio | Chi è | Aspetto |
|-------------|-------|---------|
| **Elide** | La protagonista, piccola di casa | Gattina piccola, **bianca** |
| **Rio** | L'amico a quattro zampe | **Bulldog francese** color **miele** |
| **Papà** | Il papà | **Labrador bianco** |
| **Mamma** | La mamma | **Gatta color miele** con **macchie bianche** |

- Non tutti i personaggi compaiono in ogni minigioco: si scelgono in base al contesto.
- Proporzioni "baby": testa grande, corpo piccolo e tondo, occhi grandi e lucidi, contorni morbidi, nessun angolo vivo.
- Ogni personaggio ha un set minimo di stati animati: **idle** (respiro/battito ciglia), **felice/festeggia**, **incoraggia**, **parla**.

---

## 3. Stile grafico e sonoro

- **Colori**: palette vivace ma morbida (tinte pastello sature), sfondi luminosi e illustrati.
- **Forme**: tutto arrotondato; elementi interattivi grandi (area minima di tocco ~ 64 dp) e ben distanziati.
- **Tipografia**: quasi assente (i bambini di 3 anni non leggono); dove serve, font tondo e grande.
- **Feedback**: ogni tocco produce un'animazione (rimbalzo, schiacciamento, scintille) e un suono.
- **Successo**: festa con coriandoli/stelline, personaggio che salta, suono allegro.
- **Errore**: mai punitivo — l'oggetto torna morbidamente al suo posto, il personaggio incoraggia.
- **Audio**: musica di sottofondo leggera e a volume basso, effetti brevi e gentili, voci chiare.

### Palette "pastello vivace" (D-016)

| Nome | Hex | Uso principale |
|------|-----|----------------|
| `skyBlue` | `#8FD3F4` | cielo, sfondi aperti |
| `butterYellow` | `#FFE08A` | luce, stelle, evidenziazioni |
| `meadowGreen` | `#9BDB7C` | prati, conferme |
| `peachPink` | `#FFB5A7` | dettagli caldi, guance |
| `lavender` | `#C7B8F5` | elementi magici, area hub |
| `honey` | `#E8B060` | Rio e Mamma, legno |
| `cream` | `#FFF6E5` | sfondi interni, Elide e Papà (bianco caldo) |
| `cocoa` | `#5A3E36` | contorni morbidi e testo (al posto del nero) |

- Niente nero puro: i contorni usano `cocoa`.
- Per il minigioco Colori si usano colori **puri e ben distinti** (rosso, giallo, blu, verde, arancione, viola), definiti a parte nel minigioco.

### Font (D-017)

- **Fredoka** (SIL OFL 1.1), file in `assets/fonts/`.

*(Il set di effetti sonori verrà fissato qui quando deciso.)*

---

## 4. Struttura del codice (prevista)

```
lib/
├── main.dart                     # avvio: solo orizzontale, schermo intero immersivo
├── app/
│   ├── elides_family_app.dart    # WidgetsApp, localizzazioni, stile testo
│   ├── game_colors.dart          # palette (D-016)
│   └── game_route.dart           # transizione tra scene
├── core/
│   └── bouncy_tap.dart           # feedback al tocco comune (D-020)
├── characters/                   # Elide, Rio, Papà, Mamma (Rive)
├── hub/
│   └── hub_scene.dart            # scena principale (provvisoria)
├── parental_gate/                # area adulti protetta
├── l10n/                         # app_it.arb, app_en.arb (+ file generati, non versionati)
└── minigames/
    └── colors/
        └── colors_game_scene.dart  # segnaposto del minigioco Colori
assets/
├── images/
├── animations/                   # file .riv
├── audio/
│   ├── music/
│   ├── sfx/
│   └── voice/{it,en}/            # voci TTS pre-generate (D-015)
└── fonts/                        # Fredoka (D-017)
test/
└── widget_test.dart
```

Le cartelle vuote contengono un `.gitkeep`, da togliere quando ricevono il primo file.

---

## 5. Convenzioni

- **Lingua**: codice (identificatori) in inglese; commenti, documentazione e commit in italiano.
- **Dart**: stile ufficiale (`dart format`), regole di `flutter_lints`.
- **Naming**: file `snake_case.dart`, classi `PascalCase`, variabili/metodi `camelCase`, costanti `lowerCamelCase`.
- **Asset**: `snake_case`, con prefisso di categoria (es. `char_elide_idle.riv`, `sfx_pop.ogg`, `bg_kitchen.png`).
- **Minigiochi**: cartella `lib/minigames/<nome>/`; scena Flutter d'ingresso `<Nome>GameScene`, gioco Flame `<Nome>Game`.
- **Testi e voci**: chiavi ARB in `camelCase` (es. `gameColorsName`); il file voce corrispondente si chiama `voice_<chiave_in_snake_case>` nella cartella della lingua (es. `assets/audio/voice/it/voice_game_colors_name.ogg`).
- **Colori**: solo dalle costanti di `GameColors`, mai valori esadecimali sparsi (eccezione: i colori "da imparare" definiti dentro il minigioco Colori).
- **Commit**: prefisso convenzionale in italiano (vedi `AGENTS.md`).

---

## 6. Asset di terze parti

| Asset | Fonte | Licenza | Note |
|-------|-------|---------|------|
| *(nessuno per ora)* | | | |
