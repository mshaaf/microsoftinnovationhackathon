---
id: P1-09
title: "Azure setup (human-led)"
phase: 1
lane: humans
status: todo
owner: "M"
depends_on: []
research: [R02, R03, R04, R08, R09]
branch: ""
---

## Execute in phases
Phase 1, lane humans. Wave and session: see docs/PLAN.md. **Start any time.** It runs alongside every phase, and no code task waits on it. Inside the session: read → plan (in the Log) → test first → build → `make check` → hand off (AGENTS.md). Facts for this task are already researched in the docs/research files named in `research:`.

## Goal
Every Azure resource that live mode needs exists, `.env` is filled in locally, and `APP_MODE=live make dev` reports each service `ok` on /api/health. Nothing else waits on this task. The app is fully usable in mock mode without it.

## Why it matters
"Use of Azure" is scored, and the demo should run live. The 4 resources below are all we need (decision 0002).

## Files you may touch
- .env (local, never committed)
- .env.example (only if a variable name was wrong)
- docs/decisions/0003-azure-resources.md (names, region, SKUs)

## Steps (an agent can run these with you; each `az` call is safe to re-run)
```bash
brew install azure-cli && az login
az extension add --name containerapp --upgrade
RG=rg-navigator; LOC=eastus2
az group create -n $RG -l $LOC
# 1) Microsoft Foundry (AIServices): model + PII + Translator + Content Safety + DocIntel
az cognitiveservices account create -n navigator-ai -g $RG -l $LOC --kind AIServices --sku S0 --custom-domain navigator-ai-<unique> --yes
#    then in the Foundry portal (ai.azure.com): create a project on this resource, deploy the newest mini chat model
#    (gpt-5-mini or newer, Global Standard), and note the project endpoint and deployment name
# 2) AI Search, Free tier
az search service create -n navigator-search-<unique> -g $RG -l $LOC --sku free
# 3) Application Insights (workspace-based)
az monitor app-insights component create -a navigator-ai-insights -g $RG -l $LOC
# 4) Budget alert: portal > Cost Management > Budgets (e.g. $50 with an email alert)
```
Fill `.env` from `.env.example`: endpoints, `AZURE_AI_SERVICES_KEY` (`az cognitiveservices account keys list`), `AZURE_AI_SERVICES_REGION=eastus2`, `AZURE_SEARCH_KEY` (admin key for `make index`), and the App Insights connection string.

## Acceptance criteria
- [ ] All 4 resources exist in one resource group; names recorded in decision 0003
- [ ] A model is deployed; `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL` work with `az login`
- [ ] `APP_MODE=live make dev`, then `curl localhost:8000/api/health`: services report `ok` for each adapter that's built so far
- [ ] `make index` uploads the KB (once P1-05 is done)
- [ ] Budget alert configured

## How to verify (human, under 5 minutes)
1. `az resource list -g rg-navigator -o table` shows the resources.
2. `APP_MODE=live make dev`, then `curl localhost:8000/api/health`.

## Log

## Follow-ups
