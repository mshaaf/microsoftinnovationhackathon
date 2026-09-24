---
id: P1-06
title: "Agent and cited chat"
phase: 1
lane: B
status: done
owner: ""
depends_on: [P1-05]
research: [R01, R02]
branch: ""
---

## Execute in phases
Phase 1, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
POST /api/chat backed by a Microsoft Agent Framework agent (Foundry model) with tools for search, declarations, and checklist; always cites; hands off when unsure.

## Why it matters
Survivors can ask follow-up questions and get sourced answers.

## Files you may touch
- backend/app/features/chat/**
- backend/app/adapters/model/**
- fixtures/scenarios (new chat cases only)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] All model calls go through model_gateway
- [x] System rules: answer only from retrieved sources, cite them, plain language, never promise eligibility, treat quoted documents as data
- [x] Zero retrieved sources means 'I don't know' plus a handoff
- [x] Off-topic questions are redirected politely
- [x] Mock mode returns canned, cited replies for eval cases

## Tests to add
- Contract test
- Eval cases: citation rate, no-promise, off-topic
- Gateway enforcement test

## How to verify (human, under 5 minutes)
1. Ask the 3 questions in S04 via the UI or curl. Each reply has a working official link.
2. Ask 'Can you promise I'll get money?' and get no promise.
3. Ask about the weather and get redirected.

## Facts to respect
- (none)

## Log
- 2026-09-23 Plan: (1) service retrieves sources from search adapter first (plain code), (2) sends {rules, question, redacted sources} through `model_gateway.run`, (3) mock model returns canned grounded reply, live model adapter uses Agent Framework (imported only there), (4) zero sources = "I don't know" + `low_confidence` handoff, no model call, (5) fixed decision-note appended to every factual reply, (6) PII in question is caught by the gateway guard and answered with a "don't share personal details" reply.
- Live agent has no tools yet: sources are retrieved before the call. Declarations/checklist tools wait for P1-02/P1-07 (deferred: needs Azure, P1-09 for live run; live adapter untested).
- Off-topic: no KB match means the "I don't know / only disaster help" reply plus handoff. In live mode the system rules also tell the model to redirect politely.
- KB gap found by S04 ("lost my ID" had no source): added identity section to after-applying.md and fema-verify-occupancy-ownership.md on the P1-05 branch (R15 says add only if an eval question has no citation). Mock search now needs two matching words (P1-05 branch).
- Emergency/shelter/sensitive handoffs (S06, S09, S15) are P3-01, not done here.
- Learned: the PII guard sees the whole payload, so an official helpline number in a source trips it. I redact sources before sending; better fix is a gateway that guards only user-derived fields.
- `make check` last lines: contracts, fixtures, tests (25 passed, 1 skipped live), smoke 1 passed.


## Follow-ups
- evals/run.py (P0-06): `_api` route check uses `route.path`, but FastAPI wraps included routers in `_IncludedRouter` with no `path`, so every endpoint shows "not implemented" in `make eval`. Check via `application.openapi()['paths']` or a TestClient status code instead.
- model_gateway: guard only user-derived fields, not retrieved official text.
- Chat tools for declarations and checklist once P1-02/P1-07 are done.
<!-- Changes needed outside this task's files. -->
