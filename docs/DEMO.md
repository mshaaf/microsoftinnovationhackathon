# Demo

## Video = presentation + demo (R18)

Required: a video with a **demo** and a **presentation** covering project goals, solution components and architecture, how we thought through the approach, and key learnings. No length limit was given. Target 5 minutes or less: about 1:30 presentation (P4-03 deck), then the 3:00 demo below, then 0:30 of learnings.

Demo disaster: **DR-4936-HI Kona Earthquake**, demo ZIP **96704**, demo letter **L03** (letter date 2026-09-15, appeal due 2026-11-14).

## Demo story (3 minutes)

Persona: **Rosa**, a synthetic renter in Hawaiʻi County (Kona side) whose home was damaged in the earthquake. She prefers Spanish. She received a "not approved" letter because FEMA needs her insurance decision (her renters policy excludes earthquakes, and FEMA needs the denial letter).

| Time | Beat | What judges should notice |
|---|---|---|
| 0:00–0:20 | The problem: 1.7M found ineligible in 2016–18, many for missing paperwork; confusing letters; 60-day clock | The problem is real and specific |
| 0:20–0:50 | Stage 1: ZIP → county → Individual Assistance open → Serious Needs Assistance apply-by date | Deterministic, official data, instant |
| 0:50–1:40 | Stage 3: photo of letter → "What we removed" → plain explanation in Spanish → checklist | **Privacy boundary visible**, grounded explanation |
| 1:40–2:10 | Stage 4: countdown + appeal draft; show DevTools proving her name never left the phone | Responsible AI you can see |
| 2:10–2:30 | Everything you're owed: DUA and D-SNAP cards with honest labels | Beyond FEMA, honest uncertainty |
| 2:30–2:45 | Emergency phrase → handoff card | Humans stay in the loop |
| 2:45–3:00 | Eval scorecard + architecture (Azure services) | It's tested and it's real |

## Before recording

- [ ] Gate 3 passed.
- [ ] Browser zoom 125%, notifications off, clean profile.
- [ ] Demo ZIP and letter file ready on the phone or desktop.
- [ ] `evals/reports/latest.md` freshly generated.
- [ ] Live URL warmed up (hit it once a minute before recording).

## Fallback

If Azure or Wi-Fi fails, run `make dev` in mock mode and record the same script. Record the fallback **before** the live version, so it exists no matter what.

## Submission checklist

Required (R18): the video (demo + presentation). Have these ready too: description, repo link, deployed URL, Azure services used, Responsible AI notes, eval scorecard.
