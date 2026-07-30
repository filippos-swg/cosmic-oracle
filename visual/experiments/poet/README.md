# Experiment: the found item (letters + dreams)

**Status:** sandbox — the production ceremony (visual/tv.html) is untouched.

After the archive closes the visitor's file, one item remains: an unsigned
**letter**, or a **dream** recorded on the night they were born and never
interpreted. The librarian did not write these. The librarian merely cannot
explain them. This is ASTRA's single unguarded beat — Rumi's craft (direct
address, the turn, the invitation) in the archive's own imagery, per the
discussion logged 2026-07 (no outside tones; the dry ceremony earns one
moment of tenderness at the end).

## Try it

Run the normal stack (`bash run.sh`, or oracle.py + server.py), then open:

    http://localhost:8000/experiments/poet/tv.html

Dial any birthdate. The final two screens are the experiment: the framing
("ONE ITEM REMAINS") and the piece itself, held 18s.

## How it chooses

- Container (letter vs dream): seeded by birthdate + day — alternates
  per visitor and rotates daily.
- Piece: keyed to the LEAD TRANSIT's aspect mode (Conjunction/Opposition/
  Trine/Square/Sextile, or 'none' when the natal chart is unaspected),
  2 authored pieces per mode per container = 24 total, seed-selected.

## Corpus rules (from ASTRA_MIND_v0.1)

Second person. The turn in the last line. Archive/sky imagery only —
doors, locks, lamps, ledgers, shelves, rivers, keys. No fridge magnets:
if a line would survive on a poster, cut it. Letters speak TO the visitor;
dreams never address anyone — they are witnessed, not sent.

## Merging into production (when blessed)

Everything lives in three blocks in this file's copy of tv.html:
1. CSS: the `.r-body.poem` rule
2. JS: the `FOUND_ITEMS` const + `pickFoundItem()`
3. JS: the `readingScreens.push(...)` block after the close-file screen,
   plus the one-line `poem` class addition in renderReadingScreen and the
   `READING_HOLD_LAST_MS` bump.
Copy those into visual/tv.html and delete this folder (or keep it for the
v2.0 thermal-printer work — the printer will want `found.piece` + stamp).
