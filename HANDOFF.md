# HANDOFF: Phase 0 complete, Phase 1 ready

Last updated **2026-09-23 21:50 ET** after the Phase 0 gate. Start here, then read `AGENTS.md`, `docs/PLAN.md`, and the task file for the work you claim.

## Current state

- **Phase 0 is complete. Gate 0 is logged `PASS` in `docs/TESTING.md`.**
- P0-01 through P0-08 are merged to `main` and marked `done`.
- GitHub PRs #1, #2, and #4–#9 contain the Phase 0 implementation. CI is green.
- Mock mode is the default and requires no Azure credentials or internet access.
- Azure is not provisioned yet. P1-09 is the human-led setup task and can run alongside Phase 1.
- The next legal implementation tasks are **P1-01**, **P1-05**, and **P1-04**, one per worktree/session.

## What Phase 0 delivered

| Task | Delivered |
|---|---|
| P0-01 | Python/React repository skeleton, Make targets, task board, worktree scripts, mock-first local workflow, and router discovery. |
| P0-02 | GitHub Actions CI running `make check` on pull requests and `main`. |
| P0-03 | Frozen JSON Schemas, example payloads, validators, backend contract helpers, and typed frontend API client. |
| P0-04 | Mock/live adapter boundary, model gateway, PII-safe logging, deterministic clock, configuration, and `/api/health`. |
| P0-05 | 15 synthetic scenarios, 8 watermarked FEMA-style letters, 12 OpenFEMA snapshot rows, and fixture validation. |
| P0-06 | Fixture-driven evaluation harness, eight metrics, per-case results, and Markdown/JSON scorecards. Unimplemented Phase 1/2 endpoints remain visibly `not implemented`. |
| P0-07 | Mobile-first shell, eight routes, four-stage stepper, in-memory journey state, English/Spanish toggle, disclaimer, and service-status page. |
| P0-08 | Isolated Chromium journey smoke test, seven 360px screenshots, per-screen axe scans, HTML report, request-capture privacy helpers, and browser-console error detection. |

The setup session also completed the product/architecture/testing workflow and research set `docs/research/R01–R20` (R17 is intentionally deferred with Voice Live).

## Gate 0 evidence

Verified from merged `main` on 2026-09-23:

- `make setup`: passed.
- `make check`: passed.
- Backend: **14 tests passed**.
- Frontend: **13 component tests passed**.
- Playwright: **1 full-journey Chromium test passed** across Help here, Apply, Letter, Deadline, Programs, About, and Status.
- Contracts: **14 examples validated**, including the validator's negative mismatch check.
- Fixtures: **15 scenarios, 8 letters, and 12 OpenFEMA rows validated**.
- Eval: generated `evals/reports/latest.md` and `.json` with **15 scenarios and 8 letters**.
- Health: `/api/health` returned `mode: mock`; all eight runtime services reported `mock`.
- Visual check: L01 and L02 were readable and carried the `SAMPLE — NOT A REAL FEMA LETTER` watermark.
- Accessibility is warn-only through Phase 2. Phase 3 changes critical/serious axe findings to failures.

## Next work: Phase 1

Run these claim commands **sequentially from the clean `main` worktree**; after creation, run the three agents in parallel:

```bash
scripts/start_task.sh P1-01 zip-to-county
scripts/start_task.sh P1-05 knowledge-base
scripts/start_task.sh P1-04 stage1-ui
```

### Session lanes

1. **Lane A — deterministic data and rules**
   - P1-01 ZIP to county
   - P1-02 OpenFEMA declarations
   - P1-03 rules regimes and Serious Needs
   - P1-07 checklist endpoint

2. **Lane B — knowledge and cited chat**
   - P1-05 curated knowledge base and search
   - P1-06 Agent Framework chat with citations

3. **Lane C — survivor interface**
   - P1-04 Stage 1 UI
   - P1-08 Stage 2 checklist/chat UI

4. **Human lane, in parallel**
   - P1-09 Azure resources and local `.env` setup
   - Review/merge PRs and change merged task statuses from `review` to `done`

After all Phase 1 tasks are merged and marked `done`, run and log Gate 1 before starting Phase 2.

## Known follow-ups

- `scripts/dev.sh` forwards `APP_MODE` to the backend but not `VITE_APP_MODE` to Vite. Fix this before relying on `APP_MODE=live make dev` for the browser.
- `scripts/finish_task.sh` still uses a P0-01-specific sentence in every generated PR body. Generalize it when workflow polish is scheduled.
- The exact submission time/time zone is still unknown. The plan assumes Friday 2026-09-25 at 5:00 pm local and targets submission by 2:00 pm.

## Non-negotiable rules for the next agent

- Do not start Phase 2 until Gate 1 is logged `PASS`.
- One task, branch, and worktree per session; stay inside the task's allowed files.
- Test first, run `make check`, record its final output, add a `Learned:` line, set `status: review`, and open the PR.
- After merging, mark the task `done` on `main`; dependencies do not unlock on `review`.
- Personal data never reaches a model. All model calls go through `backend/app/core/model_gateway.py`.
- Mock mode must remain green and runnable even if Azure is unavailable.
