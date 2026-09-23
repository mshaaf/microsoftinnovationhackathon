# HANDOFF: current status and next steps

Last updated 2026-09-23 by Claude Code (setup session). Whoever picks this up (Codex, Claude, or M) reads this file, then `AGENTS.md`.

## Tool compatibility
- **Codex CLI reads `AGENTS.md`** (root, plus `backend/AGENTS.md` and `frontend/AGENTS.md` in those folders). Every rule lives there.
- `CLAUDE.md` only imports `AGENTS.md` for Claude Code. It has no rules of its own, so Codex misses nothing.
- Global `~/.codex/AGENTS.md` isn't needed.

## Done (setup session)
- Docs flattened to repo root; `git init` on `main`; `.gitignore` added.
- **Research complete**: `docs/research/R01–R20` (R17 voice deferred). Every VERIFY marker outside research is resolved.
- Key findings that changed the plan (decision `docs/decisions/0002-research-driven-decisions.md`):
  - Demo disaster **DR-4936-HI Kona Earthquake**, Hawaii County, ZIP **96704**; IA registration open until 2026-11-01.
  - SNA **$770** for declarations on/after 2024-10-01 ($750 before). 2024 IA rule still in effect.
  - OpenFEMA: use `ihProgramDeclared`, and `lastIAFilingDate` for "registration open".
  - **fema.gov web pages return 403 to scripts**, so the knowledge base is curated markdown in `fixtures/kb/`, not scraped.
  - One Foundry (AIServices) resource covers model + PII + Translator + Content Safety + DocIntel. One Container App serves API + frontend.
  - Agent Framework is GA (`agent-framework` 1.19). Code patterns are in R01.
- Plan rewritten for **solo + 3 parallel sessions** in phases, waves, and lanes (`docs/PLAN.md`, `docs/WORKFLOW.md`).
- Conflict hotspots removed from task files: no Makefile edits after P0-01, router auto-discovery, all routes in P0-07, per-feature i18n, one e2e spec per stage, all deps installed in P0-01, per-worktree ports.
- Every task file has an "Execute in phases" block. New tasks: `P1-09` Azure setup (human), `P4-03` presentation deck.
- Hackathon requirement (R18): a **video with demo + presentation** (goals, components/architecture, approach, key learnings). Every task Log needs a `Learned:` line.

## Not done yet: next steps, in order
1. ~~Initial commit~~ done.
2. **GitHub repo** (M decides the name and visibility): `gh repo create mshackathon --private --source . --push`.
3. **Wave 0A** (docs/WORKFLOW.md → Bootstrap): launch **P0-01** and **P0-05** in two worktrees at the same time.
4. When P0-01 merges, use `scripts/start_task.sh` for everything after.
5. M, in parallel: `tasks/P1-09-azure-setup.md` when the Azure subscription is ready.

## Open questions for M
- Exact submission time and time zone (assumed 5 pm local; plan to submit by 2 pm Friday).
- GitHub repo name and visibility.
