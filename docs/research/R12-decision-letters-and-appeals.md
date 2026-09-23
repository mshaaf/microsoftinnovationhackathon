# R12: FEMA decision letters, reasons, and appeals

Checked 2026-09-23. Sources: FEMA public explainers only.

## Answer

**"Not approved" isn't always final.** FEMA: a not-approved letter "may not be a denial or final decision". Often FEMA needs more information.

**Reason taxonomy** (FEMA's decision-letter fact sheet reasons mapped to our IDs):

| Our ID | FEMA reason | What to send (FEMA wording, shortened) |
|---|---|---|
| `insurance_docs_missing` | Insurance / other funding: FEMA can't pay for needs already covered | Insurance settlement or **denial letter**. If the settlement wasn't enough, proof of that. |
| `identity_not_verified` | Identity couldn't be verified | Contact FEMA. Send an identity document (for example a driver's license, passport, or other government ID). |
| `ownership_not_verified` | Ownership couldn't be verified | Deed or title, mortgage document, homeowner's insurance statement, property tax receipt or bill, manufactured home certificate or title, bill of sale, or a will plus death certificate naming you heir |
| `occupancy_not_verified` | Couldn't confirm the home was your main residence | Lease, utility bill, bank or credit card statement, or other mail showing the address (main residence = where you live more than 6 months a year) |
| `insufficient_damage` | Damage not enough, or in non-essential areas | Repair estimates, photos, contractor statement. Damage to non-essential areas, landscaping, or spoiled food isn't eligible. |
| `missed_inspection_or_contact` | FEMA couldn't reach you, or the inspection wasn't completed | Call the FEMA Helpline to reschedule. Return FEMA's calls. |
| `other_or_unclear` | Anything else (including duplicate applications, which can mean fraud) | Always hand off to the Helpline or a Disaster Recovery Center |

**How to appeal:**
- Deadline: within 60 days of the date on your letter (see R13 for the rule text).
- The Appeal Request form (FF-104-FY-22-229) is at the end of the letter. It's **optional**.
- Put your FEMA application number and disaster number **on every page**.
- Submit online at DisasterAssistance.gov (account upload), in person at a Disaster Recovery Center, by **mail** to FEMA – IHP National Processing Service Center, P.O. Box 10055, Hyattsville, MD 20782-8055, or by **fax** to 800-827-8112.
- A decision usually comes within 30 days, but can take up to 90.

**FEMA Helpline:** 1-800-621-3362 (1-800-621-FEMA). Hours differ by source: the letter fact sheet says 6 a.m.–10 p.m. CT daily, and the DR-4936 release says 7 a.m.–10 p.m. HST. **Show the number and "hours vary" only.** Don't show hours.

**Late appeals:** fema.gov doesn't say. We say: "Your 60 days may have passed. Call the FEMA Helpline to ask about your options." This goes to a human and never claims a late appeal will be accepted.

## Evidence
- https://www.fema.gov/fact-sheet/understanding-fema-decision-letter
- https://www.fema.gov/assistance/individual/after-applying/appeals (updated 2026-06-26)
- https://www.ecfr.gov/current/title-44/chapter-I/subchapter-D/part-206/subpart-D (206.115)

## Impact
P2-03 (`data/reason_taxonomy.json`), P2-04, P2-06 (appeal draft template content and submission options), P0-05 letters, PRODUCT.md facts.
