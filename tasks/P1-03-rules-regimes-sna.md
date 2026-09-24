---
id: P1-03
title: "Rules regimes and Serious Needs window"
phase: 1
lane: A
status: done
owner: ""
depends_on: [P1-02]
research: [R13]
branch: "task/P1-03-rules-regimes-sna"
---

## Execute in phases
Phase 1, lane A. Wave and session: see docs/PLAN.md. **Start only after Gate 0 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
data/ihp_rules.json plus logic that picks the rules regime by declaration date and fills the serious_needs block (amount by effective date, apply_by = declaration + 30 days, extension_possible).

## Why it matters
The most time-sensitive benefit in the journey. It must be exactly right.

## Files you may touch
- data/ihp_rules.json
- backend/app/features/rules/**
- backend/app/features/declarations/service.py (attach rules output only)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Regime 'pre-2024-03-22' for earlier declarations: serious_needs.available false
- [x] Regime '2024-03-22' for declarations on or after 2024-03-22: amount chosen by effective date
- [x] apply_by = declaration_date + 30 days
- [x] Every value has a source_url; file has last_verified
- [x] Nothing in the rules file stays marked VERIFY once R13 is answered

## Tests to add
- Boundaries: 2024-03-21 vs 2024-03-22
- Month-end and leap-year date math
- Amount switch at the $770 effective date
- Schema validation of the rules file

## How to verify (human, under 5 minutes)
1. Run `PYTHONPATH=backend:. uv run --project backend pytest backend/app/features/rules backend/app/features/declarations -q`; expect 24 passed and 1 live test skipped.
2. Run `API_PORT=8080 WEB_PORT=5253 make dev` in one terminal.
3. Run `curl -sS 'http://localhost:8080/api/declarations?state=HI&county_fips=15001'`; DR-4936 should show regime `2024-03-22`, amount `770`, and `apply_by: 2026-10-01`.

## Facts to respect
- Values in docs/research/R13: $750 for declarations 2024-03-22..2024-09-30, $770 for declarations on/after 2024-10-01 (by **declaration date**). 30-day window; may extend to 60 on state/territory/Tribal request.
- Callout copy says FEMA *may* offer it (R13 caveat for DR-4936).

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

2026-09-24 plan:
- Add table-driven tests for the March 22 regime boundary, $770 effective date, and 30-day date arithmetic.
- Add a schema-validated, source-linked IHP rules file from R13.
- Implement declaration-date rule selection and attach Serious Needs fields in the declarations service.
- Run focused rules/declaration tests and `make check`, then complete the task handoff.

2026-09-24:
- Added `data/ihp_rules.json` with the R13 regimes, amount schedule, and source records; added declaration-date selection, 30-calendar-day apply-by math, and Serious Needs response fields.
- Focused verification: `PYTHONPATH=backend:. uv run --project backend pytest backend/app/features/rules backend/app/features/declarations -q` → 24 passed, 1 live test skipped. The rules data validates against the existing IHP rules schema.
- The first `make check` smoke run hit a transient Playwright artifact-cleanup `ENOENT`; the isolated rerun passed all checks: 19 backend passed, 1 live skipped, 29 frontend passed, contracts and fixtures passed, and 3 smoke tests passed.
- `make check` last 10 lines:
  ```text
  [WebServer] (node:32718) Warning: The 'NO_COLOR' env is ignored due to the 'FORCE_COLOR' env being set.
  [WebServer] (Use `node --trace-warnings ...` to show where the warning was created)

  Running 3 tests using 1 worker

    ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.0s)
    ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.0s)
    ✓  3 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (376ms)

    3 passed (7.0s)
  ```
- Learned: the amount and deadline both follow the disaster's declaration date, so using today's date would return the wrong benefit for older declarations.
- Status: review. No open implementation questions.

## Follow-ups
<!-- Changes needed outside this task's files. -->

- Frontend follow-up: update English and Spanish Serious Needs callout copy to say FEMA may offer it. R13 notes the DR-4936 press release and FAQ do not mention SNA; the existing copy says “You may qualify” and “FEMA decides.” Frontend files are outside P1-03's scope.
