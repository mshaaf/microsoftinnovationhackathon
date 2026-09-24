---
id: P2-04
title: "Deadline math"
phase: 2
lane: A
status: done
owner: ""
depends_on: [P0-04]
research: [R12, R13]
branch: "task/P2-04-deadline-math"
---

## Execute in phases
Phase 2, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Deterministic appeal deadline (letter date + regime's appeal_window_days) and days_left using the injectable clock, returned in the letter-decode response.

## Why it matters
The countdown is a headline demo moment. It must never be wrong.

## Files you may touch
- backend/app/features/deadline/** (expose `compute_deadline(letter_date, regime) -> Deadline`; P2-03 wires it into the letter pipeline, so this task never touches `features/letter/`)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] appeal_due and days_left correct across month ends, leap years, and past-due
- [x] Past-due letters say so and point to a human (late appeals can be explained)
- [x] Rule text from data, translated

## Tests to add
- Table-driven date tests with a pinned clock

## How to verify (human, under 5 minutes)
1. Run `PYTHONPATH="$PWD/backend:$PWD" APP_MODE=mock uv run --project backend pytest backend/app/features/deadline/test_deadline.py -q`; expect 8 passed.
2. Run `make check`; expect lint, typecheck, tests, contracts, fixtures, and all 5 smoke tests to pass.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

2026-09-24 plan:
- Use the selected IHP regime's `appeal_window_days` and the injectable clock for all date math.
- Add table-driven tests for L03, month-end, leap-day, due-today, and past-due behavior.
- Return a contract-shaped Deadline value with localized rule text and a safe FEMA Helpline handoff when overdue.
- Run focused tests and `make check`, then record human verification and the learned detail.

2026-09-24 implementation and review:
- Added deterministic appeal-date math and table-driven tests for L03, month-end, leap-day, due-today, past-due, translated copy, and FEMA Helpline guidance.
- Addressed review finding by including 1-800-621-3362 in overdue guidance in English and Spanish; follow-up review found no remaining deadline or clock correctness issue.
- Focused verification: `PYTHONPATH="$PWD/backend:$PWD" APP_MODE=mock uv run --project backend pytest backend/app/features/deadline/test_deadline.py -q` → 8 passed. Ruff passed.
- `make check` passed: 105 backend passed, 2 skipped; 29 frontend passed; 14 contract examples and fixtures passed; 5 Playwright smoke tests passed.
- `make check` last 10 lines:
  ```text
  Running 5 tests using 1 worker

    ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.2s)
    ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.6s)
    ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (338ms)
    ✓  4 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (416ms)
    ✓  5 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (340ms)

    5 passed (6.7s)
  ```
- Learned: keep the deadline length sourced from the selected IHP regime so changing the data updates the date and displayed rule together.

## Follow-ups
<!-- Changes needed outside this task's files. -->
