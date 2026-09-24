---
id: P1-01
title: "ZIP to county"
phase: 1
lane: A
status: review
owner: ""
depends_on: [P0-04]
research: [R11]
branch: "task/P1-01-zip-to-county"
---

## Execute in phases
Phase 1, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
POST /api/location resolves a ZIP to one or more counties using a bundled Census ZIP-to-county file; flags multi-county ZIPs.

## Why it matters
Stage 1 starts here, and it's the only location input we collect.

## Files you may touch
- backend/app/features/location/**
- backend/app/adapters/geo/**
- data/geo/zip_county.json
- scripts/build_zip_county.py

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Source file, format, and the 5% land-share rule exactly as R11 describes
- [x] Single-county ZIP returns one county with needs_confirmation false (96704 → Hawaii County 15001)
- [x] Multi-county ZIP returns all counties, primary first, needs_confirmation true
- [x] Unknown or malformed ZIP returns zip_not_found / invalid_input
- [x] Bundled data file under 5 MB, with source and version noted
- [x] Response matches the location contract

## Tests to add
- Table-driven unit tests: single (96704), multi (39426), unknown, malformed, leading zeros (00601, 02134)
- Contract test

## How to verify (human, under 5 minutes)
1. Run `PYTHONPATH=backend:. uv run --project backend pytest backend/app/features/location -q`; expect 9 tests to pass.
2. Run `API_PORT=8040 WEB_PORT=5213 make dev` in one terminal.
3. In another terminal, run `curl -sS -X POST http://localhost:8040/api/location -H 'content-type: application/json' -d '{"zip":"96704"}'`; expect Hawaii County (`15001`) and `needs_confirmation: false`.
4. Run `curl -sS -X POST http://localhost:8040/api/location -H 'content-type: application/json' -d '{"zip":"39426"}'`; expect Pearl River (`28109`) first, Hancock (`28045`) second, and `needs_confirmation: true`.
5. Run `curl -sS -X POST http://localhost:8040/api/location -H 'content-type: application/json' -d '{"zip":"00000"}'`; expect `zip_not_found` (404). Repeat with `{"zip":"12x45"}`; expect `invalid_input` (400).

## Facts to respect
- ZCTAs aren't identical to USPS ZIPs. Note the limitation in the About screen.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

2026-09-23 plan:
- Add regression tests for builder parsing and aggregation plus location response/error contracts.
- Build the Census 2020 relation-file generator and bundle the filtered ZIP-to-county map.
- Implement lookup from the bundle and `POST /api/location`, preserving leading zeros and required error codes.
- Run focused feature tests, check required sample ZIPs and bundle size, then run `make check`.
- Document the out-of-scope About disclaimer follow-up and handoff verification details.

2026-09-23:
- Built the Census 2020 pipe-delimited UTF-8 BOM generator; bundle records source/version and the state FIPS map, aggregates land area per county, keeps shares >= 5%, and sorts primary county first.
- Added bundled ZIP lookup and `POST /api/location` with frozen success/error response shapes. Bundle: 33,791 ZIPs, 1,898,490 bytes (<5 MB).
- Focused verification: `PYTHONPATH=backend:. uv run --project backend pytest backend/app/features/location -q` → 9 passed. `make check` → passed (19 backend passed, 1 live skipped; 20 frontend passed; contracts, fixtures, and 2 smoke tests passed).
- `make check` last 10 lines:
  ```text
  [WebServer] INFO:     Started server process [82088]
  [WebServer] INFO:     Waiting for application startup.
  [WebServer] INFO:     Application startup complete.
  [WebServer] INFO:     Uvicorn running on http://0.0.0.0:8140 (Press CTRL+C to quit)
  [WebServer] (node:82111) Warning: The 'NO_COLOR' env is ignored due to the 'FORCE_COLOR' env being set.
  [WebServer] (Use `node --trace-warnings ...` to show where the warning was created)
  Running 2 tests using 1 worker
    ✓  1 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.1s)
    ✓  2 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (393ms)
    2 passed (5.3s)
  ```
- Learned: feature-local tests are outside the repository's normal pytest collection paths, so they need the explicit focused command above.
- Status: review. No open implementation questions.

## Follow-ups
<!-- Changes needed outside this task's files. -->

- Add an About-screen note that Census ZCTAs approximate USPS ZIPs and that PO-box-only or new ZIPs may be missing; suggest calling 211 when no match is found. Frontend files are outside P1-01's scope.
