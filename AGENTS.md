# AGENTS.md — Guide for AI agents and human contributors

> **Elide's Family** — a collection of educational minigames for children aged 3 and up.
> Flutter · Android target (APK) · GPL-3.0 license

---

## 1. Purpose of this file

This file is the reference guide for **AI agents** and **people** working on the project.
It explains how work is done here and where to find information about the **progress made**, the **strategies adopted** and the **reasons** behind every choice.

Before any work, contributors **must read**, in this order:

1. `AGENTS.md` (this file) — the rules.
2. `MEMORY.md` — the decisions taken, the art style, the code structure and the conventions.
3. `ROADMAP.md` — what has been done and what is left to do.

---

## 2. Immutability rule for AGENTS.md

- `AGENTS.md` is created once, when the project starts.
- It **cannot be changed** without an explicit request **and** the approval of the project's human owner.
- An AI agent that believes a change to this file is needed **must propose it** to the human owner, explaining why, and wait for authorization before applying it.
- This rule only applies to `AGENTS.md`: source code, assets and project resources can be created and modified normally as part of the work.

---

## 3. Project status files

The **only status files** that agents update on their own are:

| File | Content | When to update it |
|------|---------|-------------------|
| `MEMORY.md` | Technical and design choices (with their reasons), graphic and sound style traits, code structure, syntax and naming conventions. | Every time a decision is taken or changed, a convention is introduced or the structure changes. |
| `ROADMAP.md` | Steps completed and steps still to do, giving both a **global** (phases) and a **partial** (single tasks) view of the project. | At the start and end of every work session, and every time a task changes status. |

### Update rules

- **MEMORY.md**: every decision states *what* was decided and *why*. When a decision is superseded it is not deleted: it is marked as superseded and points to the new one (the history of the choices is useful).
- **ROADMAP.md**: tasks use checkboxes (`- [ ]` to do, `- [x]` done, `- [~]` in progress). A task is marked done only when it is really complete and verified.
- Dates use the `YYYY-MM-DD` format.

---

## 4. Workflow

- **Single branch**: work happens only on `main`. No other branches are created.
- **Small, descriptive commits**, in English, with a conventional prefix:
  `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `assets:`.
  Example: `feat: add the "Shapes and colors" minigame with Elide and Rio`.
- **When in doubt, ask**: choices of taste, of content, or that affect the child's experience are submitted to the human owner **always through interactive polls** (multiple-choice questions), instead of deciding alone.
- At the end of a session: update `ROADMAP.md` and, if needed, `MEMORY.md`, then commit.
- **Code style**: every language follows its own standard conventions for naming, spacing, comments and overall code style (Dart: Effective Dart, `dart format` and `flutter_lints`; Python: PEP 8, checked with `ruff`).
- **Language**: all source code and documentation are written in **English**. The only exception is chat communication with the human owner, which is exclusively in **Italian**.

---

## 5. Project principles (non-negotiable)

1. **Designed for children aged 3 and up**: simple interactions (tap and drag; on Android TV the remote control, with the games adapted to it), no reading required, voice or visual instructions, no frustrating way to "lose".
2. **Looks like a game, not an app**: no AppBar, drop-down menus, lists or Material-style buttons. Every screen is an illustrated, colorful, animated scene.
3. **Pleasant sounds and animations** on every interaction: every touch must give a visual and audio response.
4. **Safety and privacy**: no ads, no in-app purchases, no tracking, no external links reachable by the child. Any settings for adults sit behind a "parental gate".
5. **Original assets**: characters, illustrations, sounds and music must be original or under a license compatible with GPL-3.0 / free. Assets from other games are never copied. The origin and license of every third-party asset is recorded in `MEMORY.md`.
6. **Works offline**.

---

## 6. Where to find things

| What | Where |
|------|-------|
| Working rules | `AGENTS.md` |
| Decisions, style, conventions, structure | `MEMORY.md` |
| Progress and next steps | `ROADMAP.md` |
| Public description of the game | `README.md` |
| License | `LICENSE` (GPL-3.0) |
