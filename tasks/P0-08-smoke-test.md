---
id: P0-08
title: "Playwright smoke and accessibility check"
phase: 0
lane: C
status: "review"
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
- [x] Playwright `webServer` starts API and web on `SMOKE_API_PORT`/`SMOKE_WEB_PORT`, so it never clashes with `make dev` in other worktrees
- [x] One spec per stage (`stage1`, `apply`, `letter`, `programs`) is the convention. This task creates `journey.spec.ts` (walks every placeholder stage) and shared helpers
- [x] Smoke test visits every stage in order using mock data
- [x] axe scan per screen; warn-only until Phase 3, then critical/serious violations fail
- [x] Network assertion helper ready for the appeal-draft privacy test (used in P2-06)
- [x] HTML report generated

## Tests to add
- The smoke test itself

## How to verify (human, under 5 minutes)
1. Run `make smoke`. Expect one Chromium journey test to pass.
2. Run `open frontend/playwright-report/index.html`. Expect axe results and screenshots for Help here, Apply, Letter, Deadline, Programs, About, and Status.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

2026-09-23 plan:
1. Add a journey spec that follows every placeholder stage and checks the visible route outcome.
2. Run it before configuration exists to confirm the smoke target fails for the missing Playwright setup.
3. Add shared axe, screenshot, and request-capture helpers plus a per-worktree Playwright configuration.
4. Run the journey smoke test, inspect its HTML report, then run the full `make check` gate.
5. Record verification, the accessibility warning policy, and the human handoff steps here.

2026-09-23 implementation and verification:
- Added a one-worker Chromium configuration that starts the existing mock API and Vite app on this worktree's dedicated smoke ports.
- Added one journey spec covering all placeholder stages plus About and Status at a 360px viewport.
- Added shared screenshot, WCAG-tagged axe, and request-capture/privacy assertion helpers. Axe remains warn-only through Phase 2 as required.
- RED: the first direct Playwright run failed because no base URL/server configuration existed. GREEN: `make smoke` passed after adding the configuration; seven report screenshots were visually checked and no critical/serious axe warnings appeared.

`make check` output (last 10 lines):
```text
[WebServer] INFO:     Application startup complete.
[WebServer] INFO:     Uvicorn running on http://0.0.0.0:8130 (Press CTRL+C to quit)
[WebServer] (node:95854) Warning: The 'NO_COLOR' env is ignored due to the 'FORCE_COLOR' env being set.
[WebServer] (Use `node --trace-warnings ...` to show where the warning was created)

Running 1 test using 1 worker

  ✓  1 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.1s)

  1 passed (4.9s)
```

Learned: Playwright report attachments make one compact test useful for both route verification and visual/accessibility evidence without committing screenshots.

## Follow-ups
<!-- Changes needed outside this task's files. -->
