# CLAUDE.md

@AGENTS.md

AGENTS.md is the single source of truth for every agent in this repo, including Claude Code and Codex. Follow it exactly. Don't put rules here that Codex can't see. Add them to AGENTS.md instead.

Claude Code specifics:
- Use plan mode before editing if your task touches more than three files.
- Nested CLAUDE.md files in `backend/` and `frontend/` import their own AGENTS.md.
- Don't spawn subagents that edit files outside your task's file list.
