---
id: P4-03
title: "Presentation deck for the video"
phase: 4
lane: shared
status: "in_progress"
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
- [ ] Every R18 topic has its own slide
- [ ] Speaker notes fit about 90 seconds total
- [ ] Architecture diagram matches what was actually deployed

## How to verify (human, under 5 minutes)
1. Read demo/presentation.md aloud with a timer. It fits in 90–120 seconds.

## Log

## Follow-ups
