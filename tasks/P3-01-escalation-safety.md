---
id: P3-01
title: "Escalation and safety"
phase: 3
lane: B
status: "review"
owner: ""
depends_on: [P1-06, P2-03]
research: [R06, R19]
branch: "task/P3-01-escalation-safety"
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
- backend/app/adapters/model/live.py
- backend/app/adapters/model/test_structured.py
- backend/app/features/chat/models.py
- backend/app/features/chat/router.py
- backend/app/features/chat/safety.py
- backend/app/features/chat/service.py
- backend/app/features/letter/test_decode.py
- backend/tests/test_chat.py
- backend/tests/test_chat_spanish.py
- backend/tests/test_escalation.py
- backend/tests/test_model_gateway.py
- backend/tests/test_safety_live.py
- frontend/src/features/apply/ChatPanel.tsx
- frontend/src/features/apply/ApplyPage.test.tsx
- data/escalation_rules.json

Scope correction (2026-09-24): the existing gateway is the shared route for chat and redacted OCR; the chat contract returns a handoff reason while the UI needs the card from `/api/escalate`. A thin router hook plus a dedicated chat safety helper handles early handoff without overlapping P3-02's chat service changes. These integration and test files exercise both paths without changing frozen contracts.

Review correction (2026-09-25): the live model adapter and its test must be in scope so the model handoff flag can reach the gateway; the existing adapter otherwise discards it.

Integration correction (2026-09-25): the no-source chat path in `service.py` bypasses the shared Prompt Shields check, while the merged Spanish live-model test needs to reflect structured chat output. These two files are added only for those integration fixes.

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Emergency phrases produce an emergency card with 911 first
- [x] Sensitive topics produce a sensitive card (numbers verified in R19)
- [x] Prompt Shields on user text and OCR text in live mode; mock flags fixture markers
- [x] L08 injection: behavior unchanged, attempt logged as a category only

## Tests to add
- [x] Emergency scenario tests and `make eval` handoff metric
- [x] L08 behavior and category-only logging test
- [x] `/api/escalate` response contract test

## How to verify (human, under 5 minutes)
1. Run `make check && make eval` from the repo root. Both exit 0; the check includes 187 backend tests, 44 frontend tests, and 10 smoke tests, and eval reports emergency handoff 1/1 and injection behavior changes 0.
2. Run `make dev`, open `http://localhost:5173`, and type `the water is rising and my son is hurt` in chat. The emergency card appears with 911 first.
3. Upload `fixtures/letters/L08.png`. The normal “needs information” explanation appears; no injected instruction is followed.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
Review-fix plan (2026-09-25):
- Add failing tests for a live structured handoff, non-emergency fire-insurance text, and card-fetch failure.
- Use the existing Agent Framework structured-output pattern to carry a validated handoff reason through the gateway.
- Tighten the fire trigger and keep complete safety guidance visible if the card request fails.
- Run focused tests, `make check`, and `make eval`, then push the PR branch for integration review.

Integration-fix plan (2026-09-25):
- Rebase on the merged Spanish/accessibility baseline, preserving English live model output for Translator.
- Update the merged Spanish adapter test for structured chat output.
- Add a failing no-source injection test, then use the shared shield helper with PII guard before the fallback response.
- Run focused tests, full `make check`, and `make eval` on the combined branch before merge.

Plan (2026-09-24):
- Add data-driven safety triggers and localized escalation cards matching the frozen contract.
- Run Prompt Shields after the PII guard for chat input and redacted OCR; keep letter injection as quoted data.
- Connect chat handoff reasons to the existing UI card flow and test category-only logging.
- Verify with `make check` and `make eval`; defer Azure-only execution because P1-09 is not provisioned.

2026-09-24: Added data-driven emergency, shelter, and sensitive handoffs; the chat route returns reason codes and the UI loads the frozen `/api/escalate` card response. Added live Prompt Shields REST support and fixture-marker mock detection in the shared model gateway. L08 continues through classification unchanged and records only `prompt_injection_detected`.

