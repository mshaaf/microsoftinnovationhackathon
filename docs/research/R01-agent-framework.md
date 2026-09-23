# R01: Microsoft Agent Framework (Python)

Checked 2026-09-23 against PyPI and the `microsoft/agent-framework` samples.

## Answer
- **GA.** v1.0 shipped 2026-04-02. PyPI today: `agent-framework` **1.19.0**, `agent-framework-foundry` 1.13.1. Needs Python >= 3.10. No `--pre` flag.
- Install: `uv add agent-framework azure-identity` (the meta package includes the Foundry and OpenAI clients).
- The framework does **not** auto-load `.env`. Our `core/config.py` reads env vars itself.

## Minimal code (copied from the official samples; verify imports compile in P0-04)
```python
from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential   # use ManagedIdentityCredential in Azure
from pydantic import BaseModel, Field
from typing import Annotated

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],  # https://<res>.services.ai.azure.com/api/projects/<proj>
    model=os.environ["FOUNDRY_MODEL"],                          # deployment name
    credential=AzureCliCredential(),
)

@tool(approval_mode="never_require")
def search_official_pages(query: Annotated[str, Field(description="What to look up")]) -> str:
    """Search official FEMA and partner pages."""
    ...

agent = Agent(client=client, name="Navigator", instructions=SYSTEM_RULES, tools=[search_official_pages])
result = await agent.run("What if I lost my ID?")
print(result.text)

# Structured output (letter classifier)
class LetterReading(BaseModel):
    decision_type: str
    reason_ids: list[str]
    confidence: float
    letter_date: str | None
result = await agent.run(redacted_text, options={"response_format": LetterReading})
reading = result.value   # parsed Pydantic object or None; treat None as low confidence
```

**Middleware** (for the PII guard and safety): subclass `ChatMiddleware` and implement `async def process(self, context: ChatContext, call_next)`. It can inspect and rewrite `context.messages` before the model call, or stop the call with `MiddlewareTermination`. Register it at the agent level: `Agent(..., middleware=[...])`. See `python/samples/02-agents/middleware/chat_middleware.py`.

## Our design (keep it simple)
- `core/model_gateway.py` is still the only path to a model. It runs `guard()` **before** calling `agent.run`. Middleware is a second layer: a `ChatMiddleware` that calls `guard()` on every outgoing message. That also catches tool results that re-enter the model.
- In mock mode, the `model` adapter returns canned responses and never imports `agent_framework`. Only `adapters/model/live.py` imports it. Tests never need the package to reach the network.

## Evidence
- https://pypi.org/project/agent-framework/ (1.19.0)
- https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent (updated 2026-08-25)
- https://github.com/microsoft/agent-framework/tree/main/python/samples (01_hello_agent.py, 02_add_tools.py, middleware/chat_middleware.py, providers/azure/openai_client_with_structured_output.py)
- https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/

## Impact
P0-04 (env var names, where the import lives), P1-06, P2-03. ARCHITECTURE.md `.env`.
