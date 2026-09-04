# TASK — Hardware Installation (the physical build)

**Status:** IN PROGRESS — physical installation is the remaining phase.
Desk work finished 2026-08-18 (TV identified, picture chain specified, dial firmware written and tested).
What remains needs the physical objects in a room.
**Supersedes:** ASTRA_TECHNICAL_HANDOFF.md (recovery-era document; its
software, runtime, folder and Cloudflare sections are obsolete — see
"Resolved since" below. Its TV-identification discipline and working
principle are carried forward here.)
**Read first:** `aios/STATE.md` → `aios/CANON.md` → `aios/LOG.md` →
`aios/ASTRA_MIND_v0.1.md` → **exhibition/BUILD_GUIDE.md** →
exhibition/PICTURE_CHAIN.md → firmware/README.md → exhibition/RUNBOOK.md →
kiosk/install.sh + kiosk/astra-kiosk.sh → aios/STATUS_REPORT.md §5–6.
BUILD_GUIDE.md is the operative document: this is a solo, non-technical
build, and everything is sequenced and de-jargoned there.
(exhibition/HARDWARE_DIAL.md is kept as the purchase record; its two-wire
firmware plan is superseded — see Phase A.)

## Where things stand (do not rediscover this)

- SOFTWARE: DONE. v1.0 + launch revision (personal margins, redesigned
  breathing sound bed) on GitHub main. Do not reopen ceremony/content
  code in this session except the CONFIG calibration block in
  visual/tv.html.
- APPLIANCE MAC: RESOLVED & RUNNING. Old MacBook Pro, user `astrologer`,
  host `Astrologer-Core`, repo at ~/Projects/cosmic-oracle, stack runs
  via run.sh. kiosk/install.sh (three launchd agents, KeepAlive,
  dedicated Chrome profile, power-cut recovery) exists — verify
  installed, then soak-test overnight.
- PHONE: ACQUIRED. LM Ericsson DBH 1001 bakelite ("modell 1947") — the
  stage phone. Försvaret surplus bare dial (Fingerskiva M 3926-990019)
  ordered as bench/firmware unit — confirm arrival.
- **TV: IDENTIFIED 2026-08-18 — DUX TYP V6397.** 220 V växelström (AC
  only → mains transformer → chassis almost certainly isolated, confirm
  with a meter), 170 W, **300 Ω balanced antenna terminals, no AV input**,
  Swedish "S" mark, multi-position front tuner. Not yet connected, not yet
  serviced. Phase B is unblocked.
- **MICROCONTROLLER: DECIDED 2026-08-18 — Raspberry Pi Pico**, Arduino Pro
  Micro as the pre-flashed spare. ESP32 dropped: a WiFi stack has no
  business in an offline piece. Neither board bought yet.
- **FIRMWARE: WRITTEN AND TESTED (firmware/).** Both boards, same state
  machine, Swedish mapping, 18 automated checks passing against
  synthesized waveforms. Untested on a real dial — that is Phase A.

## Resolved since the old handoff (do not relitigate)

Installation computer (the MBP, not a Mac mini); kiosk/autostart
(built: kiosk/); Python compatibility (fixed in repo); local vs cloud
(fully local, decided and shipped); web deployment (later track: static
site + JS ephemeris on Cloudflare Pages — no Workers/KV needed);
the p5 sketch (archived; visual/tv.html is the product).

## ⚠ THE SWEDISH DIAL TRICK — critical

Swedish rotary dials are shifted vs the international standard:
**0 sends 1 pulse, 1 sends 2, … 9 sends 10 → firmware: digit = pulses − 1.**
Faceplate tell: 0 printed beside 1 at the fingerstop (visible on the
purchased Ericsson). Getting this wrong shifts every birthdate by one
digit. Test end-to-end with a known date before anything is closed up.

## ⚠ THE OTHER RF TRICK — new, same class of expensive mistake

Sweden broadcast **625-line CCIR System B on VHF**. The modulator must
cover **VHF Band I/III** and be set to **System B/G with a 5.5 MHz sound
carrier**. Almost every cheap "AV to RF" box is UHF-only (this set has no
UHF tuner at all → nothing) or PAL I / 6.0 MHz (→ picture, no sound).
Full spec and parts list in exhibition/PICTURE_CHAIN.md.

## Phases

