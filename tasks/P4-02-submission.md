---
id: P4-02
title: "Submission package"
phase: 4
lane: shared
status: todo
owner: ""
depends_on: [P3-04]
research: [R18]
branch: ""
---

## Execute in phases
Phase 4, lane shared. Wave and session: see docs/PLAN.md. **Start only after Gate 3 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
README final, architecture diagram, Responsible AI summary, eval scorecard snapshot, video link, live URL, all submission fields filled.

## Why it matters
Nothing counts until it's submitted.

## Files you may touch
- README.md
- docs/**
- evals/reports/submission-*.md

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] All R18 required fields complete
- [ ] Scorecard snapshot committed
- [ ] Submitted with a confirmation screenshot saved

## Tests to add
- Fresh clone → make setup → make dev works (someone other than the author tries it)

## How to verify (human, under 5 minutes)
1. Open the submission page and check every field against R18's list.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
