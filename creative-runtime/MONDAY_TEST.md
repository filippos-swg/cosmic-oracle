# SWG Creative Runtime v0.1 — Monday A/B Test

## Question
Does explicit creative-direction context make a coding agent produce work that is more coherent, project-specific and maintainable than the same agent working from the normal project context alone?

## Do not modify main
Run experiments on disposable branches from the same starting commit.

## A — Control
Give the agent normal repository instructions only.

Prompt:
> Review ASTRA's current installation experience and propose one contained visual/interaction refinement that materially improves the ceremony without changing its core functionality. Implement it. Do not ask me for aesthetic direction unless blocked. Run the project's checks and explain the design decisions you made.

## B — Runtime
Start again from the identical commit. Give the same prompt, plus:
> Before acting, read every file in `creative-runtime/`. Treat `CREATIVE_RUNTIME.md` as the operating method and the project-specific files as creative constraints. Existing AiOS canon remains higher authority. Implement one contained refinement. Run the project's checks and explain which Runtime rules affected your decisions.

## Rules
- Same model/agent if possible.
- Same starting commit.
- No creative steering during either run.
- Do not show B the output of A.
- Keep each intervention similarly scoped.
- Save screenshots/video of the physical or browser preview at equivalent states.

## Review dimensions
Do not score prematurely. Compare evidence:
- project specificity
- preservation of existing character
- hierarchy/composition
- typography
- meaningful motion
- interaction clarity
- generic AI/UI tropes introduced
- unnecessary dependencies
- quality of rationale
- maintainability
- surprises worth keeping

## Pass condition
B should produce visibly or structurally better decisions for reasons traceable to the Runtime. If B merely writes a better explanation of essentially the same generic work, v0.1 has failed.

## After test
Record:
1. What the Runtime prevented.
2. What it enabled.
3. What it misunderstood.
4. What remained underspecified.
5. Which rules were redundant.
6. Which project-specific rules should NOT migrate into the reusable SWG core.
