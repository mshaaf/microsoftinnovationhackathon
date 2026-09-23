---
id: P0-06
title: "Eval harness and scorecard"
phase: 0
lane: B
status: "in_progress"
owner: ""
depends_on: [P0-03, P0-05]
research: []
branch: "task/P0-06-eval-harness"
---

## Execute in phases
Phase 0, lane B. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
`make eval` runs every scenario and letter through the API in the current mode, scores against expected results, and writes evals/reports/latest.md plus latest.json.

## Why it matters
Turns 'it seems to work' into a scorecard we can track and show judges.

## Files you may touch
- evals/** (`evals/run.py` replaces the P0-01 stub)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Metrics and thresholds from docs/TESTING.md, one table row each
- [ ] Per-case pass/fail table; endpoints not built yet show 'not implemented' instead of crashing
- [ ] Runs in mock mode in under 60 seconds
- [ ] Report header shows mode, git commit, and timestamp

## Tests to add
- Unit tests for each scorer

## How to verify (human, under 5 minutes)
1. `make eval`, then open evals/reports/latest.md. It lists 15 scenarios and 8 letters, with a metrics table at the top.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
