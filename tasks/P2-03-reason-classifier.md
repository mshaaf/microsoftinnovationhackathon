---
id: P2-03
title: "Reason taxonomy and classifier"
phase: 2
lane: B
status: todo
owner: ""
depends_on: [P2-02, P2-04]
research: [R01, R12]
branch: ""
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
- backend/app/features/letter/service.py (classify step + attach deadline by calling `features/deadline/service.py`)

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

## Follow-ups
<!-- Changes needed outside this task's files. -->
