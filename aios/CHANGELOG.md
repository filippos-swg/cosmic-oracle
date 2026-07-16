# CHANGELOG — Cosmic Oracle / Astra

Newest-first.

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
