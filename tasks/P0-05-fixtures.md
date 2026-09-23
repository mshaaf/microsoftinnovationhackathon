---
id: P0-05
title: "Synthetic letters, scenarios, OpenFEMA snapshot"
phase: 0
lane: A
status: todo
owner: ""
depends_on: []   # runs in wave 0A alongside P0-01; only new folders
research: [R10, R12, R20]
branch: ""
---

## Execute in phases
Phase 0, lane A. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
8 synthetic FEMA-style letters (L01–L08) with OCR text and expected results, 15 survivor scenarios (S01–S15), and an OpenFEMA snapshot for the demo disaster.

## Why it matters
Tests, evals, and the demo all run on these. A human (M) must review them for realism.

## Files you may touch
- fixtures/letters/**
- fixtures/scenarios/**
- fixtures/openfema/**
- fixtures/kb/README.md
- scripts/make_letters.py
- scripts/validate_fixtures.py (replaces the P0-01 stub; schema checks become strict once P0-03 merges)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Letters: L01 identity_not_verified, L02 ownership_not_verified, L03 insurance_docs_missing (demo letter: renter, DR-4936, letter date **2026-09-15**, appeal due 2026-11-14), L04 occupancy_not_verified, L05 insufficient_damage, L06 missed_inspection_or_contact, L07 unclear/garbled, L08 needs-information letter containing a prompt-injection instruction
- [ ] Each letter: PNG rendered to look like a phone photo (slight skew/noise) + .txt (mock OCR) + .expected.json with fake_pii list
- [ ] Every letter shows 'SAMPLE — NOT A REAL FEMA LETTER'
- [ ] Scenarios: S01 renter uninsured (happy path); S02 owner insured; S03 renter, not sure about insurance, lost ID; S04 three chat questions + a promise-seeking question; S05 Rosa, Spanish-speaking renter with L03 (demo persona); S06 emergency phrase; S07 gig worker, renter, car flooded, Spanish; S08 off-topic question; S09 displaced, no shelter tonight; S10 injection letter L08; S11 unclear letter L07; S12 multi-county ZIP; S13 ZIP with no active declaration; S14 disaster declared before 2024-03-22; S15 sensitive topic needing the sensitive handoff card
- [ ] OpenFEMA snapshot `fixtures/openfema/declarations_snapshot.json` with real rows for DR-4936 (HI) and DR-4930 (MS) using the R10 command, plus a synthetic statewide row (county `000`) and a synthetic pre-2024-03-22 disaster for S14
- [ ] Letters L01–L06 and L08 reference DR-4936. Scenario ZIPs: demo 96704, S12 multi-county 39426, S13 no declaration 02134 (R10)
- [ ] `fixtures/kb/README.md` explains the curated-KB format from R15
- [ ] `make validate-fixtures` validates scenarios and expected files against contracts

## Tests to add
- validate-fixtures runs in make check

## How to verify (human, under 5 minutes)
1. Open 3 PNGs in fixtures/letters/. Each has the watermark and reads like a plausible FEMA letter.
2. `make validate-fixtures` passes.
3. Skim S07.yaml. It matches the gig-worker story in docs/CONTRACTS.md.

## Facts to respect
- Letters are modeled on FEMA's public explainers only. Never use a real person's letter.
- Fake phone numbers use the 555-01xx range.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
