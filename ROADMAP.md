# ROADMAP.md — Stato del progetto

> Legenda: `- [x]` fatto · `- [~]` in corso · `- [ ]` da fare
> Le fasi danno lo **stato globale**, i task lo **stato parziale**.

Ultimo aggiornamento: 2026-11-11

---

## Stato globale

| Fase | Descrizione | Stato |
|------|-------------|-------|
| 0 | Fondamenta del repository e documentazione | 🟢 completata |
| 1 | Decisioni tecniche e di design | 🟡 in corso |
| 2 | Setup del progetto Flutter e test in tempo reale | ⚪ da iniziare |
| 3 | Motore comune (audio, animazioni, navigazione) | ⚪ da iniziare |
| 4 | Personaggi | ⚪ da iniziare |
| 5 | Hub principale | ⚪ da iniziare |
| 6 | Primo minigioco (prototipo verticale) | ⚪ da iniziare |
| 7 | Altri minigiochi | ⚪ da iniziare |
| 8 | Area genitori e impostazioni | ⚪ da iniziare |
| 9 | Rifinitura, test con la bambina, accessibilità | ⚪ da iniziare |
| 10 | Build APK e pubblicazione | ⚪ da iniziare |

**Prossimo passo:** chiudere le ultime decisioni della Fase 1 (modalità TTS, palette e font), poi Fase 2.

---

## Fase 0 — Fondamenta del repository ✅

- [x] Repository creato su GitHub (`aptecstudio/ElidesFamily`), branch `main`
- [x] `AGENTS.md` con le regole di lavoro
- [x] `MEMORY.md` con concept, personaggi, stile e convenzioni iniziali
- [x] `ROADMAP.md` (questo file)
- [x] `README.md` pubblico
- [x] `LICENSE` GPL-3.0

## Fase 1 — Decisioni tecniche e di design

- [x] Motore: Flutter + Flame (D-008)
- [x] Tecnica di animazione dei personaggi: Rive (D-007)
- [x] Orientamento schermo: solo orizzontale (D-009)
- [x] Primo minigioco: Colori (D-010)
- [x] Meccanica del minigioco Colori: ordinare + dipingere (D-011)
- [x] Voce: sintetizzata TTS (D-012)
- [x] Lingue: italiano e inglese (D-013)
- [x] Application ID Android: `com.aptecstudio.elidesfamily` (D-014)
- [ ] Modalità TTS: runtime sul dispositivo o file audio pre-generati
- [ ] Palette colori e font definitivi

## Fase 2 — Setup Flutter e test in tempo reale

- [ ] `flutter create` con application ID e nome definitivi
- [ ] Configurazione Android (minSdk, orientamento, schermo intero immersivo, icona provvisoria)
- [ ] `analysis_options.yaml` con `flutter_lints`
- [ ] Struttura delle cartelle come in `MEMORY.md`
- [ ] Guida al test in tempo reale: `flutter run` su dispositivo via USB / debug wireless + hot reload
- [ ] Prima build APK di prova (`flutter build apk --debug`)

## Fase 3 — Motore comune

- [ ] Servizio audio (musica, effetti, voci) con controllo volume
- [ ] Widget di feedback al tocco (rimbalzo + suono)
- [ ] Animazione di festa per il successo
- [ ] Transizioni tra scene in stile gioco
- [ ] Salvataggio locale dei progressi (offline)
- [ ] Blocco di uscite accidentali (tasto indietro gestito)

## Fase 4 — Personaggi

- [ ] Bozze di design: Elide, Rio, Papà, Mamma
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

## Fase 10 — Build e pubblicazione

- [ ] Icona e splash definitivi
- [ ] Build APK release firmata
- [ ] Release su GitHub con APK allegato

---

## Registro sessioni

| Data | Sessione | Fatto |
|------|----------|-------|
| 2026-11-11 | Avvio | Creati AGENTS.md, MEMORY.md, ROADMAP.md, README.md, LICENSE |
| 2026-11-11 | Decisioni | Scelti Rive, Flutter + Flame, orientamento orizzontale, primo minigioco Colori |
| 2026-11-11 | Decisioni | Colori su due livelli, voce TTS, italiano + inglese, app ID com.aptecstudio.elidesfamily |
