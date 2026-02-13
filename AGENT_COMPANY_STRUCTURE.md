# 🤖 Agent Company Structure - Implemented

## Quick Reference

```
vb (Human)
    ↓
MAIN AGENT (Primary Interface)
    ↓
    ├── BLOCKCHAIN TEAM
    │   └── solana-agent
    │       ├── wallet-agent
    │       ├── defi-agent
    │       └── token-agent
    │
    ├── WEB TEAM  
    │   └── web-agent
    │       ├── browser-agent
    │       ├── search-agent
    │       └── scrape-agent
    │
    ├── RESEARCH TEAM
    │   └── research-agent
    │       ├── analysis-agent
    │       └── synthesis-agent
    │
    ├── CODE TEAM
    │   └── code-agent
    │       ├── debug-agent
    │       ├── test-agent
    │       └── refactor-agent
    │
    └── PROJECT TEAM
        └── [Project Lead] → Worker Agents
```

---

## 🎯 How It Works

### Starting a New Project

1. **You tell MAIN**: "I want to build X"
2. **MAIN spawns PROJECT MANAGER**: Creates project structure
3. **PROJECT MANAGER**:
   - Researches requirements
   - Plans approach
   - Spawns WORKER AGENTS
   - Coordinates execution
   - Reports back to MAIN

### Example: "Research DeFi opportunities"

```
You → MAIN: "Research DeFi opportunities on Solana"

MAIN → BLOCKCHAIN MGR: "New project: Solana DeFi research"
BLOCKCHAIN MGR → PROJECT LEAD: "Plan this project"
PROJECT LEAD:
  • Researches DeFi protocols
  • Spawns: defi-agent, apy-agent, tvl-agent
  • Coordinates work
  • Reports back

BLOCKCHAIN MGR → MAIN: "Here are the findings..."

MAIN → YOU: "DeFi research complete. Top opportunities:..."
```

---

## 📦 Active Agents

### Management Layer
- **main** - Primary interface, talks to you
- **solana-agent** - Blockchain domain manager
- **staratlas-agent** - Game data domain manager

### Worker Layer (On Demand)
- **research-agent** - General research tasks
- **code-agent** - Programming assistance
- **web-agent** - Web browsing and scraping
- **analysis-agent** - Data analysis
- And more as needed...

---

## 🚀 Quick Commands

### Start a Project
```
Just tell MAIN what you want:
- "Research DeFi on Solana"
- "Build a dashboard for X"
- "Analyze this data"
- "Create a bot for Y"
```

### List Active Agents
```
# Check running agents
openclaw agents list
```

### Check Project Memory
```
# Today's projects
cat ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
```

---

## 📁 File Structure

```
~/.openclaw/
├── agents/
│   └── main/              # Primary agent
│       └── sessions/      # Subagent sessions
├── workspace/
│   ├── PROJECT_MANAGEMENT_RESEARCH.md  # Full research
│   ├── memory/
│   │   └── YYYY-MM-DD.md    # Daily project notes
│   └── MEMORY.md            # Long-term user preferences
└── skills/
    ├── solana/              # Blockchain skills
    ├── staratlas/           # Game skills
    ├── github/              # Git skills
    └── ... (more skills)
```

---

## 🎓 Principles

1. **MAIN is your interface** - Never talk to workers directly
2. **Delegation flows down** - Main → Manager → Lead → Worker
3. **Reporting flows up** - Workers → Lead → Manager → Main
4. **Memory is shared** - Project agents write to daily notes
5. **Specialization exists** - Each agent has specific skills

---

## 📖 Related Documentation

- Full Research: `PROJECT_MANAGEMENT_RESEARCH.md`
- Agent Capabilities: `SKILLS.md`
- Memory System: `memory/README.md`

---

*Status: ✅ Active*
*Version: 1.0*
*Last Updated: 2026-02-12*
