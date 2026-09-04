# STATUS REPORT — Cosmic Oracle / Astra
## State of the project + plan to finalize the installation

Date: 2026-07-16
Context: prototype is functional and design-matched. Target: a website running on a dedicated
old MacBook Pro, output to a 1950s DUX television (wooden cabinet, rounded B&W CRT, doors),
running as a physical art installation.

> Dated planning record, not current state. Read `aios/STATE.md` and the active hardware task
> first. Sections 5–6 remain useful technical reference for the tube and appliance setup.

---

## 1. Where the project stands

The full pipeline works end to end. `sky.py` reads real planetary positions from the Swiss
Ephemeris, now including longitudinal speeds, retrograde flags, and true applying/separating
determination for every aspect. The signature system prioritizes fast-moving planets, so the
daily token stream actually changes daily instead of being permanently occupied by outer-planet
aspects that hold for months. `librarian.py` translates tokens through the curated voice table,
and — new — when no curated token matches, it composes a reading from the tightest
personal-planet aspect in the same archival voice, so the generic fallback text now only
appears on genuinely quiet skies. `oracle.py` orchestrates the loop and writes the generated
oracle payload every 60 seconds.

The frontend (`visual/index.html`) matches the design reference closely: Courier Prime
typewriter mono, corrected moon-phase mathematics (the cycle-vs-illumination bug is fixed, and
the strip is a symmetric −3…+3 days with today centered), transits with full planet names,
degree°minute′ orbs and real A/S flags, retrograde markers in the celestial log, and the
particle entity rebuilt to the close-up reference: a bright ragged rim ribbon tracing a dome
head and wide shoulders, dark face, uniformly dust-filled torso, dissolving base, full-frame
starfield. 100,000 particles, software-rendered.

The naming question described in this dated report was resolved later: the piece is ASTRA and
the repository remains `cosmic-oracle`.

---

## 2. What "finalize a website" means here — two tracks, one recommendation

There are two different products hiding in the brief. The **installation** is a kiosk: one
MacBook, one TV, no visitors' phones, no internet dependency. The **public web MVP**
(stars.kidbutton.com, Cloudflare Workers/KV) is a separate, later track. Everything the
installation needs can and should run entirely on the MacBook: `oracle.py` as a background
service, the static site served locally, the browser in fullscreen kiosk mode. This keeps the
gallery piece immune to Wi-Fi failure, hosting outages, and expired certificates. The cloud
architecture stays in the plan as Phase F, unchanged, and nothing we build for the kiosk is
wasted — the state machine, TV layout, and per-sign reading engine all port directly to the
web version later.

Recommendation: finalize the installation as a **fully local website**. The MacBook is not a
"kiosk client of a cloud brain" for v1 — it is the whole organism.

---

## 3. The full UX — how the experience runs

The current page is a passive dashboard. The installation needs a *ceremony*. Proposed state
machine, five states:

**IDLE / ATTRACT.** The entity breathes in the starfield. The celestial log ticks. Every few
minutes the current day-reading headline drifts through. This state must be self-sufficiently
beautiful because it is what most passers-by will see. An invitation line appears periodically,
in the librarian's voice: "THE ARCHIVE IS OPEN. IDENTIFY YOURSELF TO RECEIVE YOUR FILE."

**IDENTIFY.** The visitor provides their date of birth. Large digit slots appear on screen
(DD · MM · YYYY) and fill one by one as the visitor dials. See §4 for the input hardware
question. A wrong digit can be cleared by a dedicated action; an abandoned entry times out
back to IDLE after ~30 seconds. No name, no other data — a date is enough and keeps the
ritual quick.

**CONSULT.** Three to six seconds of theatre. "CONSULTING THE EPHEMERIS…" — the entity swells
and agitates, the data stream accelerates, the system status bar sweeps. This pause is doing
real work: it converts a lookup into a divination.

**READING.** The personalized reading, revealed in sections per the brief's content structure
(orientation → theme → tension → attention → closing), one section at a time in large type,
with the visitor's sign named archivally: "CANCER. THE ARCHIVE HOLDS YOUR FILE." The entity
settles into a sign-tinted behavior (element-driven: fire agitation, water drift, air
scatter, earth stillness). Hold the final screen ~45 seconds, then a closing aside
("Please return borrowed certainty by closing time."), then fade to IDLE.

**SIGN-OFF (scheduled).** At closing time each night, a broadcast-era sign-off card:
"TRANSMISSION ENDS. THE SKY CONTINUES." — and at opening, a resumption card. Costs almost
nothing, deeply fits the object.

