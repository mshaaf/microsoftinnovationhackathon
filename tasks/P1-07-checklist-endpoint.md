---
id: P1-07
title: "Checklist endpoint"
phase: 1
lane: A
status: "done"
owner: ""
depends_on: [P1-03]
research: [R12, R13]
branch: "task/P1-07-checklist-endpoint"
---

## Execute in phases
Phase 1, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
POST /api/checklist returns a deterministic document checklist from the answers and the rules regime, each item with a source.

## Why it matters
Stage 2's core output, and it must be exact.

## Files you may touch
- backend/app/features/checklist/**
- data/checklist_items.json

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Covers own/rent, insured yes/no/not sure, lost ID, displaced
- [x] Each item has id, text (en/es), why, source_url
- [x] Regime-aware (e.g. no SBA-first item for the 2024-03-22 regime)

## Tests to add
- Table-driven tests over all answer combinations used in scenarios
- Contract test

## How to verify (human, under 5 minutes)
1. Start the API: `APP_MODE=mock PYTHONPATH=backend uv run --project backend uvicorn app.main:app --port 8090`.
2. In another terminal, run `curl -s -X POST http://127.0.0.1:8090/api/checklist -H 'content-type: application/json' -d '{"disaster_number":4936,"lang":"en","answers":{"housing":"rent","insured":"not_sure","lost_id":true,"displaced":true}}'`.
3. Expect `rules_regime` to be `2024-03-22` and item IDs `proof_of_occupancy`, `insurance_decision_letter`, `identity_document`, and `temporary_housing_information`, each with a FEMA source link.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

- 2026-09-24 plan:
  1. Add table-driven tests for every scenario answer combination and both rule regimes.
  2. Add a contract test for the real `/api/checklist` response.
  3. Define sourced bilingual checklist items in `data/checklist_items.json`.
  4. Implement the smallest deterministic selector and thin FastAPI route.
  5. Run focused tests and `make check`, then record verification evidence.
- 2026-09-24: Added the deterministic checklist route, bilingual sourced item data, scenario-table tests, contract validation, rule-regime behavior, and request validation.
- Focused verification: `PYTHONPATH="$PWD/backend:$PWD" APP_MODE=mock uv run --project backend pytest backend/app/features/checklist/test_checklist.py -q` → `20 passed in 0.46s`.
- `make check` passed. Last lines:
  ```text
  Running 3 tests using 1 worker
  [WebServer] INFO:     Started server process [51867]
  [WebServer] INFO:     Waiting for application startup.
  [WebServer] INFO:     Application startup complete.
  [WebServer] INFO:     Uvicorn running on http://0.0.0.0:8190 (Press CTRL+C to quit)
    ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (827ms)
    ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.0s)
    ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (426ms)

    3 passed (6.2s)
  ```
- Learned: the frozen request has only a disaster number, so regime selection needs a declaration-by-number lookup rather than the existing county-only adapter method.

## Follow-ups
<!-- Changes needed outside this task's files. -->
- Add `declaration_by_number` to the shared OpenFEMA adapter so the live checklist query is not owned by the feature service.
- Add `backend/app/features` to the root pytest target; `make check` currently misses colocated feature tests, so the focused command above is required.
