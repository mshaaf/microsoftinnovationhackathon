# R20: Synthetic letter realism

From FEMA's public explainers only (the decision-letter fact sheet and appeals page). No real letters used.

## Typical sections of an IHP determination letter (synthetic template)
1. FEMA header, letter date, and "Disaster: FEMA-4936-DR-HI"
2. Applicant name and mailing address, **FEMA Application/Registration number** (9 digits)
3. Greeting and a one-line purpose ("We reviewed your application for assistance…")
4. **Decision table:** Type of assistance | Decision | Amount. For example: "Rental Assistance | Not approved | $0.00"
5. **Reason** paragraph in agency wording. For example, "Insurance information needed: We need a copy of your insurance settlement or denial letter before we can determine…"
6. **What you can do:** appeal within 60 days of the date of this letter. Include the application number and disaster number on every page. Submission options (R12).
7. Helpline number, TTY or relay note, language line
8. Last page: **Appeal Request** form (optional)

## Fixture rules
- Every page has a large diagonal watermark: **SAMPLE — NOT A REAL FEMA LETTER**.
- No FEMA logo image. Use a plain text header ("U.S. Department of Homeland Security / FEMA", in text) to avoid imitating a real seal.
- Fake names such as "Jordan Samplewell", addresses on "Example Lane", phones in 555-01xx, and registration numbers starting with 9999.
- The PNG is rendered with Pillow from the `.txt`, then given a slight rotation (1–3°), Gaussian noise, and a light gradient to look like a phone photo.
- L03 (demo): renter, DR-4936, **letter date 2026-09-15**, reason insurance_docs_missing, so appeal_due = **2026-11-14**.

## Impact
P0-05.
