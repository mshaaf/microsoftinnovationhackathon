# R14: Programs beyond FEMA

Checked 2026-09-23.

| Program | Rule of thumb | Tier logic suggestion | Deadline anchor | Source |
|---|---|---|---|---|
| `fema_ihp` | IA declared for the county | `open` if `registration_open`, else `check_now` | `lastIAFilingDate` (from OpenFEMA) | disasterassistance.gov |
| `irs_relief` | **Automatic** for taxpayers whose IRS address of record is in a covered county. The IRS acts when FEMA designates at least one county for IA. Moved-in or outside the area: call 866-562-5227. | `likely` when the county has IA | The IRS notice date for the disaster. DR-4936: deadlines postponed to **2027-02-01**. | irs.gov/newsroom/tax-relief-in-disaster-situations |
| `dua` | For people whose work or **self-employment** was lost or interrupted by the disaster and who can't get regular unemployment. File **within 30 days of the state's DUA announcement** (late filing allowed for good cause). | `check_now` if lost work or self-employed | Unknown unless the state announced. Show "window may be short, check now". | oui.doleta.gov/unemploy/disaster.asp; 20 CFR 625.8 |
| `dsnap` | The state may request D-SNAP only for areas with an **IA declaration**, and USDA must approve. The application window is short, often about a week. You must live or work in the area and meet disaster income limits. | `check_now` if the county has IA and the user isn't already on SNAP (SNAP households may get supplements instead) | Unknown unless FNS announced. "Check now". | fns.usda.gov/disaster/disaster-assistance |
| `sba_loan` | Low-interest disaster loans for **homeowners and renters** (and businesses). For declarations on/after 2024-03-22, applying is optional and doesn't affect FEMA eligibility. | `optional` | None shown | sba.gov/funding-programs/disaster-assistance; 800-659-2955 |

For DR-4936 specifically: IRS relief confirmed (2027-02-01). SBA loans confirmed. No DUA or D-SNAP announcement found as of 2026-09-23. Keep those at `check_now` with no date.

Never "eligible". Card copy: "You may qualify. <Agency> decides."

## Impact
P2-05 `data/programs.json`; the S07 expectations stay as written (IHP open, IRS likely, DUA check_now, D-SNAP check_now, SBA optional).
