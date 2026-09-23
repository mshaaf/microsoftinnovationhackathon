#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
shopt -s nullglob
specs=("$ROOT"/frontend/e2e/*.spec.ts)

if [[ ! -f "$ROOT/frontend/playwright.config.ts" || ${#specs[@]} -eq 0 ]]; then
  echo "not implemented yet (P0-08)"
  exit 0
fi

cd "$ROOT/frontend"
exec pnpm exec playwright test
