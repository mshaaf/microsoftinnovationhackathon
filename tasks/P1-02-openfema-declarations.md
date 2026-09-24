---
id: P1-02
title: "OpenFEMA declarations lookup"
phase: 1
lane: A
status: done
owner: ""
depends_on: [P0-04]
research: [R10]
branch: "task/P1-02-openfema-declarations"
---

## Execute in phases
Phase 1, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
GET /api/declarations returns active declarations for a county, deduplicated by disaster number, with an Individual Assistance flag computed per R10.

## Why it matters
Answers the survivor's first question with official data.

## Files you may touch
- backend/app/features/declarations/**
- backend/app/adapters/openfema/**
- fixtures/openfema/**

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Live client queries DisasterDeclarationsSummaries v2 by state and county FIPS
- [x] Dedupes rows (one row per designated area) by disaster number
- [x] individual_assistance = `ihProgramDeclared or iaProgramDeclared` (R10)
- [x] 'Active' definition exactly as R10 describes (18 months, no closeout), documented in a code comment
- [x] Statewide rows (`fipsCountyCode == "000"`) match every county in that state
- [x] `registration_deadline` from `lastIAFilingDate`; `registration_open` uses `core/clock.py`
- [x] 1-hour in-memory cache; mock reads fixture snapshot
- [x] OpenFEMA down returns dependency_unavailable with retryable true

## Tests to add
- Unit tests on dedupe, IA flag, active filter using fixture rows
- Contract test
- @live integration test for the demo county

## How to verify (human, under 5 minutes)
1. Run `PYTHONPATH=backend:. uv run --project backend pytest backend/app/features/declarations backend/app/adapters/openfema -q`; expect 18 passed and 1 skipped (the live test).
2. Run `make dev`, then `curl 'http://localhost:8070/api/declarations?state=HI&county_fips=15001'`; expect DR-4936 with a 2026-11-01 filing deadline.
3. Run `curl 'http://localhost:8070/api/declarations?state=MA&county_fips=25025'`; expect `"declarations": []`.
4. Run `make check`; expect it to pass.

## Facts to respect
- Field semantics are in docs/research/R10. Don't guess beyond it.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
- 2026-09-23: Blocked before implementation. The response contract requires `county.name`, but the documented request provides only `state` and `county_fips`. When OpenFEMA returns no rows, there is no `designatedArea` to supply the name. P1-01's county lookup is still todo and outside this task's file scope. Question: should P1-02 wait for and use P1-01's lookup, or should the GET contract carry `county_name` (requiring a `[CONTRACT]` change)?
- 2026-09-24: Unblocked after P1-01 merged. Its Census ZIP-to-county bundle now provides county names by state and FIPS; P1-02 can use that data for the required response field without changing the request contract.
- 2026-09-24: Blocked before implementation because baseline `make check` fails at frontend typecheck. `frontend/src/app/routes.tsx` passes `feature` and `next` props to `ApplyPage`, whose component accepts no props. The repository stop-line rule requires main to be green before feature work resumes. Follow-up: fix the P1-08 route/component mismatch, then rerun `make check`.
- 2026-09-24: Unblocked after the main route fix merged. Clean `make check` passed on main at 87bf063 (19 backend passed, 1 live test skipped, 29 frontend tests passed, 3 smoke tests passed).
- 2026-09-23 plan:
  - Add fixture-backed and HTTP OpenFEMA adapters that query exact-county and statewide rows, select only needed fields, and cache live results for one hour.
  - Add declarations service/router logic for Census county names, IA/active filtering, deduplication, registration dates, and retryable dependency errors.
  - Add feature-local unit, contract, adapter, and skipped-by-default live tests; run them explicitly because pytest's default paths exclude feature directories.
  - Run `make check`, finish the verification instructions and log, then commit and open the P1-02 PR.
- 2026-09-23: Implemented the fixture and live OpenFEMA adapters, county declarations route/service, and feature-local tests. Focused tests: 18 passed, 1 skipped; Ruff passed. `make check` passed; last 10 lines:
  ```text
  [WebServer] (node:12091) Warning: The 'NO_COLOR' env is ignored due to the 'FORCE_COLOR' env being set.
  [WebServer] (Use `node --trace-warnings ...` to show where the warning was created)

  Running 3 tests using 1 worker

    ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (739ms)
    ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.0s)
    ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (436ms)

    3 passed (7.1s)
  ```
- Learned: OpenFEMA returns one declaration per designated area, so sorting exact-county rows ahead of statewide rows lets a single disaster-number dedupe preserve county detail.
- Live integration test is present and deferred because Azure access is not provisioned (P1-09).

## Follow-ups
<!-- Changes needed outside this task's files. -->
- P1-03 must replace the schema-compatible `serious_needs.available: false` default with rule data.
