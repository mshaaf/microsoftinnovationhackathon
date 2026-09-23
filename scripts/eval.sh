#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ! -f "$ROOT/evals/run.py" ]]; then
  echo "not implemented yet (P0-06)"
  exit 0
fi

cd "$ROOT"
exec uv run --project backend python evals/run.py
