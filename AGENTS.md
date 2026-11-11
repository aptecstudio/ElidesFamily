# AGENTS.md — Guida per agenti AI e collaboratori umani

> **Elide's Family** — raccolta di minigiochi educativi per bambini dai 3 anni in su.
> Flutter · target Android (APK) · licenza GPL-3.0

---

## 1. Scopo di questo file

Questo file è la guida di riferimento per **agenti AI** e **persone** che lavorano sul progetto.
Spiega come si lavora qui, dove si trovano le informazioni sui **progressi fatti**, sulle **strategie adottate** e sul **perché** di ogni scelta.

Prima di qualsiasi intervento, chi lavora sul progetto **deve leggere**, in quest'ordine:

1. `AGENTS.md` (questo file) — le regole.
2. `MEMORY.md` — le decisioni prese, lo stile grafico, la struttura del codice e le convenzioni.
3. `ROADMAP.md` — cosa è stato fatto e cosa resta da fare.

---

## 2. Regola di immutabilità di AGENTS.md

- `AGENTS.md` viene creato una sola volta all'avvio del progetto.
- **Non può essere modificato** senza una richiesta esplicita **e** l'approvazione del responsabile umano del progetto.
- Un agente AI che ritiene necessaria una modifica a questo file **deve proporla** al responsabile umano, spiegandone il motivo, e attendere l'autorizzazione prima di applicarla.
- Questa regola riguarda solo `AGENTS.md`: il codice sorgente, gli asset e le risorse del progetto si possono creare e modificare normalmente come parte del lavoro.

---

## 3. File di stato del progetto

Gli **unici file di stato** che gli agenti aggiornano autonomamente sono:

| File | Contenuto | Quando aggiornarlo |
|------|-----------|--------------------|
| `MEMORY.md` | Scelte tecniche e di design (con motivazione), tratti stilistici grafici e sonori, struttura del codice, convenzioni sintattiche e di naming. | Ogni volta che si prende o si cambia una decisione, si introduce una convenzione o si modifica la struttura. |
| `ROADMAP.md` | Passaggi eseguiti e passaggi ancora da eseguire, per avere uno stato **globale** (fasi) e **parziale** (singoli task) del progetto. | All'inizio e alla fine di ogni sessione di lavoro, e ogni volta che un task cambia stato. |

### Regole di aggiornamento

- **MEMORY.md**: ogni decisione riporta *cosa* si è deciso e *perché*. Se una decisione viene superata, non si cancella: si segna come superata e si indica quella nuova (la storia delle scelte è utile).
- **ROADMAP.md**: i task usano le checkbox (`- [ ]` da fare, `- [x]` fatto, `- [~]` in corso). Un task si segna come fatto solo quando è davvero completo e verificato.
- Le date usano il formato `AAAA-MM-GG`.

---

## 4. Flusso di lavoro

- **Branch unico**: si lavora solo su `main`. Non si creano altri branch.
- **Commit piccoli e descrittivi**, in italiano, con prefisso convenzionale:
  `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `assets:`.
  Esempio: `feat: aggiunto minigioco "Forme e colori" con Elide e Rio`.
- **In caso di dubbio, chiedere**: le scelte di gusto, di contenuto o che riguardano l'esperienza del bambino si sottopongono al responsabile umano **sempre tramite sondaggi interattivi** (domande a scelta multipla), invece di decidere da soli.
- A fine sessione: aggiornare `ROADMAP.md` e, se serve, `MEMORY.md`, poi fare commit.

---

## 5. Principi del progetto (non negoziabili)

1. **Pensato per bambini dai 3 anni**: interazioni semplici (tocco, trascinamento), nessuna lettura richiesta, istruzioni vocali o visive, nessun modo di "perdere" in modo frustrante.
2. **Aspetto da gioco, non da app**: niente AppBar, menu a tendina, liste o pulsanti in stile Material. Ogni schermata è una scena illustrata, colorata e animata.
3. **Suoni e animazioni gradevoli** ad ogni interazione: ogni tocco deve dare una risposta visiva e sonora.
4. **Sicurezza e privacy**: nessuna pubblicità, nessun acquisto in-app, nessun tracciamento, nessun collegamento esterno raggiungibile dal bambino. Eventuali impostazioni per adulti stanno dietro un "parental gate".
5. **Asset originali**: personaggi, illustrazioni, suoni e musiche devono essere originali o con licenza compatibile con GPL-3.0 / libera. Non si copiano asset di altri giochi. La provenienza e la licenza di ogni asset di terze parti si annota in `MEMORY.md`.
6. **Funziona offline**.

---

## 6. Dove trovare le cose

| Cosa | Dove |
|------|------|
| Regole di lavoro | `AGENTS.md` |
| Decisioni, stile, convenzioni, struttura | `MEMORY.md` |
| Avanzamento e prossimi passi | `ROADMAP.md` |
| Descrizione pubblica del gioco | `README.md` |
| Licenza | `LICENSE` (GPL-3.0) |
