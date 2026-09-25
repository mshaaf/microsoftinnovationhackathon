---
id: P3-02
title: "Spanish end to end"
phase: 3
lane: B
status: "review"
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
- [x] Full journey works in Spanish with no English left on screen (except official names)
- [x] Glossary for FEMA terms if R07 supports it
- [x] Spanish scenarios pass evals

## Tests to add
- A Spanish smoke-test variant
- i18n completeness test (no missing keys)

## How to verify (human, under 5 minutes)
1. Run `make check`; expect all checks to pass, including the Spanish S07 journey/chat smoke test.
2. Run `make eval`; expect S05 and S07 to pass, including S07's five program tiers.
3. Run `PYTHONPATH=backend uv run --project backend pytest backend/tests/test_translator.py backend/tests/test_chat_spanish.py -q`; expect 8 passed, including Entra endpoint, glossary boundary, and translated fallback citation.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
Review-fix plan (2026-09-25):
- Reproduce the live Entra request against an HTTP capture; use the configured resource endpoint for bearer auth.
- Add a Spanish chat regression where search falls back to English, then translate only the fallback citation title.
- Add a glossary boundary regression for plural terms; keep the reviewed singular mapping.
- Run focused tests, `make check`, and update this handoff before pushing the PR branch.

Plan (2026-09-24):
- Implement the Translator live adapter and glossary using R07; keep mock translations fixture-backed.
- Route Spanish model-generated chat text through translation without changing data-file translations or PII language.
- Check locale completeness, fill any missing reviewed Spanish strings, and add a Spanish journey/chat smoke path.
- Run `make check` and `make eval`, then record a plain-language review and Azure-only deferrals.

2026-09-24: Added the Azure Translator v3 adapter with R07 glossary markup, fixture-backed mock translations, and Spanish chat translation. Kept `lang=es` in the model-gateway payload for PII detection; the live model is prompted for English, and only its generated reply text is translated. Reviewed all English/Spanish locale keys; none were missing. The S07 smoke checks the Spanish reply and program cards. No Azure request was made; live credentials are deferred until P1-09.

Plain-language spot check: “Incluya el número de solicitud de FEMA y el número del desastre en cada página” is a short, direct instruction; official program names and agency acronyms remain as named.

`make check` (exit 0; last 10 lines):
```text
  ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.3s)
  ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.7s)
  ✓  3 e2e/journey.spec.ts:57:1 › S07 journey and chat work in Spanish (995ms)
  ✓  4 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.1s)
  ✓  5 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (1.0s)
  ✓  6 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (384ms)
  ✓  7 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (426ms)
  ✓  8 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (347ms)

  8 passed (10.5s)
```

`make eval`: S05 and S07 pass; program tiers 1/1; Stage 1 15/15; deadlines 8/8; letter reasons 8/8; citations 4/4; fake PII 0. Emergency handoff remains 0/1, tracked to P3-01. The generated report was restored because `evals/reports/` is outside this task's file scope; rerun after merging to refresh shared evidence.

Learned: The PII guard uses the payload language, so Spanish requests must keep `lang=es` even when the live model answers in English before Translator.

2026-09-25 review fixes: [Microsoft's Translator authentication reference](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/reference/authentication) requires a resource ID for Entra tokens at the global endpoint, but supports bearer tokens at the existing custom resource endpoint. The live adapter now uses that configured endpoint for Entra/managed-identity requests and retains the global endpoint for resource-key requests. Spanish chat translates English-fallback citation titles; glossary matches whole FEMA terms only. Focused regressions were observed failing before the fixes, then passed (8/8). Live Azure verification remains deferred until P1-09.

`make check` (exit 0; last 10 lines):
```text
  ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.5s)
  ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.4s)
  ✓  3 e2e/journey.spec.ts:57:1 › S07 journey and chat work in Spanish (985ms)
  ✓  4 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.2s)
  ✓  5 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (1.0s)
  ✓  6 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (444ms)
  ✓  7 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (476ms)
  ✓  8 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (456ms)

  8 passed (11.5s)
```

Learned: Translator's key-based global URL is not interchangeable with its Entra custom-domain URL; one existing endpoint setting covers both without adding configuration.

## Follow-ups
<!-- Changes needed outside this task's files. -->
