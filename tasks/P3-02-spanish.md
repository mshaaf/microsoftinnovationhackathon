---
id: P3-02
title: "Spanish end to end"
phase: 3
lane: B
status: "in_progress"
owner: ""
depends_on: [P2-06]
research: [R07]
branch: "task/P3-02-spanish"
---

## Execute in phases
Phase 3, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 2 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Every server-generated text honors lang=es via Translator (live) or fixtures (mock); UI strings fully translated; plain-language review.

## Why it matters
Language access is part of the track brief.

## Files you may touch
- backend/app/adapters/translator/**
- backend/app/adapters/model/live.py
- backend/app/core/i18n.py
- backend/app/features/chat/service.py
- backend/tests/test_chat_spanish.py
- backend/tests/test_translator.py
- frontend/src/features/*/i18n/es.json and frontend/src/app/i18n/es.json
- frontend/src/shared/i18n/messages.test.ts
- frontend/e2e/journey.spec.ts
- data/*.json (es fields only)

Scope correction (2026-09-24): chat service/model integration is needed to translate generated replies while preserving Spanish PII detection; the listed tests are required by this task's acceptance criteria. The Spanish chat regression has its own test file so it does not collide with P3-01's safety tests. UI pages already use the shared message loader, so only locale data and its completeness/smoke tests are in scope.

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Full journey works in Spanish with no English left on screen (except official names)
- [ ] Glossary for FEMA terms if R07 supports it
- [ ] Spanish scenarios pass evals

## Tests to add
- A Spanish smoke-test variant
- i18n completeness test (no missing keys)

## How to verify (human, under 5 minutes)
1. Switch to Español and complete Stage 1 → Programs with S07.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
Plan (2026-09-24):
- Implement the Translator live adapter and glossary using R07; keep mock translations fixture-backed.
- Route Spanish model-generated chat text through translation without changing data-file translations or PII language.
- Check locale completeness, fill any missing reviewed Spanish strings, and add a Spanish journey/chat smoke path.
- Run `make check` and `make eval`, then record a plain-language review and Azure-only deferrals.

## Follow-ups
<!-- Changes needed outside this task's files. -->
