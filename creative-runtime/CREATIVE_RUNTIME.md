# SWG Creative Runtime v0.1

## Purpose
A creative-direction layer for coding agents. It does not design the work. It preserves authored intent while an agent implements, extends, or refactors it.

## Order of authority
1. Existing project canon and locked decisions
2. Project-specific Creative Runtime files
3. Existing implementation evidence
4. External references
5. Component/tool defaults

Never overwrite a stronger source with a weaker one.

## Operating loop
Before visual or interaction work:
1. Read project canon and current state.
2. Read DESIGN.md, MOTION.md, INTERACTION.md, VOICE.md.
3. Inspect the existing implementation before proposing changes.
4. State the design intention being preserved or improved.
5. Use external references to answer a specific question, never to choose an aesthetic wholesale.
6. Prefer the simplest implementation that preserves the intention.
7. Compare the result against the Runtime and project canon.
8. Flag conflicts instead of silently averaging them.

## Core rules
- Intent before convention.
- Existing authored character before library defaults.
- Restraint before decoration.
- Components are raw material, not creative direction.
- Motion expresses behaviour or state, not polish.
- References require a reason.
- Do not fill ambiguity with generic SaaS, AI, dashboard, glassmorphism, or portfolio conventions.
- Do not add a dependency merely because the Runtime names it.
- A capability may be explicitly rejected when it conflicts with runtime, hardware, offline, performance, or authorship constraints.
- Preserve productive strangeness. Do not normalise unusual decisions solely because a conventional pattern exists.

## External capability policy
### Refero
Use for targeted precedent and agent-readable design research. Record WHAT is useful and WHY. Never clone a complete visual language.

### OriginKit
Use when an editable source component solves a real implementation problem and fits the project's stack. Strip default styling and re-author it through the project Runtime. Do not use where dependency-free/local constraints make it inappropriate.

### Motion
Use when the project's stack benefits from it and authored motion cannot be achieved more simply. Motion behaviour must originate in MOTION.md, not library demos.

## Agent self-check
Before declaring visual work complete ask:
- Could this belong to any competent AI-generated product?
- Which decisions make it specifically this project?
- Did I introduce visual language not supported by the canon?
- Did a library choose the aesthetic for me?
- Did I add motion without meaning?
- Did I remove something strange merely to make it cleaner?
- Can any dependency or UI element be removed without losing intent?

If the first answer is yes, the work is not finished.