**Startup screen: yes.** When the MacBook boots and the page loads, it should not snap
straight into the dashboard. A boot ritual — the ORACLE v.3.7 identity, a calibration
sequence (ephemeris sync counting up, status bar filling), then settle into IDLE. This doubles
as an honest loading screen while the first oracle.json arrives, and it is the moment the
piece states its name (see the open naming decision).

**What the date of birth actually buys us.** From DD·MM·YYYY, swisseph computes the visitor's
natal sun sign — and, using noon as default birth time, their natal moon sign is correct in
roughly 93% of cases. That enables three layers of personalization, in increasing depth:
(1) sign temperament filtering of the daily reading, per the brief's interpretation
hierarchy — requires writing 12 sign-temperament voice fragments for the librarian;
(2) natal-transit hits — "Saturn is currently squaring your natal Sun" — computed with math
sky.py already has, giving readings that differ meaningfully person to person on the same
day; (3) the birth-sky signature — run the existing signature engine on their birth date and
let the librarian compare the two skies ("You were filed under a Pisces stack. Today's sky
disagrees with your paperwork."). Layer 1 is required for launch; layers 2–3 are cheap,
high-payoff follow-ups since the machinery exists.

Implementation shape: `oracle.py` generates readings for all 12 signs each cycle into
oracle.json (readings are cheap to compose); the frontend state machine selects by the sign
derived from the dialed date. Natal-transit personalization (layer 2) adds a tiny local
endpoint to `server.py` that runs a natal computation on demand — still fully offline.

---

## 4. The input hardware question

The one genuinely open UX decision. Options, in period-appropriateness order:

**Rotary telephone dial (recommended).** A bakelite rotary dial (or whole period telephone)
wired through a €10 microcontroller (ESP32/Arduino) that emulates a USB keyboard. The visitor
dials eight digits; each digit lands in a slot on screen with a mechanical clunk. Dialing your
birthdate into a 1950s television via a rotary phone is the strongest single interaction this
piece can offer: era-correct, self-explanatory, robust, and slow in exactly the right ceremonial
way. Dial 0 twice to clear/restart.

**The TV's own knobs.** Poetic but problematic: destructive to the object, only practical for
a 12-position sign selector rather than a full date, and the brief's v1 model (sign selection
only) explicitly deferred DOB. If the DOB requirement stands — and the question you're asking
suggests it does — the TV knobs are the wrong input.

**Hidden numeric keypad / brass keypad.** Functional, faster, less magical. Acceptable
fallback if the rotary dial proves flaky in testing.

**No input at all.** Pure ambient mode remains valuable as the IDLE state and as a fallback
if input hardware fails mid-exhibition — the piece must degrade gracefully to the daily
reading. This behavior should be explicit in the state machine (a config flag).

---

## 5. TV legibility — the honest audit

The DUX set is a rounded-corner B&W CRT behind glass, fed (via the converter chain) at
PAL-era resolution. Practical assumptions: effective canvas ≈ 720×576 before overscan,
5–10% overscan crop on every edge, heavy corner rounding from the tube mask, and real-world
luma resolution well below 576 lines once the signal chain and phosphor are done with it.
The monochrome design is a perfect match for the B&W tube — that part costs nothing.

Current layout is a 1500×1000 stage. Scaled onto 720×576 it renders at 0.48×. What survives:

| Element | Designed px | On TV px | Verdict |
|---|---|---|---|
| Headline | 44 | ~21 | Legible — the only survivor |
| Reading body | 13 | ~6 | Illegible |
| Celestial log rows | 11.5 | ~5.5 | Illegible |
| Section headers | 10.5 | ~5 | Illegible |
| Transits panel | 10 | ~4.8 | Illegible |
| Moon strip moons | 40 | ~19 | Visible, cramped |
| 1px rules/dashes | 1 | <0.5 | Gone / interlace flicker |
| Particle entity | — | — | Survives beautifully; CRT adds free grain |

Conclusion: the desktop dashboard cannot be the TV experience. It stays as the design-parity
reference and the future web version. The TV needs a dedicated **tv.html** built on three
rules: 4:3 stage (1024×768 design space) with all critical content inside a rounded "safe
ellipse" of roughly the central 80%; minimum text size ~26px in that design space (≈ 20
scanlines delivered) with the headline at 72–96px; and no 1px lines, no dense dot textures —
2px minimum strokes, slight glow instead of hairlines, because thin horizontals shimmer on an
interlaced CRT.

