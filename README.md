# OpenClaw Dashboard

A live dashboard for OpenClaw with real-time status monitoring and interactive agent terminal.

## Features

- 📊 **Live System Status** - Gateway health, model, context usage
- 🤖 **Agent Management** - View all agents, switch between them
- 💬 **Interactive Terminal** - Send messages to any agent directly
- ⏰ **Cron Jobs** - Monitor scheduled tasks
- 🖥️ **Linux Desktop App** - Launch from app menu or desktop

## Requirements

- Python 3.8+
- OpenClaw gateway running (`openclaw gateway start`)
- Linux desktop environment

## Installation

```bash
cd ~/openclaw-dashboard
chmod +x install.sh
./install.sh
```

This will:
- Create a Python virtual environment
- Install dependencies (rich, requests)
- Set up the desktop launcher in `~/.local/share/applications/`

## Running

**Option 1: Desktop App**
- Search for "OpenClaw Dashboard" in your app launcher
- Or click the desktop launcher

**Option 2: Terminal**
```bash
cd ~/openclaw-dashboard
./run-dashboard.sh
```

## Terminal Commands

When in the dashboard terminal:

| Command | Description |
|---------|-------------|
| `/agents` | List all configured agents |
| `/use <id>` | Switch to a different agent |
| `/status` | Show gateway status |
| `/crons` | List cron jobs |
| `/clear` | Clear message history |
| `/quit` | Exit dashboard |

Just type a message to send it to the current agent.

## Architecture

```
openclaw-dashboard/
├── dashboard.py          # Main TUI application
├── install.sh           # Installation script
├── run-dashboard.sh     # Launch script
├── requirements.txt     # Python dependencies
└── openclaw-dashboard.desktop  # Desktop entry
```

## Current Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| main | MiniMax-M2.1 | Primary assistant |
| agent-qwen | qwen2.5:1.5b | Fast local backup |
| agent-llama | llama3.1:8b | Complex tasks |
| agent-thinking | lfm2.5-thinking:latest | Reasoning |
| agent-repair | qwen2.5:1.5b | System repair |

## Troubleshooting

**Gateway unreachable?**
```bash
openclaw gateway start
```

**Permission denied?**
```bash
chmod +x *.sh
```

**Missing dependencies?**
```bash
source venv/bin/activate
pip install -r requirements.txt
```