**A. Dial firmware (bench). NO SOLDERING REQUIRED — buy a Pico *H* (headers
pre-soldered) and a screw-terminal expansion board; the surplus bench dial
already has screw terminals, so it is four wires and a screwdriver at both
ends.** Firmware is written; this phase is electrical, not software. Find the
IMPULSE and OFF-NORMAL contacts on the surplus dial with a continuity meter
(dial 9, listen for ten beeps — procedure in BUILD_GUIDE.md), not by wire
colour → GPIO with internal pull-ups. **Wire the off-normal contact.** The old two-wire plan
is superseded: in the Swedish mapping a single pulse is a legitimate `0`,
so one spurious pulse types a `0` into a visitor's birthdate and the
machine reads the wrong day with complete confidence. The test suite
demonstrates the difference. Then run the bench checklist in
firmware/README.md, and only then migrate into the Ericsson's base —
original wiring untouched, fully reversible, no new holes in bakelite.
Hook switch stays unwired for v1.

**B. Picture chain — RECOMMENDATION REVISED 2026-08-18.** Ask the
technician who recaps the set to add a composite video input (and an audio
input) while it is open; the chain then becomes one yellow plug and the
modulator is not bought at all. The set is permanently modified — a real
loss, outweighed for a solo build. Modulator route retained as the fallback
if the technician declines. **STEP 0: the set has never been powered on and
must not be, before the technician sees it.** See
exhibition/PICTURE_CHAIN.md for the chain, parts, costs and bring-up
order. In short: service the set first (1950s capacitors, then eight
hours a day in a closed cabinet — recap and dim-bulb bring-up by a
technician, who also confirms chassis isolation and which channels the
tuner covers); **never open the back yourself, a CRT holds a lethal
charge unplugged**; prove the modulator on a modern analog tuner before
it goes near the DUX; first page on the tube is **/testcard.html**, not
the ceremony; then calibrate ONLY `CONFIG.SAFE` and `CONFIG.TYPE_SCALE`
in visual/tv.html and commit the values with a note naming the set.
Open sub-decision: consumer HDMI→CVBS box (~300 SEK, buy three) vs
Blackmagic two-box (~3 800 SEK) — decide after watching the cheap one
cold-boot twenty times.

**C. Sound.** Whichever route, the sound must come out of the object —
where a sound comes from is part of what the object is; a laptop on the
floor is located instantly and the illusion goes. Preference order: audio
input added by the technician into the TV's own sound stage → a small
powered speaker hidden in the cabinet → the Mac's own speakers, last, and
only if the Mac ends up outside the cabinet. (On the fallback modulator
route the MT47 carries audio on the 5.5 MHz subcarrier and it arrives at the
TV speaker for free.) Judge
the redesigned bed **through that speaker**: a 1950s elliptical in a
wooden cabinet will eat the bottom of the drone and exaggerate the
whistler, and the correction will be larger than feels reasonable on a
laptop. Levels are labelled numbers in the AUDIO module. Verify
`--autoplay-policy=no-user-gesture-required` survives in astra-kiosk.sh —
without it the piece is silent with no error to explain why.

**D. Assembly.** Mac in/behind the cabinet: mind HEAT (170 W of valves
plus a MacBook in a closed teak box — Mac *below* the tube chassis, never
against the back panel, never block the vents, cabinet top stays clear
because it is the air exit). Dial/phone planted at hand height beside the
cabinet, cabling hidden, wall label (exhibition/WALL_LABEL.md) printed —
instruction panel by the phone.

**E. Opening checklist.** Now written as the acceptance test at the end of
exhibition/RUNBOOK.md. Ten cold boots out of ten reaching IDLE with no
keyboard, mouse, desktop or terminal ever visible; 24 h soak with zero
phantom digits; one full ceremony dialled on the real dial with a known
birthdate; sound and CONFIG values committed; doors-open ritual decided.

## Deliverables

- [x] `firmware/` — dial sketch, both boards, tested (2026-08-18)
- [x] `exhibition/PICTURE_CHAIN.md` — chain, parts and bring-up (2026-08-18)
- [x] `exhibition/RUNBOOK.md` — open/close, triage and acceptance (2026-08-18)
- [x] `aios/LOG.md` entry (2026-08-18)
- [x] Final hardware list after the TV was identified, in PICTURE_CHAIN.md
- [ ] Calibrate `CONFIG.SAFE` / `CONFIG.TYPE_SCALE` on the tube
- [ ] Fill in RUNBOOK contacts for the TV technician
- [x] `exhibition/BUILD_GUIDE.md` — solo, non-technical, no soldering (2026-08-18)
- [ ] Take the TV to a technician and ask the four listed questions
- [ ] Buy the USB-C-to-HDMI adapter for the Mac
- [ ] Confirm the HDMI2AV box has a PAL switch
- [ ] Buy the Pico H, screw-terminal board and multimeter
- [ ] Decide converter grade if the modulator route is forced
