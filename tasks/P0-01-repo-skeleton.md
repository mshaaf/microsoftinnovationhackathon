---
id: P0-01
title: "Repo skeleton, Makefile, task board"
phase: 0
lane: shared
status: in_progress
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
- [ ] uv (backend) and pnpm (frontend), per decision 0002. Styling: CSS Modules + `frontend/src/shared/ui/tokens.css`
- [ ] `make setup`, `make dev`, `make test`, `make check`, `make board` work on macOS
- [ ] **Every** target exists: `smoke`, `eval`, `contracts`, `validate-fixtures`, `index`, `test-live`, `smoke-live`. Each non-core target calls a script (`scripts/validate_contracts.py`, `scripts/validate_fixtures.py`, `evals/run.py`, `scripts/ingest_kb.py`, `frontend/e2e`, ...). Stubs print `not implemented yet (<TASK-ID>)` and exit 0. Later tasks replace the stub script, never the Makefile.
- [ ] Makefile does `-include .worktree.env` and exports `API_PORT` (default 8000), `WEB_PORT` (5173), `SMOKE_API_PORT` (8100), `SMOKE_WEB_PORT` (5273). Vite proxies `/api` to `API_PORT`.
- [ ] `make dev` runs API and web with APP_MODE=mock by default
- [ ] `backend/app/main.py` auto-registers every `app/features/*/router.py` that exposes `router` (one loop with pkgutil/importlib), prefix `/api`. In production it also serves `frontend/dist` at `/` with an SPA fallback to index.html (decision 0002 #6).
- [ ] **All dependencies installed now** (decision 0002 #4). Backend: fastapi, uvicorn[standard], pydantic, httpx, python-multipart, pyyaml, jsonschema, agent-framework, azure-identity, azure-ai-documentintelligence, azure-search-documents, azure-monitor-opentelemetry; dev: pytest, pytest-asyncio, ruff, pillow. Frontend: react, react-dom, react-router; dev: vite, typescript, vitest, jsdom, @testing-library/react, @testing-library/user-event, @testing-library/jest-dom, @playwright/test, @axe-core/playwright
- [ ] `make board` prints a table of every tasks/*.md: id, title, phase, lane, status, owner, and flags blocked tasks
- [ ] `scripts/start_task.sh <ID> <slug>`: checks depends_on are done, claims the task on main (frontmatter + commit + push if a remote exists), creates worktree `../mshackathon-<ID>` on `task/<ID>-<slug>`, writes `.worktree.env` with ports offset by a free slot (slot n: +10n), copies `.env` if present, runs `make setup`, and prints the Claude and Codex launch commands plus the session prompt from docs/WORKFLOW.md
- [ ] `scripts/finish_task.sh <ID>`: runs `make check`, pushes the branch, opens a PR with `gh pr create` titled `[<ID>] <title>`
- [ ] `.env.example` matches docs/ARCHITECTURE.md

## Tests to add
- One backend test hitting /api/health
- One frontend component test
- A test for task_board.py frontmatter parsing
- A test that a dummy `features/_probe/router.py` gets auto-registered (or an equivalent unit test of the discovery function)

## How to verify (human, under 5 minutes)
1. `make setup`
2. `make dev`, then open http://localhost:5173. You see 'Survivor Journey Navigator'.
3. Open http://localhost:8000/api/health. You get JSON.
4. `make board`. You see all P0–P4 tasks.
5. `scripts/start_task.sh P0-02 ci`, then `ls ../mshackathon-P0-02` and `cat ../mshackathon-P0-02/.worktree.env`. Ports differ from 8000/5173. Remove it with `git worktree remove ../mshackathon-P0-02` and revert the claim if you're not starting P0-02 yet.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
