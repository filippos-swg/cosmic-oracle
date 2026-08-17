# AI_HANDOFF — ASTRA (Cosmic Oracle)

**AIOS version:** 2.0

**Read this first. Every session.** Then: ASTRA_MIND_v0.1.md (the character),
PROJECT_CANON.md (the identity), DECISIONS.md, CHANGELOG.md (newest-first).

Last updated: 2026-08-17
Project status: Content complete and curated; kiosk hardened. Awaiting
TV-calibration session and rotary-dial hardware — those are the only things
left before the piece can stand in a room. Ready to tag v1.0.

---

## What This Is Now

ASTRA is a physical art installation: a 1950s DUX television (B&W CRT) driven
by a dedicated old MacBook Pro, with a rotary telephone dial as the only input.
A visitor dials their date of birth and receives a personal, astronomically
real horoscope reading from "the librarian of the celestial archive" — a
Character Actor (see designing-intelligence project) whose voice runs on six
Douglas Adams operations, defined in ASTRA_MIND_v0.1.md.

Fully local, fully offline. No cloud. The web MVP (stars.kidbutton.com,
Cloudflare) is a LATER track that will reuse everything.

---

## To Run

```bash
bash run.sh          # starts oracle loop + server, opens the experience
# main page:        http://localhost:8000/tv.html   ← THE experience
# desktop dashboard: /index.html (design-parity reference, not the ceremony)
# CRT calibration:   /testcard.html
# stop:  pkill -f oracle.py; pkill -f server.py
```

Dev keys on tv.html: digits = dial · 000 mid-entry = reset date ·
Enter/Space = advance · Esc = abandon · M = mute · P = preview the ending ·
Enter during boot = skip boot.

---

## The Ceremony (tv.html — the product)

BOOT (calibration ritual) → IDLE (entity + rotating sky line + invitation) →
IDENTIFY (dial DD·MM·YYYY, validation, 000-reset, 30s timeout) →
CONSULT (theatre; /natal fetch happens behind it) →
FILE card → **CLARIFY** ("DIAL 1 — WORK / 2 — LOVE / 3 — THE OTHER THING";
25s timeout = archive chooses) → domain-shaped reading:
lead transit + LANDING sentence → ruler-story → observation → constraint →
second transit → temperament lens → **THE VERDICT** (plain register, real
moon deadline) → FOR THE RECORD (shelf/form/color) → file closes →
**ONE ITEM REMAINS** → a found LETTER or DREAM, in total silence.

Everything is in ONE file, visual/tv.html, organized in labeled blocks:
CONFIG (safe area, timings — TV calibration edits only this) · FOUND_ITEMS
corpus · DOMAINS/LANDINGS/VERDICTS/RECORD_* corpus · AUDIO module (WebAudio,
synthesized, silence-drop on found item) · state machine · ENTITY particle
engine (rim-defined figure, PROFILE lookup measured from reference images).

Typography: JetBrains Mono (self-hosted in visual/fonts/, Menlo fallback),
letterspaced, small scale, narrow tall center column. Machine layer and
librarian voice share the mono; found items are italic. NOTE: Courier Prime
was rejected (slab serifs); do not reintroduce serif or script faces —
tried and reverted (see CHANGELOG 2026-07-29).

Screens hold longer for longer copy (+35ms/char past 80, capped +5s).
Server sends Cache-Control: no-store — never let browsers cache the kiosk.

---

## Pipeline (unchanged spine, deepened organs)

```
sky.py        planets + speeds + retrograde + aspects with real
              applying/separating; speed-weighted signature
oracle.py     60s loop → visual/oracle.json (incl. readings_by_sign, all 12)
librarian.py  the voice: TOKEN_MEANINGS (20 curated), ASPECT_MODES (10
              verbs_one / 10 verbs / 14 omens / 8 constraints per mode),
              MARGINALIA (50), TRANSIT_NOTES (10/mode), ASIDE_CLOSINGS (20),
              QUIET_OMENS + QUIET_HEADLINES (unaspected rulers),
              SIGN_TEMPERAMENT (2 address + 2 lens per sign — LISTS, index
              them) + SIGN_RULERS, compose_* functions.
              Selection: _idx() salted hash, and _DayAllocator, which hands
              out lines without replacement so no two signs share a line on
              one date. Do not replace either with arithmetic — see CHANGELOG
              2026-08-14; a modulo pick cannot decorrelate two pools.
visual/server.py  static server + /natal?d&m&y endpoint: natal sun/moon
              (noon UT) + up to 6 transits vs current sky, no-store headers
```

