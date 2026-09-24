---
id: P2-01
title: "OCR adapter"
phase: 2
lane: B
status: "in_progress"
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
- backend/app/features/letter/ocr_step.py
- backend/app/features/letter/router.py (upload handling)
- backend/app/features/letter/service.py (create the pipeline skeleton: OCR step only)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Accepts jpeg/png/pdf up to 10 MB; otherwise file_too_large or unsupported_file
- [ ] Files stay in memory, never on disk or in logs
- [ ] Returns text, page count, confidence
- [ ] Mock matches uploaded fixture letters by name or hash

## Tests to add
- Size/type validation
- No temp files created (assert tmp dir unchanged)
- @live test on L01.png

## How to verify (human, under 5 minutes)
1. Upload L01.png to /api/letter/decode (partial pipeline OK). The response has an ocr block with confidence.
2. Upload a 12 MB file and get file_too_large.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
