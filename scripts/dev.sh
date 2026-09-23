#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_MODE="${APP_MODE:-mock}"
API_PORT="${API_PORT:-8000}"
WEB_PORT="${WEB_PORT:-5173}"

(
  cd "$ROOT/backend"
  export APP_MODE
  exec uv run uvicorn app.main:app --host 0.0.0.0 --port "$API_PORT"
) &
api_pid=$!

cleanup() {
  kill "$api_pid" 2>/dev/null || true
  wait "$api_pid" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

cd "$ROOT/frontend"
APP_MODE="$APP_MODE" API_PORT="$API_PORT" WEB_PORT="$WEB_PORT" pnpm dev --host 0.0.0.0
