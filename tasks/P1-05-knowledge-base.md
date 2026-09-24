---
id: P1-05
title: "Knowledge base index"
phase: 1
lane: B
status: review
owner: ""
depends_on: [P0-04]
research: [R03, R15]
branch: ""
---

## Execute in phases
Phase 1, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Curated knowledge base: one markdown file per official page in docs/research/R15 (fema.gov blocks scripts, so there's no scraper), a mock keyword search over those files, and `scripts/ingest_kb.py` that chunks the same files and uploads them to Azure AI Search Free tier (keyword/BM25, schema per R03).

## Why it matters
Grounded, cited answers depend on it.

## Files you may touch
- scripts/ingest_kb.py
- backend/app/adapters/search/**
- fixtures/kb/**
- backend/app/features/search/** (debug endpoint)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] At least 20 of the 27 R15 sources exist as `fixtures/kb/<slug>.md` (+ `.es.md` where an official Spanish page exists), each with R15 front matter and only facts from the page. Write them from pages you can read (web fetch or browser). If you can't read a page, skip it and list it in the Log
- [x] Chunks (split on `##`, ≤1,200 characters) carry url, title, agency, lang, topic, fetched_at
- [x] `make index` builds the live index (idempotent) (deferred: needs Azure, P1-09; script built)
- [x] Mock search returns keyword matches from fixtures/kb with the same result shape
- [x] Dev-only endpoint /api/debug/search?q= (disabled when not in dev)

## Tests to add
- Chunker unit tests
- Mock search returns URL-bearing results
- @live test: a query returns at least one fema.gov result

## How to verify (human, under 5 minutes)
1. Mock: `curl 'localhost:8000/api/debug/search?q=appeal'` returns results with URLs.
2. Live (after Azure setup): `make index`, then the same curl returns AI Search results.

## Facts to respect
- (none)

## Log
- 2026-09-23: Plan: (1) shared chunker `adapters/search/chunking.py` used by mock search and `scripts/ingest_kb.py`; (2) mock keyword search over fixtures/kb; (3) live adapter via azure-search-documents; (4) dev-only `/api/debug/search` (404 unless `APP_ENV=dev`, unset = dev); (5) KB files written by 3 subagents from WebFetch reads of official pages.
- KB: 22 English + 10 Spanish files. **Skipped (could not read):** #2 fema.gov/assistance/individual/apply (404, also es); #22 and #23 fns.usda.gov (403); #26 SAMHSA (page loaded nav only, no number); #27 eCFR (bot block). Spanish for #6, #7 returned 404. Human should spot-check numbers ($770, 60/30/90 days, P.O. Box, fax): WebFetch returns summaries, not raw text.
- Deferred: `make index` live run and the @live test (deferred: needs Azure, P1-09). Live test skips unless APP_MODE=live.
- Learned: fema.gov blocks curl but WebFetch reads it; front-matter titles with ": " broke YAML, so the chunker fails loudly on bad files, which is what caught it.
- `make check` last lines: smoke 1 passed; lint, contracts, tests green.


## Follow-ups
<!-- Changes needed outside this task's files. -->