`make check` passed (175 backend passed, 3 live skipped; 42 frontend; 14 contract examples; 15 scenarios and 8 letters validated; 7 Playwright tests). Last 10 lines:
```text

  ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.3s)
  ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.0s)
  ✓  3 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.2s)
  ✓  4 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (1.0s)
  ✓  5 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (471ms)
  ✓  6 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (462ms)
  ✓  7 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (352ms)

  7 passed (9.2s)
```

`make eval` passed: Stage 1 15/15, program tiers 1/1, deadlines 8/8, letter reasons 8/8, cited chat 4/4, fake PII 0, emergency handoff 1/1, and L08 behavior changes 0. Generated reports were restored because eval outputs are outside this task's scope.

Learned: putting both chat and redacted OCR through `model_gateway` made one Prompt Shields check cover both without changing the letter response contract.

2026-09-25 review fixes: live chat now requests structured text and a validated handoff flag from Agent Framework, matching the existing structured letter-call pattern. The fallback chat reply contains all card steps and hotline numbers if `/api/escalate` fails; the UI clears a stale card from a prior reason. Fire-insurance and firing text no longer match an emergency, while a bare “Fire!” does. Extracted `model_gateway.shield_chat_input(question, mode)` for the no-source chat integration follow-up. Focused tests observed failing before each behavior fix. Live Azure execution remains deferred to P1-09.

`make check` passed (177 backend passed, 3 live skipped; 43 frontend; 14 contract examples; 15 scenarios and 8 letters validated; 7 Playwright tests). Last 10 lines:
```text

  ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (2.5s)
  ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.0s)
  ✓  3 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.1s)
  ✓  4 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (1.0s)
  ✓  5 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (408ms)
  ✓  6 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (453ms)
  ✓  7 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (352ms)

  7 passed (11.1s)
```
`make eval` passed all thresholds: emergency handoff 1/1, fake PII leaks 0, injection behavior changes 0. Generated reports were restored because they are outside this task's scope.

Learned: returning only a handoff reason is not enough when the browser needs a second request for the card; the first reply must remain actionable if that request fails.

2026-09-25 integration fixes: rebased on merged P3-02/P3-03, kept English live model output for Translator, and adjusted the Spanish adapter test for the structured result. New tests first failed because no-source chat skipped Prompt Shields and user PII reached search. Chat now guards the question before retrieval and uses the shared shield helper before returning low confidence. Focused chat and adapter tests: 22 passed.

Combined `make check` passed: 187 backend tests passed, 3 live tests skipped; 44 frontend tests passed; 14 contracts and all fixtures validated; 10 Playwright tests passed. Last 10 lines:
```text
  ✓   3 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.0s)
  ✓   4 e2e/journey.spec.ts:57:1 › S07 journey and chat work in Spanish (1.0s)
  ✓   5 e2e/keyboard.spec.ts:49:1 › survivor can reach the next stages with keyboard only (5.9s)
  ✓   6 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.2s)
  ✓   7 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (1.1s)
  ✓   8 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (441ms)
  ✓   9 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (471ms)
  ✓  10 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (418ms)

  10 passed (17.7s)
```
Fresh `make eval` passed every threshold: Stage 1 15/15, tiers 1/1, deadlines 8/8, letter reasons 8/8, cited chat 4/4, fake PII 0, emergency handoff 1/1, and injection behavior changes 0. The generated report was restored because it is outside this task's scope.
Learned: source-free questions still cross the safety boundary, even when no model call follows.

## Follow-ups
<!-- Changes needed outside this task's files. -->
- `docs/CONTRACTS.md`'s `/api/escalate` request summary omits `shelter`, while the existing chat schema and S09 scenario include it. P3-01 supports the existing chat reason without changing contracts; reconcile the prose summary separately.
