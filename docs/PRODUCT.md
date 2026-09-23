# Product

## The problem

- From 2016 to 2018, FEMA referred 4.4 million people to its Individuals and Households Program and found roughly 1.7 million ineligible. The most common reasons were insufficient damage, failure to submit evidence of losses, and failure to make contact with the FEMA inspector. GAO recommended FEMA improve its decision letter. (https://www.gao.gov/products/gao-20-503)
- FEMA says a "not approved" letter may not be a final decision. Often FEMA just needs more information. (https://www.fema.gov/fact-sheet/understanding-fema-decision-letter)
- Appeals must be sent within 60 days of the decision letter's date.
- Phone help gets overwhelmed during disasters.

**Our bet:** a guided journey that turns a confusing letter into a clear next step gets more eligible people the help they already qualify for.

## Users

- **Primary: a disaster survivor.** Stressed, probably on a phone, maybe without ID or documents, maybe more comfortable in Spanish, maybe on a bad connection.
- **Secondary: a human helper** (FEMA helpline, legal aid, caseworker). They only see what the survivor chooses to share through a handoff card.

## The journey

| Stage | Survivor gives | Survivor gets | Decided by |
|---|---|---|---|
| 1. Is help available here? | ZIP code only | County, active disaster declarations, whether Individual Assistance is open, Serious Needs Assistance apply-by date | Code: OpenFEMA + rules file |
| 2. What do I need to apply? | Own or rent, insured (yes/no/not sure), lost ID or documents, displaced now | Document checklist with sources; a chat for follow-up questions with citations | Code for the checklist; AI for explaining and answering, grounded in official pages |
| 3. What does my letter mean? | Photo or PDF of the FEMA letter | Plain-language explanation, reason for the decision, what to send | AI reads and classifies; code maps reasons to checklists |
| 4. Fix it before the deadline | Optional: name and registration number, typed only in the browser | Countdown (letter date + 60 days), draft appeal note, where to submit | Code |
| Everything you're owed | A few yes/no answers | Program cards with honest confidence labels | Code: rules file |
| Handoff (any time) | Nothing extra | A card with what to do and who to call | Code rules, plus low AI confidence |

## Scope

**Must have** (the demo breaks without it):
- Stages 1–4 working end to end
- English and Spanish
- 6 decision-reason types
- 5 program cards
- Handoff card
- Mock mode
- Deployed on Azure
- Eval scorecard

**Should have:** `/status` page, Azure Maps ZIP lookup, accessibility pass.

**Stretch:** Voice Live voice mode, SMS, a third language.

**Out of scope:** user accounts, saving any user data, submitting anything to FEMA, real letters, production scaling, native mobile apps.

## Demo disaster

**DR-4936-HI, Kona Earthquake, Hawaiʻi County** (docs/research/R10). Declared 2026-09-01 (incident 2026-05-22). Individual Assistance registration is open until 2026-11-01. One county. Demo ZIP **96704** (Captain Cook). The code-computed Serious Needs Assistance apply-by date is 2026-10-01, and the callout says FEMA *may* offer it (R13 caveat). IRS relief runs to 2027-02-01. SBA loans are available.

Backup: DR-4930-MS, Tropical Storm Arthur (4 counties). Its Serious Needs window has already closed, which makes it a good "window closed" state.

## Non-negotiables

- Never say someone *is* eligible. Say "may qualify" and name who decides.
- Every factual answer cites an official source.
- Never ask for a Social Security number, date of birth, bank details, or full address.
- Always offer a human path.
- Clearly say: not a government site, not FEMA.

## Facts the app depends on

All verified 2026-09-23. See docs/research/R12, R13, R14, R19.

| Fact | Value | Source |
|---|---|---|
| Rules regime change date | Disasters declared on or after 2024-03-22 use the updated IHP rules. Still in effect (no 44 CFR 206 amendments since 2024-08-15). | Federal Register 2024-00677; eCFR |
| SBA loan application before Other Needs Assistance | Not required for declarations on/after 2024-03-22 | fema.gov/assistance/individual/2024-reform |
| Appeal content | "Written explanation **or** verifiable documentation". A written explanation must be signed. A signed letter isn't needed when you send documents only. | 44 CFR 206.115(b) |
| Serious Needs Assistance amount | $750 for declarations 2024-03-22 to 2024-09-30; **$770 for declarations on/after 2024-10-01** | Federal Register 2024-24701 |
| Serious Needs Assistance window | Apply within 30 days of declaration; may extend to 60 on state/territory/Tribal request | fema.gov/fact-sheet/serious-needs-assistance-0 |
| Appeal window | "Within 60 days of the date on your letter" (FEMA wording) | fema.gov appeals page; 44 CFR 206.115(a) |
| Where to send an appeal | DisasterAssistance.gov, a Disaster Recovery Center, mail to FEMA – IHP NPSC, P.O. Box 10055, Hyattsville, MD 20782-8055, or fax 800-827-8112 | fema.gov appeals page |
| FEMA Helpline | 1-800-621-3362 (hours vary; don't show hours) | fema.gov |
| Fraud hotline | 1-866-720-5721 | fema.gov/assistance/individual/disaster-fraud |
| IA registration deadline | `lastIAFilingDate` from OpenFEMA, per disaster | OpenFEMA DisasterDeclarationsSummaries v2 |
