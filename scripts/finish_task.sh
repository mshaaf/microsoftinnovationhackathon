#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -ne 1 || ! "$1" =~ ^P[0-4]-[0-9]{2}$ ]]; then
  echo "usage: scripts/finish_task.sh P0-01" >&2
  exit 2
fi

task_id="$1"
branch="$(uv run --project "$ROOT/backend" python "$ROOT/scripts/task_board.py" --field "$task_id" branch)"
title="$(uv run --project "$ROOT/backend" python "$ROOT/scripts/task_board.py" --field "$task_id" title)"
if [[ "$(git -C "$ROOT" branch --show-current)" != "$branch" ]]; then
  echo "check out $branch before finishing $task_id" >&2
  exit 1
fi

make -C "$ROOT" check
remote="$(git -C "$ROOT" remote | sed -n '1p')"
if [[ -z "$remote" ]]; then
  echo "No git remote configured; cannot push or open the PR." >&2
  exit 1
fi
if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI is required to open the PR." >&2
  exit 1
fi

git -C "$ROOT" push -u "$remote" "$branch"
body_file="$(mktemp)"
trap 'rm -f "$body_file"' EXIT
cat > "$body_file" <<EOF
Task: $task_id — $title

Implemented the P0-01 repo skeleton and its verification workflow.

Run `make check` from the repository root. See the task file for human verification steps.
EOF
gh pr create --title "[$task_id] $title" --body-file "$body_file" --base main --head "$branch"
