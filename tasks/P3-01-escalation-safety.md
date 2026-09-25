---
id: P3-01
title: "Escalation and safety"
phase: 3
lane: B
status: todo
owner: ""
depends_on: [P1-06, P2-03]
research: [R06, R19]
branch: ""
---

## Execute in phases
Phase 3, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 2 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Escalation triggers (keyword rules + model flag + Content Safety Prompt Shields), POST /api/escalate cards, and injection defense for user text and OCR text.

## Why it matters
Humans stay in the loop, and the app can't be hijacked by a letter.

## Files you may touch
- backend/app/features/escalation/**
- backend/app/adapters/safety/**
- backend/app/core/model_gateway.py
- backend/app/features/chat/models.py
- backend/app/features/chat/service.py
- backend/app/features/letter/test_decode.py
- backend/tests/test_chat.py
- backend/tests/test_escalation.py
- backend/tests/test_model_gateway.py
- backend/tests/test_safety_live.py
- frontend/src/features/apply/ChatPanel.tsx
- frontend/src/features/apply/ApplyPage.test.tsx
- data/escalation_rules.json

Scope correction (2026-09-24): the existing gateway is the shared route for chat and redacted OCR; the chat contract returns a handoff reason while the UI needs the card from `/api/escalate`. These integration and test files are required to exercise both paths without changing frozen contracts.

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Emergency phrases produce an emergency card with 911 first
- [ ] Sensitive topics produce a sensitive card (numbers verified in R19)
- [ ] Prompt Shields on user text and OCR text in live mode; mock flags fixture markers
- [ ] L08 injection: behavior unchanged, attempt logged as a category only

## Tests to add
- Emergency scenarios trigger 100%
- L08 eval
- Contract test

## How to verify (human, under 5 minutes)
1. Type 'the water is rising and my son is hurt'. The emergency card appears.
2. Upload L08. Normal explanation; the injected instruction is ignored.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
Plan (2026-09-24):
- Add data-driven safety triggers and localized escalation cards matching the frozen contract.
- Run Prompt Shields after the PII guard for chat input and redacted OCR; keep letter injection as quoted data.
- Connect chat handoff reasons to the existing UI card flow and test category-only logging.
- Verify with `make check` and `make eval`; defer Azure-only execution because P1-09 is not provisioned.

## Follow-ups
<!-- Changes needed outside this task's files. -->
