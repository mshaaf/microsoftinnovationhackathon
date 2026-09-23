# R13: IHP rules in effect (2026)

Checked 2026-09-23.

## Answer

| Fact | Status | Evidence |
|---|---|---|
| Individual Assistance Program Equity rule (89 FR 3990, Jan 22 2024) applies to disasters **declared on or after 2024-03-22** | **Still in effect.** eCFR shows the last amendment to 44 CFR part 206 was 2024-08-15. No 2025–2026 amendments. | eCFR versioner API, part 206 amendment dates |
| SBA loan application no longer required before Other Needs Assistance (for declarations on/after 2024-03-22) | **Confirmed** | FEMA 2024 reform page; CRS R45238 |
| Appeals: "written explanation **or** verifiable documentation"; a written explanation must be signed; a signed statement is needed only when someone else files for you | **Confirmed** (current 44 CFR 206.115(b)). So a signed appeal letter is not required when you send documents only. | eCFR 206.115 |
| Appeal window | "within 60 days after the date that we notify the applicant" (reg). FEMA's public wording: "within 60 days of the date on your letter". **Use FEMA's wording in the UI.** | 206.115(a); fema.gov appeals page (updated 2026-06-26) |
| Appeal decision time | Usually within 30 days, up to 90 days | same |
| Serious Needs Assistance amount | **$750** for declarations 2024-03-22 to 2024-09-30. **$770** for declarations **on or after 2024-10-01**. No later adjustment notice exists in the Federal Register as of 2026-09-23, even though the reg says it's adjusted annually (206.119(b)(1)). | 89 FR (2024-24701, Oct 24 2024); Federal Register API search |
| SNA window | Apply within the first 30 days after declaration. FEMA may extend to 60 days on written request from the state, territory, or Tribal Nation. | FEMA SNA fact sheet (updated 2025-05-07) |
| IHP caps | $25,000 housing and $25,000 ONA, CPI-adjusted each year. **Don't show caps.** They're not needed and they go stale. | 206.110(b) |

**Caveat for the demo disaster:** the DR-4936 press release and FAQ don't mention Serious Needs Assistance. The fact sheet says SNA is "available in all disasters declared for Individual Assistance", but whether an applicant gets it is FEMA's call. The callout must say "FEMA **may** offer…", show the code-computed apply-by date, and link the fact sheet. Never promise.

## data/ihp_rules.json values (final, no VERIFY left)
```json
{"last_verified":"2026-09-23","regimes":[
 {"id":"pre-2024-03-22","declared_before":"2024-03-22","appeal_window_days":60,
  "sba_application_required_for_some_ona":true,"signed_appeal_letter_required":true,
  "serious_needs":{"available":false}},
 {"id":"2024-03-22","declared_on_or_after":"2024-03-22","appeal_window_days":60,
  "sba_application_required_for_some_ona":false,"signed_appeal_letter_required":false,
  "serious_needs":{"available":true,"window_days":30,"extension_max_days":60,
   "amounts":[{"amount_usd":750,"effective":"2024-03-22"},{"amount_usd":770,"effective":"2024-10-01"}]}}]}
```
`effective` means **declaration date** on or after, not today's date.

## Evidence
- https://www.ecfr.gov/current/title-44/chapter-I/subchapter-D/part-206/subpart-D (206.110, 206.115, 206.119)
- https://www.federalregister.gov/documents/2024/01/22/2024-00677/individual-assistance-program-equity
- https://www.federalregister.gov/documents/2024/10/24/2024-24701/notice-of-award-amount-adjustment-for-serious-needs-assistance
- https://www.fema.gov/fact-sheet/serious-needs-assistance-0
- https://www.fema.gov/assistance/individual/2024-reform
- https://www.fema.gov/assistance/individual/after-applying/appeals

## Impact
P1-03, P1-07, P2-04, PRODUCT.md facts table. Before recording the demo, re-check the Federal Register for a new SNA amount notice (FEMA adjusts around October 1).
