---
id: P0-01
title: "Repo skeleton, Makefile, task board"
phase: 0
lane: shared
status: done
owner: "luna-s1"
depends_on: []
research: []
branch: "task/P0-01-repo-skeleton"
---

## Execute in phases
Phase 0, lane shared. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
A runnable skeleton that lets 3 parallel sessions work without touching shared files: FastAPI app with a stub /api/health and router auto-discovery, a Vite React TypeScript app, a Makefile with **every** command in AGENTS.md (stubs delegate to scripts), all dependencies pre-installed, per-worktree ports, and the task start/finish/board scripts.

## Why it matters
Every other task depends on these commands existing.

## Files you may touch
- Makefile
- backend/** (initial scaffold only)
- frontend/** (initial scaffold only)
- scripts/** (task_board.py, start_task.sh, finish_task.sh, and stub scripts for later targets)
- .env.example
- .gitignore
- .editorconfig

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] uv (backend) and pnpm (frontend), per decision 0002. Styling: CSS Modules + `frontend/src/shared/ui/tokens.css`
- [x] `make setup`, `make dev`, `make test`, `make check`, `make board` work on macOS
- [x] **Every** target exists: `smoke`, `eval`, `contracts`, `validate-fixtures`, `index`, `test-live`, `smoke-live`. Each non-core target calls a script (`scripts/validate_contracts.py`, `scripts/validate_fixtures.py`, `evals/run.py`, `scripts/ingest_kb.py`, `frontend/e2e`, ...). Stubs print `not implemented yet (<TASK-ID>)` and exit 0. Later tasks replace the stub script, never the Makefile.
- [x] Makefile does `-include .worktree.env` and exports `API_PORT` (default 8000), `WEB_PORT` (5173), `SMOKE_API_PORT` (8100), `SMOKE_WEB_PORT` (5273). Vite proxies `/api` to `API_PORT`.
- [x] `make dev` runs API and web with APP_MODE=mock by default
- [x] `backend/app/main.py` auto-registers every `app/features/*/router.py` that exposes `router` (one loop with pkgutil/importlib), prefix `/api`. In production it also serves `frontend/dist` at `/` with an SPA fallback to index.html (decision 0002 #6).
- [x] **All dependencies installed now** (decision 0002 #4). Backend: fastapi, uvicorn[standard], pydantic, httpx, python-multipart, pyyaml, jsonschema, agent-framework, azure-identity, azure-ai-documentintelligence, azure-search-documents, azure-monitor-opentelemetry; dev: pytest, pytest-asyncio, ruff, pillow. Frontend: react, react-dom, react-router; dev: vite, typescript, vitest, jsdom, @testing-library/react, @testing-library/user-event, @testing-library/jest-dom, @playwright/test, @axe-core/playwright
- [x] `make board` prints a table of every tasks/*.md: id, title, phase, lane, status, owner, and flags blocked tasks
- [x] `scripts/start_task.sh <ID> <slug>`: checks depends_on are done, claims the task on main (frontmatter + commit + push if a remote exists), creates worktree `../mshackathon-<ID>` on `task/<ID>-<slug>`, writes `.worktree.env` with ports offset by a free slot (slot n: +10n), copies `.env` if present, runs `make setup`, and prints the Claude and Codex launch commands plus the session prompt from docs/WORKFLOW.md
- [x] `scripts/finish_task.sh <ID>`: runs `make check`, pushes the branch, opens a PR with `gh pr create` titled `[<ID>] <title>`
- [x] `.env.example` matches docs/ARCHITECTURE.md

## Tests to add
- One backend test hitting /api/health
- One frontend component test
- A test for task_board.py frontmatter parsing
- A test that a dummy `features/_probe/router.py` gets auto-registered (or an equivalent unit test of the discovery function)

## How to verify (human, under 5 minutes)
1. `make setup`, then `make check`. Both exit successfully; Phase 0 stubs print `not implemented yet (<TASK-ID>)`.
2. `make dev`, then open http://localhost:5173. The page shows “Survivor Journey Navigator”.
3. `curl -fsS http://localhost:8000/api/health`. The JSON includes `"mode":"mock"` and the mock service statuses.
4. `make board`. It lists the P0–P4 tasks and their IDs, titles, phases, lanes, statuses, and owners.
5. After P0-01 is merged and marked done on main, run `scripts/start_task.sh P0-02 ci`; check `../mshackathon-P0-02/.worktree.env` for offset ports. Remove the worktree and revert its claim if you are not starting P0-02.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

Plan:
1. Add failing health, router-discovery, frontend title, and task-board parsing tests.
2. Build the minimal FastAPI and Vite skeleton, install the specified dependencies, and wire every required Make target through scripts.
3. Implement task board, worktree start/finish scripts, and later-task stubs within the allowed paths.
4. Run setup, targeted tests, and `make check`; record exact human verification steps and the final check output.
5. Commit P0-01 and open its PR if the configured remote and GitHub CLI allow it.

2026-09-23 — Added the mock API health route and discovery loop, frontend skeleton, locked dependencies, Makefile targets, task board, and task lifecycle scripts. Ran `make setup`, `make test`, `make board`, all stub targets, `make dev` plus API/web curl checks, and the launcher in a temporary Git repo. `make check` passed.

`make check` output (last 10 lines):
```text
      Tests  1 passed (1)
   Start at  17:54:31
   Duration  830ms (transform 56ms, setup 0ms, collect 143ms, tests 43ms, environment 333ms, prepare 80ms)

uv run --project backend python scripts/validate_contracts.py
not implemented yet (P0-03)
uv run --project backend python scripts/validate_fixtures.py
not implemented yet (P0-05)
bash scripts/smoke.sh
not implemented yet (P0-08)
```

Learned: Agent Framework 1.x pulls its Azure AI Search adapter as a prerelease, so the project lock must allow that dependency graph and include Azure Search SDK 12.

## Follow-ups
- P0-06 owns `evals/run.py`; `scripts/eval.sh` invokes it automatically once that task adds the file.
