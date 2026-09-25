---
id: P3-03
title: "Accessibility and mobile pass"
phase: 3
lane: C
status: done
owner: ""
depends_on: [P2-06, P2-07]
research: [R16]
branch: "task/P3-03-a11y-mobile"
---

## Execute in phases
Phase 3, lane C. Wave and session: see docs/PLAN.md. **Start only after Gate 2 is logged as passed and every `depends_on` task is `done`.** Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
axe clean (no critical/serious), full keyboard support, visible focus, 360px layouts, 44px targets, reading-level spot check.

## Why it matters
Accessibility is named in the brief and scored in Responsible AI.

## Files you may touch
- frontend/src/**
- frontend/e2e/**

## Do not touch
- Anything not listed above. Put needed changes under Follow-ups.

## Acceptance criteria
- [x] axe in smoke now fails on critical/serious
- [x] Keyboard-only journey works
- [x] Headings, labels, and alt text correct
- [x] Reading level spot-check notes in the task Log

## Tests to add
- axe gating in smoke
- Keyboard navigation Playwright test

## How to verify (human, under 5 minutes)
1. Run `make smoke`. Expect 9 tests to pass, including axe scans with no critical/serious violations and the 360px keyboard journey through the decoded letter and appeal draft.
2. Run `cd frontend && pnpm exec playwright test e2e/keyboard.spec.ts`. Expect one pass; it checks the header brand's 44px target and white focus outline, reaches program cards using real keyboard events, exercises the letter upload and local draft controls, checks visible focus and 44px targets, and detects horizontal overflow.

## Facts to respect
- (none)

## Log
<!-- Agent appends: date, what was done, last 10 lines of `make check`, open questions. -->

2026-09-25 review-fix plan:
- Extend the existing keyboard smoke test to visit the header brand and navigation.
- Assert the brand has a 44px target and focused header controls have a contrasting outline.
- Run the test to confirm both failures before changing CSS.
- Apply the smallest header-only CSS fix, rerun the focused test and `make check`.
- Record the verification result and push the existing PR branch for integration review.

2026-09-25 plan:
- Make smoke fail on critical/serious axe findings and add a regression check for the gate itself.
- Add a keyboard-only Playwright journey using Tab and Enter through the survivor path.
- Fix only accessibility issues exposed by the smoke and keyboard runs; preserve the 44px target and visible-focus rules.
- Review headings, labels, alt text, and representative English/Spanish copy; record a grade 6–8 spot check.
- Run `make check` and `make eval`, restore generated eval reports, and record the results and one `Learned:` line.

2026-09-25:
- Changed the shared axe helper from warning to failing on critical/serious findings. The axe-gate regression test failed before the change on an unnamed button (three serious findings), then passed after the assertion was added. Smoke audits pass on the main path and dynamic checklist, chat, and program-result screens.
- Added a keyboard-only journey from ZIP lookup through the checklist, chat, letter, deadline, and program cards. It uses Tab/Enter plus Space and ArrowRight for native radio controls, checks one h1 per screen, visible focus, 44x44px targets, and no horizontal overflow at the configured 360px viewport.
- The first keyboard run found the letter screen's Continue link was 18px tall. Styled that existing link to a 44px minimum target; the journey then passed.
- Reviewed headings and labels on the exercised screens. No `<img>` elements exist; the redacted letter preview is accessible text in a `<pre aria-label="Redacted preview">`.
- Reading-level spot-check: selected 124 words across English help, apply, letter, and programs descriptions/questions scored grade 4.7 by Flesch–Kincaid using Pyphen syllable counts. The Spanish sample uses short direct sentences; agency names and SNAP remain official terms. The English sample is simpler than the 6–8 grade ceiling. `textstat` could not fetch its optional NLTK cmudict because this environment's CA verification failed, so the same formula was calculated with Pyphen's local English syllable dictionary.
- `make eval` on this task's main-based branch: Stage 1 15/15, program tiers 1/1, deadlines 8/8, letter reasons 8/8, citations 4/4, fake PII 0, injection changes 0; emergency handoff is 0/1 because P3-01's separate PR is not included in this branch. Fresh `make eval` on P3-01's branch passes emergency handoff 1/1.
- `make check` passed: 161 backend tests passed, 3 live tests skipped; 42 frontend tests passed; 14 contract examples and fixtures validated; 9 Playwright tests passed. Last 10 lines:
  ```text
    ✓  2 e2e/axe-gate.spec.ts:4:1 › axe audit rejects a serious violation (376ms)
    ✓  3 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.7s)
    ✓  4 e2e/keyboard.spec.ts:45:1 › survivor can reach the next stages with keyboard only (3.5s)
    ✓  5 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.2s)
    ✓  6 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (983ms)
    ✓  7 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (411ms)
    ✓  8 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (459ms)
    ✓  9 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (384ms)

  9 passed (13.2s)
  ```
- Learned: mouse-driven smoke paths did not reveal the undersized Continue link; the keyboard journey's 44px assertions caught it.
- Review follow-up: changed all text entry to keyboard events; opened the letter chooser with Enter, decoded the synthetic L03 fixture, edited the local appeal draft, and activated Copy draft by keyboard. Its success assertion first failed because the isolated Chromium context lacked clipboard permissions; granting clipboard read/write in this test context made the “Draft copied” status appear. CI measured the focused radio at 800.14px in an 800px viewport, so the viewport assertion now allows up to 1% clipping for subpixel rounding while the label still must meet 44px. The axe regression asserts `button-name` on a valid document. Focus checks require a visible outline and near-full viewport visibility.
- Fresh `make check` after review fixes passed: 161 backend tests passed, 3 live tests skipped; 42 frontend tests passed; 14 contract examples and fixtures validated; all 9 Playwright smoke tests passed. Last 10 lines:
  ```text
    ✓  2 e2e/axe-gate.spec.ts:4:1 › axe audit rejects a serious violation (374ms)
    ✓  3 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.7s)
    ✓  4 e2e/keyboard.spec.ts:49:1 › survivor can reach the next stages with keyboard only (5.3s)
    ✓  5 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.2s)
    ✓  6 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (1.0s)
    ✓  7 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (402ms)
    ✓  8 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (421ms)
    ✓  9 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (345ms)

    9 passed (14.9s)
  ```
- Fresh `make eval` completed; all metrics pass except emergency handoff (0/1), which remains covered by P3-01's separate, unmerged branch. Generated reports were restored after evaluation.
- Review fix: the expanded keyboard test failed on the brand link's 20px target before CSS was changed. The brand now has a 44px target; the dark header uses a white focus outline instead of the low-contrast global rust outline. Header brand, language toggle, and navigation links are exercised by keyboard. Focused test passed.
- Fresh `make check` after the review fix passed: 161 backend tests, 3 live skips, 42 frontend tests, contract/fixture validation, and 9 Playwright tests. Last 10 lines:
  ```text
    ✓  2 e2e/axe-gate.spec.ts:4:1 › axe audit rejects a serious violation (394ms)
    ✓  3 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.9s)
    ✓  4 e2e/keyboard.spec.ts:49:1 › survivor can reach the next stages with keyboard only (5.5s)
    ✓  5 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.1s)
    ✓  6 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (979ms)
    ✓  7 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (475ms)
    ✓  8 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (479ms)
    ✓  9 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (409ms)

    9 passed (15.9s)
  ```
- Learned: testing only the main form controls missed the first focusable link in the page header.

## Follow-ups
<!-- Changes needed outside this task's files. -->
