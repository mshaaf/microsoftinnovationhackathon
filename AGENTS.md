# AGENTS.md: Survivor Journey Navigator

Instructions for every AI coding agent in this repo: **Codex CLI and Claude Code read this same file** (`CLAUDE.md` just imports it). Nested `backend/AGENTS.md` and `frontend/AGENTS.md` add rules for those folders. Humans start with README.md and docs/WORKFLOW.md.

## What we're building

A **demo-ready, not production-ready** web app for the Microsoft Innovation Studio hackathon (Disaster Assistance Navigator track), due **Friday 2026-09-25**. A disaster survivor:

1. enters a ZIP code and learns whether FEMA Individual Assistance is open for their county,
2. gets a document checklist for applying,
3. photographs a confusing FEMA decision letter and gets a plain-language explanation,
4. gets a checklist, a draft appeal note, and a deadline countdown,
5. sees other programs they may qualify for ("Everything you're owed").

Full context: docs/PRODUCT.md. Demo disaster: **DR-4936-HI (Kona Earthquake, Hawaiʻi County), demo ZIP 96704** (docs/research/R10).

## Execute in phases

The build runs in **phases with gates** (docs/PLAN.md). Up to **3 agent sessions run in parallel**, each in its own git worktree, each on **one task**.

- **Never start a task from a later phase** until that phase's gate is logged as passed in docs/TESTING.md, **and** every task in your `depends_on` has `status: done`.
- Stay inside your task's **"Files you may touch"**. That list is what keeps parallel sessions from colliding.
- Inside your session, execute your task in these phases, in order:
  1. **Read.** This file, docs/PLAN.md (find your phase and wave), your task file, docs/CONTRACTS.md, and any docs/research/R*.md named in your task's `research:` field.
  2. **Plan.** Write a 3–7 line plan in your task Log before editing code.
  3. **Test first.** Add or extend tests for the acceptance criteria.
  4. **Build.** Make the tests pass. Smallest change that meets the criteria.
  5. **Verify.** `make check` must pass. Paste its last 10 lines in the Log.
  6. **Hand off.** Fill in "How to verify", add a `Learned:` line to the Log, set `status: review`, commit, open the PR.

## Read before writing code (in this order)

1. This file.
2. docs/PLAN.md: the current phase, wave, and gate.
3. Your task file in tasks/. **It is your entire scope.**
4. docs/CONTRACTS.md and contracts/: the API shapes you must match.
5. docs/research/R*.md listed in your task's `research:` field. **These are the verified facts.** Don't re-research them; don't contradict them.
6. docs/TESTING.md: how your work gets verified.

Also read docs/ARCHITECTURE.md and docs/RESPONSIBLE_AI.md if your task touches AI, Azure, or personal data.

## Golden rules

1. **One task per session, one branch per task, one worktree per session.** Branch: `task/<TASK-ID>-<short-slug>`.
2. **main is always green and runnable in mock mode.** Never merge a red build.
3. **Every change ships with tests.** No test means not done.
4. **Every task ends with a "How to verify" section** a human can run in under 5 minutes, with exact commands and expected results.
5. **Mock mode is the default** (`APP_MODE=mock`). Tests never need Azure keys or internet access. **Azure isn't provisioned yet.** Acceptance criteria that need live Azure (`@live` tests, `make test-live`, `make index`) are **deferred, not blocking**: build the live adapter code, mark those checkboxes `(deferred: needs Azure, P1-09)`, and the task can still reach `done`.
6. **Anything that must be exactly right is plain code, not AI.** Eligibility signals, deadlines, dollar amounts, dates, and rule versions are computed in code from data files. AI only understands, reads, explains, and translates.
7. **Personal data never reaches a model.** Letter text flows OCR → PII redaction → model. Every model call goes through `backend/app/core/model_gateway.py`. Never log raw letter text, images, names, addresses, phone numbers, or FEMA registration numbers.
8. **Stay inside the files your task lists.** If you need a change elsewhere, write it under "Follow-ups" in your task file. Don't make it.
9. **Contracts are frozen unless your task says otherwise.** A contract change needs `[CONTRACT]` in the PR title, updated `contracts/` and `docs/CONTRACTS.md`, and a new decision record in `docs/decisions/`.
10. **No new dependencies.** P0-01 installs everything the plan needs. If you truly need another one, stop and ask (Follow-ups + `status: blocked`). Lockfile conflicts across parallel branches cost more than the feature.
11. **Never commit secrets.** Only `.env.example` is committed.
12. **If blocked or unsure, stop.** Set `status: blocked`, write the question under "Log", and end the session. Never guess on facts: if docs/research doesn't answer it, it's a question for the human.
13. **Don't edit shared files** (`Makefile`, lockfiles, `backend/app/main.py`, `frontend/src/app/routes.tsx`, CI) unless your task file lists them. P0 tasks set these up so later tasks never need to.

