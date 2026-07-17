# CHANGELOG — Cosmic Oracle / Astra

Newest-first.

---

## 2026-07-17 — Ruler-led sign readings

- build_sign_readings() now leads each sign's reading with what its RULING
  planet is doing in today's sky (SIGN_RULERS: modern primary, traditional
  fallback; freshest aspect preferred via other-planet speed rank; curated
  token wins if it involves the ruler; graceful "reports nothing unusual"
  when the ruler is unaspected). New "governor" line ("Your file is kept by
  the engine room.") shown under the headline in tv.html. The shared middle
  of the reading now differs across signs on any day with multiple aspects.

---

## 2026-07-17 — Natal transits + instrument panels (post first live test)

- Fixed the "identical readings" problem: /natal now also computes TRANSITS from
  the current sky to the visitor's natal Sun and Moon (tightest two, diverse),
  so different birthdates get genuinely different readings on the same day.
  librarian.compose_transit() renders them in the archival voice ("The office
  of expansion is cooperating, unprompted, with your natal Sun.").
- READING gains 1–2 "IN YOUR SKY TODAY" screens (personal transits).
- Instrument graphics restored, large-format, flanking the entity during the
  reading: CELESTIAL LOG (glyphs, degrees, retrograde R) on the left; YOUR
  NATAL SKY (personal transit rows, correct-phase moon icon, age/illumination)
  on the right. Panels fade in after the FILE card; sized for the safe frame.

---

## 2026-07-17 — Installation experience built (Phases B–D, pre-calibration)

- **visual/tv.html** — the ceremony. 4:3 stage (1024×768), all content inside the
  CONFIG.SAFE frame (0.80 until the tube is measured). State machine:
  BOOT (calibration ritual) → IDLE (entity + rotating sky line + invitation) →
  IDENTIFY (DD·MM·YYYY digit slots, validation, 30s timeout) →
  CONSULT (entity agitation + ephemeris theatre, min 5.2s) →
  READING (FILE card → headline → observations → constraint → temperament lens →
  closing, auto-advance or Enter) → IDLE. Optional SIGNOFF state (config-gated).
  Input is plain digit keystrokes (rotary dial = USB keyboard; Esc abandons,
  Backspace corrects). Entity engine embedded with state hooks
  (agitation/dim, element-tinted during readings). All calibration numbers in
  one CONFIG block.
- **librarian.py** — SIGN_TEMPERAMENT (12 archival address + lens fragments);
  build_sign_readings() refracts the day's reading through each temperament.
- **oracle.py** — oracle.json now carries readings_by_sign (all 12, every cycle).
- **visual/server.py** — /natal?d&m&y endpoint (swisseph, noon UT): natal sun +
  approximate moon sign, fully offline; client has a date-table fallback.

---

## 2026-07-16 — Installation build begins (Phase A)

- Name resolved: ASTRA (DECISIONS.md)
- Decisions logged: rotary-dial DOB input, fully local architecture, installation-first
- v1 desktop dashboard frozen in snapshots/v1-2026-07-16-desktop-dashboard/ (runnable)
- Added visual/testcard.html — CRT calibration card (safe rects 90/80/70, corner-mask
  arcs, 1/2/3px line samples, 18–44px type ladder, grayscale steps, 1 Hz blinker,
  'i' invert / 'g' grid-only). First thing to display on the DUX through the converter.
- Added aios/STATUS_REPORT.md — status + finalization plan (UX ceremony, TV legibility
  audit, MacBook appliance checklist, roadmap)

---

## 2026-07-16 — Design-parity + data-layer pass (AI session, reviewed by filippos)

**sky.py**
- Capture longitudinal speeds from swisseph; planets now carry `speed` and `retrograde`
- Aspects now carry `applying` (true orb-shrinking test against positions 30 min ahead)
- Signature ordering weighted by planet speed (Moon/inner planets first) so months-long
  outer-planet aspects no longer permanently crowd the 8-token budget

**librarian.py**
- New composed-reading layer: when no curated token matches, a reading is assembled
  from the tightest personal-planet aspect (planet "departments" × aspect "modes",
  same archival voice). The generic library-quiet fallback now only appears on
  genuinely empty skies.

**visual/index.html**
- Moon strip: fixed phase math (cycle fraction was fed to a renderer expecting
  illuminated fraction — full moon rendered as half moon, waning half of the month wrong);
  strip is now symmetric −3..+3 days with today centered
- Particle figure rebuilt from the close-up entity reference: RIM-DEFINED —
  a bright ragged band of scratchy streak particles traces the head dome and
  shoulder tops (brightest on the crown, fragmenting away down the sides);
  interior stays dark (the face reads as dark space) with sparse dust that
  densifies toward the rim; per-row half-width lookup (dome head widest
  0.147, jaw pinch 0.132, concentrated shoulder flare, widest 0.50 at 62%
  height, near-vertical fading sides; aspect 0.75, bust ≈ 78% of frame
  height, centered at 0.687 of frame width); vertical fade + base dissolve;
  full-frame canvas so the starfield spans the whole interface; 80k
  particles (down from 100k)
- Canvas seam fixed: alpha-composited particle buffer instead of opaque black slab
- Transits: full planet names, deg°min′ orbs, real applying/separating from sky.py
- Celestial Log: retrograde "R" markers
- Typeface: Courier Prime (typewriter mono per design mockup), JetBrains Mono fallback
- Status bar 12 cells; dashed vertical rule + plus marks per mockup

**repo**
- visual/sketch.js (unused legacy p5 renderer) moved to archive/sketch_p5_legacy.js

---

## 2026-06-18 — AIOS v1 preservation pass

- Initialized git repository
- Committed all existing files (prototype + project briefs) as initial commit
- Created GitHub repository: filippos-swg/cosmic-oracle (private)
- Added requirements.txt documenting pyswisseph dependency
- Created AIOS v1 shell: AI_HANDOFF.md, PROJECT_BRIEF.md, PROJECT_CANON.md, DECISIONS.md, CHANGELOG.md, tasks/
- No code changes. No structural changes. Preservation only.

---

## 2026-05-20 — Prototype functional (snapshot date)

- Prototype running locally: sky.py → oracle.py → oracle.json → p5.js visual
- sky_state.json and oracle.json snapshots date from this session
- Signature system working: symbolic compression of planetary aspects into TOKEN format
- librarian.py token library populated with aspect-to-prose mappings
- p5.js visual rendering: ghost membrane + orbital rings + aspect lines
- Local development workflow confirmed (two-terminal setup)

---

## Earlier — Project origin (undated, inferred from brief versions)

- v1 brief: "Cosmic Oracle" — initial project concept, astronomical interpretation machine
- v2 brief: "Cosmic Oracle" — combined local prototype + web/API deployment direction + voice identity (self-aware cosmic librarian)
- v3 brief: renamed to "Astra" — added two-layer architecture framing, Cloudflare deployment plan, physical object direction, horoscope content system, voice rules
