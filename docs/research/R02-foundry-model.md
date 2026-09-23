# R02: Foundry model choice and auth

Checked 2026-09-23. **Azure isn't set up yet, so confirm in the portal during P1-09.**

## Answer
- Create **one Microsoft Foundry resource** (kind `AIServices`) plus a project. The same resource and endpoint also give us Language (PII), Translator, Content Safety, and Document Intelligence. That's one key and one endpoint for five services.
- Model: deploy the **newest "mini" chat model the subscription offers** (gpt-5-mini or newer) as **Global Standard**. Default quota is usually in **East US 2** or **Sweden Central**. It needs tool calling and JSON-schema structured outputs, which all current gpt-5 family models support. Avoid the gpt-4.1 family, which Microsoft lists for retirement in 2026.
- The deployment name goes in `FOUNDRY_MODEL`, so swapping models is a config change.
- Latency: if it's a reasoning model, set the lowest reasoning effort for chat. Measure p95 in P1-06 and note it in the task Log.
- **Auth:** local dev uses `AzureCliCredential` (`az login`). Azure uses the Container App's system-assigned managed identity with the **Cognitive Services OpenAI User** and **Azure AI User** roles on the Foundry resource. Keys are the fallback if role assignment slows us down.

## Env vars
```
FOUNDRY_PROJECT_ENDPOINT=   # https://<resource>.services.ai.azure.com/api/projects/<project>
FOUNDRY_MODEL=              # deployment name, e.g. gpt-5-mini
AZURE_AI_SERVICES_ENDPOINT= # https://<resource>.cognitiveservices.azure.com/  (PII, Translator, Content Safety, DocIntel)
AZURE_AI_SERVICES_KEY=      # local dev only; blank when using managed identity
AZURE_AI_SERVICES_REGION=   # needed by Translator with a multi-service key
```

## Evidence
- https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource
- https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability
- https://learn.microsoft.com/en-us/azure/foundry-classic/agents/concepts/model-region-support

## Impact
ARCHITECTURE.md `.env` (collapses 5 endpoints into 1), P0-04, P1-09 (setup).
