# 0001: Initial decisions

Date: 2026-09-23. Status: accepted.

| # | Decision | Why |
|---|---|---|
| 1 | Project: Survivor Journey Navigator with Letter Decoder (+ Everything You're Owed) | Council pick: most distinctive in the Disaster track, strongest demo |
| 2 | Backend Python 3.12 + FastAPI; frontend React + TypeScript + Vite | Team's existing stack; fastest path |
| 3 | Mock mode is the default; every adapter has a mock | Tests without keys; demo fallback |
| 4 | Contracts first (JSON Schema + examples) | Frontend and backend build in parallel |
| 5 | Code decides, AI explains | Accuracy and Responsible AI |
| 6 | OCR → text PII redaction → model, through a single model gateway | Personal data never reaches a model |
| 7 | Rules chosen by declaration date (before or on/after 2024-03-22) | Program rules changed on that date |
| 8 | No persistence, no accounts | Data minimization; demo scope |
| 9 | One file per task, status in frontmatter; one file per decision | Conflict-free parallel work |
| 10 | Microsoft Agent Framework (Python) with a Foundry model | Track resources; multi-agent practice |
| 11 | Host on Azure Static Web Apps (frontend) + Azure Container Apps (API) | Azure-native, simple |

New decisions: add `docs/decisions/NNNN-short-title.md` with date, decision, why, and alternatives considered.
