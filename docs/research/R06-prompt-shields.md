# R06: Content Safety Prompt Shields

## Answer
- REST (GA): `POST {AZURE_AI_SERVICES_ENDPOINT}/contentsafety/text:shieldPrompt?api-version=2024-09-01`
```json
{"userPrompt":"<user chat text or empty>","documents":["<redacted OCR text>"]}
```
Response: `userPromptAnalysis.attackDetected` (bool) and `documentsAnalysis[i].attackDetected`. Up to 5 documents.
- Call it from `adapters/safety/live.py` with `httpx`. Run it **before** the model call on (a) chat user text and (b) redacted OCR text. If an attack is detected on a letter, keep the normal flow, pass the text to the model as quoted data, log only the category `prompt_injection_detected`, and add nothing to the response. On chat, answer with a polite redirect.
- Also runs as a model-gateway step, not as Agent Framework middleware. That keeps it one code path for chat and letters.
- Mock: flags text containing the fixture marker `IGNORE PREVIOUS INSTRUCTIONS` or `[[INJECT]]`.

## Evidence
- https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-jailbreak
- https://learn.microsoft.com/en-us/rest/api/contentsafety/text-operations/shield-prompt?view=rest-contentsafety-2024-09-01

## Impact
P3-01.
