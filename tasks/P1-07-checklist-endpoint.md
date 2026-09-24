---
id: P1-07
title: "Checklist endpoint"
phase: 1
lane: A
status: "in_progress"
owner: ""
depends_on: [P1-03]
research: [R12, R13]
branch: "task/P1-07-checklist-endpoint"
---

## Execute in phases
Phase 1, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
POST /api/checklist returns a deterministic document checklist from the answers and the rules regime, each item with a source.

## Why it matters
Stage 2's core output, and it must be exact.

## Files you may touch
- backend/app/features/checklist/**
- data/checklist_items.json

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Covers own/rent, insured yes/no/not sure, lost ID, displaced
- [ ] Each item has id, text (en/es), why, source_url
- [ ] Regime-aware (e.g. no SBA-first item for the 2024-03-22 regime)

## Tests to add
- Table-driven tests over all answer combinations used in scenarios
- Contract test

## How to verify (human, under 5 minutes)
1. curl the checklist with renter + not sure + lost ID. You get occupancy, insurance, and identity items with links.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
