# ASTRA / Cosmic Oracle — Decision & Change Log

**Vocabulary.** An entry with a `**Status:**` is a decision. An entry without one is a change.
`APPROVED` — signed · `RECOMMENDED` — awaiting pass / adjust / kill · `OPEN` — undecided,
needs work · `SUPERSEDED` — replaced, with a pointer to what replaced it.

Newest first. Append only — never rewrite an entry. A correction is a new entry that
supersedes the old one. The complete pre-v2 change history is preserved at
`archive/aios-v1.3/CHANGELOG.md`.

---

## 2026-09-04 — Migrated ASTRA to AiOS v2.0

**Status:** RECOMMENDED
**Decision:** Use the `build` profile and public visibility. Keep the live canon, ASTRA mind,
hardware task and still-useful installation report active; preserve superseded v1.3 context,
plans and the complete change history under `archive/`.
**Evidence:** GitHub reports `filippos-swg/cosmic-oracle` as public; tagged software v1.0 and
the later launch revision are present; the active task says desk work is complete and the
remaining work requires the physical television, dial and installation hardware.
**Practical consequence:** Sessions enter through `CLAUDE.md`, use `aios/STATE.md`, this log,
`aios/CANON.md` and `aios/tasks/`, and do not treat generated runtime outputs or obsolete
automation proposals as current project truth.

---

## 2026-07-16 — Project name: ASTRA

**Status:** APPROVED (filippos)
**Decision:** The project and the piece are named ASTRA. Resolves the open v2/v3 naming
question. Startup screen, sign-off cards, and all user-facing copy use ASTRA. Repo/folder
names stay `cosmic-oracle` (rename not worth the churn).

---

## 2026-07-16 — Visitor input: date of birth via rotary telephone dial

**Status:** APPROVED (filippos)
**Decision:** The installation takes the visitor's date of birth (DD·MM·YYYY), entered on a
rotary telephone dial wired through a microcontroller emulating a USB keyboard. The frontend
listens for plain digit keystrokes, so a normal keyboard works for development and as a
fallback. Supersedes "V1 user input: zodiac sign selection only" below — that decision was
scoped to the web MVP; the installation leads with DOB.

---

## 2026-07-16 — Installation architecture: fully local

**Status:** APPROVED (filippos)
**Decision:** The installation runs entirely on the dedicated MacBook Pro: oracle loop,
local server, and site, with zero network dependency. The Cloudflare web MVP remains a
later, separate track that reuses the TV build's state machine and content engine.

---

## 2026-07-16 — Installation before web MVP

**Status:** APPROVED (implicit in installation build)
**Decision:** The physical TV installation is being built first, running fully on a dedicated
MacBook Pro. Supersedes "Physical object deferred until web MVP validated" below. The web MVP
(stars.kidbutton.com) remains planned and inherits the TV build's state machine and content
engine.

---

## 2026-07-16 — Snapshot before experience rebuild

**Status:** APPROVED
**Decision:** The v1 desktop-dashboard experience is frozen in
`snapshots/v1-2026-07-16-desktop-dashboard/` (runnable copy) before the installation UX
(tv.html, ceremony state machine) is built.

---

## 2026-06-18 — AIOS v1 preservation pass

**Status:** APPROVED
**Decision:** Initialize git repository, push to GitHub (filippos-swg/cosmic-oracle, private), add AIOS v1 shell.
**Reason:** Project was the only RED item in the portfolio — no version control, no remote backup. This pass moves it to GREEN.
**What did not change:** No code was modified. No files were deleted. No structure was redesigned. Preservation only.

---

## 2026-06-18 — Project name: Cosmic Oracle vs Astra (SUPERSEDED)

**Status:** SUPERSEDED — by “Project name: ASTRA” (2026-07-16)
**Background:**
- v2 brief (cosmic_oracle_master_project_brief_v2.md) calls the project "Cosmic Oracle"
- v3 brief (astra_master_project_brief_v3.md) calls the project "Astra"
- The local folder is named `cosmic-oracle/`
- Internal code (oracle.py, oracle.json) uses "oracle" naming
- "Astra" appears to be a rename that happened between v2 and v3 — no record of when or why
**Options:** Keep "Astra", revert to "Cosmic Oracle", choose a third name.
**Unblocked by:** Next active work session.

---

## 2026-06-18 — Astrologer_UPLOAD/ folder name (SUPERSEDED)

**Status:** SUPERSEDED — source files now live at the repository root and current run instructions use them
**Background:** All source code lived in the folder named Astrologer_UPLOAD. That name suggested a staging or upload folder rather than a permanent source directory. Its origin and intent were undocumented.
**Options:** Rename to `src/`, rename to `astrologer/`, leave as-is.
**Note:** Any rename requires updating relative path references in oracle.py.
**Unblocked by:** Next active work session.

---

## 2026-06-18 — Two-layer architecture (machine layer / human translation layer)

**Status:** APPROVED (from v3 brief)
**Decision:** The system maintains two distinct layers. Machine layer is cold/symbolic/compressed. Human layer is warm/dry/readable. These must not collapse into each other.
**Documented in:** `aios/CANON.md`

---

## 2026-06-18 — Physical object deferred until web MVP validated (SUPERSEDED)

**Status:** SUPERSEDED — by “Installation before web MVP” (2026-07-16)
**Decision:** Build web version first. Physical retro TV/cabinet kiosk comes after web MVP is working and validated.

---

## 2026-06-18 — V1 user input: zodiac sign selection only

**Status:** APPROVED (from v3 brief)
**Decision:** Do not add date-of-birth input in v1. Too much friction too early. Sign selection is sufficient for first public interaction.
