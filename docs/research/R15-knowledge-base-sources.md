# R15: Knowledge base sources

Checked 2026-09-23.

## Key finding: fema.gov blocks scripts
Every `www.fema.gov` page returns **HTTP 403** to `curl` and `httpx`, even with browser headers. That's bot protection. The OpenFEMA **API** (`/api/open/...`) works. irs.gov, sba.gov, fns.usda.gov, disasterassistance.gov, oui.doleta.gov, and samhsa.gov return 200.

**So the KB is curated, not scraped.** Each source becomes one markdown file in `fixtures/kb/`, with front matter (below) and a faithful, shortened summary of the official page in plain language, written by an agent that can read the page (a browser, or Claude/Codex web fetch) and reviewed by the human. The same files feed the mock search and `make index` for AI Search. There's no scraping script to break during the demo.

```markdown
---
url: https://www.fema.gov/assistance/individual/after-applying/appeals
title: Disagreeing with FEMA's decision
agency: FEMA
lang: en
topic: appeals
fetched_at: 2026-09-23
---
## How long do I have to appeal?
...
```

Rules for KB files: only facts that are on the page, no advice beyond it, one file per URL, and a Spanish file (`*.es.md`) where the official Spanish page exists (`fema.gov/es/...`).

## Source list (topic → URL)

| # | Topic | Agency | URL | es page |
|---|---|---|---|---|
| 1 | apply | FEMA | https://www.disasterassistance.gov/ | https://www.disasterassistance.gov/es |
| 2 | apply | FEMA | https://www.fema.gov/assistance/individual/apply | /es/ |
| 3 | programs overview | FEMA | https://www.fema.gov/assistance/individual/program | /es/ |
| 4 | housing and other needs | FEMA | https://www.fema.gov/assistance/individual/housing | /es/ |
| 5 | 2024 changes | FEMA | https://www.fema.gov/assistance/individual/2024-reform | /es/ |
| 6 | serious needs | FEMA | https://www.fema.gov/fact-sheet/serious-needs-assistance-0 | /es/ |
| 7 | letters | FEMA | https://www.fema.gov/fact-sheet/understanding-fema-decision-letter | /es/ |
| 8 | appeals | FEMA | https://www.fema.gov/assistance/individual/after-applying/appeals | /es/ |
| 9 | appeals tips | FEMA | https://www.fema.gov/fact-sheet/helpful-tips-appeal-fema-decision-2 | |
| 10 | appeals timing | FEMA | https://www.fema.gov/node/can-i-appeal-femas-decision-anytime | |
| 11 | after applying / inspection | FEMA | https://www.fema.gov/assistance/individual/after-applying | /es/ |
| 12 | fraud | FEMA | https://www.fema.gov/assistance/individual/disaster-fraud | /es/ |
| 13 | rumors | FEMA | https://www.fema.gov/disaster/recover/rumor-response | /es/ |
| 14 | SBA and FEMA | FEMA | https://www.fema.gov/assistance/individual/small-business | /es/ |
| 15 | demo disaster | FEMA | https://www.fema.gov/disaster/4936 | |
| 16 | demo disaster FAQ | FEMA | https://www.fema.gov/fact-sheet/faqs-understanding-fema-assistance-kona-earthquake | |
| 17 | demo disaster release | FEMA | https://www.fema.gov/press-release/20260911/federal-disaster-assistance-available-hawaii-county-residents-impacted-kona | es version linked on page |
| 18 | IRS relief | IRS | https://www.irs.gov/newsroom/tax-relief-in-disaster-situations | |
| 19 | IRS demo disaster | IRS | https://www.irs.gov/newsroom/irs-announces-tax-relief-for-taxpayers-impacted-by-the-earthquake-in-hawaii-county-various-deadlines-postponed-to-feb-1-2027 | |
| 20 | IRS FAQ | IRS | https://www.irs.gov/businesses/small-businesses-self-employed/faqs-for-disaster-victims | |
| 21 | DUA | DOL | https://oui.doleta.gov/unemploy/disaster.asp | |
| 22 | D-SNAP | USDA FNS | https://www.fns.usda.gov/disaster/disaster-assistance | |
| 23 | D-SNAP facts | USDA FNS | https://www.fns.usda.gov/disaster/factsheet | |
| 24 | SBA loans | SBA | https://www.sba.gov/funding-programs/disaster-assistance | |
| 25 | SBA home loans | SBA | https://www.sba.gov/funding-programs/disaster-assistance/physical-damage-loans | |
| 26 | crisis support | SAMHSA | https://www.samhsa.gov/find-help/helplines/disaster-distress-helpline | Spanish on page |
| 27 | rules text | eCFR | https://www.ecfr.gov/current/title-44/chapter-I/subchapter-D/part-206/subpart-D | |

27 English sources and about 10 Spanish ones. That's enough for the demo. Add more only if an eval question comes back with no citation.

## Impact
P1-05 is rewritten: curated markdown files plus an index loader. There's no scraper.
