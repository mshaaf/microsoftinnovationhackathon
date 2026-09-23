# 0002: Decisions from the research pass

Date: 2026-09-23. Status: accepted. Evidence: docs/research/R01–R20.

| # | Decision | Why | Alternatives considered |
|---|---|---|---|
| 1 | Solo builder + up to 3 parallel agent sessions (Claude Code + Codex CLI), one lane each, git worktrees | Team is one human | Two-human lanes (original plan) |
| 2 | Package managers: **uv** (backend), **pnpm** (frontend) | Both installed; fast; lockfiles | pip/poetry, npm |
| 3 | Styling: **CSS Modules + one `shared/ui/tokens.css`** (no CSS framework) | Native to Vite, zero deps, per-feature files mean no conflicts across sessions | Tailwind (extra dep + config), global CSS (conflicts) |
| 4 | All dependencies installed in P0-01; later tasks add none | Avoids lockfile conflicts across parallel branches | Add as needed |
| 5 | Routers auto-discovered; all frontend routes created in P0-07; per-feature i18n files; one Playwright spec per stage | Removes every shared-file conflict hotspot | One-line-per-feature edits with manual conflict resolution |
| 6 | **One Container App serves API + built frontend** (replaces 0001 #11) | One deploy command, one URL, no CORS, no Static Web Apps pipeline | ACA + Static Web Apps |
| 7 | **One Microsoft Foundry (AIServices) resource** for the model, Language PII, Translator, Content Safety, Document Intelligence | One endpoint, one credential, 5 services | Separate resources per service |
| 8 | Model: newest "mini" chat model available (gpt-5-mini or newer), Global Standard, name in `FOUNDRY_MODEL` | Tool calling + structured outputs; gpt-4.1 retiring in 2026 | gpt-4.1-mini |
| 9 | Agent Framework (`agent-framework` 1.x, GA) imported **only** in `adapters/model/live.py` | Mock mode and tests never touch the network | Framework throughout |
| 10 | Simple REST services (PII, Translator, Prompt Shields) via `httpx`; SDKs only for Document Intelligence and AI Search | Fewer deps, easy to mock | SDK for everything |
| 11 | **Knowledge base is curated markdown** in `fixtures/kb/`, feeding both mock search and AI Search | fema.gov returns HTTP 403 to scripts (R15); curated text is also more reliable | Scraper |
| 12 | AI Search **Free tier, keyword (BM25) only**, no vectors | ~40 short pages; free; fewer moving parts. Upgrade: add integrated vectorization if citation relevance fails evals | Basic tier + vectors + semantic ranker |
| 13 | Document Intelligence **S0**, model `prebuilt-read` | F0 caps at 2 pages / 4 MB | F0 with 4 MB upload limit |
| 14 | PII redaction = GA text PII + our own `[CATEGORY]` replacement from offsets + regex for 9-digit numbers; `DateTime` category off | Keeps the letter date for deadline math; registration numbers aren't a built-in category | Preview redaction policies |
| 15 | Secrets: Container Apps secrets + managed identity where easy; Key Vault is an upgrade path, not required | Time | Key Vault references |
| 16 | "IA open" = `ihProgramDeclared or iaProgramDeclared`; registration open = today ≤ `lastIAFilingDate` | OpenFEMA field semantics (R10) | Guessing from incident dates |
| 17 | Demo disaster **DR-4936-HI**, demo ZIP **96704** | Declared after 2024-03-22, IA open to 2026-11-01, one county (R10) | DR-4930-MS (SNA window already closed) |
| 18 | Rollback: `az containerapp ingress traffic set --revision-weight <previous>=100` | One command | Redeploy old commit |