## Commands (run from repo root)

| Command | What it does |
|---|---|
| `make setup` | Install backend and frontend dependencies |
| `make dev` | Run API and web in mock mode. Ports come from `API_PORT`/`WEB_PORT` (default 8000/5173; each worktree gets its own via `.worktree.env`) |
| `make test` | Unit and contract tests, backend and frontend |
| `make smoke` | Playwright end-to-end smoke test in mock mode (uses `SMOKE_API_PORT`/`SMOKE_WEB_PORT`) |
| `make check` | Lint + typecheck + test + contracts + fixtures + smoke. **Must pass before you finish.** |
| `make eval` | Scenario and letter evals, writes `evals/reports/latest.md` |
| `make contracts` | Validate every example in `contracts/examples/` against its schema |
| `make board` | Print the task board from task-file frontmatter |
| `make validate-fixtures` | Validate scenarios and expected-letter files against contracts |
| `make index` | Upload `fixtures/kb/*.md` to the Azure AI Search index (live) |
| `make test-live` | Integration tests against real Azure. Needs `.env`; humans run this at gates. |
| `make smoke-live URL=...` | Smoke test against a deployed URL |

Every target exists from P0-01 on. A target whose task isn't done yet prints `not implemented yet (<TASK-ID>)` and exits 0. The owning task replaces the stub **script**, never the Makefile.

## Definition of done

All of these must be true before you set `status: review`:

- Every acceptance criterion in the task file is checked off (or marked deferred per rule 5).
- New or changed logic has unit tests. New endpoints have contract tests. UI changes update component tests or the smoke test.
- `make check` passes locally. Paste the last 10 lines of its output into the task file's Log.
- The "How to verify" section has exact steps and expected results.
- The Log has one `Learned:` line (what surprised you, what you'd do differently). The final presentation's "key learnings" come from these.
- Work is committed on the task branch. A PR is open with the task ID in the title, e.g. `[P1-02] OpenFEMA declarations lookup`. If your sandbox can't push, say so in the Log; the human runs `scripts/finish_task.sh`.

## Repo map

| Path | Contents | Conventions |
|---|---|---|
| `backend/` | FastAPI app, Python 3.12, uv | `backend/AGENTS.md` |
| `frontend/` | React + TypeScript + Vite, pnpm | `frontend/AGENTS.md` |
| `contracts/` | JSON Schemas + example payloads | Source of truth for API shapes |
| `data/` | Rules, reason taxonomy, programs, checklist items, escalation rules, ZIP→county | Versioned JSON; every fact has a source URL |
| `fixtures/` | Synthetic letters, OpenFEMA snapshots, scenarios, curated knowledge base | Synthetic only, never real letters or people |
| `evals/` | Eval runner and reports | |
| `scripts/` | Task start/finish, board, builders, validators | |
| `tasks/` | One file per task | Status lives in each file's frontmatter |
| `docs/` | Product, architecture, plan, testing, workflow, RAI, demo, decisions, research | Agents edit docs only when their task says so |

## Style

- Small PRs: aim for under 400 changed lines.
- Plain names over clever ones. Comments explain why, not what.
- User-facing text: plain language, short sentences, about a 6th–8th grade reading level, sentence case.
- Never tell a user they *are* eligible. FEMA and other agencies decide. Say "may qualify" and name who decides.
