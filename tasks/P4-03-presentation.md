---
id: P4-03
title: "Presentation deck for the video"
phase: 4
lane: shared
status: in_progress
owner: ""
depends_on: []
research: [R18]
branch: "task/P4-03-presentation"
---

## Execute in phases
Phase 4, lane shared. Wave and session: see docs/PLAN.md. **Draft any time after Gate 1** (an agent can write the first draft from docs/). Finalize after Gate 3 with the real eval numbers. Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
A short deck (6–8 slides) for the video's presentation part. It must cover what R18 requires: project **goals**, **solution components and architecture**, **how we thought through the approach**, and **key learnings**.

## Why it matters
The submission is a video with a demo **and** a presentation. Without this, the submission is incomplete.

## Files you may touch
- demo/presentation.md (slide text and speaker notes)
- demo/architecture.svg or .png (diagram)
- demo/deck.* (exported deck: pptx, pdf, or a Claude slides artifact link noted in presentation.md)

## Slides
1. The problem (GAO numbers from PRODUCT.md, the 60-day clock)
2. Goals (the 5-stage journey, who it's for)
3. Solution components (Azure services table: Foundry model + Agent Framework, AI Search, Document Intelligence, Language PII, Translator, Content Safety, Container Apps, App Insights)
4. Architecture (the diagram from ARCHITECTURE.md; the privacy boundary)
5. Approach: code decides, AI explains; contracts first; mock mode; parallel agents in phases with gates; evals
6. Responsible AI you can see (PII removed before the model, citations, honest tiers, handoff)
7. Results (eval scorecard numbers from `evals/reports/latest.md`)
8. Key learnings (harvest the `Learned:` lines from every task Log: `grep -h "Learned:" tasks/*.md`)

## Acceptance criteria
- [x] Every R18 topic has its own slide
- [x] Speaker notes total 195 words, about 90 seconds at 130 words per minute
- [x] Draft diagram matches the current mock-mode runtime and labels Azure targets as unprovisioned
- [ ] Refresh results and deployment claims after Gate 3, then export a 6–8 slide deck

## How to verify (human, under 5 minutes)
1. For the draft, read `demo/presentation.md` aloud with a timer. Expect about 90 seconds for the notes at 130 words per minute, and 90–120 seconds total with slide transitions. A final exported deck is still pending Gate 3.

## Log

2026-09-25 plan:
- Draft eight slides and speaker notes in `demo/presentation.md`; do not export a deck or record video.
- Source problem, goals, architecture, and Responsible AI claims from PRODUCT, ARCHITECTURE, RESPONSIBLE_AI, DEMO, and R18.
- Show Azure services as planned targets; label the current mock deployment and pre-Gate-3 eval snapshot clearly.
- Synthesize the `Learned:` entries across P0–P3 into concise, task-sourced takeaways.
- Verify all R18 topics, slide count, note length near 90 seconds, and `make check`; leave finalization for after Gate 3.

2026-09-25:
- Drafted eight slides in `demo/presentation.md` covering the problem, goals, planned Azure components, current mock architecture and privacy boundary, approach, visible Responsible AI, provisional eval results, and synthesized P0–P3 task learnings.
- Kept deployment claims explicit: the solid architecture path is the runnable mock app; Azure targets are marked unprovisioned. The scorecard uses the 2026-09-24 report and flags emergency handoff 0/1 before P3-01 integration.
- Review correction: changed the 911-first emergency card from a current-behavior claim to a P3-01 feature pending integration.
- Verified eight slides, all R18 topics, and 195 speaker-note words (about 90 seconds at 130 words per minute). No deck export or recording was made; this is the requested first draft.
- `make check` passed: 161 backend tests passed, 3 live tests skipped; 42 frontend tests passed; 14 contract examples and fixtures validated; 7 Playwright smoke tests passed. Last 10 lines from the final run:
  ```text
  [WebServer] (Use `node --trace-warnings ...` to show where the warning was created)
  Running 7 tests using 1 worker
    ✓  1 e2e/apply.spec.ts:3:1 › renter, not sure, lost ID shows checklist and a chat link (1.3s)
    ✓  2 e2e/journey.spec.ts:18:1 › a survivor can walk through every placeholder stage (2.8s)
    ✓  3 e2e/letter.spec.ts:8:1 › letter draft fields stay in the browser (1.1s)
    ✓  4 e2e/programs.spec.ts:3:1 › S07 sees five program cards in Spanish urgency order (929ms)
    ✓  5 e2e/stage1.spec.ts:3:1 › stage 1 happy path in mock mode (347ms)
    ✓  6 e2e/stage1.spec.ts:21:1 › multi-county ZIP asks the survivor to choose (427ms)
    ✓  7 e2e/stage1.spec.ts:33:1 › ZIP without an active declaration shows other help (345ms)

  7 passed (9.2s)
  ```
- Learned: a provisional scorecard and a clearly labeled mock architecture let the team draft the story early without presenting unprovisioned services or unfinished gate results as final.
- Integration review: this PR is a mergeable draft, not a completed P4-03 task. Leave status `in_progress` until a final deck is exported and checked against the integrated eval and actual deployment state.

## Follow-ups
- After Gate 3, rerun `make eval`, update the architecture to match the actual deployment, and finalize/export the deck.
