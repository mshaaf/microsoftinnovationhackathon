---
id: P1-08
title: "Stage 2 UI and chat panel"
phase: 1
lane: C
status: todo
owner: ""
depends_on: [P0-07]
research: []
branch: ""
---

## Execute in phases
Phase 1, lane C. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Four quick questions, a checklist screen, and an 'Ask a question' chat panel that shows citations and handoff cards.

## Why it matters
Turns the survivor's situation into a concrete list.

## Files you may touch
- frontend/src/features/apply/**
- frontend/src/features/handoff/**
- frontend/e2e/apply.spec.ts

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Big-button questions, one per screen, with a back option
- [ ] Checklist items show why and a source link
- [ ] Chat replies show citations as links; handoff renders the handoff card
- [ ] Works in Español

## Tests to add
- Component tests: questions, checklist, chat with citations, handoff

## How to verify (human, under 5 minutes)
1. Mock mode: answer renter / not sure / lost ID and see the checklist.
2. Ask a question in chat and see a reply with a link.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
