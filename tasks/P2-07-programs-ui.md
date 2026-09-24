---
id: P2-07
title: "Program cards UI"
phase: 2
lane: C
status: "in_progress"
owner: ""
depends_on: [P0-07]
research: []
branch: "task/P2-07-programs-ui"
---

## Execute in phases
Phase 2, lane C. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Programs screen with a few yes/no questions and cards sorted by urgency, each showing tier label, why, deadline, how to apply, source, and last verified.

## Why it matters
Shows help beyond FEMA with honest labels.

## Files you may touch
- frontend/src/features/programs/**
- frontend/e2e/programs.spec.ts

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Tier labels readable without color alone (icon + text)
- [ ] Sorted: check_now, open, likely, optional
- [ ] Works in Español

## Tests to add
- Component tests per tier

## How to verify (human, under 5 minutes)
1. Mock mode: run the S07 answers and see 5 cards in the right order with the right labels.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
