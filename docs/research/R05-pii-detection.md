# R05: Azure Language PII detection

## Answer
- Use **text PII** after OCR. **Document** PII redaction is an async batch job through Blob Storage, which doesn't fit a live photo flow. Confirmed.
- REST: `POST {AZURE_AI_SERVICES_ENDPOINT}/language/:analyze-text?api-version=2024-11-01` (GA)
```json
{"kind":"PiiEntityRecognition",
 "parameters":{"modelVersion":"latest","piiCategories":["Person","Address","PhoneNumber","Email",
   "USSocialSecurityNumber","USBankAccountNumber","CreditCardNumber","USDriversLicenseNumber",
   "USUKPassportNumber","DateOfBirth"]},
 "analysisInput":{"documents":[{"id":"1","language":"en","text":"..."}]}}
```
- **Don't** enable the generic `DateTime` category, or it redacts the letter date that deadline math needs. Only `DateOfBirth` is redacted.
- Do our **own replacement** from the returned entity offsets: replace each span with `[PERSON]`, `[ADDRESS]`, and so on. The GA API's built-in redaction masks with `*`. The entity-label redaction policies are preview-only (2025-11-15-preview), so we skip them.
- **Defense in depth (code, both modes):** also redact 9-digit numbers (FEMA registration numbers aren't a built-in category), phone patterns, and ZIP+4.
- Spanish is supported (`language: "es"`). The limit is 5,120 characters per document per request in synchronous mode, so split long OCR text into chunks and merge offsets.
- **Fail closed:** any error or timeout means `dependency_unavailable`, and nothing goes to the model.
- Plain `httpx` call. No SDK needed.

## Evidence
- https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/how-to/redact-text-pii
- https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories
- https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/how-to/redact-document-pii

## Impact
P2-02. ARCHITECTURE.md: remove the VERIFY on the letter pipeline.
