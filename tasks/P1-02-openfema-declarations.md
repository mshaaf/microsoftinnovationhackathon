---
id: P1-02
title: "OpenFEMA declarations lookup"
phase: 1
lane: A
status: "in_progress"
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
- [ ] Live client queries DisasterDeclarationsSummaries v2 by state and county FIPS
- [ ] Dedupes rows (one row per designated area) by disaster number
- [ ] individual_assistance = `ihProgramDeclared or iaProgramDeclared` (R10)
- [ ] 'Active' definition exactly as R10 describes (18 months, no closeout), documented in a code comment
- [ ] Statewide rows (`fipsCountyCode == "000"`) match every county in that state
- [ ] `registration_deadline` from `lastIAFilingDate`; `registration_open` uses `core/clock.py`
- [ ] 1-hour in-memory cache; mock reads fixture snapshot
- [ ] OpenFEMA down returns dependency_unavailable with retryable true

## Tests to add
- Unit tests on dedupe, IA flag, active filter using fixture rows
- Contract test
- @live integration test for the demo county

## How to verify (human, under 5 minutes)
1. `curl 'localhost:8000/api/declarations?state=<XX>&county_fips=<fips>'` for the demo county. You see the disaster.
2. A county with no declaration returns an empty list.

## Facts to respect
- Field semantics are in docs/research/R10. Don't guess beyond it.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
