---
id: P2-01
title: "OCR adapter"
phase: 2
lane: B
status: "done"
owner: ""
depends_on: [P0-04]
research: [R04]
branch: "task/P2-01-ocr-adapter"
---

## Execute in phases
Phase 2, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Document Intelligence Read adapter (live) and fixture OCR (mock), used by the letter-decode pipeline, with file type and size checks.

## Why it matters
The first step of the Letter Decoder.

## Files you may touch
- backend/app/adapters/ocr/**
- backend/app/features/letter/__init__.py (router discovery)
- backend/app/features/letter/ocr_step.py
- backend/app/features/letter/router.py (upload handling)
- backend/app/features/letter/service.py (create the pipeline skeleton: OCR step only)
- backend/pyproject.toml (register pytest's live marker)
- backend/tests/test_ocr.py (pytest discovery)
- backend/tests/integration/test_ocr_live.py (@live test discovery)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Accepts jpeg/png/pdf up to 10 MB; otherwise file_too_large or unsupported_file
- [x] Files stay in memory, never on disk or in logs
- [x] Returns text, page count, confidence
- [x] Mock matches uploaded fixture letters by name or hash

## Tests to add
- Size/type validation
- No temp files created (assert tmp dir unchanged)
- @live test on L01.png (deferred: needs Azure, P1-09)

## How to verify (human, under 5 minutes)
1. Run `cd backend && PYTHONPATH=. uv run pytest -q tests/test_ocr.py tests/integration/test_ocr_live.py`. Expect 12 passed and the Azure test skipped in mock mode.
2. Run `make dev`, then `curl -s -F file=@fixtures/letters/L01.png -F lang=en http://localhost:8000/api/letter/decode`. Until P2-03 completes the required fields, expect `dependency_unavailable` with “Letter review cannot be completed right now. Try again later.” No OCR call is made.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
2026-09-24 plan:
1. Add focused upload, fixture, and live-adapter tests inside the allowed OCR folder.
2. Stream multipart uploads into a bounded memory buffer and validate type and size.
3. Implement fixture-backed mock OCR and Document Intelligence Read live OCR.
4. Expose the OCR-only pipeline through the frozen letter response shape.
5. Run focused tests and `make check`, then record verification and hand off.

2026-09-24: Initial implementation was blocked because the new tests were outside pytest discovery and router discovery skipped the feature. The endpoint also returned an invented 1970 deadline, and invalid Azure documents looked like outages.

2026-09-24 coordinator scope clarification: add the letter package marker, pytest-discovered test paths, and live marker registration. The original test file was excluded by pytest's `testpaths`; the router was excluded by automatic feature discovery; and the `live` marker was unregistered. This task owns these minimal integration fixes. Keep the endpoint unavailable until P2-03 can return a truthful frozen response; do not publish a fabricated appeal date.

2026-09-24 resumed: Added and ran failing tests for router registration, staged 503 behavior, and Azure 400/503 classification before fixing them. Focused verification: 12 passed, 1 Azure test skipped. After rebase, `make check` passed with 124 backend passed, 3 skipped, 29 frontend passed, 14 contract examples, 15 scenarios/8 letters/12 OpenFEMA rows validated, and 5 smoke tests.

Initial `make check` output (superseded):
```text
[WebServer] INFO:     Waiting for application startup.
[WebServer] INFO:     Application startup complete.
[WebServer] INFO:     Uvicorn running on http://0.0.0.0:8310 (Press CTRL+C to quit)
  ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (918ms)
  ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.7s)
  ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (350ms)
  ✓  4 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (423ms)
  ✓  5 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (345ms)

  5 passed (6.4s)
```
Learned: Router discovery treats a feature as a package only when the folder has `__init__.py`; the scoped package marker is part of endpoint integration, not optional scaffolding.

Pre-review-fix `make check` output (exit 0; last 10 lines):
```text
Running 5 tests using 1 worker

  ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.3s)
  ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.6s)
  ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (418ms)
  ✓  4 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks which county (470ms)
  ✓  5 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (377ms)

  5 passed (8.1s)
```

2026-09-24 review fix: The reviewer found that the staged endpoint called OCR, then returned a retryable error. Changed the stage to validate the upload and stop before any adapter call; the error now says the full review cannot be completed right now. The regression test failed when the OCR adapter was called and now passes. Final `make check`: 124 backend passed, 3 skipped; 29 frontend passed; contracts and fixtures passed; 5 smoke tests passed.

2026-09-24 independent review: No outstanding code findings. The route validates and bounds uploads, then stops before OCR until the safe full response pipeline exists.

Final `make check` output after review fix (exit 0; last 10 lines):
```text
Running 5 tests using 1 worker

  ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.3s)
  ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.9s)
  ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (417ms)
  ✓  4 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks which county (488ms)
  ✓  5 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (400ms)

  5 passed (7.4s)
```

## Follow-ups
<!-- Changes needed outside this task's files. -->
- P2-02/P2-03 complete the redaction and classification steps before `/api/letter/decode` returns a successful frozen response.
