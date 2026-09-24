# Plan

**Target:** demo-ready and submitted by **Friday, September 25, 2026**. The exact time wasn't given. Assume 5:00 pm local and **submit by 2:00 pm** (R18).
**Team:** one human (M), with up to **3 agent sessions in parallel** (Claude Code and Codex CLI), each in its own git worktree.
**Azure:** not provisioned yet. Everything is built **mock-first**. Live Azure lands when P1-09 is done, and nothing else waits on it.

Demo-ready means:
- It runs from a public Azure URL **and** locally in mock mode. If Azure never happens, a mock-mode deploy or local demo is the fallback.
- Every must-have in docs/PRODUCT.md passes its gate check.
- The eval scorecard meets the thresholds in docs/TESTING.md.
- A **video** exists with (1) a demo and (2) a presentation covering goals, solution components and architecture, how we thought through the approach, and key learnings (R18). There's also a fallback demo recording made in mock mode.

## Execute in phases

1. Phases run in order: **0 → 1 → 2 → 3 → 4**. A phase ends at its **gate**, and the next phase starts only after the gate checklist in docs/TESTING.md passes and is logged.
2. Inside a phase, tasks run in **waves**. Tasks in the same wave run **at the same time** in separate sessions and never touch the same files.
3. Each session takes **one lane** for the whole phase and works its lane's tasks in the order listed. That keeps one agent's context warm and removes cross-session conflicts.
4. A task starts only when every `depends_on` task is `done` (merged to main).
5. Merge order inside a wave: whichever finishes first. Rebase on main right before merging.

## Lanes = sessions

| Session | Lane | Owns | Suggested agent |
|---|---|---|---|
| S1 | A: Data & rules | OpenFEMA, ZIP-to-county, rules, checklist, deadlines, programs (deterministic backend) | Codex (table-driven tests suit it) |
| S2 | B: AI & Azure | Adapters, model gateway, KB/search, chat, letter pipeline, PII, safety, translation, deploy | Claude Code |
| S3 | C: Frontend | Journey UI, letter upload, cards, status page, i18n, accessibility, smoke tests | Claude Code or Codex |
| M | humans | Reviews, gates, Azure setup (P1-09), demo, presentation | M |

Cross-review: a PR written by Codex gets reviewed by Claude, and the reverse (docs/WORKFLOW.md). M does the final 5-minute skim and merge.

## Gates

| Gate | Target time | Meaning |
|---|---|---|
| Gate 0 | Wed 11:59 pm | Skeleton, contracts, mock mode, fixtures, test harness all work |
| Gate 1 | Thu 1:00 pm | Stage 1 (help here?) and Stage 2 (checklist + cited chat) work in mock |
| Gate 2 | Thu 10:00 pm | Letter Decoder and program cards work; PII leak tests green |
| Gate 3 | Fri 10:00 am | **Feature freeze.** Deployed (Azure if P1-09 done), Spanish, handoff and safety, accessibility pass |
| Gate 4 | Fri 2:00 pm | Video recorded (demo + presentation), submitted |

## Phase 0: Foundation (Wednesday evening)

| Wave | S1 | S2 | S3 |
|---|---|---|---|
| 0A (start now) | **P0-01** Repo skeleton, Makefile, board, scripts | **P0-05** Fixtures: letters, scenarios, OpenFEMA snapshot (content only; new folders, no conflicts) | M: create the GitHub repo, review research, start P1-09 Azure signup |
| 0B (after P0-01 merged) | **P0-03** Contracts | **P0-04** Mock mode, adapters, model gateway | **P0-02** CI (small), then idle |
| 0C (after P0-03 merged) | **P0-07** Frontend shell (then P0-08) | **P0-06** Eval harness (needs P0-05) | **P0-08** Smoke + axe (after P0-07 merges) |

**Critical path:** P0-01 → P0-03 → P0-07 → P0-08. Keep S1 on it.

## Phase 1: Help here + apply (Thursday morning)

| Session | Order |
|---|---|
| S1 (A) | P1-01 ZIP to county → P1-02 OpenFEMA declarations → P1-03 Rules and SNA → P1-07 Checklist endpoint |
| S2 (B) | P1-05 Knowledge base (curated markdown) → P1-06 Agent and cited chat |
| S3 (C) | P1-04 Stage 1 UI → P1-08 Stage 2 UI and chat panel (both build on contract examples) |
| M | **P1-09 Azure setup** (whenever the subscription is ready). Review PRs. |

## Phase 2: Letter Decoder + programs (Thursday afternoon and evening)

| Session | Order |
|---|---|
| S1 (A) | P2-04 Deadline math → P2-05 Programs rules and endpoint → P2-08 OpenFEMA disaster-number lookup |
| S2 (B) | P2-01 OCR adapter → P2-02 PII gate and leak tests → P2-03 Reason classifier (needs P2-04 and P2-08) |
| S3 (C) | P2-06 Letter Decoder UI and appeal draft → P2-07 Program cards UI |
| M | Draft P4-03 presentation outline from docs (an agent can do the first draft) |

P2-08 was added after tracing P2-03's acceptance path: the existing OpenFEMA adapter only looks up declarations by county, but letter validation must verify arbitrary disaster numbers globally. The feature task depends on this adapter capability; no letter-specific network call belongs in the feature service.

## Phase 3: Safety, language, deploy (Friday morning, ends at feature freeze)

| Session | Order |
|---|---|
| S1 | P3-01 Escalation and safety, then P3-04 Azure deploy (needs P1-09) |
| S2 | P3-02 Spanish end to end |
| S3 | P3-03 Accessibility and mobile pass |
| — | P3-05 Voice Live: stretch, only if Gate 3 is green with time left (it won't be; plan to cut) |

## Phase 4: Video + submission (Friday, by 2 pm)

| Task | Who |
|---|---|
| P4-03 Presentation deck (goals, components/architecture, approach, learnings) | agent drafts, M finalizes |
| P4-01 Demo script, rehearsal, recordings (fallback first) | M |
| P4-02 Submission package | M + agent |

## If we fall behind: cut in this order

1. Voice Live (P3-05)
2. Azure deploy of everything: keep live Foundry model + mock for the rest, or a mock-mode deploy
3. Program card polish (plain list is fine)
4. Chat panel (keep the checklist; the chat can be a single "ask a question" box)
5. Letter reason types beyond the 4 most common

**Never cut:** tests, the PII gate, Stage 1, Letter Decoder, mock-mode fallback, the handoff card, the video.

## Freeze rules

- After Gate 3, only bug fixes and demo polish merge.
- If main goes red, every session stops feature work until it's green again ("stop the line").
