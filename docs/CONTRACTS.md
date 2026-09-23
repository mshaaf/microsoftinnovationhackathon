# Contracts

`contracts/schemas/*.json` (JSON Schema draft 2020-12) and `contracts/examples/*.json` are the **source of truth**. This page is the readable summary. If they disagree, the schema wins, and whoever notices opens a `[CONTRACT]` PR to fix the drift.

## Rules

- Backend contract tests validate real responses against the schemas.
- Frontend mock mode serves `contracts/examples/`, so both sides test against the same payloads.
- `make contracts` validates every example against its schema.
- Changing a contract requires `[CONTRACT]` in the PR title, updated schema + example + this page, a decision record, and M's OK.

## Conventions

- Dates: `YYYY-MM-DD`. Timestamps: ISO 8601 UTC.
- `lang`: `en` or `es`. User-facing text in responses comes back in that language.
- Every response includes `request_id`.
- Error shape: `{"request_id": "...", "error": {"code": "zip_not_found", "message": "...", "retryable": false}}`
- Error codes: `invalid_input` (400), `zip_not_found` (404), `file_too_large` (413), `unsupported_file` (415), `unreadable_letter` (422), `dependency_unavailable` (503, retryable).

Example data below is **illustrative and synthetic**: disaster 9999 does not exist.

## GET /api/health

```json
{"request_id":"r1","mode":"mock","version":"0.1.0",
 "services":{"openfema":"mock","geo":"ok","search":"mock","model":"mock","ocr":"mock","pii":"mock","translator":"mock","safety":"mock"}}
```

Service status is one of `ok | mock | down | not_configured`.

## POST /api/location

Request: `{"zip":"12345"}`

```json
{"request_id":"r2","zip":"12345",
 "counties":[{"state":"XX","county_fips":"99001","name":"Example County"}],
 "needs_confirmation":false}
```

`needs_confirmation` is true when the ZIP spans more than one county. The UI then asks the user to pick one.

## GET /api/declarations?state=XX&county_fips=99001&lang=en

```json
{"request_id":"r3","county":{"state":"XX","county_fips":"99001","name":"Example County"},
 "declarations":[{
   "disaster_number":9999,"title":"Example Severe Storms and Flooding","incident_type":"Flood",
   "declaration_date":"2026-09-10","individual_assistance":true,"rules_regime":"2024-03-22",
   "registration_deadline":"2026-11-09","registration_open":true,
   "serious_needs":{"available":true,"amount_usd":770,"apply_by":"2026-10-10","extension_possible":true,
     "source_url":"https://www.fema.gov/fact-sheet/serious-needs-assistance-0"},
   "fema_url":"https://www.fema.gov/disaster/9999"}],
 "checked_at":"2026-09-23T18:00:00Z"}
```

`registration_deadline` = OpenFEMA `lastIAFilingDate`. `registration_open` = today <= that date (R10). `serious_needs.amount_usd` is picked by **declaration date** (R13).

An empty `declarations` list means "no active declaration found". The UI shows the 211 and FEMA Helpline guidance.

## POST /api/checklist

Request: `{"disaster_number":9999,"lang":"en","answers":{"housing":"rent","insured":"not_sure","lost_id":true,"displaced":true}}`

```json
{"request_id":"r4","rules_regime":"2024-03-22",
 "items":[{"id":"proof_of_occupancy","text":"Something that shows you lived there, like a lease or a utility bill.",
   "why":"FEMA needs to confirm the home was your main residence.","source_url":"https://www.fema.gov/..."}]}
```

## POST /api/chat

Request: `{"session_id":"uuid","message":"What if I lost my ID?","lang":"en","context":{"disaster_number":9999}}`

```json
{"request_id":"r5","reply":"...","citations":[{"title":"...","url":"https://www.fema.gov/..."}],"handoff":null}
```

Rule: a factual reply with zero citations is a bug. If no source is found, the reply says so and `handoff` is set.

## POST /api/letter/decode (multipart)

Fields: `file` (jpeg/png/pdf, 10 MB max), `lang`.

```json
{"request_id":"r6",
 "ocr":{"confidence":0.97,"pages":1},
 "redaction":{"entities_removed":7,"categories":["Person","Address","PhoneNumber","Other"]},
 "decision":{"type":"not_approved","assistance_types":["rental"],"letter_date":"2026-09-01",
   "disaster_number":9999,"disaster_number_verified":true},
 "reasons":[{"taxonomy_id":"insurance_docs_missing","confidence":0.92}],
 "explanation":"...",
 "checklist":[{"id":"insurance_decision_letter","text":"...","source_url":"https://www.fema.gov/..."}],
 "deadline":{"appeal_due":"2026-10-31","days_left":38,"rule":"60 days from the date on your letter"},
 "appeal_template_id":"insurance_docs_missing",
 "redacted_preview":"... [PERSON] ... [ADDRESS] ...",
 "handoff":null}
```

