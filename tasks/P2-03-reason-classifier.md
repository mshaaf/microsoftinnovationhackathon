---
id: P2-03
title: "Reason taxonomy and classifier"
phase: 2
lane: B
status: done
owner: ""
depends_on: [P2-02, P2-04, P2-08]
research: [R01, R12, R10]
branch: "task/P2-03-reason-classifier"
---

## Execute in phases
Phase 2, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
data/reason_taxonomy.json (7 reasons incl. other_or_unclear) and a structured-output classifier over redacted text, validated by code, with low-confidence handoff.

## Why it matters
Turns a confusing letter into a specific next step.

## Files you may touch
- data/reason_taxonomy.json
- backend/app/features/letter/classify_step.py
- backend/app/features/letter/service.py
- backend/app/features/letter/router.py
- backend/app/features/letter/ocr_step.py
- backend/app/features/letter/test_decode.py
- backend/app/adapters/model/live.py
- backend/app/adapters/model/mock.py
- backend/app/adapters/model/test_structured.py
- backend/tests/test_ocr.py

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Model returns structured JSON: decision type, assistance types, reason IDs + confidence, letter date, and disaster number.
- [x] Code parses the letter date and checks the disaster number through OpenFEMA (`disaster_number_verified`). Synthetic mock rows stay unverified (R10).
- [x] Reasons below the taxonomy threshold, or `other_or_unclear`, set handoff.
- [x] Checklist comes from the taxonomy (code), not the model.
- [x] Explanation uses taxonomy text in the requested language.

## Tests to add
- [x] Validation tests cover bad dates, an OpenFEMA-absent disaster number, a synthetic snapshot row, the confidence threshold boundary, L07 handoff, and unchanged L08 behavior.
- [x] Structured-output adapter tests cover the live response format and deterministic mock classification.
- [x] `make eval`: mock reason accuracy 8/8, deadlines 8/8, fake PII 0, injection behavior unchanged. Live accuracy (deferred: needs Azure, P1-09).

## How to verify (human, under 5 minutes)
1. Run `uv run --project backend pytest backend/app/features/letter/test_decode.py backend/app/adapters/model/test_structured.py backend/tests/test_ocr.py`. Expected: 30 passed.
2. Run `make eval`. Expected: letters 8/8, deadlines 8/8, fake PII 0, L07 handoff, and L08 injection pass.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
2026-09-24 scope correction: The acceptance path requires a global disaster-number lookup, but the existing OpenFEMA adapter only supports county queries. P2-08 now owns the adapter capability; this task depends on it so validation stays in the adapter boundary. The route currently discards upload bytes and language, so this task also owns passing the validated in-memory upload and language through OCR to response assembly. No implementation has started. Resume after P2-08 is merged.

2026-09-24 resume plan after P2-08 merge:
1. Add the sourced seven-reason taxonomy and structured letter output model.
2. Add failing tests for mock/live structured output, date and disaster validation, L07 handoff, and response contract/privacy.
3. Pass the validated upload bytes and language through OCR, redaction, classification, and frozen response assembly.
4. Derive checklist and explanation from taxonomy data and calculate the deadline through the existing deadline service.
5. Run focused tests, `make check`, and `make eval`; record the final evidence before handoff.

2026-09-24 resumed: P2-08 PR #28 merged to main; P2-02, P2-04, and P2-08 are all done.

2026-09-24 scope correction: Added `backend/tests/test_ocr.py` to this task's file list with coordinator approval. It asserts the endpoint is still staged and expects 503 for valid uploads, so it must change alongside P2-03 enabling the full decode pipeline.

2026-09-24 build: Routed validated upload bytes and `lang` through OCR, PII redaction, the model gateway, OpenFEMA validation, taxonomy output, and deadline math. Mock 9999 is a synthetic snapshot row: it remains available for its pre-2024 deadline regime but is not verified as a real disaster (R10). `make eval`: letters 8/8, deadlines 8/8, PII leaks 0, L07 handoff and L08 injection pass; aggregate emergency handoff is 0/1 (P3-01 follow-up). Live accuracy is deferred because Azure is not provisioned (P1-09).

2026-09-24 review follow-up: Added a separate absent-number case for 987654; it verifies OpenFEMA returns no declaration, the confident classification still hands off as unverified, and the valid letter date still produces the 2026-11-14 deadline. This is distinct from synthetic 9999, whose mock declaration is retained only to select the pre-2024 regime.

2026-09-24 `make check` passed: 161 backend passed, 3 live skipped; 29 frontend passed; 14 contract examples and 15 scenarios/8 letters/12 OpenFEMA rows validated; 5 smoke tests passed. Focused decode/model/OCR tests passed: 30. The 7-reason taxonomy also validates against its JSON schema. The coordinator independently reran `make check` with the same totals. Last 10 lines:

```text
Running 5 tests using 1 worker

  ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.4s)
  ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.9s)
  ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (361ms)
  ✓  4 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (480ms)
  ✓  5 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (380ms)

  5 passed (7.7s)
```

2026-09-24 independent review: No blockers. Defer missing model-output behavior refinement because the letter response contract is frozen; defer live SDK initialization error handling verification until Azure is available (P1-09).

Learned: The OpenFEMA snapshot contains synthetic rows used by other evaluations; existence in the mock snapshot is not enough to claim a disaster number is verified.

2026-09-24: PR #29 merged to main after independent review and green CI. Status set to done.

## Follow-ups
<!-- Changes needed outside this task's files. -->