Since one 1024×768 screen holds perhaps one panel's worth of information at those sizes, the
TV experience becomes **sequential rather than simultaneous** — which is exactly what the
state machine in §3 already implies. IDLE rotates slow scenes (entity → headline → moon strip
→ one or two instrument readouts, 20–30s each, like late-night programming); READING reveals
one section at a time. Nothing is lost; the dashboard's density is redistributed into time.

**First concrete step before any resizing: a test card.** A `testcard.html` — calibration
grid, concentric circles, safe-area rectangles at 70%, 80%, and 90%, and sample text at 18,
22, 26, 32, and 44px — displayed on the actual DUX through the actual converter chain. Ten minutes with that
page answers every sizing question with measurements instead of assumptions, and tells us the
true visible area of the rounded mask. Build this first, tune tv.html to what the tube
actually shows.

---

## 6. The MacBook as a dedicated appliance

The machine must behave like a component, not a computer. Checklist: auto-login; the oracle
loop and local server installed as launchd agents with KeepAlive (auto-restart on crash);
browser launched at login in kiosk mode (`--kiosk --noerrdialogs --disable-session-crashed-bubble`)
pointed at the local tv.html; a watchdog that reloads the page if oracle.json goes stale;
`caffeinate`/energy settings so the machine never sleeps with the lid closed (closed-lid
operation needs power + display adapter connected); cursor hidden via CSS; notifications, Spotlight
indexing, and auto-updates disabled; Wi-Fi optional — the piece must boot to a working state
with no network (it already tolerates fetch failure; the ephemeris is local). Output
resolution set to match the converter's happiest input (typically 800×600 or 720×576);
overscan/underscan tuned on the converter, then fine-tuned in CSS via the test card.
Performance: 100k particles is fine for design review on a modern machine, but plan on
`COUNT` ≈ 40–60k and DPR 1 for the old MacBook — at CRT resolution the difference is
invisible. A weekly scheduled reboot (cron) is cheap insurance for long exhibitions.

---

## 7. Roadmap

**Phase A — Measure the tube.** Build testcard.html, connect the chain, photograph the
screen, record: true visible area, safe ellipse, minimum legible size, converter quirks.
Half a day, mostly hardware fiddling. Everything downstream depends on these numbers.

**Phase B — tv.html.** The 4:3 TV-mode page: entity full-frame, scene rotation, large-type
layout system built to Phase A's measurements. The particle engine and data plumbing are
reused as-is. 1–2 sessions.

**Phase C — The ceremony.** State machine (IDLE → IDENTIFY → CONSULT → READING → IDLE),
startup/boot ritual, sign-off cards, DOB entry UI, keyboard-event input handling (works with
any input hardware that types digits — testable from a regular keyboard before the dial
exists). 1–2 sessions.

**Phase D — Personalized content.** Twelve sign-temperament fragments for the librarian
(layer 1), all-signs readings in oracle.json, natal sun/moon computation, and if appetite
allows, natal-transit hits (layer 2). This is mostly *writing* in the established voice —
the code is the easy part. 1–2 sessions plus editorial passes.

**Phase E — The rotary dial.** Microcontroller + rotary dial → USB keyboard emulation.
Independent of all software phases; can be prototyped any time. One hardware afternoon plus
debounce tuning.

**Phase F — Appliance hardening.** The §6 checklist on the actual MacBook, soak test running
overnight, weekly reboot schedule. One session.

**Phase G (later, unchanged from brief) — Public web MVP.** Cloudflare Workers/KV,
stars.kidbutton.com. Everything from Phases B–D ports.

Suggested order: A → B → C (with keyboard input) → D → F → E — the dial is the only custom
hardware and shouldn't block the software being finished; the keyboard makes everything
testable without it.

---

## 8. Risks and open items

The converter chain is the biggest unknown — cheap HDMI/VGA-to-composite converters vary
wildly in sharpness, sync stability, and overscan behavior; Phase A exposes this immediately.
Content repetition is the slow risk: a long-running installation will show the same curated
tokens to repeat visitors — Phase D's natal layers and the composed-reading engine are the
mitigation, and the token library can keep growing editorially. The naming decision
(Cosmic Oracle vs Astra) blocks the startup screen copy. And one physical note: the cabinet
doors are part of the dramaturgy — a piece that lives behind doors can have an "opening the
archive" moment each day; consider whether visitors or staff open them, because it changes
whether the sign-off card is ever seen.
