# Workflow: one human, 2–3 agent sessions, one repo

The bottleneck isn't agent speed. It's merge conflicts and your review time. This workflow minimizes both.

## Execute in phases

Work follows docs/PLAN.md: phases, then waves, then one lane per session. Never launch a task from a later phase until the current gate is logged as passed in docs/TESTING.md.

## Why parallel sessions don't collide

| Risk | How it's prevented |
|---|---|
| Two sessions edit the same file | Every task lists "Files you may touch". Lanes own disjoint folders (table below). |
| Router or route registration conflicts | `backend/app/main.py` auto-discovers `features/*/router.py`. `frontend/src/app/routes.tsx` has every route from P0-07. Later tasks never edit either. |
| Makefile conflicts | P0-01 creates every target. Each target calls a script, and the owning task replaces the stub script. |
| i18n string conflicts | UI strings live per feature: `frontend/src/features/<feature>/i18n/{en,es}.json`, merged at runtime. |
| Smoke test conflicts | One Playwright spec per stage: `frontend/e2e/<stage>.spec.ts`. |
| Lockfile conflicts | P0-01 installs every dependency the plan needs. Later tasks add none. |
| Port clashes (3 dev servers) | `scripts/start_task.sh` gives each worktree its own ports in `.worktree.env`. |
| Two sessions take the same task | You launch every session with `scripts/start_task.sh`, which marks the task `in_progress` on main first. |

## Ownership (who may edit what)

| Path | Owner lane |
|---|---|
| `backend/app/features/location, declarations, rules, checklist, programs, deadline` | A |
| `backend/app/features/chat, letter, escalation, health, search` | B |
| `backend/app/core/`, `backend/app/adapters/` | B (others propose changes via Follow-ups) |
| `data/` | A (B edits `reason_taxonomy.json` in P2-03 and `escalation_rules.json` in P3-01 only) |
| `frontend/src/**` | C |
| `contracts/` | `[CONTRACT]` PRs only |
| `fixtures/`, `evals/` | shared: add new files, don't rewrite others' files |
| `docs/` | M (agents only when their task says so) |
| `tasks/<your task>.md` | the session working that task |
| `Makefile`, lockfiles, CI, `main.py`, `routes.tsx` | P0 tasks only |

## Bootstrap (once, before P0-01 exists)

`scripts/start_task.sh` is built by P0-01, so launch wave 0A by hand:
```bash
cd ~/Documents/mshackathon
git worktree add ../mshackathon-P0-01 -b task/P0-01-repo-skeleton
git worktree add ../mshackathon-P0-05 -b task/P0-05-fixtures
# edit both task files' frontmatter to in_progress on main first, commit "claim P0-01 P0-05", push
```
Start the agents in those folders, the same way as below. Their ports don't matter yet because nothing runs.

## Launching a session (you, M)

```bash
# from the main checkout (~/Documents/mshackathon), on main, clean tree
scripts/start_task.sh P1-02 openfema-declarations
```
The script (built in P0-01):
1. Checks that every `depends_on` task is `done`.
2. Sets the task's frontmatter to `status: in_progress`, `branch: task/P1-02-openfema-declarations`, then commits `claim P1-02` to main and pushes.
3. Creates the worktree `../mshackathon-P1-02` on a new branch.
4. Writes `.worktree.env` with unique ports, copies `.env` if present, and runs `make setup`.
5. Prints the exact commands and the prompt to paste.

Then start the agent **inside the worktree**:

**Claude Code**
```bash
cd ../mshackathon-P1-02 && claude
```

**Codex CLI.** A worktree's git data lives in the main repo's `.git`, so let Codex write there, and allow network for `uv`/`pnpm`/`gh`:
```bash
cd ../mshackathon-P1-02 && codex \
  --add-dir "$(git rev-parse --git-common-dir)" \
  -c sandbox_workspace_write.network_access=true
```

Paste this prompt (the script prints it with the ID filled in):
```
Read AGENTS.md, then docs/PLAN.md, then tasks/<TASK-ID>*.md, then every docs/research file listed in the task's `research:` field.
Work only on that task, on this branch, in this worktree. Execute in phases as AGENTS.md describes: read, plan (write it in the task Log), test first, build, verify with `make check`, hand off.
Before finishing: paste the last 10 lines of `make check` into the task Log, add a `Learned:` line, fill in "How to verify", set status: review, commit, and open a PR titled "[<TASK-ID>] <title>".
If a fact isn't in docs/research or the task file, stop and set status: blocked with your question.
```

**Limit:** 3 active sessions. Past that, your review becomes the bottleneck.

## Finishing a task

1. The agent sets `status: review` and commits. If it could push and open the PR itself, done. If not: `scripts/finish_task.sh P1-02` pushes the branch and opens the PR with `gh`.
2. **Cross-review (5 min, the other tool):**
   - PR by Codex → in any Claude Code session: `/code-review` on the branch, or "Review PR #N against tasks/P1-02*.md acceptance criteria."
   - PR by Claude → `codex review` in the worktree.
3. **You (≤ 5 min):** skim the diff, run the task's "How to verify" if it's on the main path, check CI is green.
4. Squash-merge. Then set `status: done` in the task file (same PR or a `done P1-02` commit on main).
5. `git worktree remove ../mshackathon-P1-02`, then start that session's next lane task.

## Pull requests

- Title: `[P1-02] OpenFEMA declarations lookup`. Add `[CONTRACT]` if contracts change.
- CI (`make check`) must be green.
- Rebase on main right before merging. Squash merge.
- Lockfile conflict: never hand-merge. Take main's version and reinstall. (There shouldn't be any, since no new dependencies are allowed.)

## Sync points

- **At every gate:** all sessions finish or pause, everything is merged, and you run the gate checklist. Nothing from the next phase starts until it passes.
- **Every ~3 hours between gates:** 5 minutes on the board (`make board`): what's blocked, what's next, what to cut.

## Decisions and questions

- Decisions go in `docs/decisions/NNNN-short-title.md`, one file per decision so parallel PRs don't conflict.
- Questions for you go in the task file's Log with `status: blocked`. Check `make board` for blocked tasks.
- Verified facts live in `docs/research/`. Agents don't re-research them.

## Stop the line

If main is red, whoever notices says so. Nobody merges features until main is green. The session whose merge broke it fixes it first.