Generated artifacts (gitignore candidates): sky_state.json,
sky_signature.txt, visual/oracle.json.

---

## Folder Map

```
visual/tv.html            THE experience (single file)
visual/index.html         desktop dashboard (reference)
visual/testcard.html      CRT calibration card
visual/fonts/             self-hosted woff2 (offline requirement)
visual/experiments/       history of the sandbox chain (poet → type →
                          sound → clarify); clarify was promoted to
                          production 2026-07-30. Keep as archaeology.
visual/preview.html       GENERATED review build: whole ceremony in one
                          file, no server. python3 tools/build_preview.py.
                          Gitignored. Never install this on the machine.
snapshots/v1-.../         frozen v1 desktop dashboard (runnable)
tools/                    verification harnesses — npm run check runs all.
                          verify_corpus.mjs (tv.html pools + selection),
                          verify_librarian.py (corpus, cross-sign no-repeat,
                          curated tokens vs real ephemeris), edge_cases.mjs
                          (14 kiosk input paths), walkthrough.mjs (ceremony),
                          orphan_sweep.mjs (every printable string rendered
                          at the real column width), typography_audit.mjs
kiosk/                    launchd agents + Chrome kiosk launcher.
                          bash kiosk/install.sh — prints the nine settings
                          launchd cannot do. install.sh uninstall to remove.
aios/                     this context system; STATUS_REPORT.md has the
                          full roadmap and MacBook appliance checklist
```

---

## Decisions Locked (see DECISIONS.md)

Name: ASTRA · input: rotary dial (USB keyboard emulation, digits only) ·
fully local architecture · found items (letter/dream) close every ceremony ·
balance rule for concreteness: body stays enigmatic, ONE landing sentence
per unit names the visitor's domain, only THE VERDICT speaks plainly
(~70% visitor-directed).

Canon guardrails still absolute: no mysticism, no coaching tone outside the
verdict, no fridge-magnet lines, no outside voices (Rumi CRAFT allowed in
found items — direct address, the turn — never the costume).

---

## Pending / Next Work

1. ~~CONTENT DEEPENING~~ DONE 2026-08-14/17. Corpus roughly tripled, the
   repetition fixed at its mechanical root (the pools carried no day term and
   the seed collapsed distinct birthdates), OBSERVATION/CONSTRAINT rewritten
   toward the visitor, day-level no-repeat allocation across signs, curated
   coverage 43% → 76% of days. Curated by filippos 2026-08-17.
   BEFORE ADDING CORPUS: run npm run check. Two of the defects fixed here
   were introduced by an earlier "improvement" that looked correct.
2. TV SESSION (blocked on hardware): testcard.html on the DUX →
   edit CONFIG.SAFE / TYPE_SCALE only.
3. ROTARY DIAL (hardware): ESP32/Arduino → USB keyboard digits.
4. KIOSK HARDENING: launchd, Chrome kiosk flags (incl.
   --autoplay-policy=no-user-gesture-required for the hum), see
   STATUS_REPORT.md §6.
5. v2.0: thermal receipt printer prints the found item (found.piece +
   stamp); optional per-sign memory conceits; web MVP (ASTRA_MIND becomes
   the LLM system prompt, per the Aio build-brief pattern).

## Workflow Note

Small design/CSS/copy tweaks: Claude Code locally on the Mac (direct disk,
instant reload). Larger structured sessions (content batches, features,
research): Cowork/cloud. Both must read this file first and log to
CHANGELOG.md. Git: commit after every session; watch for stale .git/*.lock
files if a cloud session committed via the device bridge (move them to
_to_delete/, never leave them).
