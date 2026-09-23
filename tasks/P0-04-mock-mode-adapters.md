---
id: P0-04
title: "Mock mode, adapters, model gateway, /api/health"
phase: 0
lane: B
status: "in_progress"
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

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Each adapter has base.py, mock.py, live.py (live may raise NotConfigured until its task)
- [ ] APP_MODE=mock by default; APP_MODE=live with no config reports services as not_configured instead of crashing
- [ ] model_gateway.guard() raises PIILeakError when a payload contains any fixture fake_pii string (mock) or detected PII (live)
- [ ] A test fails if any module calls the model adapter without going through model_gateway
- [ ] core/clock.py provides an injectable today()
- [ ] Logging redaction filter installed

## Tests to add
- Health contract test
- guard() blocks seeded fake PII
- Grep-style test that no feature imports adapters.model directly
- Clock override works

## How to verify (human, under 5 minutes)
1. `make dev`, then `curl localhost:8000/api/health`. Every service says mock.
2. `APP_MODE=live make dev` with no .env. Health says not_configured and the app still runs.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
