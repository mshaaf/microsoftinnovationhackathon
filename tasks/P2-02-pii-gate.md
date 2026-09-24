---
id: P2-02
title: "PII redaction gate and leak tests"
phase: 2
lane: B
status: "review"
owner: ""
depends_on: [P2-01]
research: [R05]
branch: "task/P2-02-pii-gate"
---

## Execute in phases
Phase 2, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Azure Language PII redaction on OCR text (live), a mock redactor, the redaction block in responses, and leak tests across all letters.

## Why it matters
The core Responsible AI promise: personal data never reaches a model.

## Files you may touch
- backend/app/adapters/pii/**
- backend/app/features/letter/redact_step.py
- backend/app/features/letter/service.py (insert the redact step)
- backend/app/core/model_gateway.py (guard wiring)
- backend/tests/**/test_pii_*.py

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Entity categories per R05, including names, addresses, phone numbers, and ID-like numbers
- [x] The redaction component returns `redaction.entities_removed`, `categories`, and `redacted_preview`; P2-03 attaches these fields to the full `/api/letter/decode` response.
- [x] For every fixture letter, no fake_pii string appears in the redacted text, model payloads, or captured logs
- [x] If PII detection fails, the redaction component raises a safe `NotConfigured` error and the model gateway never calls the model; P2-03 verifies the endpoint maps this to `dependency_unavailable`.

## Tests to add
- Leak test over L01–L08
- Fail-closed test
- Log capture test

## How to verify (human, under 5 minutes)
1. Run `PYTHONPATH="$PWD/backend:$PWD" APP_MODE=mock uv run --project backend pytest backend/tests/test_pii_live.py backend/tests/test_pii_redaction.py -q`. The leak, category, adapter, response-field, language, and fail-closed tests pass.
2. Run `make check`. Expected: lint, typecheck, tests, contracts, fixtures, and smoke pass.
3. The HTTP endpoint remains staged until P2-03 assembles the complete response; its contract behavior is verified there.

## Facts to respect
- Document PII redaction is batch/Blob-based; we use text PII after OCR (confirm in R05).

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

- Plan: Add leak, chunk-boundary, Unicode-offset, and fail-closed tests using synthetic letters L01–L08.
- Share category/span results between mock and live PII adapters, with labeled replacement and full-text regex fallback.
- Implement the Azure Language REST adapter and keep model-gateway detection fail-closed.
- Pass the requested language through the model guard, including Spanish.
- Keep `/letter/decode` safely staged; P2-03 assembles the contract-valid full response from the redaction fields.
- Initial `make check` before the Spanish guard fix: backend 144 passed/3 skipped, frontend 29 passed, contracts/fixtures passed, smoke 5 passed. Superseded by the final check below.
- Initial output (superseded):
  ```

  Running 5 tests using 1 worker

    ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.2s)
    ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.9s)
    ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (400ms)
    ✓  4 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (430ms)
    ✓  5 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (385ms)

    5 passed (7.2s)
  ```
- 2026-09-24 scope clarification: P2-01 deliberately stages the endpoint until a full frozen response is ready. P2-02 owns the redaction component, its serializable response fields, and fail-closed behavior; P2-03 owns attaching these fields to the complete API response and verifying the HTTP 503 mapping. Gate 2 still requires the successful endpoint and remains open until P2-03 and the UI tasks pass.
- 2026-09-24 implementation: Added the Azure Language adapter, shared mock/live categories and regex fallback, Unicode-safe redaction, and fail-closed behavior. Leak checks cover L01–L08. The Spanish model-guard regression failed first because the detector received `en`; it passed after forwarding `lang`. Focused PII tests: 21 passed. Live Azure is deferred per AGENTS.md rule 5.
- Independent review after the task-boundary clarification confirmed the redaction response fields and Spanish detector path; no remaining P2-02 component findings. The full endpoint remains P2-03/Gate 2 work.
- Final `make check`: backend 145 passed/3 skipped, frontend 29 passed, 14 contract examples, 15 scenarios/8 letters/12 OpenFEMA rows, and smoke 5 passed. Last 10 lines:
  ```

  Running 5 tests using 1 worker

    ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.4s)
    ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.0s)
    ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (448ms)
    ✓  4 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (494ms)
    ✓  5 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (388ms)

    5 passed (7.7s)
  ```
- Learned: Keeping the HTTP route staged until all contract fields exist avoids publishing incomplete results or inventing classification facts; P2-02 supplies reusable response fields for P2-03.

## Follow-ups
<!-- Changes needed outside this task's files. -->
- Verify in P2-03 that the full `/api/letter/decode` response includes the fields from `RedactionResult.response_fields()` and detector errors map to `dependency_unavailable`.
- Chat's response mapping for `NotConfigured` is outside this task; the model call is still stopped. Revisit if chat needs the same 503 contract mapping.
