---
id: P3-03
title: "Accessibility and mobile pass"
phase: 3
lane: C
status: todo
owner: ""
depends_on: [P2-06, P2-07]
research: [R16]
branch: ""
---

## Execute in phases
Phase 3, lane C. Wave and session: see docs/PLAN.md. **Start only after Gate 2 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
axe clean (no critical/serious), full keyboard support, visible focus, 360px layouts, 44px targets, reading-level spot check.

## Why it matters
Accessibility is named in the brief and scored in Responsible AI.

## Files you may touch
- frontend/src/**
- frontend/e2e/**

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] axe in smoke now fails on critical/serious
- [ ] Keyboard-only journey works
- [ ] Headings, labels, and alt text correct
- [ ] Reading level spot-check notes in the task Log

## Tests to add
- axe gating in smoke
- Keyboard navigation Playwright test

## How to verify (human, under 5 minutes)
1. Unplug the mouse and complete the journey with Tab/Enter.
2. `make smoke`. Accessibility passes.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
