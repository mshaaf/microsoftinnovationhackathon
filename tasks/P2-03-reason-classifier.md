---
id: P2-03
title: "Reason taxonomy and classifier"
phase: 2
lane: B
status: "blocked"
owner: ""
depends_on: [P2-02, P2-04, P2-08]
research: [R01, R12]
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

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Model returns JSON: decision type, assistance types, reason ids + confidence, letter date, disaster number
- [ ] Code validates: letter date parses; disaster number exists in OpenFEMA (sets disaster_number_verified)
- [ ] Reasons below the taxonomy threshold, or other_or_unclear, set handoff
- [ ] Checklist comes from the taxonomy (code), not the model
- [ ] Explanation is grounded in the taxonomy text and translated per lang

## Tests to add
- Validation unit tests (bad date, unknown disaster)
- Structured-output adapter tests, including deterministic mock classification.
- Eval: reason accuracy ≥ 7/8 letters in mock; report live accuracy separately
- L07 leads to handoff; L08 behavior unchanged

## How to verify (human, under 5 minutes)
1. Upload L01–L06. Each shows the expected reason.
2. Upload L07 and get a handoff card.
3. `make eval`. The letter accuracy row passes.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
2026-09-24 scope correction: The acceptance path requires a global disaster-number lookup, but the existing OpenFEMA adapter only supports county queries. P2-08 now owns the adapter capability; this task depends on it so validation stays in the adapter boundary. The route currently discards upload bytes and language, so this task also owns passing the validated in-memory upload and language through OCR to response assembly. No implementation has started. Resume after P2-08 is merged.

## Follow-ups
<!-- Changes needed outside this task's files. -->
