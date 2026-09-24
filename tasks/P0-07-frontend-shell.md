---
id: P0-07
title: "Frontend shell, stepper, status page"
phase: 0
lane: C
status: review
owner: "Codex"
depends_on: [P0-03]
research: []
branch: "task/P0-07-frontend-shell"
---

## Execute in phases
Phase 0, lane C. Wave and session: see docs/PLAN.md. **Start only after none (start now) is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Mobile-first app shell with a 4-stage stepper plus Programs, routes for each stage, an en/es UI toggle, a persistent 'Not FEMA' banner, and a /status page, all driven by contract examples in mock mode.

## Why it matters
The frontend can build every screen before the backend exists.

## Files you may touch
- frontend/src/App.tsx
- frontend/src/App.module.css
- frontend/src/App.test.tsx
- frontend/src/app/**
- frontend/src/features/*/ (placeholder screens)
- frontend/src/features/status/**
- frontend/src/shared/**

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Routes: /, /help-here, /apply, /letter, /deadline, /programs, /status, /about. **All routes are created here** with placeholder screens, so later tasks never edit `routes.tsx`
- [x] i18n loader merges per-feature files `features/<feature>/i18n/{en,es}.json` (Vite `import.meta.glob`), so parallel UI tasks never share a strings file
- [x] Journey state (ZIP, county, answers, disaster number) lives in one React context in memory only. Never localStorage, sessionStorage, or URLs
- [x] CSS Modules per feature + `shared/ui/tokens.css` (decision 0002)
- [x] Stepper shows the current stage and allows going back
- [x] Language toggle switches UI text via shared/i18n
- [x] Banner: 'Not a government website. Not FEMA. FEMA makes all decisions.'
- [x] /status renders /api/health (mock example)
- [x] Looks right at 360px wide

## Tests to add
- Component tests for stepper, language toggle, status page

## How to verify (human, under 5 minutes)
1. Run `make dev` and open http://localhost:5173. Expect the ZIP-code start screen, disclaimer, and four-stage stepper.
2. Use Continue to visit Apply, Letter, and Deadline; use the stepper to return to Help here. Open Programs and About from the header.
3. Select Español. Expect the page title, step names, and disclaimer in Spanish; select English to switch back.
4. Open http://localhost:5173/status. Expect App mode Mock and all eight services: OpenFEMA, Geo, Search, Model, OCR, PII, Translator, and Safety.
5. Set DevTools device width to 360px. Expect no horizontal page scrolling.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

2026-09-23: Plan
- Add the eight required routes and a responsive app shell with the persistent FEMA disclaimer.
- Keep journey data in an in-memory React context; load shared and per-feature English/Spanish strings with Vite globs.
- Add the four-stage stepper and fetch `/api/health` for `/status`.
- Write stepper, language toggle, and status component tests before implementing those behaviors.

2026-09-23: Implemented routes, shared shell, stepper, in-memory journey context, feature-scoped en/es loading, and contract-backed service status. Added route, stepper, language, context, and status coverage. Browser checked home and status at 360px with no horizontal overflow.
Learned: Vite's eager glob imports made feature-owned translation files work without a shared strings file or dependency.

2026-09-23: Review follow-up: widened journey answers for string, boolean, numeric, and null values; synchronized the document language with the UI toggle; added the App entry files to this task's allowlist.

`make check` (exit 0):
```text
   Duration  1.24s (transform 160ms, setup 0ms, collect 666ms, tests 276ms, environment 1.26s, prepare 175ms)

uv run --project backend python scripts/validate_contracts.py
Validator mismatch check passed.
Validator required-contract check passed.
Validated 14 contract examples against their schemas.
uv run --project backend python scripts/validate_fixtures.py
Validated 15 scenarios, 8 letters, and 12 OpenFEMA rows using contract schemas.
bash scripts/smoke.sh
not implemented yet (P0-08)
```
`pnpm --dir frontend build` passed; Vite noted React Router's ignored `use client` module directive.

## Follow-ups
<!-- Changes needed outside this task's files. -->
