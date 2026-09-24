---
id: P1-04
title: "Stage 1 UI: is help available here?"
phase: 1
lane: C
status: done
owner: ""
depends_on: [P0-07]
research: []
branch: "task/P1-04-stage1-ui"
---

## Execute in phases
Phase 1, lane C. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
ZIP entry, county confirmation for multi-county ZIPs, disaster card, Serious Needs callout, and a no-declaration state.

## Why it matters
First screen judges see.

## Files you may touch
- frontend/src/features/help-here/**
- frontend/e2e/stage1.spec.ts

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Numeric ZIP input with validation and a clear error message
- [x] County picker when needs_confirmation is true
- [x] Disaster card: title, declaration date, Individual Assistance open/closed, official link
- [x] Serious Needs callout: amount, 'apply by' date, 'may be extended', 'this isn't the total help available'
- [x] Registration deadline shown; a "registration closed" state if `registration_open` is false
- [x] No-declaration state: what that means, 211, FEMA Helpline
- [x] Loading and error states

## Tests to add
- Component tests for each state
- Smoke test covers the happy path

## How to verify (human, under 5 minutes)
1. In mock mode, enter the demo ZIP and see the card and the callout.
2. Enter the multi-county ZIP from S12 and get asked to choose.
3. Enter the no-declaration ZIP from S13 and see the empty state.

## Facts to respect
- (none)

## Log
2026-09-23
Plan: (1) HelpHerePage with view states form/loading/error/pick/result; (2) ZIP validated as /^\d{5}$/; POST /api/location then GET /api/declarations via shared client; (3) store zipCode/county/disasterNumber in journey context only; (4) en+es strings, CSS module, 44px targets; (5) Vitest tests stub fetch with VITE_APP_MODE=live for S12/S13/closed/error/loading; e2e stage1.spec.ts in mock mode.
Human-approved scope exceptions: (a) frontend/src/app/routes.tsx edited ONLY to mount HelpHerePage at "/" and "/help-here". (b) frontend/e2e/journey.spec.ts: 2 lines added (enter ZIP + click Check) because Continue now appears only after a result; unavoidable to keep make check green.
Learned: the mock client returns one fixed example, so multi-county and empty states can only be tested by stubbing fetch in live mode.
make check last lines: `2 passed (4.6s)` (journey + stage1 smoke); all lint/typecheck/tests/contracts green.

## Follow-ups
- Mock mode always returns the single example county; S12/S13 states are only reachable in live mode or unit tests.
