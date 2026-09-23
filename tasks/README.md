# Tasks

One file per task. **Status lives in each file's frontmatter**, so parallel work never conflicts on a shared board.

## Frontmatter fields

| Field | Values |
|---|---|
| `id` | `P<phase>-<nn>` or `BUG-<nnn>` |
| `phase` | 0–4 |
| `lane` | `A` (data & rules), `B` (AI & Azure), `C` (frontend), `shared`, `humans` |
| `status` | `todo`, `in_progress`, `blocked`, `review`, `done` |
| `owner` | e.g. `M+codex`, `partner+claude` |
| `depends_on` | task IDs that must be `done` first |
| `research` | research IDs (docs/research/QUESTIONS.md) that must be answered first |
| `branch` | `task/<id>-<slug>` |

## Board

`make board` prints every task's ID, title, lane, status, and owner (created in P0-01).

## Rules

- Claim a task by editing its frontmatter and pushing `claim <ID>` to main (see docs/WORKFLOW.md).
- Only edit your own task file.
- Agents append to "Log"; they don't rewrite earlier entries.
- New work that isn't in a task gets a new task file from `_TEMPLATE.md`, after a human agrees.
- Bugs use `_BUG_TEMPLATE.md`.
