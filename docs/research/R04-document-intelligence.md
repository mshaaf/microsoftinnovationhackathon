# R04: Document Intelligence (OCR)

## Answer
- Model: **`prebuilt-read`**. We only need text, and it's the cheapest and fastest option. Layout isn't needed.
- Python: `azure-ai-documentintelligence`:
```python
from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
poller = await client.begin_analyze_document("prebuilt-read", AnalyzeDocumentRequest(bytes_source=data))
result = await poller.result()
text = result.content; pages = len(result.pages)
conf = mean(w.confidence for p in result.pages for w in p.words)
```
- Uses the shared Foundry (AIServices) endpoint.
- **F0 limits:** first 2 pages only, 4 MB max, 500 pages per month. Our contract allows 10 MB, so use **S0** (pay per page, pennies at our volume). Otherwise set the upload limit to 4 MB. **Decision: S0.**
- **Retention:** the service stores input and results for **24 hours**, then deletes them. Say so on the About screen.
- Photo accuracy tips (show them in the upload UI): flat surface, good light, no glare, fill the frame. The service handles skew.

## Evidence
- https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme
- https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/service-limits
- https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/document-intelligence/data-privacy-security

## Impact
P2-01, RESPONSIBLE_AI.md (24 h retention note).
