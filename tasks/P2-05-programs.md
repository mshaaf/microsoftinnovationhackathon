---
id: P2-05
title: "Programs rules and endpoint"
phase: 2
lane: A
status: done
owner: ""
depends_on: [P1-03]
research: [R14]
branch: "task/P2-05-programs"
---

## Execute in phases
Phase 2, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
data/programs.json and POST /api/programs returning cards with honest tiers for fema_ihp, irs_relief, dua, dsnap, sba_loan.

## Why it matters
'Everything you're owed' goes beyond FEMA with honest uncertainty.

## Files you may touch
- data/programs.json
- backend/app/features/programs/**

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Tier logic exactly as documented in the data file
- [x] Deadlines only where the anchor date is known; otherwise 'window may be short, check now'
- [x] Every card has how_to_apply, source_url, last_verified
- [x] Never claims eligibility

## Tests to add
- All scenario expectations for programs pass (100%)
- Contract test

## How to verify (human, under 5 minutes)
1. Run `PYTHONPATH="$PWD/backend:$PWD" APP_MODE=mock uv run --project backend pytest backend/app/features/programs/test_programs.py -q`; expect 7 passed, including S07's exact program tiers.
2. Run `make check`; expect lint, typecheck, tests, contracts, fixtures, and all 5 smoke tests to pass.

## Facts to respect
- DUA generally has a 30-day filing window from the state's announcement. D-SNAP requires an IA declaration, a state request, and USDA approval, and runs short application windows. IRS relief is automatic for the IRS address of record. Confirm all in R14.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

2026-09-24 plan:
- Encode the five sourced program rules and known date anchors in `data/programs.json`.
- Build cards from the existing OpenFEMA county lookup and current declaration/rules logic.
- Add scenario-driven tier tests, boundary tests for SNAP/work/deadline cases, and a contract response test.
- Run focused tests and `make check`, then record verification and handoff.

2026-09-24 implementation and review:
- Added sourced program data and `POST /api/programs` with data-driven triggers, tiers, and deadline anchors; included bilingual card copy and the known DR-4936 IRS deadline.
- Focused tests first failed because the endpoint and data were absent. Added tests for S07, contract shape, answer triggers, old rules, and unknown deadlines; focused verification: 7 passed.
- Review found non-IA declarations were rejected before DUA/SBA evaluation and SBA copy overclaimed that applying could not affect FEMA help. Added coverage, supported active non-IA DR/EM declarations for triggered cards, and narrowed the copy to FEMA eligibility. Follow-up review found no remaining actionable issue.
- `make check` passed: 112 backend passed, 2 skipped; 29 frontend passed; 14 contract examples and fixtures passed; 5 Playwright smoke tests passed.
- `make check` last 10 lines:
  ```text
  Running 5 tests using 1 worker

    ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.3s)
    ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.8s)
    ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (378ms)
    ✓  4 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (439ms)
    ✓  5 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (341ms)

    5 passed (7.0s)
  ```
- Learned: IRS relief can have a notice-specific deadline, while DUA and D-SNAP need users to check quickly because no exact date is confirmed.

## Follow-ups
<!-- Changes needed outside this task's files. -->
