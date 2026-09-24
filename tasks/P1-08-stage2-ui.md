---
id: P1-08
title: "Stage 2 UI and chat panel"
phase: 1
lane: C
status: done
owner: ""
depends_on: [P0-07]
research: []
branch: "task/P1-08-stage2-ui"
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
- [x] Big-button questions, one per screen, with a back option
- [x] Checklist items show why and a source link
- [x] Chat replies show citations as links; handoff renders the handoff card
- [x] Works in Español

## Tests to add
- Component tests: questions, checklist, chat with citations, handoff

## How to verify (human, under 5 minutes)
1. Mock mode: answer renter / not sure / lost ID and see the checklist.
2. Ask a question in chat and see a reply with a link.

## Facts to respect
- (none)

## Log
2026-09-23 Plan: (1) tests for questions/checklist/chat/handoff; (2) HandoffCard in features/handoff; (3) ApplyPage (4 questions, back, POST /api/checklist, states) + ChatPanel (POST /api/chat, citations, handoff, escalate button); (4) en/es i18n; (5) e2e apply.spec.ts; (6) mount at /apply.
HUMAN-APPROVED SCOPE EXCEPTION: edited frontend/src/app/routes.tsx only to mount ApplyPage at /apply (one route line + one import). FeaturePage.tsx untouched. ApplyPage keeps a Continue link to /letter so journey.spec.ts still passes.
Disaster number falls back to 9999 when Stage 1 has not set one.
Learned: mock mode returns fixed examples, so component tests spy on apiRequest to cover error/empty/handoff paths.
`make check` passed (last lines): vitest 22 passed; contracts validated 14; fixtures validated; smoke 2 passed (apply.spec.ts, journey.spec.ts).

## Follow-ups
<!-- Changes needed outside this task's files. -->
