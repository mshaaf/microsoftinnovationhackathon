# R07: Azure Translator

## Answer
- REST v3: `POST https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=en&to=es`
  Headers: `Ocp-Apim-Subscription-Key`, `Ocp-Apim-Subscription-Region: <region>` (required with the multi-service Foundry key), `Content-Type: application/json`. Body: `[{"Text":"..."}]`.
- **Glossary without Custom Translator:** wrap terms in dynamic dictionary markup, for example `<mstrans:dictionary translation="Asistencia Individual">Individual Assistance</mstrans:dictionary>`. Keep a small glossary dict in `core/i18n.py` (FEMA, Individual Assistance, Serious Needs Assistance, Disaster Recovery Center, appeal).
- Limits: 50,000 characters per request. We send short explanations only.
- **Use Translator only for model-generated text** (explanation, chat reply). Data files (checklist, taxonomy, programs, escalation) already hold reviewed `en` and `es` strings. That's more accurate and cheaper.
- Mock: return the fixture translation if one exists, otherwise prefix `[es] `.

## Evidence
- https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/reference/v3/translate
- https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/how-to/use-dynamic-dictionary

## Impact
P3-02.
