# Architecture

## Overview

```
 Phone browser
     │
     ▼
 One Azure Container App (decision 0002 #6)
 ├─ Frontend (React + Vite, built to static files, served at /)
 └─ Backend (FastAPI, /api/*)        HTTPS JSON (contracts/), same origin, no CORS in prod
     │
     ├─ features/ location, declarations, rules, checklist, chat, letter, programs, escalation, health
     │
     └─ adapters/ (mock.py | live.py chosen by APP_MODE)
          geo ........ Census ZCTA-to-county file, bundled as data/geo/zip_county.json (R11)
          openfema ... OpenFEMA DisasterDeclarationsSummaries v2 (no key) (R10)
          search ..... Azure AI Search, Free tier, keyword; index built from fixtures/kb/*.md (R03, R15)
          model ...... Microsoft Foundry model via Microsoft Agent Framework 1.x (R01, R02)
          ocr ........ Document Intelligence prebuilt-read (R04)      ┐
          pii ........ Azure Language text PII, GA API (R05)          │ one Microsoft Foundry
          translator . Azure Translator v3 (R07)                      │ (AIServices) resource,
          safety ..... Content Safety Prompt Shields (R06)            ┘ one endpoint

 Secrets: Container Apps secrets + managed identity (live only); Key Vault optional
 Telemetry: Application Insights via OpenTelemetry (no personal data)
```

## Code vs AI

| Job | Who does it | Why |
|---|---|---|
| ZIP to county | Code | Must be exact |
| Is Individual Assistance open? | Code (OpenFEMA fields) | Must be exact |
| Which rules apply (by declaration date) | Code (`data/ihp_rules.json`) | Must be exact |
| Deadlines and dollar amounts | Code | Must be exact |
| Document checklist | Code (rules + taxonomy) | Must be exact |
| Program confidence labels | Code (`data/programs.json`) | Must be exact |
| Reading a letter photo | Document Intelligence | Perception |
| Removing personal data | Azure Language PII | Detection |
| Classifying the letter's reason | Model, structured JSON output | Language understanding |
| Explaining in plain language | Model, grounded in retrieved sources | Language generation |
| Answering follow-up questions | Model + AI Search, must cite | Grounded Q&A |
| Translation | Translator | Language |
| Emergency / sensitive detection | Code keyword rules **and** model flag **and** Content Safety | Defense in depth |

## Letter pipeline (the privacy boundary)

```
upload (memory only)
  → OCR (Document Intelligence Read)            ┐ personal-data zone
  → PII redaction (Azure Language)              ┘ never stored, never logged
  → model_gateway.guard(payload)  ← raises if any PII entity remains
  → classify reason (model, JSON schema)        ┐ de-identified zone
  → validate (letter date parses, disaster       │
    number exists in OpenFEMA)                   │
  → taxonomy lookup → checklist (code)           │
  → deadline = letter_date + 60 days (code)      │
  → explanation (model, grounded) → translate    ┘
```

Document PII redaction runs as a batch job through Blob Storage, which doesn't fit a live photo flow. So we run OCR first, then text PII detection (confirmed in R05). Redaction replaces entity spans with `[PERSON]`, `[ADDRESS]`, and so on, from the returned offsets. A code regex also removes 9-digit numbers (registration numbers), phones, and ZIP+4. The `DateTime` category stays off so the letter date survives for deadline math. If PII detection fails, the pipeline stops (fail closed).

## model_gateway

`backend/app/core/model_gateway.py` is the only path to a language model.

- Every call passes through `guard(payload)`, which runs PII detection. In mock mode it checks the fixture fake-PII list. It raises `PIILeakError` if anything is found.
- It logs model name, token counts, latency, and feature. It never logs content.
- Tests assert that every model call in the codebase goes through it. Add a grep-based test.

## Mock mode

`APP_MODE=mock` is the default. Every adapter has a deterministic mock:

| Adapter | Mock behavior |
|---|---|
| openfema | Reads `fixtures/openfema/*.json` snapshots |
| geo | Bundled ZIP-to-county file (same as live) |
| search | Keyword search over `fixtures/kb/*.md` (the same files `make index` uploads in live mode) |
| model | Canned responses keyed by scenario or letter ID; structured outputs from `fixtures/letters/*.expected.json` |
| ocr | Returns `fixtures/letters/<id>.txt` matched by file hash or name |
| pii | Redacts strings listed in fixture `fake_pii` lists, plus simple regexes for phone numbers and ZIP+4 |
| translator | Returns text prefixed `[es] ` unless a fixture translation exists |
| safety | Flags text containing fixture injection markers |

Mock mode also serves as the demo fallback if Azure or Wi-Fi fails.

## Configuration (`.env.example`)

```
APP_MODE=mock                    # mock | live
FRONTEND_ORIGIN=http://localhost:5173   # local dev CORS only; prod is same-origin
FOUNDRY_PROJECT_ENDPOINT=        # https://<resource>.services.ai.azure.com/api/projects/<project>  (R01, R02)
FOUNDRY_MODEL=                   # model deployment name, e.g. gpt-5-mini
AZURE_AI_SERVICES_ENDPOINT=      # https://<resource>.cognitiveservices.azure.com/  (PII, Translator, Content Safety, DocIntel)
AZURE_AI_SERVICES_KEY=           # local dev only; blank when using managed identity
AZURE_AI_SERVICES_REGION=        # e.g. eastus2 (Translator needs it)
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_KEY=                # query key at runtime; admin key only for `make index`
AZURE_SEARCH_INDEX=navigator-kb
APPLICATIONINSIGHTS_CONNECTION_STRING=
```

Local dev uses `az login` (AzureCliCredential) or keys in `.env`. In Azure, use the Container App's managed identity where role assignment is quick, and Container Apps secrets otherwise.

## Security basics (demo-level)

- Same origin in production (one container). In local dev, CORS is locked to `FRONTEND_ORIGIN`.
- Upload limit 10 MB. Accept `image/jpeg`, `image/png`, and `application/pdf` only.
- No database, no user accounts, no persistence of user input.
- Logging redaction filter on by default.
- Budget alert on the Azure subscription.
- Document Intelligence keeps inputs and results for 24 hours, then deletes them (R04). Say so on the About screen.

## Open technical questions

All R01–R20 questions are answered in docs/research/ (R17 voice is deferred). If code needs a fact that isn't there, stop and ask. Don't guess.
