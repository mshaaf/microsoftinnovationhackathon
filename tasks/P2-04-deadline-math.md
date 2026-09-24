---
id: P2-04
title: "Deadline math"
phase: 2
lane: A
status: "in_progress"
owner: ""
depends_on: [P0-04]
research: [R12, R13]
branch: "task/P2-04-deadline-math"
---

## Execute in phases
Phase 2, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Deterministic appeal deadline (letter date + regime's appeal_window_days) and days_left using the injectable clock, returned in the letter-decode response.

## Why it matters
The countdown is a headline demo moment. It must never be wrong.

## Files you may touch
- backend/app/features/deadline/** (expose `compute_deadline(letter_date, regime) -> Deadline`; P2-03 wires it into the letter pipeline, so this task never touches `features/letter/`)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] appeal_due and days_left correct across month ends, leap years, and past-due
- [ ] Past-due letters say so and point to a human (late appeals can be explained)
- [ ] Rule text from data, translated

## Tests to add
- Table-driven date tests with a pinned clock

## How to verify (human, under 5 minutes)
1. `make test`. The table includes L03: letter date 2026-09-15 gives appeal_due 2026-11-14, and with the clock pinned to 2026-09-25, days_left is 50.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
