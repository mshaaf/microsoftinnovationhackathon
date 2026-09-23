# frontend/AGENTS.md

Frontend conventions. Root AGENTS.md rules still apply.

## Stack

- React + TypeScript + Vite, React Router.
- Tests: Vitest + Testing Library for components, Playwright for end-to-end (`frontend/e2e/`), axe-core for accessibility.
- Package manager: pnpm. Styling: CSS Modules per feature + `shared/ui/tokens.css` (decision 0002). No CSS framework.

## Layout

```
frontend/src/
  app/            # router, layout, stepper
  features/
    help-here/    # Stage 1
    apply/        # Stage 2 (+ chat panel)
    letter/       # Stage 3
    deadline/     # Stage 4 (+ appeal draft)
    programs/     # Everything you're owed
    handoff/      # handoff card
    status/       # /status service health page
  shared/
    api/          # typed client; mock mode uses contracts/examples
    ui/           # shared components
    i18n/         # loader only; strings live in features/<feature>/i18n/{en,es}.json
```

## Rules

- Mobile first. Design at 360px wide, then scale up. Tap targets at least 44px.
- API types come from `contracts/`. Don't hand-invent response shapes.
- UI text lives in `features/<feature>/i18n/{en,es}.json` (per feature, so parallel tasks don't conflict). Shared strings (banner, stepper) live in `app/i18n/`. Server-generated text arrives already translated via the `lang` parameter.
- **No personal data in URLs, localStorage, sessionStorage, or analytics.**
- The appeal draft's name and registration-number fields live only in component state and are merged into the template in the browser. They are never sent to the API. A Playwright test asserts this.
- Every screen needs a loading state, an error state that says what to do next, and an empty state.
- Plain language, short sentences, sentence case. No jargon without a one-line explanation.
- New screens need a component test, plus steps in that stage's own spec (`frontend/e2e/<stage>.spec.ts`) if they're on the main path.
- Never edit `app/routes.tsx`; P0-07 created every route. Journey state lives in one in-memory React context.
- Dev server port comes from `WEB_PORT`, and the `/api` proxy targets `API_PORT` (per-worktree `.worktree.env`).
