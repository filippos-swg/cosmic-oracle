# CLAUDE.md

Standard: AiOS v2.0 · canon: `../AIOS/Framework/project-aios/aios/CANON.md` · **Profile:** build · **Visibility:** public
State: read `aios/STATE.md` first. If its HEAD stamp ≠ `git rev-parse HEAD`, or the tree is dirty, regenerate before acting.
Truth: git history and `aios/`. Not chat. Not this file.
Depends on: designing-intelligence
Do not create AiOS core files at project root. Commit as filippos@southnorth.se.

## What this repo is

ASTRA is a fully local physical art installation: a cosmic librarian interprets real
astronomical conditions through a dedicated MacBook Pro, a 1950s DUX television and a rotary
telephone dial. The public web version is a later track, not the installation runtime.

Run the current software with `bash run.sh`; verify software changes with `npm run check`.
`visual/tv.html` is the installation experience. Read `aios/CANON.md` for identity,
`aios/ASTRA_MIND_v0.1.md` for voice, and the active file in `aios/tasks/` for current work.
Generated sky and preview files are runtime/review outputs, never durable project evidence.

## Asset storage rule (universal)
Original heavy assets (full-res PNGs, PSDs, video and audio masters) are never committed to
this repo. They live on the Mac at `~/Pictures/projects-images/cosmic-oracle/`. The repo
carries only web-optimised delivery copies.
