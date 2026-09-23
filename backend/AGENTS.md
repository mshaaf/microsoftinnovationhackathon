# backend/AGENTS.md

Backend conventions. Root AGENTS.md rules still apply.

## Stack

- Python 3.12, FastAPI, Pydantic v2, pytest, ruff (lint and format).
- Package manager: uv. All dependencies were installed in P0-01; don't add new ones.
- Simple Azure REST calls (Language PII, Translator, Content Safety) use `httpx`. SDKs only for Document Intelligence and AI Search. `agent_framework` is imported **only** in `adapters/model/live.py` (decision 0002).

## Layout

```
backend/
  app/
    main.py                  # creates app, auto-discovers features/*/router.py; don't edit
    core/
      config.py              # settings from env; APP_MODE = mock | live
      logging.py             # structured logs with a redaction filter
      clock.py               # injectable "today" for deadline math
      model_gateway.py       # the ONLY path to a language model; runs PII guard
    adapters/                # the ONLY code that talks to the network
      <service>/base.py      # interface
      <service>/mock.py      # fixture-backed implementation
      <service>/live.py      # real Azure/OpenFEMA implementation
    features/
      <feature>/router.py    # thin HTTP layer
      <feature>/service.py   # logic; deterministic where possible
      <feature>/models.py    # Pydantic models matching contracts/
  tests/
    unit/                    # fast, no network, table-driven
    contract/                # responses validated against contracts/schemas
    integration/             # marked @pytest.mark.live; skipped unless APP_MODE=live
```

Adapter services: `openfema`, `geo`, `search`, `model`, `ocr`, `pii`, `translator`, `safety`.

## Rules

- Routers stay thin. Logic lives in `service.py`.
- Services never import `live.py` directly. They receive an adapter chosen by `APP_MODE`.
- Every adapter has a mock that returns fixtures and is deterministic.
- Date logic takes today's date from `core/clock.py` so tests can pin it.
- Use `core/logging.py` only. No `print`. Never log request bodies from `/api/letter/*`.
- Uploaded files stay in memory. Never write them to disk.
- A new feature router is picked up automatically. Just create `features/<name>/router.py` exposing `router`.
- A new endpoint needs a contract test that validates the response against `contracts/schemas/`.
- Mark integration tests `@pytest.mark.live`. They must never run in `make test`.
