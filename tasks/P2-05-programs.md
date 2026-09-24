---
id: P2-05
title: "Programs rules and endpoint"
phase: 2
lane: A
status: "in_progress"
owner: ""
depends_on: [P1-03]
research: [R14]
branch: "task/P2-05-programs"
---

## Execute in phases
Phase 2, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
data/programs.json and POST /api/programs returning cards with honest tiers for fema_ihp, irs_relief, dua, dsnap, sba_loan.

## Why it matters
'Everything you're owed' goes beyond FEMA with honest uncertainty.

## Files you may touch
- data/programs.json
- backend/app/features/programs/**

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Tier logic exactly as documented in the data file
- [ ] Deadlines only where the anchor date is known; otherwise 'window may be short, check now'
- [ ] Every card has how_to_apply, source_url, last_verified
- [ ] Never claims eligibility

## Tests to add
- All scenario expectations for programs pass (100%)
- Contract test

## How to verify (human, under 5 minutes)
1. Scenario S07 (gig worker): IHP open, IRS likely, DUA check now, D-SNAP check now, SBA optional.

## Facts to respect
- DUA generally has a 30-day filing window from the state's announcement. D-SNAP requires an IA declaration, a state request, and USDA approval, and runs short application windows. IRS relief is automatic for the IRS address of record. Confirm all in R14.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
