# AIOS Automation Proposal
**Status:** DRAFT — under review. Do not implement until approved.
**Date:** 2026-06-26
**Scope:** Operational automation layer for cosmic-oracle / Astra

---

## What AIOS Is Today

A documentation system: five markdown files that an AI session reads manually at the start of each conversation. It records state but does nothing to maintain or verify it. The burden of keeping it accurate sits entirely with the human.

This is fine for a prototype in preservation mode. It becomes a liability the moment active development resumes.

---

## The Problem Worth Solving

Not "we need more automation." The problem is that AIOS can describe the project but cannot verify it. Every session starts by trusting that the documentation is current — and this session's first act was discovering that it isn't.

**Evidence from this session:**
- `AI_HANDOFF.md` run instructions reference `Astrologer_UPLOAD/oracle.py` — that folder no longer exists. The prototype cannot be launched from the documented instructions.
- Three stale lock files in `.git/` that required manual identification and removal (and then couldn't be removed via the mounted filesystem).
- Two master project briefs at repo root (`cosmic_oracle_master_project_brief_v2.md`, `astra_master_project_brief_v3.md`) alongside the consolidated `aios/PROJECT_BRIEF.md`. Three sources of truth = eventual drift.
- Generated runtime artifacts (`sky_state.json`, `sky_signature.txt`) are tracked in git. These change every time the prototype runs. They pollute the commit history and will produce noisy diffs during active development.
- `aios/tasks/` exists as a directory with only `.gitkeep`. No workflow. No format. No current tasks.
- No single command to start the prototype. The run instructions describe a two-terminal workflow by hand.

**What this costs:**
- Every session starts with trust rather than verification.
- Stale paths mean the first run attempt fails.
- Doc drift is already present eight days into the project.

---

## Design Principle

Apply the same rule the project applies to itself:

> Do not over-engineer prematurely. Small, understandable changes. Working loops over ambitious systems.

The automation layer should remove work, not create new work to maintain itself. If it requires documentation to explain how to use the automation, that automation is already too complex.

---

## Friction Tiers

### Tier 1 — Quick Wins
*One file, one afternoon, immediate payoff.*

**1. `Makefile` at repo root**

The single highest-impact change. Replaces manual two-terminal startup and ad-hoc git commands with named, discoverable targets.

Proposed targets:
```makefile
make run        # start oracle.py + visual/server.py (two tmux panes or background processes)
make health     # check git status, lock files, key files present, run instructions valid
make clean      # remove .git/*.lock, __pycache__, .DS_Store
make session    # print AI_HANDOFF summary + current git status (session bootstrap)
```

Cost: ~30 lines of Makefile. No dependencies beyond what's already installed.

**2. Update `.gitignore` to exclude generated artifacts**

Add:
```
sky_state.json
sky_signature.txt
visual/oracle.json
```

These change every run. Tracking them in git produces meaningless diffs and inflates history. They are outputs, not source.

Cost: 3 lines. Zero risk.

**3. Fix stale paths in `AI_HANDOFF.md`**

The documented run instructions point to `Astrologer_UPLOAD/` which no longer exists. This is an immediate blocker. The folder structure section is also stale — it still describes the old layout.

Cost: 10-minute edit. Zero risk.

---

### Tier 2 — Medium Automation
*Small scripts, git hooks. Implement after Tier 1 is stable.*

**4. `aios/scripts/health.sh`**

A shell script that `make health` calls. Checks:
- Are the key source files present? (`sky.py`, `oracle.py`, `librarian.py`)
- Does `visual/` contain `index.html`, `sketch.js`, `server.py`?
- Are there stale lock files in `.git/`?
- Is the working tree clean?
- Does `requirements.txt` exist?
- Are the paths in `AI_HANDOFF.md` valid? (grep for referenced filenames and check they exist)

Output: a pass/fail summary. One line per check. No output on clean pass (Unix convention).

Cost: ~40 lines of bash.

**5. Git pre-commit hook: block generated artifacts**

A simple pre-commit hook that rejects commits containing `sky_state.json`, `sky_signature.txt`, or `visual/oracle.json`. Belt-and-suspenders alongside `.gitignore`.

Cost: 10 lines of bash in `.git/hooks/pre-commit`.
Note: hooks are not tracked in git by default. If this matters, use a `hooks/` directory and symlink in `make setup`.

**6. Consolidate root-level briefs**

`cosmic_oracle_master_project_brief_v2.md` and `astra_master_project_brief_v3.md` at repo root are superseded by `aios/PROJECT_BRIEF.md`. They should be archived or deleted — not left as parallel documents where drift is inevitable.

Proposal: move both to `aios/archive/` with a header noting they are superseded. Update `AI_HANDOFF.md` to remove references to the root-level versions.

Cost: two file moves + two file edits.

---

### Tier 3 — Long-Term AIOS Capabilities
*Implement only after web MVP is in active development. Not before.*

**7. Session log in `aios/sessions/`**

A lightweight dated session log: what was worked on, what changed, what was deferred. Not a transcript — just a one-paragraph entry per work session, written by the AI at session close.

Value: fills the gap between CHANGELOG (commit-level) and DECISIONS (architectural). Creates a searchable record of context that doesn't fit elsewhere.

Format: `aios/sessions/YYYY-MM-DD.md`. One file per session.

Risk: another file that can go stale. Only implement once the pattern is clear.

**8. Automated AI_HANDOFF drift detection**

A script (or extension of `health.sh`) that detects when `AI_HANDOFF.md` references paths, file names, or commands that no longer match the actual repo state. Runs as part of `make health`.

This catches the class of error observed this session — stale documentation — before it costs a session's worth of confusion.

Cost: moderate. Requires a defined schema for what AI_HANDOFF is allowed to reference.

**9. `make session` as a true bootstrap**

Extend the Makefile `session` target to: run health check, print current phase from PROJECT_BRIEF.md, list any open tasks in `aios/tasks/`, and print last CHANGELOG entry. All in one invocation.

Value: replaces the current manual "read 5 files" startup ritual.

---

## Recommendation: Smallest Move with Biggest Return

**Do Tier 1 first. All three items. In one session.**

Priority order:
1. Fix `AI_HANDOFF.md` paths — the prototype is currently undocumented to run.
2. Update `.gitignore` — before the next `sky.py` run pollutes the commit history.
3. Write the `Makefile` — replaces the two-terminal manual startup permanently.

This eliminates: stale documentation, polluted git history, and manual startup. Three root-cause frictions. One short session.

Tier 2 follows naturally once active development resumes. Tier 3 only if the pattern proves itself useful at scale.

---

## What This Proposal Does Not Recommend

- CI/CD pipelines (premature; web MVP doesn't exist yet)
- A task tracking system (the `aios/tasks/` directory is sufficient; see `FRICTION_BACKLOG.md` for format)
- Any new external tool dependencies
- Automation that requires its own documentation to operate
- A separate `automation/` directory (one more directory to maintain; Makefile and scripts can live at root and in `aios/scripts/`)

---

## File Structure After Implementation

```
cosmic-oracle/
├── Makefile                        NEW — session, run, health, clean targets
├── .gitignore                      UPDATED — exclude generated artifacts
├── aios/
│   ├── AI_HANDOFF.md               UPDATED — fix stale paths
│   ├── AUTOMATION_PROPOSAL.md      THIS FILE
│   ├── FRICTION_BACKLOG.md         NEW — canonical backlog
│   ├── CHANGELOG.md
│   ├── DECISIONS.md
│   ├── PROJECT_BRIEF.md
│   ├── PROJECT_CANON.md
│   ├── archive/                    NEW — superseded briefs
│   │   ├── cosmic_oracle_master_project_brief_v2.md
│   │   └── astra_master_project_brief_v3.md
│   ├── scripts/                    NEW (Tier 2) — health.sh, session.sh
│   └── tasks/
│       └── .gitkeep
├── sky.py
├── oracle.py
├── librarian.py
├── requirements.txt
└── visual/
```

---

## Open Questions for Filippos

1. **Makefile vs shell scripts:** Do you prefer `make health` or `./aios/scripts/health.sh`? Makefile is more discoverable; script is more portable.
2. **Artifact gitignore:** Confirm that `sky_state.json` and `sky_signature.txt` should be excluded. These are the last known good snapshots — removing them from git means losing that reference.
3. **Root-level briefs:** Archive or delete? Archive is safer; delete is cleaner.
4. **`AI_HANDOFF.md` run instructions:** The documented path (`Astrologer_UPLOAD/`) no longer exists. Should the instructions be updated to use the root-level files, or is there a restructure planned before this becomes relevant?
