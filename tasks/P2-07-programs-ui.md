---
id: P2-07
title: "Program cards UI"
phase: 2
lane: C
status: "done"
owner: ""
depends_on: [P0-07, P2-05, P2-06]
research: []
branch: "task/P2-07-programs-ui"
---

## Execute in phases
Phase 2, lane C. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Programs screen with a few yes/no questions and cards sorted by urgency, each showing tier label, why, deadline, how to apply, source, and last verified.

## Why it matters
Shows help beyond FEMA with honest labels.

## Files you may touch
- frontend/src/features/programs/**
- frontend/src/app/routes.tsx
- frontend/e2e/programs.spec.ts

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Tier labels readable without color alone (icon + text)
- [x] Sorted: check_now, open, likely, optional
- [x] Works in Español

## Tests to add
- Component tests per tier

## How to verify (human, under 5 minutes)
1. Run `make dev`, open `http://localhost:5173`, enter ZIP `96704`, and continue through the renter checklist to Programs.
2. Switch to Español. Answer lost work **Sí**, SNAP **No**, and household size **1**; select **Ver programas**.
3. Expect five cards ordered DUA and D-SNAP (**Revisar ahora**), FEMA (**Abierto**), IRS (**Podría aplicar**), SBA (**Opcional**), with an icon and text on each tier label.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

- 2026-09-24: Scope correction: added `frontend/src/app/routes.tsx`; without mounting the screen, `/programs` remains the placeholder and the requested flow cannot be used. Added P2-05/P2-06 dependencies because this screen calls the programs API and follows the deadline journey.
- Plan:
  1. Reuse the existing journey context, API client, and `/api/location` county mapping.
  2. Add component coverage for each tier, urgency order, and Spanish labels; add S07 browser-flow coverage.
  3. Implement the smallest accessible form and result-card screen, including loading/error/empty states.
  4. Run focused checks and `make check`, record the output and a `Learned:` line, then hand off for review.

- 2026-09-24 implementation:
  - Mounted the programs screen at `/programs`; it asks the two program questions plus household size, maps the saved ZIP/county through `/api/location`, and submits the existing `/api/programs` contract.
  - Cards sort by `check_now`, `open`, `likely`, `optional`; each tier has an icon and readable text. Added Spanish UI labels and localized dates, with P2-05's short-window, check-now message when a date is unknown.
  - Test-first: component test initially failed because the new screen did not exist. Focused component tests now pass (3); S07 browser flow passes (1), including the five-card order in Spanish.
  - `make check` passed: 161 backend passed, 3 live skipped; 42 frontend passed; 14 contract examples and fixtures passed; 7 Playwright smoke tests passed.
  - Independent review found no critical or important issues; fixed deadline copy and restored assertions for how-to and last-verified card fields.
  - `make check` last 10 lines:
    ```text

      ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows a checklist and a chat link (1.3s)
      ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.9s)
      ✓  3 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.1s)
      ✓  4 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (943ms)
      ✓  5 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (385ms)
      ✓  6 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (423ms)
      ✓  7 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (343ms)

      7 passed (9.3s)
    ```
  - Learned: the programs endpoint needs a county FIPS code, while the journey only stores a county name, so the screen reuses the ZIP lookup and matches the user-selected county before sending answers.
- 2026-09-24: PR #31 merged to `main` (merge commit `a1d3988`).

## Follow-ups
<!-- Changes needed outside this task's files. -->