- `decision.type`: `approved | not_approved | needs_information | unclear`
- `unclear`, or any reason with confidence below the threshold in `data/reason_taxonomy.json`, sets `handoff`.
- `redacted_preview` contains only redacted text.

## POST /api/programs

Request: `{"disaster_number":9999,"county_fips":"99001","lang":"en","answers":{"housing":"rent","lost_work_or_self_employed":true,"on_snap":false,"household_size":3}}`

```json
{"request_id":"r7","cards":[
  {"program_id":"fema_ihp","tier":"open","title":"FEMA help for individuals and households",
   "why":"Individual Assistance is open for your county.","deadline":{"date":"2026-11-09","label":"Apply by"},
   "how_to_apply":"DisasterAssistance.gov or 1-800-621-3362","source_url":"https://www.disasterassistance.gov/",
   "last_verified":"2026-09-23"}]}
```

`tier` is one of `open | likely | check_now | optional`. Meanings are in docs/PRODUCT.md and `data/programs.json`.

## POST /api/escalate

Request: `{"session_id":"uuid","reason":"emergency","lang":"en"}`. `reason` is one of `emergency | sensitive | low_confidence | user_request`.

```json
{"request_id":"r8","card":{"title":"Get help now","steps":["..."],
 "phones":[{"label":"Emergency","number":"911"},{"label":"FEMA Helpline","number":"1-800-621-3362"}]}}
```

## Data file schemas

### data/ihp_rules.json

```json
{"last_verified":"2026-09-23","regimes":[
  {"id":"pre-2024-03-22","declared_before":"2024-03-22","appeal_window_days":60,
   "sba_application_required_for_some_ona":true,"signed_appeal_letter_required":true,
   "serious_needs":{"available":false}},
  {"id":"2024-03-22","declared_on_or_after":"2024-03-22","appeal_window_days":60,
   "sba_application_required_for_some_ona":false,"signed_appeal_letter_required":false,
   "serious_needs":{"available":true,"window_days":30,"extension_max_days":60,
     "amounts":[{"amount_usd":750,"effective":"2024-03-22"},{"amount_usd":770,"effective":"2024-10-01"}]}}],
 "sources":[{"fact":"...","url":"..."}]}
```

### data/reason_taxonomy.json

```json
{"confidence_threshold":0.6,"reasons":[
  {"id":"insurance_docs_missing","label":{"en":"...","es":"..."},
   "plain_explanation":{"en":"...","es":"..."},
   "what_to_send":[{"id":"insurance_decision_letter","text":{"en":"...","es":"..."}}],
   "match_hints":["insurance","settlement","denial letter"],"source_url":"..."}]}
```

Initial IDs: `insurance_docs_missing`, `identity_not_verified`, `ownership_not_verified`, `occupancy_not_verified`, `insufficient_damage`, `missed_inspection_or_contact`, and `other_or_unclear` (always hands off).

### data/programs.json

Program IDs: `fema_ihp` (includes Serious Needs Assistance), `irs_relief`, `dua`, `dsnap`, `sba_loan`. Each entry has trigger conditions, tier logic, deadline anchor, `how_to_apply`, `source_url`, and `last_verified`.

### fixtures/scenarios/Sxx.yaml

```yaml
id: S07
persona: Gig worker, renter, car flooded, Spanish speaker   # synthetic
lang: es
zip: "12345"
answers: {housing: rent, insured: "no", lost_id: false, displaced: false,
          lost_work_or_self_employed: true, on_snap: false, household_size: 1}
letter: null            # or L03
expected:
  individual_assistance: true
  checklist_includes: [proof_of_occupancy]
  programs: {fema_ihp: open, irs_relief: likely, dua: check_now, dsnap: check_now, sba_loan: optional}
  handoff: null         # or emergency | sensitive | low_confidence
```

### fixtures/letters/Lxx.expected.json

```json
{"id":"L03","decision_type":"not_approved","reasons":["insurance_docs_missing"],
 "letter_date":"2026-09-01","disaster_number":9999,
 "fake_pii":["Jordan Samplewell","123 Example Lane","555-0142","987654321"]}
```

`fake_pii` drives the leak tests. None of these strings may appear in any model payload or log.
