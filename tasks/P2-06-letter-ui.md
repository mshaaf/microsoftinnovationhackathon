---
id: P2-06
title: "Letter Decoder UI and appeal draft"
phase: 2
lane: C
status: done
owner: ""
depends_on: [P0-07, P2-03]
research: []
branch: "task/P2-06-letter-ui"
---

## Execute in phases
Phase 2, lane C. Wave and session: see docs/PLAN.md. **Start only after Gate 1 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Upload/camera screen, progress states, 'What we removed' panel, explanation, checklist, countdown, and an appeal draft merged in the browser.

## Why it matters
The hero demo moment.

## Files you may touch
- frontend/src/features/letter/**
- frontend/src/features/deadline/**
- frontend/e2e/letter.spec.ts (letter flow + appeal-draft privacy test)
- frontend/src/app/routes.tsx (wire `/letter` to the screen built by this task)

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] Camera capture on mobile and file picker on desktop
- [x] Progress: reading → removing personal details → explaining
- [x] 'What we removed' shows counts and categories only
- [x] Countdown with appeal_due and days_left
- [x] Appeal draft: template by appeal_template_id; name and registration fields merge locally; copy and print buttons
- [x] Handoff card when handoff is set

## Tests to add
- Component tests
- Playwright: type a name in the appeal draft, then assert it appears in zero network requests

## How to verify (human, under 5 minutes)
1. Run `pnpm --dir frontend test -- LetterPage.test.tsx`. Expect 39 tests passing, including ten letter component tests.
2. Run `make check`. Expect 161 backend tests passed (3 live skipped), 39 frontend tests, contracts and fixtures valid, and 6 Playwright tests passed. The letter Playwright test uploads L03, receives HTTP 200 from `/api/letter/decode`, shows a safe preview without L03 fake PII, and proves typed draft fields never enter a request.
3. In mock mode, open `/letter`, upload L03, type `Jordan` in the draft, and search DevTools → Network requests for `Jordan`. Expect zero hits.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->
2026-09-24 plan:
1. Add component tests for upload, progress, redaction summary, deadline, draft privacy, and handoff.
2. Add a Playwright letter-flow privacy check using network request capture.
3. Build the upload and result screen from the frozen decode contract and local UI strings.
4. Build the deadline and appeal draft from the returned date and template ID; keep draft fields in component state.
5. Run `make check`, record the final output, and hand off the complete letter flow.

2026-09-24 scope correction: P0-07 left `/letter` on a shared placeholder, so the completed feature has no reachable route and the Playwright privacy test cannot run. This task now owns that one route edit. The real decode response also needs P2-03's reason classifier and deadline assembly; P2-03 is added to `depends_on`. Keep the full `make check` pending until P2-03 is merged.

2026-09-24 focused verification: Before wiring the route, `pnpm exec playwright test e2e/letter.spec.ts --timeout=10000` timed out waiting for "Choose a letter". After wiring `/letter` to `LetterPage`, the test reaches `/api/letter/decode` and receives HTTP 404 (expected 200); P2-03 has not merged and the decode router is absent in this worktree. `pnpm --dir frontend typecheck` passes and the frontend suite passes 32/32 tests, including the three letter component tests. Full `make check` remains pending on P2-03. No backend response has been mocked or substituted in the browser test.

2026-09-24 review fixes: Added failing tests first for `days_left: 0`, Spanish date and category labels, and preview text that contains HTML-like input. The UI now says "Due today"/"Vence hoy" at zero days, formats the contract date in the selected language with UTC, translates the four contract example categories, and renders `redacted_preview` as escaped React text. Playwright now checks the preview against every `fake_pii` string in L03's expected fixture. `pnpm --dir frontend test -- LetterPage.test.tsx`: 7 files passed, 34 tests passed (5 letter tests). `pnpm --dir frontend typecheck`: passed. `git diff --check`: passed. Playwright still awaits the real P2-03 decode endpoint; full `make check` remains pending.
2026-09-24 browser check: `pnpm exec playwright test e2e/letter.spec.ts --timeout=15000` starts the app and uploads L03, then fails at `expect(response.status()).toBe(200)`: received 404 from `/api/letter/decode`. The preview and draft privacy assertions cannot run until P2-03 provides that endpoint. Frontend typecheck passed again.
2026-09-24 category review fix: R05 lists Person, Address, PhoneNumber, Email, USSocialSecurityNumber, USBankAccountNumber, CreditCardNumber, USDriversLicenseNumber, USUKPassportNumber, and DateOfBirth; the mock detector also uses RegistrationNumber and FixtureFakePII. Added a failing English/Spanish component test for Email, USSocialSecurityNumber, RegistrationNumber, and an unknown future category. The known categories now have localized labels, and unknown categories display a localized "Other personal detail" label instead of a raw translation key. `pnpm --dir frontend test -- LetterPage.test.tsx`: 7 files passed, 36 tests passed (7 letter tests). `pnpm --dir frontend typecheck` and `git diff --check`: passed. Full `make check` remains pending P2-03.
2026-09-24 ZIP category follow-up: Added failing English and Spanish component cases for `ZipCode`; both showed the generic fallback before the fix. Added explicit "ZIP code" and "Código postal" labels. `pnpm --dir frontend test -- LetterPage.test.tsx`: 7 files passed, 38 tests passed (9 letter tests). `pnpm --dir frontend typecheck` and `git diff --check`: passed. Full `make check` remains pending P2-03.

2026-09-24: Built camera/file upload, ordered progress, redaction counts/categories, explanation/checklist, deadline from API fields, local-only appeal draft with copy/print, and low-confidence handoff. Component tests: 32 passed. Typecheck passed. `make check` reached smoke with backend tests, frontend tests, contracts, and fixtures passing, then failed because `/letter` still renders `FeaturePage`.
Learned: The frozen router has no feature registration seam; the new letter screen needs an authorized shared-route change before an end-to-end check can pass.

2026-09-24 integration: P2-03 PR #29 merged. The real mock decode endpoint returns HTTP 200. Initial full check exposed the existing journey smoke test losing its `Continue` link when `/letter` mounted the new screen. Added a component test, confirmed it failed, then restored the shared `Continue` link to `/deadline`. Focused component tests pass: 39 across 7 files. The journey and letter Playwright tests pass together: 2 passed.

2026-09-24 `make check` passed: 161 backend tests, 3 live skipped; 39 frontend tests; 14 contract examples; 15 scenarios, 8 letters, and 12 OpenFEMA rows; 6 smoke tests. Last 10 lines:
```
Running 6 tests using 1 worker

  ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.4s)
  ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (3.0s)
  ✓  3 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.2s)
  ✓  4 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (441ms)
  ✓  5 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks which county (494ms)
  ✓  6 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (397ms)

  6 passed (9.0s)
```

2026-09-24 independent review: No Critical or Important findings. Review confirmed `/deadline` continuation and the local-only draft privacy path. Reviewer did not run tests.

2026-09-24: PR #30 merged to main after green CI. Status set to done.

## Follow-ups
<!-- Changes needed outside this task's files. -->
- `/deadline` remains a placeholder; P2-06 presents the real appeal countdown and draft inside the letter screen.
