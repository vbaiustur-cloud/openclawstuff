# Agent: game-tester

## Purpose
Playtest the latest builds, report issues, and verify deployments for the Star Atlas games.

## Current Target
- **Game:** Star Atlas sidescroller
- **Build:** `/home/vbai/.openclaw/workspace/games/staratlas-sidescroller/dist/index.html`

## Intended Workflow
1. Ensure a fresh build exists (gamedev pipeline finished).
2. Launch a browser pointing at the `dist/` build (local static server or `npm run preview`).
3. Perform scripted test passes (controls, collisions, scoring, basic performance).
4. Write a test report to `memory/game-testing/YYYY-MM-DD.md` summarizing:
   - What was tested
   - Bugs found
   - Pass/fail for core flows

## Status (2026-02-04)
- No active dedicated game-tester cron yet; tests are manual/on-demand.

## Fallback / Reset Plan
If agents are reset:
1. Confirm latest build at `games/staratlas-sidescroller/dist/index.html`.
2. Run manual or scripted tests as above.
3. Log results to `memory/game-testing/` for traceability.
