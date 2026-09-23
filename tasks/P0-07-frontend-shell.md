---
id: P0-07
title: "Frontend shell, stepper, status page"
phase: 0
lane: C
status: todo
owner: ""
depends_on: [P0-03]
research: []
branch: ""
---

## Execute in phases
Phase 0, lane C. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Mobile-first app shell with a 4-stage stepper plus Programs, routes for each stage, an en/es UI toggle, a persistent 'Not FEMA' banner, and a /status page, all driven by contract examples in mock mode.

## Why it matters
The frontend can build every screen before the backend exists.

## Files you may touch
- frontend/src/app/**
- frontend/src/features/*/ (placeholder screens)
- frontend/src/features/status/**
- frontend/src/shared/**

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [ ] Routes: /, /help-here, /apply, /letter, /deadline, /programs, /status, /about. **All routes are created here** with placeholder screens, so later tasks never edit `routes.tsx`
- [ ] i18n loader merges per-feature files `features/<feature>/i18n/{en,es}.json` (Vite `import.meta.glob`), so parallel UI tasks never share a strings file
- [ ] Journey state (ZIP, county, answers, disaster number) lives in one React context in memory only. Never localStorage, sessionStorage, or URLs
- [ ] CSS Modules per feature + `shared/ui/tokens.css` (decision 0002)
- [ ] Stepper shows the current stage and allows going back
- [ ] Language toggle switches UI text via shared/i18n
- [ ] Banner: 'Not a government website. Not FEMA. FEMA makes all decisions.'
- [ ] /status renders /api/health (mock example)
- [ ] Looks right at 360px wide

## Tests to add
- Component tests for stepper, language toggle, status page

## How to verify (human, under 5 minutes)
1. `make dev`. On http://localhost:5173, click through every stage.
2. Toggle Español. UI text changes.
3. Open /status. You see every service listed.
4. DevTools device mode at 360px. Nothing overflows.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

## Follow-ups
<!-- Changes needed outside this task's files. -->
