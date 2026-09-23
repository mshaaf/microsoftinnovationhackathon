#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ! -f "$ROOT/frontend/e2e/live.spec.ts" ]]; then
  echo "not implemented yet (P3-04)"
  exit 0
fi
if [[ -z "${1:-}" ]]; then
  echo "usage: make smoke-live URL=https://your-app.example" >&2
  exit 2
fi

cd "$ROOT/frontend"
BASE_URL="$1" exec pnpm exec playwright test e2e/live.spec.ts
