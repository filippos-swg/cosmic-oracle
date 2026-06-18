# AI_HANDOFF — Cosmic Oracle / Astra

**Read this first. Every session.**

Last updated: 2026-06-18
Project status: Prototype functional, preserved. Web MVP not started.

---

## What This Project Is

A symbolic atmospheric interpretation machine.

> A strange machine that interprets incomprehensible symbolic weather into human language.

Not a horoscope app. Not a chatbot. Not generative art. A cold symbolic system with a warm, dry translation layer.

---

## System Architecture

Five files. One pipeline.

```
sky.py
  ↓ astronomical computation (Swiss Ephemeris)
  ↓ writes: sky_state.json, sky_signature.txt

oracle.py
  ↓ orchestration loop (runs every 60s)
  ↓ calls sky.py → calls librarian.py → writes visual/oracle.json

librarian.py
  ↓ token-to-language engine
  ↓ applies voice identity: dry, wry, self-aware cosmic librarian

visual/sketch.js
  ↓ p5.js, fetches oracle.json every 1s, renders atmospheric display

visual/server.py
  ↓ local HTTP server, serves visual/ at localhost:8000
```

**To run locally:**
```bash
# Terminal 1
python Astrologer_UPLOAD/oracle.py

# Terminal 2
python Astrologer_UPLOAD/visual/server.py
# open http://localhost:8000
```

**Dependency:** `pyswisseph` — install via `pip install -r requirements.txt`

---

## Two Layers — The Core Distinction

**Machine Layer:** sky.py → signatures. Cold, compressed, symbolic. Observatory-style.
Example signatures: `SUN_TRI_JUP`, `VEN_CON_SAT`, `STACK_CANCER_3`

**Human Translation Layer:** librarian.py → prose. Calm, intelligent, slightly wry. Grounded.
Voice: self-aware cosmic librarian. Reference: Douglas Adams as restraint, not imitation.

---

## Folder Structure

```
cosmic-oracle/
├── Astrologer_UPLOAD/          source code (name is legacy, not meaningful)
│   ├── sky.py                  astronomical truth engine
│   ├── oracle.py               orchestration loop
│   ├── librarian.py            voice/interpretation engine
│   ├── sky_state.json          last computed sky state (generated artifact)
│   ├── sky_signature.txt       last signature string (generated artifact)
│   └── visual/
│       ├── index.html          p5.js canvas page
│       ├── sketch.js           generative visual engine
│       ├── server.py           local HTTP server
│       └── oracle.json         last generated reading (generated artifact)
├── cosmic_oracle_master_project_brief_v2.md   older brief (historical)
├── Astrologer_UPLOAD/astra_master_project_brief_v3.md   current brief
├── aios/                       AIOS v1 context system
└── requirements.txt
```

---

## Open Decisions (do not resolve without Filippos)

- **Project name:** "Cosmic Oracle" (folder, v2 brief) vs "Astra" (v3 brief). OPEN.
- **`Astrologer_UPLOAD/` folder name:** Legacy staging name. Purpose unclear. OPEN — rename or restructure at next active work session.
- **Deployment:** Web MVP not started. Domain: stars.kidbutton.com. Cloudflare Worker + KV planned.
- **Physical object:** Retro TV/cabinet kiosk. Deferred until web MVP validated.

---

## Locked (do not change without approval)

- The two-layer architecture (machine layer / human translation layer)
- The signature system — `TOKEN_MEANINGS` in librarian.py is the intellectual core
- Visual aesthetic: black and white, spectral, oscilloscope-like, no gloss
- Voice: self-aware cosmic librarian. Never mystical, never parody.
- Pipeline sequence: sky.py → oracle.py → oracle.json → p5 visual

---

## Current Phase

Prototype functional and preserved.
Next work: stabilize pipeline → clean sketch.js → build typography layer → web MVP.
See PROJECT_BRIEF.md for priority order.
See tasks/ for next task when assigned.
