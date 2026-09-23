import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"


def parse_frontmatter(content: str) -> dict:
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("task file must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("task file has no closing frontmatter marker") from error
    metadata = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(metadata, dict) or not metadata.get("id"):
        raise ValueError("task frontmatter must contain an id")
    return metadata


def read_tasks() -> list[tuple[Path, dict]]:
    return [
        (path, parse_frontmatter(path.read_text(encoding="utf-8")))
        for path in sorted(TASKS_DIR.glob("*.md"))
        if path.name != "README.md" and not path.name.startswith("_")
    ]


def find_task(task_id: str) -> tuple[Path, dict]:
    matches = [(path, task) for path, task in read_tasks() if task["id"] == task_id]
    if len(matches) != 1:
        raise ValueError(f"expected one task with id {task_id}, found {len(matches)}")
    return matches[0]


def check_ready(task_id: str) -> tuple[Path, dict]:
    path, task = find_task(task_id)
    for dependency_id in task.get("depends_on") or []:
        _, dependency = find_task(dependency_id)
        if dependency.get("status") != "done":
            raise ValueError(
                f"{task_id} depends on {dependency_id} (status: "
                f"{dependency.get('status', 'missing')})"
            )
    return path, task


def claim_task(task_id: str, branch: str) -> None:
    path, task = check_ready(task_id)
    if task.get("status") != "todo":
        raise ValueError(f"{task_id} is {task.get('status')}, not todo")

    lines = path.read_text(encoding="utf-8").splitlines()
    end = lines.index("---", 1)
    values = {"status": "in_progress", "branch": branch}
    for field, value in values.items():
        replacement = f"{field}: {json.dumps(value)}"
        for index in range(1, end):
            if lines[index].startswith(f"{field}:"):
                lines[index] = replacement
                break
        else:
            lines.insert(end, replacement)
            end += 1
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_board() -> None:
    rows = []
    for _, task in read_tasks():
        status = str(task.get("status", ""))
        if status == "blocked":
            status = "BLOCKED!"
        rows.append(
            [
                str(task.get("id", "")),
                str(task.get("title", "")),
                str(task.get("phase", "")),
                str(task.get("lane", "")),
                status,
                str(task.get("owner", "")),
            ]
        )
    headers = ["ID", "TITLE", "PHASE", "LANE", "STATUS", "OWNER"]
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(6)]
    print(" | ".join(headers[i].ljust(widths[i]) for i in range(6)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(row[i].ljust(widths[i]) for i in range(6)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-ready", metavar="TASK_ID")
    parser.add_argument("--claim", nargs=2, metavar=("TASK_ID", "BRANCH"))
    parser.add_argument("--field", nargs=2, metavar=("TASK_ID", "FIELD"))
    args = parser.parse_args()

    try:
        if args.check_ready:
            check_ready(args.check_ready)
            print(f"{args.check_ready} dependencies are done")
        elif args.claim:
            task_id, branch = args.claim
            claim_task(task_id, branch)
            print(f"Claimed {task_id} on {branch}")
        elif args.field:
            task_id, field = args.field
            _, task = find_task(task_id)
            if field not in task:
                raise ValueError(f"{task_id} has no {field} field")
            print(task[field])
        else:
            print_board()
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"task board: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
