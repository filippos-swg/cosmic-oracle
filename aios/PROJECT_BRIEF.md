# PROJECT_BRIEF — Cosmic Oracle / Astra

Source: consolidated from v2 (cosmic_oracle_master_project_brief_v2.md) and v3 (astra_master_project_brief_v3.md).
v3 supersedes v2 except where noted.

---

## Current State

Local Python/p5.js prototype is functional.

Working:
- `sky.py` — Swiss Ephemeris integration, planetary positions, aspect calculation, signature extraction
- `oracle.py` — orchestration loop (60s update cycle)
- `librarian.py` — token-to-language interpretation engine with voice identity
- `visual/oracle.json` — structured reading output
- `p5.js` fetch system — live updating atmospheric visuals

Not started:
- Web MVP
- Cloudflare deployment
- Physical object

---

## Current Build Priorities

### Phase 1: Stabilize local prototype

1. Stabilize the `oracle.py → oracle.json → p5 fetch loop` — robust, predictable, no fragile path assumptions
2. Clean `sketch.js` — remove dead drawing logic, organize into clear sections (fetch / state / rendering / typography / helpers)
3. Build the typography layer — hierarchy, spacing, atmospheric overlays, archival labels, orbital text where appropriate. No glitch aesthetics.
4. Evolve the ghost entity — less blob, more entity, more membrane physics, more field intelligence
5. Add planetary metadata overlays — instrument readouts (`SUN 14° PIS`, `VEN ∧ SAT`, `ORB 0.21`)

### Phase 2: Web MVP

Target domain: `stars.kidbutton.com`

Planned architecture:
- `stars.kidbutton.com` — self-built public frontend
- `stars-admin.kidbutton.com` — private Sky State admin UI (Cloudflare Access protected)
- Cloudflare Worker — API brain
- Cloudflare KV — stores Sky State, cached horoscopes, sign cards
- OpenAI API — language generation

Worker endpoints planned:
```
GET  /v1/health
GET  /v1/sky-state
PUT  /v1/sky-state
GET  /v1/horoscope?sign=aries
```

Web MVP steps (in order):
1. Set up Cloudflare domain/DNS
2. Create Worker `/v1/health` endpoint
3. Create KV namespaces
4. Store `sky_state:today` manually
5. Store initial sign cards
6. Create `/v1/horoscope?sign=aries` endpoint
7. Build minimal admin UI
8. Connect public frontend

Do not attempt all of these at once. Start with the smallest working loop.

### Phase 3: Physical Object

- Retro TV/cabinet object, screen replacement or embedded display
- Mac mini (2011/2012 era), 8GB RAM, SSD, macOS High Sierra
- Browser fullscreen/kiosk mode
- The local machine is a kiosk client. The brain lives in the cloud.

Deferred until web MVP is validated.

---

## User Interaction Model (Web MVP v1)

1. Idle / attract state
2. User selects zodiac sign
3. Short "reading the sky" pause
4. Sign-specific visual response
5. Horoscope reveal
6. Calm closing / return invitation

V1: sign selection only. Do not add date-of-birth input until v2 — adds friction too early.

---

## Horoscope Content Structure

Five internal sections per reading (may not all be visible as separate blocks):
1. Orientation
2. Theme
3. Tension
4. Attention
5. Closing

Interpretation hierarchy:
1. Moon Sign — how the day feels
2. Primary Planet — what energy is active
3. Lunar Phase — opening / building / peaking / releasing
4. Secondary Planet — restraint or modifier
5. Zodiac Sign Temperament — personal filter

If influences conflict: Moon outweighs planets. Sign temperament outweighs all. Do not resolve tension too neatly — describe it.

---

## Strategic Warning

Do not over-engineer prematurely.

Wrong direction:
- unnecessary frameworks
- excessive abstraction
- premature backend complexity
- adding features before stabilization
- turning this into a generic app

Right direction:
- small, understandable changes
- preserve the symbolic architecture
- preserve atmosphere
- working loops over ambitious systems
