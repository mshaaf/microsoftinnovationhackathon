---
id: P1-01
title: "ZIP to county"
phase: 1
lane: A
status: todo
owner: ""
depends_on: [P0-04]
research: [R11]
branch: ""
---

## Execute in phases
Phase 1, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
POST /api/location resolves a ZIP to one or more counties using a bundled Census ZIP-to-county file; flags multi-county ZIPs.

## Why it matters
Stage 1 starts here, and it's the only location input we collect.

## Files you may touch
- backend/app/features/location/**
- backend/app/adapters/geo/**
- data/geo/zip_county.json
- scripts/build_zip_county.py

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Source file, format, and the 5% land-share rule exactly as R11 describes
- [ ] Single-county ZIP returns one county with needs_confirmation false (96704 → Hawaii County 15001)
- [ ] Multi-county ZIP returns all counties, primary first, needs_confirmation true
- [ ] Unknown or malformed ZIP returns zip_not_found / invalid_input
- [ ] Bundled data file under 5 MB, with source and version noted
- [ ] Response matches the location contract

## Tests to add
- Table-driven unit tests: single (96704), multi (39426), unknown, malformed, leading zeros (00601, 02134)
- Contract test

## How to verify (human, under 5 minutes)
1. `curl -X POST localhost:8000/api/location -H 'content-type: application/json' -d '{"zip":"<demo zip>"}'` returns the demo county.
2. Try a known multi-county ZIP. needs_confirmation is true.
3. Try 00000. You get a clean error.

## Facts to respect
- ZCTAs aren't identical to USPS ZIPs. Note the limitation in the About screen.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
