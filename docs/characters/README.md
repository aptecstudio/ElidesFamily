# Personaggi — direzione artistica

Riferimento visivo comune per tutti i personaggi di Elide's Family.
Ogni scheda in questa cartella rispetta queste regole: cambia l'identità del personaggio, non lo stile.

> Stato: **bozze approvate provvisoriamente** (2026-11-12). Forme, colori e pose sono la base di lavoro; la resa finale verrà ottimizzata.

## Stile

- Cartoon morbido, dolce e allegro, con volumi resi da sfumature morbide.
- **Contorni colorati**: ogni contorno è una versione più scura del colore che delimita (lilla scuro sul pelo bianco, verde acqua scuro sul vestito turchese, rosa scuro su naso e bocca). Mai un nero uniforme.
- Poche linee interne: occhi, bocca, pochi dettagli dei vestiti.
- Luce dall'alto a sinistra, ombre lilla morbide, piccoli riflessi lucidi.
- Vietati: realismo, stile anime, flat 2D.

## Proporzioni

- Testa circa metà dell'altezza, rotonda e piena.
- Occhi rotondi e distanziati (circa un occhio di distanza), sopracciglia colorate.
- Musetto grande e chiaro nella parte bassa del viso, nasino in cima, sorriso semplice.
- Braccia e gambe paffute, più spesse alla radice; manine con pollice e tre ditine, piedi con le dita.
- Piccoli (Elide, Rio) e adulti (Papà, Mamma) hanno la stessa testa: cambia il corpo.

## Occhi

- Iride grande, scura in alto e chiara in basso; pupilla grande; riflesso grande in alto a destra e uno piccolo in basso a sinistra.
- Palpebra superiore spessa; ciglia solo per i personaggi femminili.
- Quando sorride, le guance salgono e chiudono l'occhio dal basso.

## Espressioni e pose

Ogni personaggio ha almeno questi stati, costruiti con lo stesso modello (cambiano solo braccia, occhi, sopracciglia, bocca e inclinazione):
a riposo, ciao, evviva, curiosa/o, sorpresa/o, bravo/a.

## Suite di animazioni (D-033)

Ogni personaggio ha la **suite completa**, uguale per tutti. In Rive è una state machine a **livelli separati** (corpo, viso, occhi, bocca) che si combinano: per esempio Elide può camminare, parlare e sorridere nello stesso momento. Tutte le transizioni sono interpolate, senza scatti.

| Gruppo | Animazioni |
|--------|------------|
| **A riposo** | Respiro, battito di ciglia, guardarsi intorno, attesa dopo un po' di inattività (sbadiglio, dondolarsi), seduto |
| **Movimento** | Camminata (di fronte e di lato), corsa, girarsi, entrata e uscita di scena, salto sul posto, salto in avanti con atterraggio morbido |
| **Contentezza** | Sorriso, saltello di gioia, evviva a braccia alzate, applauso, risata, pollice su, cuoricino / abbraccio |
| **Balli** | Almeno 3 balli diversi in loop (dondolio, giravolta, battimani a ritmo) |
| **Disapprovazione gentile** | "No" con la testa, ditino che fa no-no, broncio, braccia conserte, spalle giù deluse, faccino triste leggero |
| **Pensiero e sorpresa** | Curiosità (mano al mento), confusione (grattarsi la testa), sorpresa, piccolo spavento buffo |
| **Interazione** | Salutare, chiamare con la mano, indicare a destra e a sinistra, prendere e porgere un oggetto, reazione al tocco (solletico, risatina) |
| **Routine** | Mangiare, bere, lavarsi, sbadigliare e dormire |
| **Parlato** | Lip sync a visemi per le voci TTS: riposo, A, E, I, O, U, M-B-P, F-V |

La disapprovazione è sempre dolce e buffa, mai punitiva o spaventosa: serve a dire "riproviamo", non "hai sbagliato".

## Schede

| Personaggio | Stato | Scheda |
|-------------|-------|--------|
| Elide | Bozza approvata provvisoriamente | [elide.md](elide/elide.md) |
| Rio | Da fare | — |
| Papà | Da fare | — |
| Mamma | Da fare | — |

Le immagini delle bozze sono generate da `tools/character-drafts/` (SVG creato da script Python, convertito in PNG con `rsvg-convert`).
