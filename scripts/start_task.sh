#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -ne 2 || ! "$1" =~ ^P[0-4]-[0-9]{2}$ || ! "$2" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "usage: scripts/start_task.sh P0-02 ci" >&2
  exit 2
fi

task_id="$1"
slug="$2"
branch="task/$task_id-$slug"
worktree="$(dirname "$ROOT")/mshackathon-$task_id"
uv run --project "$ROOT/backend" python "$ROOT/scripts/task_board.py" --check-ready "$task_id"

if [[ "$(git -C "$ROOT" branch --show-current)" != "main" ]]; then
  echo "start tasks from a clean main worktree" >&2
  exit 1
fi
if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then
  echo "main worktree must be clean before claiming a task" >&2
  exit 1
fi
if [[ -e "$worktree" ]] || git -C "$ROOT" show-ref --verify --quiet "refs/heads/$branch"; then
  echo "worktree or branch already exists: $branch" >&2
  exit 1
fi

task_files=("$ROOT"/tasks/"$task_id"-*.md)
if [[ ${#task_files[@]} -ne 1 ]]; then
  echo "expected one task file for $task_id" >&2
  exit 1
fi

port_data="$(python3 - "$ROOT" <<'PY'
import socket
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
worktrees = subprocess.check_output(
    ["git", "-C", str(root), "worktree", "list", "--porcelain"], text=True
)
paths = [Path(line[9:]) for line in worktrees.splitlines() if line.startswith("worktree ")]
keys = {"API_PORT", "WEB_PORT", "SMOKE_API_PORT", "SMOKE_WEB_PORT"}
used = set()
for path in paths:
    env_file = path / ".worktree.env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.partition("=")
            if separator and key in keys and value.isdigit():
                used.add(int(value))

for slot in range(1, 100):
    ports = (8000 + 10 * slot, 5173 + 10 * slot, 8100 + 10 * slot, 5273 + 10 * slot)
    if used.intersection(ports):
        continue
    for port in ports:
        try:
            with socket.socket() as sock:
                sock.bind(("127.0.0.1", port))
        except OSError:
            break
    else:
        print(slot, *ports)
        raise SystemExit(0)

raise SystemExit("no free worktree port slot found")
PY
)"
read -r slot api_port web_port smoke_api_port smoke_web_port <<< "$port_data"

uv run --project "$ROOT/backend" python "$ROOT/scripts/task_board.py" --claim "$task_id" "$branch"
git -C "$ROOT" add "tasks/${task_files[0]##*/}"
git -C "$ROOT" commit -m "claim $task_id"
remote="$(git -C "$ROOT" remote | sed -n '1p')"
if [[ -n "$remote" ]]; then
  git -C "$ROOT" push "$remote" main
else
  echo "No git remote configured; the claim is committed locally."
fi

git -C "$ROOT" worktree add "$worktree" -b "$branch" main
cat > "$worktree/.worktree.env" <<EOF
API_PORT=$api_port
WEB_PORT=$web_port
SMOKE_API_PORT=$smoke_api_port
SMOKE_WEB_PORT=$smoke_web_port
EOF
if [[ -f "$ROOT/.env" ]]; then
  cp "$ROOT/.env" "$worktree/.env"
fi
make -C "$worktree" setup

echo
echo "Worktree: $worktree"
echo "Ports: API=$api_port web=$web_port smoke API=$smoke_api_port smoke web=$smoke_web_port"
echo "Claude: cd $worktree && claude"
echo "Codex:  cd $worktree && codex --add-dir \"\$(git rev-parse --git-common-dir)\" -c sandbox_workspace_write.network_access=true"
echo
echo "Session prompt:"
python3 - "$ROOT/docs/WORKFLOW.md" "$task_id" <<'PY'
import re
import sys
from pathlib import Path

workflow = Path(sys.argv[1]).read_text(encoding="utf-8")
match = re.search(r"Paste this prompt[^\n]*\n```[^\n]*\n(.*?)\n```", workflow, re.S)
if not match:
    raise SystemExit("could not find the session prompt in docs/WORKFLOW.md")
print(match.group(1).replace("<TASK-ID>", sys.argv[2]))
PY
