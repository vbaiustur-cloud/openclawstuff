# Agents & Automation Dashboard (vb)

_Last updated: 2026-02-11_

---

## 🎮 Holosim Agent - PROJECT COMPLETE ✅

| Component | Status | Details |
|-----------|--------|---------|
| **Watchdog** | ✅ Done | Every 5 min - Browser health |
| **Progress Report** | ✅ Done | Every 15 min - Stats snapshot |
| **Quest Automation** | 🔲 TODO | Prompts ready, needs testing |
| **Fleet Management** | 🔲 TODO | Prompts ready, needs testing |

**Location:** `~/.openclaw/workspace-holosim/`

### Files Created
- `README.md` - Overview & quick start
- `TASKS.md` - Complete task breakdown  
- `PROMPTS.md` - All agent prompts

### Crons Active
```
✅ Holosim watchdog (Ollama)  - every 5m
✅ Holosim progress ping      - every 15m
```

---

## 🤖 All Agents

| Agent | Model | Status |
|-------|-------|--------|
| **main** | MiniMax-M2.1 | ✅ Stable |
| **holosim-agent** | Ollama qwen2.5:1.5b | ✅ Active |
| **ollama-test-agent** | Ollama qwen2.5:1.5b | ✅ Tested |

---

## 📁 Project Structure

```
~/.openclaw/workspace-holosim/
├── README.md      ← Start here
├── TASKS.md       ← Complete task list
├── PROMPTS.md    ← All prompts reference
└── [OpenClaw system files]

~/.openclaw/workspace/dashboard/
├── AGENTS_DASHBOARD.md  ← This file
└── index.html           ← Visual dashboard
```

---

## 🎯 Quick Links

| Task | Command |
|------|---------|
| Test watchdog | `openclaw agent --agent holosim-agent --message "Watchdog check"` |
| Test progress | `openclaw agent --agent holosim-agent --message "Progress report"` |
| List crons | `openclaw cron list` |
| Full status | `openclaw health` |

---

## 💰 Cost: $0 (All local Ollama)

---
_Last updated: 2026-02-11 21:00 GMT+1_
