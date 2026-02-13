# Agent: holosim-play-assistant

## Purpose
Play Holosim for vb: keep the game running, monitor progress (XP, zAtlas, quests, fleets), and perform safe, incremental actions.

## Current Automation
- **Holosim watchdog (auto-recover + alert)** – cron `f4cd545c-...`
  - Schedule: every 3 minutes
  - Model: `ollama/qwen2.5:1.5b` (local)
  - Role: ensure browser profile `openclaw` is running; ensure a Holosim tab exists; attempt a single gentle recovery (reload) if stuck; alert vb on persistent problems.

- **Holosim progress ping (every 15 min)** – cron `3d90a9b4-...`
  - Schedule: every 30 minutes
  - Model: `ollama/qwen2.5:1.5b` (local)
  - Role: snapshot Holosim UI and report:
    - Level
    - zAtlas
    - Active quests + progress
    - Recently completed quests
    - Fleet blockers (out of ammo/food, etc.)

## Dependencies / Requirements
- **Browser profile:** `openclaw`
- **Extension:** OpenClaw Chrome extension must be attached to a Holosim tab at least once so automation can see the UI.

## Known Issues (2026-02-04)
- Crons often output meta/JSON-style text instead of actually using the browser tools and returning clean `OK`/`ALERT` or progress bullets.
- No reliable, structured XP/quest updates are reaching vb yet.

## Fallback / Reset Plan
If GPT or tooling breaks and vb needs to rebuild:

1. Ensure OpenClaw and Ollama are installed.
2. Recreate these crons (or import from backup):
   - `Holosim watchdog` (every 3 min) on `ollama/qwen2.5:1.5b`
   - `Holosim progress ping` (every 15–30 min) on `ollama/qwen2.5:1.5b`
3. Attach the OpenClaw extension to a Holosim tab under profile `openclaw`.
4. Verify by manually triggering each cron once and checking that:
   - Watchdog returns `OK: Holosim watchdog healthy` or a single clear `ALERT: ...`.
   - Progress ping returns a short summary including level/zAtlas/quests.
