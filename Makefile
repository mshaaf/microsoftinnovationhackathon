-include .worktree.env

export API_PORT ?= 8000
export WEB_PORT ?= 5173
export SMOKE_API_PORT ?= 8100
export SMOKE_WEB_PORT ?= 5273
export APP_MODE ?= mock
export PYTHONPATH := $(CURDIR)/backend:$(CURDIR)$(if $(PYTHONPATH),:$(PYTHONPATH))

UV_RUN = uv run --project backend

.PHONY: setup dev test lint typecheck contracts validate-fixtures smoke eval index test-live smoke-live check board

setup:
	cd backend && uv sync
	cd frontend && pnpm install --frozen-lockfile

dev:
	bash scripts/dev.sh

test:
	APP_MODE=mock $(UV_RUN) pytest backend/tests backend/app/features scripts/tests evals
	cd frontend && pnpm test

lint:
	$(UV_RUN) ruff check backend scripts evals
	$(UV_RUN) ruff format --check backend scripts evals

typecheck:
	cd frontend && pnpm typecheck

contracts:
	$(UV_RUN) python scripts/validate_contracts.py

validate-fixtures:
	$(UV_RUN) python scripts/validate_fixtures.py

smoke:
	bash scripts/smoke.sh

eval:
	bash scripts/eval.sh

index:
	$(UV_RUN) python scripts/ingest_kb.py

test-live:
	bash scripts/test_live.sh

smoke-live:
	bash scripts/smoke_live.sh "$(URL)"

check: lint typecheck test contracts validate-fixtures smoke

board:
	$(UV_RUN) python scripts/task_board.py
