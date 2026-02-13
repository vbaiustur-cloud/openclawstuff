# OpenClaw - Simple Guide

## Quick Setup (One Command)
```bash
bash ~/.openclaw/setup.sh
```

## Daily Commands
```bash
# Check status
openclaw health

# Restart if broken
openclaw gateway restart

# List agents
openclaw agents list

# List crons
openclaw cron list

# Telegram test
openclaw message send --channel telegram --target 6703664422 --message "Test"
```

## Current Agents
| Agent | Purpose | Status |
|-------|---------|--------|
| main | Primary chat | ✅ |
| holosim-agent | Holosim automation | ✅ |
| game-tester-agent | Game testing | ✅ |

## Current Model
**MiniMax-M2.1** (cloud, free tier)

## Ollama Note
Ollama isolated agents have auth bug. Using MiniMax for now until fixed.

## Files
- `setup.sh` - One command setup
- `setup-simple.sh` - Detailed setup script
