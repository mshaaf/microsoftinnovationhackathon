---
id: P0-03
title: "Contracts: schemas, examples, contract tests"
phase: 0
lane: shared
status: todo
owner: ""
depends_on: [P0-01]
research: [R10, R13]
branch: ""
---

## Execute in phases
Phase 0, lane shared. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
JSON Schemas and example payloads for every endpoint and data file in docs/CONTRACTS.md, a backend contract-test helper, and a typed frontend client that serves the examples in mock mode.

## Why it matters
Lets frontend and backend build at the same time against identical shapes.

## Files you may touch
- contracts/schemas/*.json
- contracts/examples/*.json
- backend/tests/contract/helpers.py
- frontend/src/shared/api/**
- scripts/validate_contracts.py (replaces the P0-01 stub)
- docs/CONTRACTS.md (only if the schema needs a clarifying note)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] A schema and at least one example for: health, location, declarations, checklist, chat, letter-decode, programs, escalate, error
- [ ] declarations includes `registration_deadline` and `registration_open` (R10; already in docs/CONTRACTS.md)
- [ ] Schemas for data files: ihp_rules, reason_taxonomy, programs, scenario, letter-expected
- [ ] `make contracts` validates all examples and fails on a mismatch
- [ ] Backend helper `assert_matches_schema(response, 'declarations')`
- [ ] Frontend typed client; mock mode returns the matching example

## Tests to add
- make contracts runs in make check
- A deliberately wrong example fails (unit test of the validator)

## How to verify (human, under 5 minutes)
1. `make contracts`. All pass.
2. Change one field type in contracts/examples/declarations.json, rerun, and see it fail. Revert.

## Facts to respect
- Example data is synthetic: disaster 9999, 'Example County'.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
