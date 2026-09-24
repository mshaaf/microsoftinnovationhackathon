# HANDOFF: Gate 1 passed; Phase 2 ready

Updated 2026-09-24 ET. Start here, then read `AGENTS.md`, `docs/PLAN.md`, and the task file for the work you claim.

## Current state

- Gates 0 and 1 are logged `PASS` in `docs/TESTING.md`. Phase 2 may start; Phase 3 must wait for Gate 2.
- P0-01–P0-08 and P1-01–P1-08 are merged to `main` and marked `done`. `make board` is the status source.
- Mock mode needs no Azure keys or internet. `make dev` runs the mock backend and connects the browser to that API. Component tests still use frozen contract examples by default.
- P1-09 Azure setup remains `todo`. Live chat and `make test-live` are deferred under AGENTS.md rule 5; they are not part of the mock Gate 1 pass.
- No Phase 2 task has been claimed yet.
- On this machine, use `mshackathon-main` for new task claims. The original `mshackathon` folder remains the older P1-06 task worktree.

## What is complete

| Phase | Delivered |
|---|---|
| 0 | Repo, CI, frozen contracts, mock/live adapter boundary, 15 synthetic scenarios, 8 watermarked letters, 12 OpenFEMA rows, evaluation harness, frontend shell, and browser smoke test. |
| 1 · data/rules | ZIP-to-county lookup; OpenFEMA declarations and active-IA checks; declaration-date rule regimes and Serious Needs dates; deterministic bilingual, sourced checklist. |
| 1 · knowledge/chat | Curated official-page knowledge base and search; cited chat through the model gateway, with no eligibility promises and a low-confidence handoff when no source is found. |
| 1 · interface | ZIP result, county picker, no-declaration guidance, Serious Needs callout, four apply questions, checklist, and chat panel in English and Spanish. |

Gate 1 recovery PRs: [#18](https://github.com/mshaaf/microsoftinnovationhackathon/pull/18) brought P1-06 onto `main`; [#19](https://github.com/mshaaf/microsoftinnovationhackathon/pull/19) added P1-07; [#20](https://github.com/mshaaf/microsoftinnovationhackathon/pull/20) fixed evaluation route detection and historical S14 scoring; [#21](https://github.com/mshaaf/microsoftinnovationhackathon/pull/21) connected local browser flows to the mock API; [#22](https://github.com/mshaaf/microsoftinnovationhackathon/pull/22) added feature and eval tests to `make check`.

## Gate 1 evidence

From the merged mock-mode app:

- `make check`: 97 Python tests passed, 2 live tests skipped; 29 frontend tests and 5 Playwright tests passed. Contracts validated 14 examples; fixtures validated 15 scenarios, 8 letters, and 12 declaration rows.
- `make eval`: Stage 1 **15/15 (100%)**; cited chat **4/4 (100%)**. The S14 pre-2024 rules and Serious Needs checks pass. See `evals/reports/latest.md`.
- Browser tests use the running backend: ZIP 96704 shows DR-4936, Hawaiʻi County, IA open, and the October 1 Serious Needs date; 39426 asks for a county; 02134 shows 211/FEMA guidance; renter + insurance not sure + lost ID shows the correct checklist; all S04 questions return official citations, and the promise question says FEMA decides.
- The full scorecard is not yet all green: letter and program checks belong to Phase 2; emergency, shelter, and sensitive handoffs belong to P3-01. The live Azure checks await P1-09.

To recheck: `git pull --ff-only && make check && make eval && make board` from clean `main`.

## Next work: Phase 2

Claim the first three tasks sequentially from a clean `main` worktree, then run the resulting worktrees in parallel (one task per session, maximum three active agent sessions):

```bash
cd ../mshackathon-main  # from the original mshackathon folder
scripts/start_task.sh P2-04 deadline-math
scripts/start_task.sh P2-01 ocr-adapter
scripts/start_task.sh P2-06 letter-decoder-ui
```

| Lane | First task | Continue after merge |
|---|---|---|
| A · rules (Codex) | P2-04 deadline math | P2-05 program rules/cards API. P2-04 unblocks P2-03. |
| B · letter pipeline (Claude) | P2-01 OCR | P2-02 PII gate, then P2-03 classifier after P2-04 is `done`. |
| C · interface (Claude or Codex) | P2-06 Letter Decoder UI | P2-07 program cards UI. |

P1-09 Azure setup can proceed in the human lane. After P2 tasks merge, run the Gate 2 checklist and its letter/PII eval thresholds before starting Phase 3.

## Follow-ups and boundaries

- For deployment, build the frontend with `VITE_APP_MODE=live` so it calls the deployed API; local `make dev` already sets this while keeping backend `APP_MODE=mock` by default.
- A direct visit to `/apply` without completing Stage 1 still uses the synthetic disaster 9999 fallback. Use the ZIP-first journey in the demo; replace that fallback before feature freeze.
- The checklist's live declaration-number lookup currently lives in its feature service. Move it behind the shared OpenFEMA adapter when live integration is exercised; mock behavior is covered now.
- P1-06 retrieves official sources before the model call. Its declaration/checklist agent tools and live Azure behavior remain to verify after P1-09.
- Keep personal data out of models and logs; do not start a later phase until its prior gate is logged. Stay within each task's file list, test first, run `make check`, and use a task PR before marking `done`.
