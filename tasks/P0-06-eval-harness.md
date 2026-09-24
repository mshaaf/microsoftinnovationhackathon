---
id: P0-06
title: "Eval harness and scorecard"
phase: 0
lane: B
status: "review"
owner: ""
depends_on: [P0-03, P0-05]
research: []
branch: "task/P0-06-eval-harness"
---

## Execute in phases
Phase 0, lane B. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
`make eval` runs every scenario and letter through the API in the current mode, scores against expected results, and writes evals/reports/latest.md plus latest.json.

## Why it matters
Turns 'it seems to work' into a scorecard we can track and show judges.

## Files you may touch
- evals/** (`evals/run.py` replaces the P0-01 stub)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Metrics and thresholds from docs/TESTING.md, one table row each
- [x] Per-case pass/fail table; endpoints not built yet show 'not implemented' instead of crashing
- [x] Runs in mock mode in under 60 seconds
- [x] Report header shows mode, git commit, and timestamp

## Tests to add
- Unit tests for each scorer

## How to verify (human, under 5 minutes)
1. Run `PYTHONPATH=. uv run --project backend pytest -c backend/pyproject.toml evals/test_scoring.py evals/test_run.py -q`. Expect all 18 tests to pass.
2. Run `make eval`, then open `evals/reports/latest.md`. Expect 15 scenario rows, 8 letter rows, all 8 metrics and thresholds, plus mode, commit, and UTC timestamp. Currently unavailable API routes show `not implemented`.
3. Run `make check`. Expect exit code 0; the P0-08 smoke target may still print its scaffold message.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

2026-09-23 plan:
1. Add unit tests for percentage, zero-leak, deadline, and injection scorers.
2. Implement a mock-first runner that loads all scenarios and expected letters and calls registered API routes through FastAPI's test client.
3. Treat absent routes as `not implemented`; score observed outputs against fixtures and documented thresholds.
4. Write mode, commit, UTC timestamp, metrics, and per-case results to `evals/reports/latest.md` and `latest.json`.
5. Run scorer tests, `make eval`, and `make check`; record verification and hand off the task.

2026-09-23 — Implemented the fixture-driven evaluator with FastAPI's in-process test client, metric scorers, report generation, and fake-PII monitoring for model payloads and logs. Added scorer and report tests; all 11 focused tests passed. `make eval` completed in under one second and wrote scorecard files for all 15 scenarios and 8 letters; all API-dependent results show `not implemented` because those endpoints are not registered yet. The metrics table includes all eight documented thresholds.

2026-09-23 review fixes:
1. Add runner regression tests for unsafe explanations/chat replies, split denial-plus-unsafe instructions, legacy DR-9999 results, and referenced letter decode/handoff failures.
2. Score injection against both L08's explanation and S10's reply; constrain the sensitive-action matcher to one sentence.
3. Evaluate S14's rules and Serious Needs values using its referenced DR-9999 snapshot county while keeping ZIP 02134 Stage 1 independent.
4. Include each referenced letter's checks in its scenario status.
5. Rerun focused tests, `make check`, and `make eval`; confirm absent API routes remain `not implemented`.

Verification: 18 focused tests passed; `make check` passed; `make eval` completed in under one second with 15 scenarios, 8 letters, all 8 metrics, and API-dependent results marked `not implemented`.

`make check` output (last 10 lines):
```text
   Duration  868ms (transform 93ms, setup 0ms, collect 190ms, tests 49ms, environment 754ms, prepare 149ms)

uv run --project backend python scripts/validate_contracts.py
Validator mismatch check passed.
Validator required-contract check passed.
Validated 14 contract examples against their schemas.
uv run --project backend python scripts/validate_fixtures.py
Validated 15 scenarios, 8 letters, and 12 OpenFEMA rows using contract schemas.
bash scripts/smoke.sh
not implemented yet (P0-08)
```

Learned: a score with no implemented endpoint must stay visibly unevaluated; reporting it as zero would look like a real failed result and mislead the next task.

## Follow-ups
<!-- Changes needed outside this task's files. -->
