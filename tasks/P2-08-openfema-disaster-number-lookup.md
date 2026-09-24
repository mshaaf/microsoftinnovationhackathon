---
id: P2-08
title: "OpenFEMA disaster-number lookup"
phase: 2
lane: A
status: "done"
owner: ""
depends_on: [P2-05]
research: [R10]
branch: "task/P2-08-openfema-disaster-number-lookup"
---

## Execute in phases
Phase 2, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Add a global OpenFEMA lookup by disaster number to the adapter and route the checklist's existing lookup through that adapter.

## Why it matters
The letter pipeline must verify that a disaster number exists without hard-coding the demo county or making network calls from a feature service.

## Files you may touch
- backend/app/adapters/openfema/base.py
- backend/app/adapters/openfema/mock.py
- backend/app/adapters/openfema/live.py
- backend/app/adapters/openfema/test_live.py
- backend/app/features/checklist/service.py
- backend/app/features/checklist/test_checklist.py

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Adapter lookup returns a matching declaration or `None` in mock mode using the OpenFEMA snapshot.
- [x] Live lookup filters globally by disaster number, selects only required fields, caches for one hour, and maps service failures to `OpenFEMAUnavailable`.
- [x] Checklist obtains declaration dates only through the adapter; its existing behavior and contract remain unchanged.

## Tests to add
- Adapter tests cover fixture hit/miss, live query parameters, cache expiry, and upstream failure.
- Checklist tests continue to prove the correct rules regime and reject unknown disaster numbers.

## How to verify (human, under 5 minutes)
1. Run `PYTHONPATH="$PWD/backend:$PWD" APP_MODE=mock uv run --project backend pytest backend/app/adapters/openfema/test_live.py backend/app/features/checklist/test_checklist.py -q`.
   Expected: all adapter and checklist tests pass without network access.
2. Run `make check`.
   Expected: lint, typecheck, tests, contracts, fixtures, and all smoke tests pass.

## Facts to respect
- OpenFEMA's DisasterDeclarationsSummaries v2 accepts `$filter=disasterNumber eq N`; R10 records the endpoint and query evidence.
- Mock mode must use the checked-in snapshot; tests do not call OpenFEMA.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
2026-09-24 plan:
1. Read the existing adapter, checklist lookup, R10, and current test conventions.
2. Add tests for mock hit/miss and live filtering, caching, and failure handling.
3. Add the minimal adapter method and refactor checklist date lookup to use it.
4. Run focused tests and `make check`, then record verification and hand off.

2026-09-24 implementation:
- Added fixture-backed mock lookup and a live filtered lookup with only `disasterNumber`/`declarationDate`, one-hour positive/negative caching, and upstream error mapping.
- Routed checklist regime dates through `get_adapter("openfema")`; unknown disaster numbers still return the existing 400 error.
- Focused adapter and checklist tests: 31 passed. Full `make check`: passed (147 backend, 29 frontend, 14 contract examples, 15 scenarios / 8 letters / 12 OpenFEMA rows, 5 smoke tests).
- Last 10 lines of `make check` output:
  ```text

  Running 5 tests using 1 worker

    ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.2s)
    ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.8s)
    ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (361ms)
    ✓  4 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (425ms)
    ✓  5 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (354ms)

    5 passed (6.9s)
  ```
- Learned: The checklist’s direct OpenFEMA call duplicated both mock/live selection and cache behavior; moving the number lookup into the adapter removed that split.
- 2026-09-24 independent review and merge: No critical or important findings; CI passed. Review noted that negative lookup expiry is implemented but not separately tested. PR #28 merged to main.

## Follow-ups
<!-- Changes needed outside this task's files. -->
