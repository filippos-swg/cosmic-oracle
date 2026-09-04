# TASK — The Great Language Expansion

**Status:** COMPLETE — delivered and curated 2026-08-17; v1.0 tagged.
**Read first:** `aios/STATE.md`, then `aios/ASTRA_MIND_v0.1.md` (the voice
bible — the six Adams operations and failure modes govern every line).

## Goal

Roughly triple ASTRA's corpus and eliminate same-day repetition, per visitor
feedback ("still slightly abstract, phrases repeat, friends compared
readings"). All new writing in the librarian's voice; filippos curates after.

## Scope (agreed numbers)

In **librarian.py**:
1. TOKEN_MEANINGS: 6 → ~20 curated aspects (cover common personal-planet
   pairs: Sun/Moon/Mercury/Venus/Mars × Conj/Sqr/Tri/Opp/Sxt highlights,
   plus Moon-Saturn, Venus-Jupiter, Mars-Saturn etc.).
2. ASPECT_MODES: per mode → ~10 verbs_one / ~10 verbs / ~14 omens /
   ~8 constraints. Keep the existing lines; add, don't replace.
3. MARGINALIA: 25 → ~50.
4. TRANSIT_NOTES: 6 → ~10 per mode.
5. ASIDE_CLOSINGS: 12 → ~20.
6. SIGN_TEMPERAMENT: add a second address + lens variant per sign
   (seeded selection).

In **visual/tv.html** (corpus blocks near top of script):
7. LANDINGS: 2 → 6 variants per domain × mode (this is the highest-value
   writing — it's what visitors take home).
8. VERDICTS: 2 → 6 per domain × mode. Plain register. Time-bounded feel.
9. LANDING_FRAMES: 4 → ~8.
10. FOUND_ITEMS: 24 → ~48 pieces (2 → 4 per mode per container).
    Letters address; dreams witness. The turn in the last line.
11. RECORD_FORMS / RECORD_COLORS: a few more entries each.

Mechanics (code, small):
12. Day-level no-repeat allocation in build_sign_readings: allocate pool
    sentences across the 12 signs WITHOUT replacement per day, so no two
    signs share an omen/marginalia line on the same date.
13. Shift more selection weight to the visitor seed (dob) vs day seed
    where pools allow.

## Guardrails

- Voice: bathos, specificity, escalation, swerve, understatement,
  institutional pathos. If a line would survive on a poster, cut it.
- Balance rule (locked): body enigmatic, ONE landing per unit names the
  domain, only THE VERDICT speaks plainly. ~70% visitor-directed.
- No mysticism, no coaching outside verdicts, no outside voices.
- Verify after: regenerate oracle.json, check 12-sign distinctness AND
  same-day cross-sign no-repeat programmatically; run the Playwright
  walkthrough if in a cloud session, or a manual dial-through locally.
- Log to `aios/LOG.md`. Filippos curates the new corpus before v1.0.

## Completion

- [x] Corpus expansion delivered and curated
- [x] Day-level no-repeat allocation and visitor-seeded selection delivered
- [x] Full verification suite passed
- [x] v1.0 tagged

## After this task

Phone hardware confirmation → curation pass → tag v1.0 → website build
(static, astronomy-engine JS ephemeris, Cloudflare Pages) → hardware
assembly (testcard calibration → dial → kiosk hardening).
