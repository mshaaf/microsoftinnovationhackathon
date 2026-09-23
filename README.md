# Survivor Journey Navigator

Hackathon entry for the Microsoft Innovation Studio hackathon, **Disaster Assistance Navigator** track.
Status: in development. Due Friday, September 25, 2026 (video: demo + presentation). Demo disaster: DR-4936-HI, Kona Earthquake, ZIP 96704.

**Picking this up (human or agent)? Read `HANDOFF.md` first, then `AGENTS.md`.**

After a disaster, many FEMA "no" decisions are fixable paperwork problems, explained in letters people find hard to read, with a 60-day appeal clock, while phone lines are jammed. This app walks a survivor through the whole journey:

1. **Is help available here?** Enter a ZIP code and see whether FEMA Individual Assistance is open for your county.
2. **What do I need to apply?** Get a document checklist for your situation.
3. **What does my letter mean?** Photograph your FEMA letter and get a plain-language explanation. Personal details are removed before any AI sees it.
4. **Fix it before the deadline.** Get a checklist, a draft appeal note, and a countdown.
5. **Everything you're owed.** See other programs you may qualify for.

## Quick start (mock mode, no Azure needed)

```bash
make setup
make dev
```

- App: http://localhost:5173
- Service status: http://localhost:5173/status
- API health: http://localhost:8000/api/health

## Live mode (real Azure services)

```bash
cp .env.example .env   # fill in Azure values (tasks/P1-09-azure-setup.md)
APP_MODE=live make dev
```

## Where things are

| You want to... | Read |
|---|---|
| Understand the product and scope | docs/PRODUCT.md |
| See how it's built | docs/ARCHITECTURE.md |
| Know what we're doing today | docs/PLAN.md |
| Test something | docs/TESTING.md |
| Work in parallel with your partner and agents | docs/WORKFLOW.md |
| Check privacy and safety rules | docs/RESPONSIBLE_AI.md |
| Run the demo | docs/DEMO.md |
| See open research questions | docs/research/QUESTIONS.md |
| Instruct a coding agent (Codex reads AGENTS.md; Claude's CLAUDE.md imports it) | AGENTS.md |
| Verified facts (rules, APIs, Azure setup) | docs/research/ |
| Current status and next steps | HANDOFF.md |

All letters, names, and people in `fixtures/` are synthetic. This is not a government website and is not affiliated with FEMA.
