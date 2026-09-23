---
id: P1-04
title: "Stage 1 UI: is help available here?"
phase: 1
lane: C
status: todo
owner: ""
depends_on: [P0-07]
research: []
branch: ""
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
- [ ] Numeric ZIP input with validation and a clear error message
- [ ] County picker when needs_confirmation is true
- [ ] Disaster card: title, declaration date, Individual Assistance open/closed, official link
- [ ] Serious Needs callout: amount, 'apply by' date, 'may be extended', 'this isn't the total help available'
- [ ] Registration deadline shown; a "registration closed" state if `registration_open` is false
- [ ] No-declaration state: what that means, 211, FEMA Helpline
- [ ] Loading and error states

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
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
