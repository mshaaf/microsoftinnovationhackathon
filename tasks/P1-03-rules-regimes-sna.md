---
id: P1-03
title: "Rules regimes and Serious Needs window"
phase: 1
lane: A
status: todo
owner: ""
depends_on: [P1-02]
research: [R13]
branch: ""
---

## Execute in phases
Phase 1, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
data/ihp_rules.json plus logic that picks the rules regime by declaration date and fills the serious_needs block (amount by effective date, apply_by = declaration + 30 days, extension_possible).

## Why it matters
The most time-sensitive benefit in the journey. It must be exactly right.

## Files you may touch
- data/ihp_rules.json
- backend/app/features/rules/**
- backend/app/features/declarations/service.py (attach rules output only)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Regime 'pre-2024-03-22' for earlier declarations: serious_needs.available false
- [ ] Regime '2024-03-22' for declarations on or after 2024-03-22: amount chosen by effective date
- [ ] apply_by = declaration_date + 30 days
- [ ] Every value has a source_url; file has last_verified
- [ ] Nothing in the rules file stays marked VERIFY once R13 is answered

## Tests to add
- Boundaries: 2024-03-21 vs 2024-03-22
- Month-end and leap-year date math
- Amount switch at the $770 effective date
- Schema validation of the rules file

## How to verify (human, under 5 minutes)
1. Declarations response for the demo county includes serious_needs with an apply_by date. Check the math by hand.
2. `make test`. The rules tests pass.

## Facts to respect
- Values in docs/research/R13: $750 for declarations 2024-03-22..2024-09-30, $770 for declarations on/after 2024-10-01 (by **declaration date**). 30-day window; may extend to 60 on state/territory/Tribal request.
- Callout copy says FEMA *may* offer it (R13 caveat for DR-4936).

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
