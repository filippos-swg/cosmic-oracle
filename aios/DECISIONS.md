# DECISIONS — Cosmic Oracle / Astra

Newest-first. Log every architectural, product, and naming decision here.

---

## 2026-06-18 — AIOS v1 preservation pass

**Status:** APPROVED
**Decision:** Initialize git repository, push to GitHub (filippos-swg/cosmic-oracle, private), add AIOS v1 shell.
**Reason:** Project was the only RED item in the portfolio — no version control, no remote backup. This pass moves it to GREEN.
**What did not change:** No code was modified. No files were deleted. No structure was redesigned. Preservation only.

---

## OPEN — Project name: Cosmic Oracle vs Astra

**Status:** OPEN — do not resolve without explicit approval
**Background:**
- v2 brief (cosmic_oracle_master_project_brief_v2.md) calls the project "Cosmic Oracle"
- v3 brief (astra_master_project_brief_v3.md) calls the project "Astra"
- The local folder is named `cosmic-oracle/`
- Internal code (oracle.py, oracle.json) uses "oracle" naming
- "Astra" appears to be a rename that happened between v2 and v3 — no record of when or why
**Options:** Keep "Astra", revert to "Cosmic Oracle", choose a third name.
**Unblocked by:** Next active work session.

---

## OPEN — Astrologer_UPLOAD/ folder name

**Status:** OPEN
**Background:** All source code lives in `Astrologer_UPLOAD/`. This name suggests a staging or upload folder — not a permanent source directory. Its origin and intent are undocumented.
**Options:** Rename to `src/`, rename to `astrologer/`, leave as-is.
**Note:** Any rename requires updating relative path references in oracle.py.
**Unblocked by:** Next active work session.

---

## APPROVED — Two-layer architecture (machine layer / human translation layer)

**Status:** APPROVED (from v3 brief)
**Decision:** The system maintains two distinct layers. Machine layer is cold/symbolic/compressed. Human layer is warm/dry/readable. These must not collapse into each other.
**Documented in:** PROJECT_CANON.md

---

## APPROVED — Physical object deferred until web MVP validated

**Status:** APPROVED (from v3 brief)
**Decision:** Build web version first. Physical retro TV/cabinet kiosk comes after web MVP is working and validated.

---

## APPROVED — V1 user input: zodiac sign selection only

**Status:** APPROVED (from v3 brief)
**Decision:** Do not add date-of-birth input in v1. Too much friction too early. Sign selection is sufficient for first public interaction.
