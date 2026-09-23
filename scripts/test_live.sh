#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
shopt -s nullglob
tests=("$ROOT"/backend/tests/integration/test_*.py)
if [[ ! -f "$ROOT/.env" || ${#tests[@]} -eq 0 ]]; then
  echo "not implemented yet (P1-09)"
  exit 0
fi

cd "$ROOT/backend"
APP_MODE=live uv run pytest -m live tests/integration
