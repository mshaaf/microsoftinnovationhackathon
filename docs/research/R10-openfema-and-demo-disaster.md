# R10: OpenFEMA declarations and the demo disaster

Checked 2026-09-23 against the live API.

## Answer

**Endpoint** (no key needed): `https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries`

Query by county (URL-encode the `$` params):
```
$filter=fipsStateCode eq '15' and (fipsCountyCode eq '001' or fipsCountyCode eq '000')
$orderby=declarationDate desc
$top=1000
```
`fipsCountyCode = '000'` means a statewide row. Always OR it in. Tribal areas (for example `Oglala Sioux Tribe`, 46000) also use `000` and have a `placeCode`. We can't map a ZIP to a tribal area, so note that on the About screen.

**Fields we use** (from the dataset page; there's no `closeoutDate` field, it's `disasterCloseoutDate`):

| Field | Meaning | Our use |
|---|---|---|
| `disasterNumber` | FEMA disaster number | Dedupe key (one row per designated area, so dedupe) |
| `declarationType` | `DR` major disaster, `EM` emergency, `FM` fire | Show DR and EM |
| `declarationDate` | Date declared | Picks the rules regime; anchors Serious Needs Assistance window |
| `ihProgramDeclared` | Individuals and Households Program declared | **Primary IA flag** |
| `iaProgramDeclared` | Legacy IA flag; `false` on all 2026 disasters we checked | `individual_assistance = ihProgramDeclared or iaProgramDeclared` (the dataset page says to use both) |
| `lastIAFilingDate` | "Last date when IA requests can be filed" | **Registration open** = today <= this date |
| `incidentBeginDate`/`incidentEndDate` | Incident period | Display only |
| `disasterCloseoutDate` | All financial transactions done | If set, not active |

**"Active" definition** (put this in code with a comment): `ihProgramDeclared or iaProgramDeclared`, declared within the last 18 months (IHP period of assistance, 44 CFR 206.110(e)), and `disasterCloseoutDate` is null. Then split into two states:
- `registration_open`: today <= `lastIAFilingDate`
- `registration_closed`: past it. The UI says the application period ended on that date and to call the FEMA Helpline about late applications.

**Contract impact:** add `registration_deadline` (date) and `registration_open` (bool) to each declaration in `contracts/schemas/declarations.json`. That's a `[CONTRACT]` change, but P0-03 hasn't been built yet, so P0-03 includes it from the start.

**Etiquette:** data refreshes about every 20 minutes. Cache 1 hour in memory. Use `$select` to shrink payloads. `$top` max is 10,000.

## Demo disaster: **DR-4936-HI, Kona Earthquake, Hawaiʻi County**

| Fact | Value |
|---|---|
| Declared | 2026-09-01 (incident 2026-05-22) |
| Designated area | Hawaii County only (state 15, county 001, FIPS 15001) |
| IH declared | true |
| `lastIAFilingDate` | 2026-11-01 |
| Rules regime | 2024-03-22 (declared after) |
| Serious Needs Assistance apply-by (code) | 2026-10-01 (declaration + 30 days); see the R13 caveat |
| IRS relief | Deadlines postponed to 2027-02-01 for Hawaii County |
| SBA | Low-interest loans for homeowners and renters, 800-659-2955 |
| Demo ZIP | **96704** (Captain Cook, Kona side). 96740 Kailua-Kona also works. Both map only to Hawaii County. |

Why this one: declared after the rules change, IA open well past the demo, one county (simple to explain), and the SNA window is still open on demo day. The FEMA press release offers Spanish.

Backup: **DR-4930-MS, Tropical Storm Arthur** (Hancock, Harrison, Pearl River, Stone). Declared 2026-08-03, registration until 2026-10-03, SNA window closed 2026-09-02. It's good for showing the "window closed" state.

Scenario ZIPs:
- S12 multi-county: **39426** (Hancock + Pearl River MS, both in DR-4930)
- S13 no declaration: **02134** (Suffolk County MA)
- S14 pre-2024 regime: synthetic fixture only (no pre-2024 disaster is still active)

## Evidence
- Dataset page: https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2 (checked 2026-09-23)
- Live query run 2026-09-23. The snapshot is saved by P0-05 into `fixtures/openfema/`.
- https://www.fema.gov/press-release/20260911/federal-disaster-assistance-available-hawaii-county-residents-impacted-kona
- https://www.irs.gov/newsroom/irs-announces-tax-relief-for-taxpayers-impacted-by-the-earthquake-in-hawaii-county-various-deadlines-postponed-to-feb-1-2027

## Impact on the build
P1-02 (IA flag, active rule, registration fields), P0-03 (declarations schema), P0-05 (snapshot for 4936, 4930, and one statewide row), PRODUCT.md (demo disaster), DEMO.md.

## Snapshot command
```bash
curl -sG 'https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries' \
  --data-urlencode "\$filter=disasterNumber eq 4936 or disasterNumber eq 4930" \
  --data-urlencode '$top=1000' > fixtures/openfema/declarations_snapshot.json
```
