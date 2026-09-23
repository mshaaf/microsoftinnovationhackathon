---
id: P4-01
title: "Demo script, rehearsal, recordings"
phase: 4
lane: humans
status: todo
owner: ""
depends_on: [P3-04, P4-03]
research: [R18]
branch: ""
---

## Execute in phases
Phase 4, lane humans. Wave and session: see docs/PLAN.md. **Start only after Gate 3 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Final video per docs/DEMO.md: presentation (P4-03 deck) + demo. Two rehearsals, a fallback mock-mode recording first, then the live recording.

## Why it matters
Judges mostly experience the video.

## Files you may touch
- docs/DEMO.md
- demo/** (script, assets)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Fallback recording saved first
- [ ] Live recording within the length limit
- [ ] Every beat in DEMO.md shown

## Tests to add
- Gate 3 checklist re-run the same morning

## How to verify (human, under 5 minutes)
1. Watch both recordings end to end. Every beat is present and nothing breaks.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
