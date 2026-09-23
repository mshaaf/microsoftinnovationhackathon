---
id: P0-03
title: "Contracts: schemas, examples, contract tests"
phase: 0
lane: shared
status: in_progress
owner: "codex"
depends_on: [P0-01]
research: [R10, R13]
branch: "task/P0-03-contracts"
---

## Execute in phases
Phase 0, lane shared. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
JSON Schemas and example payloads for every endpoint and data file in docs/CONTRACTS.md, a backend contract-test helper, and a typed frontend client that serves the examples in mock mode.

## Why it matters
Lets frontend and backend build at the same time against identical shapes.

## Files you may touch
- contracts/schemas/*.json
- contracts/examples/*.json
- backend/tests/contract/helpers.py
- frontend/src/shared/api/**
- scripts/validate_contracts.py (replaces the P0-01 stub)
- docs/CONTRACTS.md (only if the schema needs a clarifying note)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] A schema and at least one example for: health, location, declarations, checklist, chat, letter-decode, programs, escalate, error
- [x] declarations includes `registration_deadline` and `registration_open` (R10; already in docs/CONTRACTS.md)
- [x] Schemas for data files: ihp_rules, reason_taxonomy, programs, scenario, letter-expected
- [x] `make contracts` validates all examples and fails on a mismatch
- [x] Backend helper `assert_matches_schema(response, 'declarations')`
- [x] Frontend typed client; mock mode returns the matching example

## Tests to add
- make contracts runs in make check
- A deliberately wrong example fails (unit test of the validator)

## How to verify (human, under 5 minutes)
1. `make contracts`. All pass.
2. Temporarily change `declarations[0].registration_open` in `contracts/examples/declarations.json` from `true` to `"true"`; rerun `make contracts` and confirm it fails at `/declarations/0/registration_open`. Restore the boolean.

## Facts to respect
- Example data is synthetic: disaster 9999, 'Example County'.

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

2026-09-23: Started on draft base `3a3afa6`; P0-01 is at review and not merged. The user explicitly authorized starting P0-03 before that merge. Do not push or open a PR until P0-01 merges; rebase this branch on main first.

Plan:
- Add endpoint and data-file JSON Schemas/examples, matching R10/R13 and the committed P0-05 fixture shapes.
- Add a shared schema validator and a negative mismatch check within its CLI, plus the backend response assertion helper.
- Add a typed frontend request client that serves the matching contract example in mock mode, with a focused client test.
- Run focused checks and `make check`, record results and a learned line, then commit locally without pushing.

Implemented: added 14 schema/example pairs, including the P0-05 scenario fields (`questions`, `needs_confirmation`, `rules_regime`, `serious_needs_available`, chat/injection expectations, and `shelter` handoff). The examples use disaster 9999 and synthetic ZIP 12345. The validator's CLI exercises a deliberately mistyped declaration, then validates every matching schema/example pair. The backend helper was checked against `/api/health`; the frontend client test, typecheck, and production build passed. A read-only validation also accepted all 15 P0-05 scenarios and 8 expected letters.

`make check` exited 0. `validate-fixtures` and smoke still print their P0-05/P0-08 stubs in this draft worktree. P0-01 remains at review, so this task stays `in_progress`; do not push/open a PR until P0-01 merges and this branch is rebased on main.

Last 10 lines of `make check`:

```text
   Start at  18:21:36
   Duration  1.05s (transform 117ms, setup 0ms, collect 262ms, tests 52ms, environment 893ms, prepare 144ms)

uv run --project backend python scripts/validate_contracts.py
Validator mismatch check passed.
Validated 14 contract examples against their schemas.
uv run --project backend python scripts/validate_fixtures.py
not implemented yet (P0-05)
bash scripts/smoke.sh
not implemented yet (P0-08)
```

Learned: the scenario fixtures are the contract for the eval inputs, so validating all committed scenario fields up front caught several fields missing from the original abbreviated example in `docs/CONTRACTS.md`.

Review-fix plan:
- Restrict declaration and checklist rule regimes to the two researched IDs.
- Add and test typed query parameters for live API requests.
- Require the complete contract name set and exercise rejection of a deleted pair.
- Record the Vite mode wiring follow-up, verify, and commit before rebasing on main.

Review fixes: rule regime fields now use the two supported IDs. The frontend client accepts typed `URLSearchParams` and passes them in live fetch URLs; a focused test covers this. The contract validator now requires all 14 schema/example names and exercises a missing-pair negative case.

Review verification: focused frontend test (2 passed), typecheck, `make contracts`, Ruff, and `make check` passed. `make check` exited 0; fixture validation and smoke still report the P0-05/P0-08 stubs.

Last 10 lines of the review `make check`:

```text
   Duration  871ms (transform 87ms, setup 0ms, collect 208ms, tests 48ms, environment 722ms, prepare 140ms)

uv run --project backend python scripts/validate_contracts.py
Validator mismatch check passed.
Validator required-contract check passed.
Validated 14 contract examples against their schemas.
uv run --project backend python scripts/validate_fixtures.py
not implemented yet (P0-05)
bash scripts/smoke.sh
not implemented yet (P0-08)
```

## Follow-ups
<!-- Changes needed outside this task's files. -->
- Pin nested `trigger_conditions` and `tier_logic` shapes in the programs data schema when P1-03/P2-05 define their data format.
- `scripts/dev.sh` forwards `APP_MODE` to the backend only. For `APP_MODE=live make dev`, Vite must also receive `VITE_APP_MODE=live`; update the launcher to forward that value in the owning task, since it is outside P0-03 scope.
