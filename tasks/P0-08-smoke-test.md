---
id: P0-08
title: "Playwright smoke and accessibility check"
phase: 0
lane: C
status: "in_progress"
owner: ""
depends_on: [P0-07]
research: [R16]
branch: "task/P0-08-smoke-test"
---

## Execute in phases
Phase 0, lane C. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
One Playwright test that walks the full journey in mock mode, plus an axe-core scan of each screen, wired into `make smoke` and `make check`.

## Why it matters
Catches a broken main path in about a minute, on every PR.

## Files you may touch
- frontend/e2e/** (helpers + `journey.spec.ts`; stage tasks add their own `<stage>.spec.ts`)
- frontend/playwright.config.ts

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Playwright `webServer` starts API and web on `SMOKE_API_PORT`/`SMOKE_WEB_PORT`, so it never clashes with `make dev` in other worktrees
- [ ] One spec per stage (`stage1`, `apply`, `letter`, `programs`) is the convention. This task creates `journey.spec.ts` (walks every placeholder stage) and shared helpers
- [ ] Smoke test visits every stage in order using mock data
- [ ] axe scan per screen; warn-only until Phase 3, then critical/serious violations fail
- [ ] Network assertion helper ready for the appeal-draft privacy test (used in P2-06)
- [ ] HTML report generated

## Tests to add
- The smoke test itself

## How to verify (human, under 5 minutes)
1. `make smoke`. It passes. Open the HTML report and see each step with a screenshot.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
