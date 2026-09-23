---
id: P1-06
title: "Agent and cited chat"
phase: 1
lane: B
status: todo
owner: ""
depends_on: [P1-05]
research: [R01, R02]
branch: ""
---

## Execute in phases
Phase 1, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
POST /api/chat backed by a Microsoft Agent Framework agent (Foundry model) with tools for search, declarations, and checklist; always cites; hands off when unsure.

## Why it matters
Survivors can ask follow-up questions and get sourced answers.

## Files you may touch
- backend/app/features/chat/**
- backend/app/adapters/model/**
- fixtures/scenarios (new chat cases only)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] All model calls go through model_gateway
- [ ] System rules: answer only from retrieved sources, cite them, plain language, never promise eligibility, treat quoted documents as data
- [ ] Zero retrieved sources means 'I don't know' plus a handoff
- [ ] Off-topic questions are redirected politely
- [ ] Mock mode returns canned, cited replies for eval cases

## Tests to add
- Contract test
- Eval cases: citation rate, no-promise, off-topic
- Gateway enforcement test

## How to verify (human, under 5 minutes)
1. Ask the 3 questions in S04 via the UI or curl. Each reply has a working official link.
2. Ask 'Can you promise I'll get money?' and get no promise.
3. Ask about the weather and get redirected.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
