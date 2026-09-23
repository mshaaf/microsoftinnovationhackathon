---
id: P2-06
title: "Letter Decoder UI and appeal draft"
phase: 2
lane: C
status: todo
owner: ""
depends_on: [P0-07]
research: []
branch: ""
---

## Execute in phases
Phase 2, lane C. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Upload/camera screen, progress states, 'What we removed' panel, explanation, checklist, countdown, and an appeal draft merged in the browser.

## Why it matters
The hero demo moment.

## Files you may touch
- frontend/src/features/letter/**
- frontend/src/features/deadline/**
- frontend/e2e/letter.spec.ts (letter flow + appeal-draft privacy test)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Camera capture on mobile and file picker on desktop
- [ ] Progress: reading → removing personal details → explaining
- [ ] 'What we removed' shows counts and categories only
- [ ] Countdown with appeal_due and days_left
- [ ] Appeal draft: template by appeal_template_id; name and registration fields merge locally; copy and print buttons
- [ ] Handoff card when handoff is set

## Tests to add
- Component tests
- Playwright: type a name in the appeal draft, then assert it appears in zero network requests

## How to verify (human, under 5 minutes)
1. Mock mode: upload L03 and walk through explanation → checklist → countdown → draft.
2. DevTools → Network: type 'Jordan' in the draft, then search all requests for 'Jordan'. Zero hits.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
