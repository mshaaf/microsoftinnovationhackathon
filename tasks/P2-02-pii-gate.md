---
id: P2-02
title: "PII redaction gate and leak tests"
phase: 2
lane: B
status: todo
owner: ""
depends_on: [P2-01]
research: [R05]
branch: ""
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
- [ ] Entity categories per R05, including names, addresses, phone numbers, and ID-like numbers
- [ ] Response includes redaction.entities_removed, categories, and redacted_preview
- [ ] For every fixture letter, no fake_pii string appears in the redacted text, model payloads, or captured logs
- [ ] If PII detection fails, the pipeline stops with dependency_unavailable (fail closed)

## Tests to add
- Leak test over L01–L08
- Fail-closed test
- Log capture test

## How to verify (human, under 5 minutes)
1. Upload L03. The response shows entities_removed ≥ 3 and the preview shows [PERSON]/[ADDRESS] instead of the fake name.
2. `make test`. All test_pii_* pass.

## Facts to respect
- Document PII redaction is batch/Blob-based; we use text PII after OCR (confirm in R05).

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
