---
id: P3-05
title: "Stretch: Voice Live"
phase: 3
lane: B
status: todo
owner: ""
depends_on: [P3-04]
research: [R17]
branch: ""
---

## Execute in phases
Phase 3, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 2 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Optional voice mode in the browser for Stage 1 and chat, using Voice Live with our tools. Only start if Gate 3 is green.

## Why it matters
Flashy, and helps low-literacy users, but never at the expense of the must-haves.

## Files you may touch
- frontend/src/features/voice/**
- backend/app/features/voice/**

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Behind a feature flag, off by default
- [ ] Same citation and handoff rules as chat
- [ ] Recorded in the video only if rock solid

## Tests to add
- Flag-off smoke test unchanged

## How to verify (human, under 5 minutes)
1. Flag on: ask 'is help available in <demo ZIP>' by voice and hear a correct, cited answer.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
