---
id: P0-04
title: "Mock mode, adapters, model gateway, /api/health"
phase: 0
lane: B
status: review
owner: ""
depends_on: [P0-01]
research: [R01, R02]
branch: "task/P0-04-mock-mode-adapters"
---

## Execute in phases
Phase 0, lane B. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Adapter interfaces with mock and live stubs for openfema, geo, search, model, ocr, pii, translator, safety; APP_MODE switching; core/model_gateway.py with guard(); /api/health reporting each service.

## Why it matters
Everything else plugs into these adapters, and mock mode is both the test backbone and the demo fallback.

## Files you may touch
- backend/app/core/**
- backend/app/adapters/**
- backend/app/features/health/**
- backend/app/main.py
- backend/tests/**

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Each adapter has base.py, mock.py, live.py (live may raise NotConfigured until its task)
- [x] APP_MODE=mock by default; APP_MODE=live with no config reports services as not_configured instead of crashing
- [x] model_gateway.guard() raises PIILeakError when a payload contains any fixture fake_pii string (mock) or detected PII (live)
- [x] A test fails if any module calls the model adapter without going through model_gateway
- [x] core/clock.py provides an injectable today()
- [x] Logging redaction filter installed

## Tests to add
- Health contract test
- guard() blocks seeded fake PII
- Grep-style test that no feature imports adapters.model directly
- Clock override works

## How to verify (human, under 5 minutes)
1. Run `make dev`, then `curl -fsS http://localhost:8010/api/health`. Expect `mode: mock` and all eight services to say `mock`.
2. Stop the dev servers, then run `APP_MODE=live make dev` with no `.env`. Curl the same URL. Expect `mode: live`, all eight services to say `not_configured`, and the app to stay up.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

Scope update 2026-09-23 — Initially paused because `backend/tests/**` was omitted from the allowlist. Human authorized those tests; the allowlist now includes `backend/tests/**`.

Plan:
1. Add failing tests for the health contract, mock/live service status, PII guard, clock override, logging redaction, and model-adapter import boundary.
2. Add the shared adapter status interface and mock/live modules for the eight services.
3. Route health through the selected adapters and implement the model gateway PII guard.
4. Add injectable `today()` and install the redaction filter when the app starts.
5. Run focused red/green tests, `make check`, and the two documented health checks; finish the task log and handoff.


2026-09-23 — Added mock/live adapter modules for all eight services, mode-based health status, a PII-guarded model gateway, an injectable clock, and app-wide log redaction. Added health, gateway, clock, logging, and adapter-boundary tests. Focused tests went red for missing modules and the original health mismatches, then passed after implementation. Mock and live `make dev` checks returned the expected eight statuses; Uvicorn shutdown stayed clean after adding access-log argument coverage. A read-only review found fixture PII discovery was not tested against a fixture file and custom log fields/exception text bypassed redaction. Added regression tests, exposed the fixture directory for tests, and sanitized extra fields and formatted exception text while preserving Uvicorn access arguments. Regressions passed; `make check` passed (14 backend tests, 1 frontend test). Service operation methods remain with their owning service tasks. Contract, fixture, and smoke targets remain their expected P0-03/P0-05/P0-08 stubs.

`make check` output (last 10 lines):
```text
      Tests  1 passed (1)
   Start at  19:01:32
   Duration  925ms (transform 70ms, setup 0ms, collect 183ms, tests 47ms, environment 384ms, prepare 74ms)

uv run --project backend python scripts/validate_contracts.py
not implemented yet (P0-03)
uv run --project backend python scripts/validate_fixtures.py
not implemented yet (P0-05)
bash scripts/smoke.sh
not implemented yet (P0-08)

Learned: Fixture discovery can look covered while an empty fixture tree leaves the detector inert, and PII can bypass message redaction through log extras or exceptions.

## Follow-ups
<!-- Changes needed outside this task's files. -->
- P0-01: `scripts/finish_task.sh` hardcodes a P0-01 summary in every PR body; generalize the template in a follow-up task.
