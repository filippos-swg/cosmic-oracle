# FRICTION_BACKLOG
**Purpose:** Canonical log of recurring operational friction. Every entry must describe a real observed problem — not a hypothetical. When the fix ships, mark it DONE with the date and commit.

Add items here the moment you notice them. Review at the start of each active work session.

---

## How to Use This File

- **Add:** When you hit friction, add an entry immediately. One line minimum: what happened, when, what it cost.
- **Prioritize:** Use the tier labels (Quick / Medium / Long-term). If something is quick and high-impact, fix it in the same session you log it.
- **Close:** When fixed, change status to `DONE` and add the date. Do not delete entries — the history is useful.
- **Review cadence:** At session start. Takes 30 seconds.

---

## Status Legend
- `OPEN` — known, not yet addressed
- `IN PROGRESS` — being worked on (add who/when)
- `DONE` — fixed (add date + method)
- `DEFERRED` — decided not to fix, with reason

---

## Backlog

---

### F-001 — Stale git lock files
**Observed:** 2026-06-26
**Status:** OPEN
**Tier:** Quick Win
**What happened:** `.git/index.lock`, `.git/HEAD.lock`, `.git/ORIG_HEAD.lock` left behind from an interrupted git operation on 2026-06-18. Required manual identification. Could not be removed via mounted filesystem — required terminal access.
**Cost per occurrence:** ~5 minutes investigation + friction in AI sessions.
**Fix:** Add `make clean` target to Makefile. Runs `rm -f .git/*.lock`. Single command, zero risk when the working tree is clean.

---

### F-002 — AI_HANDOFF.md run instructions are stale
**Observed:** 2026-06-26
**Status:** OPEN
**Tier:** Quick Win — FIX BEFORE NEXT CODE SESSION
**What happened:** `AI_HANDOFF.md` documents the run command as `python Astrologer_UPLOAD/oracle.py`. That folder does not exist — files were moved to repo root. Any new session following the documented instructions will fail immediately.
**Cost per occurrence:** Broken first run. Trust erosion in AIOS documentation.
**Fix:** Update run instructions in `AI_HANDOFF.md` to use root-level paths (`python oracle.py`, `python visual/server.py`). Also update the folder structure diagram.

---

### F-003 — Generated artifacts tracked in git
**Observed:** 2026-06-26
**Status:** OPEN
**Tier:** Quick Win
**What happened:** `sky_state.json` and `sky_signature.txt` are committed to the repository. These are runtime outputs that change every time `sky.py` runs. During active development they will produce noisy diffs and inflate history with meaningless content changes.
**Cost per occurrence:** Polluted `git log`, confusing diffs, larger repo size over time.
**Fix:** Add to `.gitignore`: `sky_state.json`, `sky_signature.txt`, `visual/oracle.json`. Note: current committed versions will remain in history — that's fine.
**Question for Filippos:** The current committed versions are the last known good snapshots. Worth tagging the commit before excluding them?

---

### F-004 — No single command to run the prototype
**Observed:** 2026-06-26
**Status:** OPEN
**Tier:** Quick Win
**What happened:** Running the prototype requires two separate terminal sessions, two separate commands, no documented shortcut. Every restart is a manual two-step process.
**Cost per occurrence:** Friction on every development session. Easy to forget the second process.
**Fix:** `make run` in a Makefile. Can use `tmux` (two panes) or `&` background process for `visual/server.py`.

---

### F-005 — No repo health check
**Observed:** 2026-06-26
**Status:** OPEN
**Tier:** Quick Win (basic) / Medium (full)
**What happened:** This session spent time discovering the repo state manually — lock files, git status, branch tracking, untracked files — by running multiple commands. There is no single command to get a "is everything OK?" answer.
**Cost per occurrence:** 3–5 minutes of diagnostic commands per session.
**Fix:** `make health` in Makefile. Basic version checks git status + lock files. Extended version (Tier 2) adds file existence checks and AI_HANDOFF path validation via `aios/scripts/health.sh`.

---

### F-006 — Duplicate project briefs at repo root
**Observed:** 2026-06-26
**Status:** OPEN
**Tier:** Quick Win
**What happened:** `cosmic_oracle_master_project_brief_v2.md` and `astra_master_project_brief_v3.md` sit at repo root alongside the consolidated `aios/PROJECT_BRIEF.md`. Three sources of truth. Eight days in and they're already diverging (v3 brief references `Astrologer_UPLOAD/` structure; PROJECT_BRIEF.md does not).
**Cost per occurrence:** Confusion about which document is authoritative. AI sessions may read the wrong one.
**Fix:** Move both to `aios/archive/`. Add a one-line header to each noting they are superseded by `aios/PROJECT_BRIEF.md`. Update `AI_HANDOFF.md` to remove any reference to root-level briefs.

---

### F-007 — Session startup requires reading 5 files manually
**Observed:** 2026-06-26 (and implied in every prior session)
**Status:** OPEN
**Tier:** Medium Automation
**What happened:** Every AI session begins by reading `AI_HANDOFF.md`, `PROJECT_BRIEF.md`, `PROJECT_CANON.md`, `DECISIONS.md`, `CHANGELOG.md` — in full, manually. There is no synthesized session bootstrap.
**Cost per occurrence:** 10–15 minutes of context recovery per session.
**Fix:** `make session` target in Makefile. Prints: current branch + git status, last CHANGELOG entry, open items from DECISIONS.md, any tasks in `aios/tasks/`. Single command, no new tooling.

---

### F-008 — `aios/tasks/` has no format or workflow
**Observed:** 2026-06-26
**Status:** OPEN
**Tier:** Medium Automation
**What happened:** The `tasks/` directory exists with only `.gitkeep`. No active tasks. No format defined. It's a placeholder that provides no value in its current state.
**Cost per occurrence:** Tasks accumulate in AI session notes or not at all. No persistent task record between sessions.
**Fix:** Define a minimal task format. Proposal: one file per task, named `TASK-001-short-description.md`. Frontmatter: status, created, priority, phase. Body: description + acceptance criteria. `make session` lists open tasks automatically.
**Note:** Do not introduce an external task system. Keep it in git.

---

### F-009 — AI_HANDOFF drift detection is manual
**Observed:** 2026-06-26
**Status:** OPEN
**Tier:** Long-term
**What happened:** `AI_HANDOFF.md` became stale within 8 days without anyone noticing. The drift was discovered only because an AI session attempted to verify it.
**Cost per occurrence:** Invisible until a session acts on bad information.
**Fix:** Extend `aios/scripts/health.sh` to grep `AI_HANDOFF.md` for referenced filenames and verify each exists in the repo. Flag any broken references as health check failures.
**Dependency:** Requires health.sh (F-005 Tier 2 fix) to exist first.

---

## Closed Items

*(None yet — this backlog was initialized 2026-06-26)*

---

## Notes

- This file lives at `aios/FRICTION_BACKLOG.md`. Do not move it.
- Items in this backlog are operational friction only. Product decisions belong in `DECISIONS.md`. Architectural changes belong in `AUTOMATION_PROPOSAL.md`.
- The goal is an empty backlog. That means the friction is gone, not that it was never logged.
