# CHANGELOG — Cosmic Oracle / Astra

Newest-first.

---

## 2026-08-17 — Launch revision: personal margins + sound redesign

Response to final gallery feedback ("readings could feel more about ME";
"the sound reads as hardware noise").

- PERSONAL MARGINS: the reading's two most impersonal screens now turn
  toward the visitor. OBSERVATION carries a line from the new ADDRESSED
  pool (14 you-facing annotations — "The above concerns you even where it
  appears not to. Especially there."); CONSTRAINT is countersigned with
  the visitor's own coordinates via FILE_STAMPS ("Countersigned for ♏ 10°
  by the night clerk."). Seeded with pickIdx (new SALT.addressed/stamp).
- SOUND REDESIGN: the bed no longer resembles a fault. The drone carries
  a real interval (72 Hz root + fifth + 0.4 Hz-beating octave pair, clear
  of mains frequencies), the whole bed breathes on the entity's ~11 s
  cycle, the noise band moved up into airy shortwave ether (2.2 kHz), and
  rare falling ionosphere whistlers punctuate idle/reading — unmistakably
  composed. Clunks, ticks, consult murmur, and the found-item silence
  are untouched.
- Verified: full walkthrough clean, no JS errors, personalized notes
  render correctly in layout.

---

## 2026-08-17 — Harness portability (second machine, second lesson)

`npm run check` on the installation machine: both content harnesses passed,
all four Playwright harnesses died on

    Failed to launch chromium because executable doesn't exist at
    /opt/pw-browsers/chromium

That path is the cloud container's. It was hardcoded in four files — the same
class of mistake as the absolute `/tmp` default fixed earlier the same day, and
it survived because the container is the only place these had ever run.

- New `tools/browser.mjs`, one shared launcher for all four. Resolution order:
  `$ASTRA_CHROMIUM`, then the container path *if it exists*, then Playwright's
  own bundled browser — which is the normal case on a Mac.
- On failure it prints the one command that fixes it
  (`npx playwright install chromium`) instead of a stack trace.
- `npm run browsers` added for the one-time install, and `npm run sweep`
  (dump + orphan sweep) since the sweep needs its corpus dump refreshed first.

Verified both ways: through the container path here (edge 14/14, walkthrough,
sweep, typography all clean) and with the path forced invalid, which produces
the instruction rather than the trace.

Standing lesson, now twice: anything absolute in `tools/` is a bug waiting for
the second machine. There is no third machine to catch the next one.

---

## 2026-08-17 — Curated-lead allocation (found by running the harness on the real machine)

`npm run check` passed here and failed on the installation machine: **366/366
days sharing lines across signs, worst 5 signs on one line.** Not flakiness —
a real defect that this container could not see.

**Why the harness lied.** The cross-sign sweep reads `sky_state.json`, which is
*generated*. This machine's sky happened to contain no curated token at all
(all MER_/VEN_ aspects), so the entire curated-lead path went untested here
while running constantly there. A green harness on one machine proved nothing
about the other.

Three defects behind it, in order of severity:

1. **A curated lead had almost no pool.** Its omens were the token's own three
   lines, and `base_omens` were those same three lines uniq'd away — so two
   signs led by one token (Cancer and Capricorn both land on MOO_OPP_SAT) drew
   from a three-line pool, exhausted it, and repeated. Curated leads are now
   widened with the composed omens and phrasings for the same aspect plus a
   quiet-line tail: ~13 candidates instead of 3, and the curated writing still
   leads.
2. **One sign could get the same line twice in its own reading.** The
   allocator's exhaustion fallback skipped lines already taken in that *call*
   but not lines the sign had been handed a moment earlier. Worse than two
   signs sharing one. `take()` now accepts `avoid=` and degrades in order:
   unclaimed first, then a line another sign holds, and only last one of this
   sign's own.
3. **Composed leads starved the signs served last.** `compose_from_aspect`
   returned six of fourteen mode omens. Enough for the signs served early,
   not for Aquarius at the end of the rotation on a day when several signs led
   with the same aspect. It now returns the full pool in seeded order, and
   every lead carries a quiet-line tail.

**Harness fixed too, which matters more than the code.** New check [4b]: force
each of the 20 curated tokens into the signature in turn and sweep 60 days
each. 1,200 token-days, plus the 366 real-sky days, plus 90 degenerate-sky
days. That is the check that would have caught this here on Friday.

All green: corpus, librarian (10 checks), edge 14/14, walkthrough, typography
165 screens, orphan sweep 3,818 strings.

---

## 2026-08-17 — Curation pass; v1.0 ready

filippos curated. Seven changes applied out of 452 new lines.

**Cut (1).** LANDINGS other/Square: "you will be tired in a way sleep does not
fix. That is the signal, not the fault." The closest thing to a diagnosis in
the corpus, and the second sentence is reassurance, which the librarian does
not do. It also carried a failure mode nothing else does: dialled by someone
actually struggling, an unattended machine tells them their exhaustion is
meaningful. Replaced with "the thing you keep postponing is not waiting for a
better week. It has checked."

**Tightened (6).**
- "Add no verdict" collided with THE VERDICT, a named screen two beats later →
  "Nothing further is required."
- "not a symptom" raised the clinical frame in order to deny it → "not weather".
- "Today is the day it does" had *today* twice → "It will not be this easy again."
- Three verdicts were productivity-blog rather than archive: "the rest follows
  more easily than you expect" → "That is not cheating."; "the thing that
  scares you slightly" → "Say yes to one thing you would normally decline.";
  "Rest properly tonight" → "Leave it where it is tonight."

**Kept against my own objection**, recorded so the argument is not relitigated:
"a limit you have treated as a personality trait comes up for review today" and
"what you are calling a mood today is a decision waiting to be made". Both are
therapy-shaped. Both survive because they *note* rather than instruct, which is
where PROJECT_CANON draws the line.

**Full suite after:** corpus pass, librarian pass (9 checks), edge cases 14/14,
walkthrough clean, typography audit 165 screens, orphan sweep 3,818 strings
zero orphans, oracle.json regenerated, preview rebuilt.

AI_HANDOFF.md updated to the current state; TASK_language_expansion.md filed to
aios/tasks/done/. The task list in the handoff no longer has a content item —
what remains is hardware.

**v1.0 is ready to tag.** Nothing in software blocks the piece now.

---

## 2026-08-14 — Review of the day's work (three defects found, all fixed)

Adversarial pass over everything shipped today, looking specifically at what
the harnesses could NOT see.

**1. The transit line and its note moved in lockstep.** `compose_transit` drew
the verb with `_pick(verbs_one, variant, 3)` and the note with
`notes[variant % len(notes)]`. With both pools at 10, `(seed * 31 + 21) % 10`
reduces to `(seed + 1) % 10` — so the verb index was always exactly one ahead
of the note index. Measured: **10 distinct (line, note) pairs out of a possible
100**, and any two visitors whose dates differed by a multiple of ten received
an identical transit line AND note. This is the same defect fixed in tv.html in
batch 1, still live in librarian.py, on the two most visible screens in the
reading. `_pick` now runs a salted integer hash. After: 99/100 pairings occur.

**2. Fixing that broke sign distinctness — caught by the existing sweep.**
The old arithmetic accidentally guaranteed that adjacent signs drew different
verbs, so two signs whose rulers share a single aspect (Taurus and Gemini on
one Mercury-Venus sextile) never collided. The hash removed the accident and
cross-sign repeats jumped to **101 of 366 days**. Fixed properly rather than
reverted: `compose_from_aspect` now returns every phrasing the aspect can take,
and `build_sign_readings` allocates the headline through the same day allocator
as the omens. Back to 0/366 — and now guaranteed by construction rather than by
a modulo coincidence.

**3. `install.sh` rewrote a tracked file.** It sed-substituted the repo root
into `kiosk/astra-kiosk.sh` in place, so installing left the working tree
permanently dirty and a second install templated an already-templated path. The
root now arrives as argv from the launchd agent; installing touches nothing in
the repo.

Also: `tools/typography_audit.mjs` had an absolute `/tmp` path from the build
machine baked in as its default — now resolved relative to the repo, with
`ASTRA_URL` to override. Added `package.json` (harness scripts, `npm run
check` runs all four) and gitignored `node_modules`, `package-lock.json` and
the generated `visual/preview.html`.

**4. The preview had gone stale against the fix.** `build_preview.py` mirrored
the OLD `_pick` arithmetic in JS, so after the hash change the preview would
have shown different transit lines from the machine it previews. Its `pIdx` now
mirrors `librarian._idx` bit for bit — asserted against Python across a seed
range. Residual and inherent: the ~0.3deg moon approximation reorders some
transits, and since the variant is seed+index a reordered transit draws a
different verb and note. Measured 10 of 14 sentences identical to the live
server across three dates, the rest differing by position, not selection. Now
documented in the file rather than left to be discovered.

**5. Sampling was never going to be enough.** After the hash change a different
verb got drawn and a NEW orphan appeared — "COUNTERSIGNED" alone on a line —
which the 165-screen ceremony audit had never seen because that verb had never
come up. Sampling proves the lines that happened to be selected, nothing more.

New: `tools/dump_corpus.py` + `tools/orphan_sweep.mjs`. The first enumerates
every string the reading screens can print — every transit sentence the composer
can build from every desk x verb x target, every headline variant, every omen,
constraint, landing, verdict and verse: **3,818 distinct strings**. The second
renders each one in the class it will actually be printed in, at the real
column width, and reports any that would leave a line holding a single word.

First run: 12 orphans, all long words at a narrow measure — "correspondence,",
"investigations", "countersigned", "indistinguishable". Measures widened to
60% / 58% / 56% (the side panels sit at 19% per edge, so 62% is the ceiling),
and the single remaining offender fixed in the corpus instead: "are conducting
parallel investigations into one another" became "are investigating each other,
in parallel" — shorter, and better. **Now zero of 3,818.**

`text-wrap: balance` replaced `pretty` on the body too: `pretty` only protects
the last line, and every one of these was a long word landing mid-block.

New regression check, verify_librarian [9]: transit line and note must not move
together — fails if fewer than 80% of possible pairings occur.

**Full suite green:** corpus pass, librarian pass (9 checks), edge cases 14/14,
walkthrough clean, typography 165 screens / zero orphans, all four pages serve
200, natal endpoint returns transits, oracle.json regenerates.

---

## 2026-08-14 — Typography pass (Refactoring UI, no layout change)

Reported: lines left holding a single word — "bend", "owner.", "6-M.".

**Root cause was the measure, not the writing.** `CONFIG.SAFE` shrinks every
screen to 80% of the stage, so a `max-width: 42%` poem column was really ~37
characters wide while the authored verse ran to 45+. Every authored line
wrapped, and each wrap left an orphan. Measured the real rendered column in the
browser (780px, 12.44px per character at 20px) rather than estimating, then
sized the poem measure to the longest line in the corpus — 74%, at 19px. Seven
authored lines that ran past 49 characters were shortened; the turn in each is
untouched.

- `text-wrap: balance` on the short blocks and notes, `pretty` on the long
  ones. `pretty` alone still left "6-M." stranded at two lines; `balance` evens
  them and the orphan cannot occur. Both are progressive — older browsers get
  today's behaviour, nothing breaks.
- **Type scale** regularised to 15 / 16 / 18 / 19 / 21 / 24 / 27 instead of
  eleven arbitrary sizes. The kicker is the smallest thing on screen and THE
  VERDICT the largest, which is the order of importance to a visitor.
- **Ambiguous spacing fixed:** the gap above a note (52px) is now clearly
  larger than the gap below a kicker (30px), so each screen groups as
  label + body, then note — rather than three evenly spaced strangers.
- **FOR THE RECORD** gained real hierarchy: labels recede (15px, wide tracking,
  --dim), values carry (24px, --fg). Same stacked layout, via a new opt-in
  `sc.html` field on a reading screen — built only from the corpus constants in
  the file, never from anything fetched.
- Kicker and record labels stay `--dim`, NOT `--faint`: on a B&W CRT #4a4a46 on
  black is below the tube's usable floor and the label disappears. Hierarchy
  here comes from size and tracking, not contrast. Reverted after trying it.

**New: tools/typography_audit.mjs.** A corpus check cannot catch this — the
corpus is fine and the layout is what breaks it. So this measures actual
rendered line boxes: walks every text node, groups characters by vertical
position, reconstructs each visual line, and flags any line holding one word.
For `pre-line` blocks it compares rendered against authored line counts, so a
wrapped verse line is caught even when it leaves two words.
5 birthdates x 3 domains, **165 screens: zero orphans**, every block within 78
characters, no JS errors.

Note the detector's first run reported six false orphans on FOR THE RECORD — it
was reading the filing card's deliberate one-value lines as wraps. Fixed the
detector, not the card: it now measures per block.

---

## 2026-08-14 — Review pass 1 (filippos, on the preview build)

Four notes from dialling the preview. All four applied.

**1. Too abstract, hard to connect.** Measured rather than guessed: counted
second-person density per screen slot across the corpus. The two screens that
run back to back in the middle of the reading were the two lowest —
OBSERVATION (aspect omens) at **3%** and CONSTRAINT at **5%**, against ALSO IN
YOUR SKY at 86% and FOR YOU IN PARTICULAR at 100%. Not a sentence-quality
problem: a contiguous stretch where nothing was about the visitor.
44 lines revised in place across those two pools — omens now **41%**
second person, constraints **48%**. The strongest impersonal lines were kept
deliberately (the four-thousand-objections log, the unlocked door); the
abstractions went. Note this softens the locked balance rule — the body is no
longer uniformly enigmatic. The landing still does the domain-naming alone,
and only THE VERDICT still speaks plainly, so the rule holds where it matters.

**2. FOR THE RECORD was meaningless.** "AUSPICIOUS SHELF: 12" and
"UNFAVORABLE FORM: 4-J" are the archive talking to itself — a visitor has no
key to either.
- Shelf → **AUSPICIOUS HOUR**, a real clock time. The one determination on the
  card a visitor can act on.
- The forms keep their numbers and gain a note line that makes the joke
  legible: "Form 6-M is a duplicate request. See Form 6-M." RECORD_FORMS and
  RECORD_FORM_NOTES are index-parallel; the harness fails if they drift.
- **Typography:** the first attempt put the name inline and it wrapped across
  three lines, which was worse than the problem. Label above value now, both
  short — nothing can wrap at any column width, and it reads as a filing card.
  Harness asserts every value fits the column.

**3 & 4. One frame, one stamp, for every found item.** FOUND_FRAME and
FOUND_STAMP are single constants; the letter container's own frame and stamp
are gone. Two framings for the same beat meant the ending never landed the
same way twice, and this is the sentence visitors carry out of the room.
A letter read under this frame stops being an unsigned note and becomes a
prophecy recorded at the visitor's birth — the stronger reading of the same
lines. **Judgement call beyond the note:** the second-screen kicker is now
always "AS RECORDED"; "RECOVERED FROM YOUR FILE" contradicted a frame that
says the sky recorded this on the night you were born. Revert by restoring the
container test in buildMainScreens — it is one line, marked in place. The
letter/dream split still governs the register of the pieces themselves.

Harnesses updated for all of it. Full regression: corpus pass, librarian pass,
edge cases 14/14, walkthrough clean, oracle.json regenerated, preview rebuilt.

---

## 2026-08-14 — Preview build + server transit seed

- **visual/preview.html** (generated, do not hand-edit): the whole ceremony in
  one file, runnable from a file:// URL with nothing installed. Built by
  `python3 tools/build_preview.py`, which bakes the current oracle.json and
  sky_state.json into the page and shims fetch() so /oracle.json and /natal
  resolve locally. Natal positions come from truncated Meeus series in-page
  (sun ~0.01deg, moon ~0.3deg) instead of Swiss Ephemeris. Verified against the
  live server on five dates: sun degree identical to 0.01, moon sign identical
  on all five, transit counts identical on four — 04/11/1979 gives 5 against
  the server's 4, one borderline orb inside the moon approximation.
  Review only. run.sh serves the real thing; do not install this on the machine.
- The `verbs_one` / TRANSIT_NOTES / PLANET_DESK the preview needs are baked
  from librarian.py at build time, not retyped, so the preview cannot drift
  from the corpus.
- **server.py fix:** `find_transits` was seeded with `day + month*31 + year` —
  the same collapsing sum fixed in tv.html in batch 1, still live server-side.
  Two visitors whose dates summed alike received identical transit notes. Now
  the date ordinal.

---

## 2026-08-14 — Kiosk hardening (input paths + appliance boot)

STATUS_REPORT §6, and the input edge cases the happy-path walkthrough never
touched. Nothing here is blocked on hardware.

**Two defects, both fatal in front of a visitor.**

1. **CONSULT could hang forever.** `enterConsult` polls every 250ms for
   `natalResult` and CONSULT accepts no input at all by design — the theatre
   plays out. If `/natal` was *accepted but never answered* (a wedged handler
   thread, not a refused connection) the fetch promise never settled, the poll
   never exited, and the machine sat on the consult screen until someone
   power-cycled it. A rotary dial can do nothing about that. Fixed with an
   AbortController on `fetchNatal` (`NATAL_TIMEOUT_MS`, 6s) and a hard ceiling
   in the consult loop (`CONSULT_MAX_MS`, 12s) that proceeds on the offline
   sign table rather than stalling. The offline table is now `offlineNatal()`,
   split out so the watchdog can reach it without another request.
   Reproduced by stalling the route in Playwright: previously stuck for the
   full 30s test timeout, now reaches the reading.
2. **An invalid date ate the visitor's redial.** The error path cleared the
   slots on a 2.2s timer. A rotary dial takes over a second per digit, so the
   wipe landed mid-redial and the visitor watched their own input vanish with
   no explanation. Slots now clear immediately on refusal and the message
   clears on the next dialled digit.

**New: tools/edge_cases.mjs** — 14 assertions over the paths a visitor can
actually take: invalid date and recovery, redial during the error window,
`000` mid-entry reset, a birthdate ending in 000 passing through untouched,
abandoned entry timing out to IDLE, Escape, non-digit keys, hung `/natal`,
`/natal` 500, unreachable `oracle.json` (SIGNAL LOST banner plus a ceremony
that still completes), and input past 8 digits. 14/14.

**New: kiosk/** — the appliance install.
- `install.sh` / `install.sh uninstall`: templates absolute paths into three
  launchd agents, lints them, bootstraps them into the login GUI domain, then
  verifies server, natal transits and oracle.json. Kills any manual `run.sh`
  processes first — both bind port 8000, and a squatter makes launchd's server
  flap on ThrottleInterval indefinitely.
- Three agents with `KeepAlive`: oracle loop, local server, Chrome kiosk. A
  crash or a power cut comes back unattended.
- `astra-kiosk.sh`: Chrome with `--kiosk`, `--autoplay-policy=no-user-gesture-
  required` for the hum, and a **dedicated `--user-data-dir`** — on a normal
  profile any power cut raises "Chrome didn't shut down correctly", and a
  restore bar over a 1950s television ends the illusion. Waits for the server
  (launchd starts all three at once) and holds `caffeinate -dimsu` for the
  session.
- Stale-sky watchdog in tv.html: if `oracle.json` has been unreachable for ten
  minutes the page reloads — but only from IDLE or BOOT. Reloading under a
  visitor mid-ceremony would be a worse failure than the one being repaired.
- `install.sh` prints the nine things launchd cannot do (auto-login, energy,
  Do Not Disturb, automatic updates off, Spotlight exclusion, resolution and
  overscan, ENTITY_COUNT for the old MacBook, weekly `pmset` reboot, and the
  Wi-Fi-off rehearsal). The piece is not exhibition-ready until those are done
  on the machine.

Full regression after: edge cases 14/14, happy-path walkthrough clean, corpus
harness pass, librarian harness pass, tv.html JS syntax clean.

---

## 2026-08-14 — Language expansion, batch 2 (librarian.py corpus + item 12)

TASK_language_expansion.md items 1-6 and 12. With batch 1 below, the task is
complete. Corpus uncurated — filippos curates before v1.0.

Written (librarian.py), all additive, nothing replaced:
- TOKEN_MEANINGS 6 → 20. New keys cover Sun/Moon/Mercury/Venus/Mars pairs
  across all five modes, plus Moon-Saturn, Venus-Jupiter and Mars-Saturn.
- ASPECT_MODES per mode: verbs_one 6 → 10, verbs 6 → 10, omens 8 → 14,
  constraints 5 → 8.
- MARGINALIA 25 → 50. ASIDE_CLOSINGS 12 → 20. TRANSIT_NOTES 6 → 10 per mode.
- SIGN_TEMPERAMENT: second address and lens per sign, rotating by day and
  sign. NOTE: `address` and `lens` are now LISTS. Anything reading them must
  index — `t["address"][i]`, not `t["address"]`.
- QUIET_OMENS (28) and QUIET_HEADLINES (14), new pools — see below.

Curated coverage measured against real ephemeris, 730 days: a curated token
now leads the reading on **76% of days, up from 43%**. All 20 tokens fire; the
rarest (MAR_SQR_SAT) 18 times in two years. None are dead corpus.

Item 12 — day-level no-repeat allocation:
- `_DayAllocator` hands out lines without replacement for one date. Each sign
  asks in its own seeded order and receives the first lines no other sign has
  claimed. `_order()` produces a full permutation with a stride forced coprime
  to the pool length, so the walk cannot starve part of a pool.
- Signs are served in a day-rotated order. Serving Aries first every day would
  have made the readings reliably better at the start of the zodiac.
- `compose_from_aspect` now returns an ordered candidate list rather than a
  fixed two omens, so the allocator has depth to skip claimed lines.

Result: **0 shared lines across the 12 signs, on all 366 days swept.** Distinct
headlines 12/12 (was 10/12). Before this batch, one base omen appeared in 8 of
12 signs on the same date.

Two defects found while building it:

1. **Signs with an unaspected ruler all shared the day's base headline.** Not
   an omen problem — the same defect one field over. Measured: Cancer and Leo
   carried an identical headline on 366 days of 366, because neither Sun nor
   Moon was aspected in the test sky. QUIET_HEADLINES fixes it; the redundant
   "reports nothing unusual" suffix came off the governor line, since the
   headline now says it in words no other sign is using that day.
2. **The fallback pool was too small to allocate from.** With a 12-line
   QUIET_OMENS, a sky where every ruler is unaspected exhausted the pool and
   repeated silently. Sized to 28 — enough for all twelve signs on the worst
   possible day. The allocator now records exhaustion in `.exhausted` so the
   harness reports it rather than it passing unnoticed.

Verification (tools/verify_librarian.py, new): pool sizes; **that every
TOKEN_MEANINGS key can actually fire** — a key written in the wrong planet
order never matches sky.py's signature and dies silently, so the harness parses
sky.py's PLANETS order and checks each one; duplicate lines across all pools
(540 lines, none repeated); the 366-day cross-sign sweep; the degenerate
no-aspect sky; allocator headroom; variant rotation; two years of real
ephemeris. All pass.

Full re-test of both batches: corpus harness pass, librarian harness pass,
oracle.json regenerated (12/12 distinct headlines, 0 shared lines), Playwright
ceremony renders end to end with no JS errors.

---

## 2026-08-14 — Language expansion, batch 1 (tv.html corpus + selection)

TASK_language_expansion.md items 7-11 and 13. Items 1-6 and 12 (librarian.py)
are batch 2 (above). Corpus is uncurated — filippos curates before v1.0.

Written (all in visual/tv.html):
- LANDINGS 2 → 6 per domain × mode (30 → 90 lines).
- VERDICTS 2 → 6 per domain × mode (30 → 90 lines). Plain register, doable
  the same day, no metaphor.
- FOUND_ITEMS 2 → 4 pieces per mode per container (24 → 48). Letters address,
  dreams witness, turn in the last line.
- LANDING_FRAMES 4 → 8. RECORD_FORMS and RECORD_COLORS 6 → 11 each.

Three defects found and fixed while verifying — the repetition visitors
reported was mechanical, not only a shortage of lines:

1. **The pools had no day term.** Landing, verdict and frame were keyed on the
   dialled date alone, so a returning visitor received a byte-identical
   landing and verdict on every future visit, permanently. Only the found item
   mixed in the day. TASK item 13 as written ("shift weight to the visitor
   seed") had this backwards; approved as amended.
2. **The seed collapsed distinct birthdates.** `seed = d + m*31 + y` gave 2016
   for both 5 Jan 1980 and 6 Jan 1979 — two unrelated visitors, one identical
   reading, whatever the pool size. It admitted ~450 distinct values in total,
   capping the corpus regardless of how much was written. Now a proper date
   ordinal (`y*372 + m*31 + d`), injective over all 31,992 real dates tested.
3. **Multipliers cannot decorrelate equal-length pools.** `(seed*k + day) % 6`
   with any k coprime to 6 is ±1 mod 6, so a landing collision implied a
   verdict collision exactly — both measured 16.4%, the same 16.4%. Replaced
   with `pickIdx(seed, day, salt, len)`, an integer hash salted per pool.
   Deterministic, offline, no clock, no randomness.

Measured across 60k synthetic visitor pairs, same day, same domain, same lead
transit — matching landing AND verdict: **25% → 2.7%** (2.8% is the
independent floor). Same found item: 25% → 12.3%. Every entry reachable, spread
within ±8% of even across 28,896 real birthdates.

Verification (new, in tools/):
- `verify_corpus.mjs` — parses the corpus straight out of tv.html, asserts pool
  sizes, cross-pool duplicates, register (landings lowercase, verdicts plain
  and terminated, found items four lines, dreams never say "you"), seed
  injectivity, collision rates, day rotation, reachability. All pass.
- `walkthrough.mjs` — Playwright: dials a date, chooses a domain, steps every
  screen, then runs a five-visitor cohort. Full ceremony renders; 5/5 distinct
  landings, 4/5 verdicts, 5/5 found items; no JS errors.

Also fixed: one pre-existing dream piece (Sextile) addressed the visitor
directly — "The keeper nods at you as if you had ordered" — which breaks the
letters-address/dreams-witness rule. Rewritten to witness. The harness now
enforces this.

Known and deliberately not addressed in this batch: `oracle.json` still shows
base STACK omens leaking across signs (one line appears in 8 of 12 signs, two
more in 7) and 10/12 distinct headlines. That is TASK item 12 and lives in
librarian.py — batch 2.

---

## 2026-07-30 — Experiments promoted to production

- visual/tv.html is now the full experiment tip: ceremonial mono type (50%
  scale, narrow tall columns), self-hosted fonts, ambient sound layer,
  found items (letters/dreams as the final beat), clarification dial
  (work/love/the other thing), landing sentences, THE VERDICT with real
  moon deadline, FOR THE RECORD, signal-lost diagnostics. The experiment
  badge was removed; M (mute) and P (preview ending) shortcuts remain.
- Root cause of the "reverted/missing features" confusion: run.sh opens
  /tv.html, which was still the pre-experiment ceremony. Now the main page
  IS the current experience. experiments/ folders kept as history.
- Previous production tv.html preserved in git history.

---

## 2026-07-30 — EXPERIMENT: the clarification dial (visual/experiments/clarify/)

Response to visitor feedback (too abstract, repetitive, "not an actual
horoscope"). New ceremony beat + content structure:
- CLARIFY state after the FILE card: dial 1 (work) / 2 (love) / 3 (the
  other thing). Choice re-ranks transits by domain-governing planets and
  shapes the rest of the reading. 25s timeout: "THE ARCHIVE HAS CHOSEN FOR
  YOU. IT USUALLY DOES."
- LANDING sentences (domain × aspect-mode × 2): each metaphor translated
  into the visitor's life exactly once, apologetically.
- THE VERDICT: one plain takeable sentence (domain × mode × 2), time-bound
  by real astronomy — moonDeadline() computes when the Moon leaves its
  sign from live position + speed.
- FOR THE RECORD: auspicious shelf / unfavorable form / color of the day.
- /natal returns up to 6 transits (domain filtering needs material).
- Balance rule kept: body enigmatic, one landing per unit, plain close.

---

## 2026-07-29 — EXPERIMENT: ambient sound (visual/experiments/sound/)

- WebAudio layer, fully synthesized/offline: carrier hum + shortwave drift
  scaled per ceremony state, dial clunks (double on 0·0·0 reset), text
  ticks, numbers-station murmur under CONSULT, and total silence for the
  found item. M mutes; TV volume knob is the intended gallery control.
- Also this session, in experiments/type/: ceremonial typography settled on
  LETTERSPACED MONO (the idle screen's voice promoted to the whole reading,
  narrow tall center column ~46-50%); serif and script passes tried and
  reverted. Speech/TTS considered and rejected for v1.

---

## 2026-07-18 — EXPERIMENT: ceremonial typography (visual/experiments/type/)

- Sandbox (includes found-items): central voice re-set per the "Constant
  Mistakes" reference — Cormorant engraved letterspaced caps for the
  librarian's pronouncements, Great Vibes copperplate script for the
  intimate register (notes, stamps, found letters/dreams). Machine layer
  stays Courier Prime.
- Fonts now SELF-HOSTED in visual/fonts/ (@fontsource woff2, OFL) —
  discovered that production still loads fonts from Google's CDN, which
  will fail on the offline gallery MacBook. Migrate production before
  install day (see experiment README).
- Experiment pages carry a corner badge + P-preview shortcut.

---

## 2026-07-18 — EXPERIMENT: the found item (visual/experiments/poet/)

- Sandbox only — production tv.html untouched. After the archive closes the
  file, one item remains: an unsigned LETTER or a DREAM recorded on the birth
  night, never interpreted. The librarian did not write these; the ceremony
  stays dry and earns one unguarded beat at the very end (Rumi's craft —
  direct address, the turn — in the archive's own imagery; no outside tone).
- 24 authored pieces (2 per aspect mode per container + unaspected pairs),
  keyed to the visitor's lead transit, container seeded by birthdate + day.
  Instruments withdraw for the final screens; 18s hold.
- Try: http://localhost:8000/experiments/poet/tv.html — merge notes in the
  folder README. The v2.0 thermal printer will print found.piece + stamp.

---

## 2026-07-17 — Duplication fix + vocabulary expansion (post review)

- Fixed same-sentence-twice within a reading: same-type transits now take
  consecutive note/verb variants (stride-1 offsets; a 36-birthdate sweep
  shows no collisions), and tv.html deduplicates the final screen sequence
  as a guarantee regardless of source.
- Corpus expanded ~45 lines per ASTRA_MIND voice rules: every aspect mode
  now 6+6 verbs / 8 omens / 5 constraints; MARGINALIA 15→25 (the 1931
  junior clerk, the archive's deliberately fast clock, the moth in the O
  section); TRANSIT_NOTES 4→6 per mode; ASIDE_CLOSINGS 7→12.

---

## 2026-07-17 — ASTRA MIND + corpus deepening (from designing-intelligence review)

- Reviewed the designing-intelligence repo (Character Actor theory, Aio mind
  package). Adopted its structure: aios/ASTRA_MIND_v0.1.md now defines the
  librarian as a character — identity, worldview ("the sky is a bureaucracy
  that works"), relationship-to-visitor, thinking model, and VOICE MECHANICS:
  the six Douglas Adams operations (bathos, specificity, escalation, swerve,
  understatement, institutional pathos) with explicit failure modes. Doubles
  as the future web-MVP system prompt (Aio build-brief pattern).
- librarian.py corpus rebuilt to the mind doc: 4 verb variants + 5 omens +
  3 constraints per aspect mode (all rewritten with objects, precedents,
  incidents); TRANSIT_NOTES doubled to 4 per mode; new MARGINALIA pool (15
  librarian's-notes — Form 30-B, the 1994 asterisk, the sealed 1977 dinner
  file) folded into ~2/3 of readings; all selection seeded by day + sign +
  birthdate so variants rotate daily and differ per visitor.
- Runtime decision noted in ASTRA_MIND: pre-authored corpus for the local
  installation; the same mind package becomes the LLM system prompt for the
  web MVP later.

---

## 2026-07-17 — Transit-led reading spine

- The reading now leads with the visitor's tightest NATAL TRANSIT (the thing
  that genuinely differs per birthdate), not the sign story: headline = the
  transit line, followed by a "WHAT THIS MEANS" second-person note (new
  TRANSIT_NOTES pools, two variants per aspect mode, seeded by birthdate),
  then the sign's ruler-story as "MEANWHILE, IN THE ARCHIVE", two seeded
  observations, constraint, remaining transits, lens, close.
- /natal returns up to 3 transits; note variant seeded by DOB.
- Verified: three same-sign (Aries) birthdates from different years open
  with three entirely different headlines.

---

## 2026-07-17 — Ruler-led sign readings, collision fixes

- Rulers now tried in PRIORITY order (modern first, traditional only if the
  modern ruler is unaspected) — previously Scorpio collapsed into Aries
  whenever Mars was busy, which is most days.
- Ruler-twins (Taurus/Libra under Venus, Gemini/Virgo under Mercury) now
  draw DIFFERENT stories from their shared ruler's aspect list (first vs
  second candidate), with rotated observation pools. Full-identity collision
  check across all 12 signs: none.
- Governor line reflects the ruler actually used.

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
