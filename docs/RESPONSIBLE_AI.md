# Responsible AI

This is both our engineering rulebook and our pitch. Judges score Responsible AI, so every rule here should be visible in the demo.

## 1. Collect as little as possible

| We ask for | We never ask for |
|---|---|
| ZIP code | Social Security number |
| Own or rent, insured (yes/no/not sure), lost ID, displaced | Date of birth |
| A photo of the letter (processed in memory, then discarded) | Bank or payment details |
| Optional name and registration number, used only in the browser for the appeal draft | Full street address |

No accounts. No database. Nothing the survivor types or uploads is stored.

## 2. Personal data never reaches a model

- Letter pipeline: OCR → Azure Language PII redaction → `model_gateway.guard()` → model.
- `guard()` blocks any payload where PII is still detected.
- Logs record categories, counts, and latency only. A redaction filter wraps every logger.
- Leak tests seed fake names, addresses, phone numbers, and registration numbers from fixtures and fail if they show up in model payloads, logs, or browser network requests.
- The UI shows "What we removed", with counts and categories only, so the survivor and the judges can see the protection working.

## 3. Code decides, AI explains

Eligibility signals, deadlines, amounts, rule versions, checklists, and program labels come from code and versioned data files with source URLs. The model classifies letter reasons (as structured JSON, validated by code) and explains in plain language. See docs/ARCHITECTURE.md → Code vs AI.

## 4. Grounded and cited

- Factual answers must cite an official page retrieved from AI Search.
- If nothing relevant is retrieved, the app says it doesn't know and offers a human.
- Every data-file fact has a `source_url` and `last_verified` date shown in the UI.

## 5. Honest uncertainty

- Never "you are eligible". Always "you may qualify; [agency] decides".
- Program cards use explicit labels: **open**, **likely**, **check now**, **optional**.
- Low-confidence letter readings hand off instead of guessing.
- Known limitations are shown on the About screen and in the video.

## 6. Escalate to humans

Triggers, checked by code keyword rules, a model flag, and Content Safety:

| Trigger | Result |
|---|---|
| Immediate danger, injury, medical need, rising water, fire | Emergency card: 911 first |
| Unsafe housing, no shelter tonight | Shelter guidance + 211 + FEMA Helpline |
| Harm to self or others, abuse, domestic violence | Sensitive card: Disaster Distress Helpline 1-800-985-5990, 988, DV Hotline 1-800-799-7233 (R19) |
| Letter reading unclear or low confidence | Handoff to FEMA Helpline / Disaster Recovery Center |
| User asks for a person | Handoff card, always available |

## 7. Safety against manipulation

- User text and OCR text pass through Content Safety Prompt Shields (live mode) to catch direct and document-embedded prompt injection.
- The system prompt treats all letter text as data, never as instructions.
- Fixture L08 is an injection letter. Eval requires behavior to stay unchanged.

## 8. Fraud awareness

The app reminds users that we never charge fees or ask for payment and that they should apply only through official channels. Scam red-flag copy comes from FEMA's fraud guidance (R19): federal disaster workers never ask for money, never charge for help or inspections, won't ask for bank info or your SSN during inspection, and won't ask for your registration number. Report fraud: 1-866-720-5721.

## 9. Language and access

- Document Intelligence deletes uploaded letters and results after 24 hours (R04); we never store them.
- English and Spanish end to end (Translator + reviewed UI strings).
- Plain language, about a 6th–8th grade reading level.
- WCAG 2.2 AA target: keyboard access, visible focus, contrast, labels, 44px tap targets.
- Works on a slow connection: small bundle, text first.

## 10. Transparency

- A persistent banner: "Not a government website. Not FEMA. FEMA makes all decisions."
- All test data is synthetic and watermarked.
- `evals/reports/latest.md` is part of the submission.
