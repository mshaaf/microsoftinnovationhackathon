---
id: P3-04
title: "Azure deploy and live smoke"
phase: 3
lane: B
status: todo
owner: ""
depends_on: [P2-06, P1-09]
research: [R08, R09]
branch: ""
---

## Execute in phases
Phase 3, lane B. Wave and session: see docs/PLAN.md. **Start only after Gate 2 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
One Azure Container App serving the API and the built frontend (decision 0002 #6, R08), secrets as Container Apps secrets or managed identity, Application Insights without PII (R09), budget alert, and `make smoke-live URL=...`.

## Why it matters
Judges need a live URL, and 'use of Azure' is scored.

## Files you may touch
- Dockerfile (multi-stage: pnpm build, then python + uv; copy frontend/dist)
- .dockerignore
- scripts/deploy.sh (wraps `az containerapp up --source .`)
- frontend/e2e/live.spec.ts or the smoke-live stub script
- docs/decisions/*deploy*.md

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] One command or workflow deploys both
- [ ] Live health shows every service ok
- [ ] App Insights receives requests; log search for fake names returns nothing
- [ ] Budget alert configured
- [ ] Rollback note in the decision record

## Tests to add
- make smoke-live against the deployed URL
- make test-live green

## How to verify (human, under 5 minutes)
1. Open the public URL on your phone over cellular data and complete Stage 1.
2. `make smoke-live URL=<url>` passes.
3. In App Insights, search L01's fake name. Zero results.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
