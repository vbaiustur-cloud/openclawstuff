# Long-Term Memory

## OpenClaw System Timeline

**Started:** Feb 3, 2026  
**Current:** Feb 13, 2026  
**Duration:** 10 days total

---

## Timeline Summary

| Phase | Dates | Focus |
|-------|-------|-------|
| Phase 1 | Feb 3-4 | Initial setup, Telegram, first Ollama |
| Phase 2 | Feb 4-10 | Model experiments, fallbacks |
| Phase 3 | Feb 11-13 | Full rebuild, automation, parallel projects |

---

## Working Configuration

### Working Configuration

**Primary Model:** `minimax-portal/MiniMax-M2.1` (cloud - free tier, working)
**Local Ollama Models:**
- `qwen2.5:1.5b` - 986 MB ✅
- `llama3.1:8b` - 4.9 GB ✅
- `lfm2.5-thinking:latest` - 731 MB ✅
- `qwen2.5:7b-instruct` - 4.7 GB ✅

**Issue:** Isolated agents can't use Ollama (auth bug in OpenClaw)
- Workaround: Use main agent with MiniMax for now
- Fallback system implemented: cloud → qwen2.5:1.5b → llama3.1:8b

### Telegram
- Bot: @vbassistanthelper_bot
- Token: 8584738285:AAGikofXUemC3YprIYg8mqNXnvsCieBZOi4
- Status: ✅ Connected and working
- **Voice:** Send via `/voice <text>` in dashboard, receive via faster-whisper

### Agents Created (8 total)
| Agent | Workspace | Model | Purpose |
|-------|-----------|-------|---------|
| main | ~/.openclaw/workspace | MiniMax-M2.1 | Primary assistant ✅ |
| holosim-agent | ~/.openclaw/workspace-holosim | Ollama | Holosim automation |
| ollama-test-agent | ~/.openclaw/workspace-ollama-test | Ollama | Testing |
| game-tester-agent | ~/.openclaw/workspace-game-tester | Ollama | Game testing |
| game-tester | ~/.openclaw/workspace-game-tester | MiniMax-M2.1 | Testing |
| **agent-qwen** | ~/.openclaw/workspace-qwen | qwen2.5:1.5b | Fast local backup ✅ |
| **agent-llama** | ~/.openclaw/workspace-llama | llama3.1:8b | Complex tasks ✅ |
| **agent-thinking** | ~/.openclaw/workspace-thinking | lfm2.5-thinking | Reasoning ✅ |
| **agent-repair** | ~/.openclaw/workspace-repair | qwen2.5:1.5b | Fixer agent ✅ |

### Google Workspace (2026-02-12)
- Account: vbaiustur@gmail.com
- Services: Gmail, Calendar, Drive
- Test: Email sent to staratlasnews@gmail.com

### GitHub (2026-02-12)
- Repo: https://github.com/vbaiustur-cloud/openclawstuff
- Also: https://github.com/vbaiustur-cloud/openclaw-dashboard (dashboard only)
- Game repo: git@github.com:citb77/aitestsa.git

### Holosim
- Status: PRE-LAUNCH (waiting for new season)
- URL: https://holosim.staratlas.com/
- All crons: DISABLED (no point monitoring until game is live)

### Browser Stability (FIXED 2026-02-12)
- CDP port 9222 instead of extension relay
- Auto-restart watchdog every 5 minutes
- Systemd service template available
- Much more stable!

### Web Search (FREE - 2026-02-12)
No Brave API key? No problem! Free search using:
- Wikipedia API
- GitHub Search API
- Hacker News (Algolia)
- Reddit API
- Stack Overflow API
- DuckDuckGo HTML

Usage: `python3 ~/.openclaw-dashboard/web-search-enhanced.py "query"`

### Improvements Implemented (2026-02-12)
- ✅ Stable browser with CDP port 9222
- ✅ Model fallback system (cloud → local)
- ✅ Free web search (6 sources)
- ✅ Usage dashboard (tokens, cron health)
- ✅ Smart cron jobs (retry + fallback)
- ✅ Repair agent enhancements
- ✅ 11 new files in ~/openclaw-dashboard/

### Troubleshooting

```bash
# Check health
openclaw health

# Restart gateway
openclaw gateway restart

# Test Ollama CLI
curl http://localhost:11434/api/tags

# List agents
openclaw agents list

# Telegram test
openclaw message send --channel telegram --target 6703664422 --message "Test"

# Start stable browser
~/.openclaw-dashboard/browser-launcher.sh

# Web search
python3 ~/.openclaw-dashboard/web-search-enhanced.py "AI agent"

# Check stats
python3 ~/.openclaw-dashboard/stats.py
```

### Important Paths
- Config: `/home/vbai/.openclaw/openclaw.json`
- Agents: `~/.openclaw/agents/`
- Workspaces: `~/.openclaw/workspace*`
- Dashboard: `~/openclaw-dashboard/`
- Improvements: `~/openclaw-dashboard/IMPROVEMENTS.md`

## User Preferences
- User: vb (Europe/Berlin)
- Primary use: Holosim gaming, Star Atlas development
- Priority: Cost-free operation, local models preferred
- IP: 192.168.0.242 (local), 109.40.240.190 (external)

---

## 2026-02-13 - OOM Incident & Memory Monitor
- **Feb 13, 12:18:54** - openclaw-gateway killed by OOM (7GB memory used, 167MB free)
- **Solution:** Created `~/.openclaw/memory-monitor.py` with 5-minute cron checks
- **Thresholds:** Warning <800MB, Critical <500MB
- **Logs:** `~/.openclaw/logs/memory-monitor.log` & `memory-alerts.log`

## System Health Notes
- **Weakness:** Memory-constrained system (13GB total, prone to OOM when Firefox + other apps run)
- **Firefox:** Consistently high memory consumer (~4-5% per process, multiple tabs)
- **Fleet Alerts:** Network issues connecting to staratlas.com API (DNS/connectivity)

### CRITICAL: Config Fragility
- **DO NOT modify openclaw.json without explicit permission**
- Previous incidents: JSON corruption when adding Google AI/xAI providers
- User had to restore from backup (`openclawbroken.json`)
- Lesson: Ask first, validate JSON, backup before changes

### Claude Opus Anomaly
- Claude Opus appeared mysteriously in TUI status
- **Never added to config** - config only has MiniMax and Ollama
- Possible causes: cached session data, race condition
- Investigate if recurs

### System Health (2026-02-13 Analysis)
- **Score: 7/10**
- Strengths: Project execution, infrastructure, automation
- Weaknesses: Config fragility, session hanging, unexplained anomalies
- Productivity: ~4-6 accomplishments/day with 4-6 concurrent tasks

### Working History (Feb 11-13)
- Sessions: 24 | Files: 136 | Projects: 12 (8 done, 4 in progress)
- Agents: 15 total (5 infra, 5 domain, 3 utility, 2 automation)
- Completed: Shared Memory, Templates, Communications, Dashboard, Fleet Alerts, Games, Twitter Agent, Test Agent
- In Progress: SAGE Fleet Decoding, Solana DEX, Holosim Core, Portfolio Tracker

### User Preferences (Reaffirmed)
- Prioritize stability over new features
- Local AI (Ollama) preferred when available
- Ask before making system changes
- Keep working configuration intact

### API Keys Available (NOT Added to Config)
- GEMINI_API_KEY: Configured but NOT in openclaw.json
- XAI_API_KEY: Not found (needs user to add)
- These remain in ~/.bashrc, not in OpenClaw config

---

## 2026-02-13 Afternoon - Browser Enhancement & ChatGPT Atlas

### ChatGPT Atlas Research
- User asked about OpenAI's new browser (chatgpt.com/atlas)
- **Finding:** macOS only + Apple Silicon M1+ required
- **Cannot install:** Linux Mint system incompatible
- **Decision:** Enhanced Playwright browser instead

### Browser Skill Enhanced
- Created new `browser.py` with advanced features:
  - Screenshot (full page or element)
  - Cookie management (save/restore)
  - Session management (cookies + localStorage)
  - Form auto-fill from JSON
  - Page analysis (detect forms, inputs, blockers)
  - Multi-tab support
  
- **Location:** `~/.openclaw/skills/browser-runner/browser.py`
- **Documentation:** `~/.openclaw/skills/browser-runner/SKILL.md`

### Commands Added
```bash
python3 ~/.openclaw/skills/browser-runner/browser.py browse <url>
python3 ~/.openclaw/skills/browser-runner/browser.py screenshot
python3 ~/.openclaw/skills/browser-runner/browser.py analyze
python3 ~/.openclaw/skills/browser-runner/browser.py cookies --save/--restore
python3 ~/.openclaw/skills/browser-runner/browser.py session --save/--restore
python3 ~/.openclaw/skills/browser-runner/browser.py fill '{"#email": "test"}'
```

### Memory Monitor
- **Disabled:** Heartbeat cron (too many notifications)
- **Still available:** `~/.openclaw/memory-monitor.py` for manual checks
- **Command:** `python3 ~/.openclaw/memory-monitor.py`

### Web Access Note
- OpenClaw web interface bound to localhost only
- PC access requires SSH tunnel or use TUI (`openclaw`)
- User using TUI/webchat instead

---

## 2026-02-14 - StarAtlasTV Tweet Pipeline

### New Project Created
Built complete automated tweet pipeline for Star Atlas + Z.ink content promotion.

**Location:** `/home/vbai/openclaw_unified/apps/bots/tweet-pipeline/`

### Features
- Ingests from YouTube (@staratlastv) + Aephia blog
- Hybrid spellcheck (dictionary + LLM for corrections)
- Fact extraction using local qwen2.5:1.5b model
- Human-like tweet generation (not hypey/robotic)
- Relevance gate: must mention Star Atlas/Z.ink
- Deduplication: 48-hour window
- Browser posting via existing browser-runner skill
- API posting stub for future Twitter API integration

### Configuration (`config/pipeline.yaml`)
```yaml
mode: "auto"        # "auto" posts, "draft" saves only
post_method: "browser"  # "browser" or "api"
interval_hours: 3
required_terms_any: ["Star Atlas","StarAtlas","Z.ink","z.ink"]
spellcheck:
  enabled: true
  strategy: "hybrid"
```

### Commands
```bash
cd /home/vbai/openclaw_unified/apps/bots/tweet-pipeline
pip install -r requirements.txt
python3 src/pipeline_run.py --dry-run  # Test without posting
python3 src/pipeline_run.py           # Run pipeline

# Add to crontab
0 */3 * * * cd /home/vbai/openclaw_unified/apps/bots/tweet-pipeline && \
  /usr/bin/python3 src/pipeline_run.py >> \
  /home/vbai/openclaw_unified/ops/logs/tweet-pipeline.log 2>&1
```

### Output Locations
- `data/drafts/` - Draft tweets
- `data/sent/` - Posted tweets
- `data/failed/` - Failed attempts
- `data/state/status.json` - Dashboard status

### Tests
16 smoke tests created, all passing (normalize, spellcheck, dedupe, relevance, config).

### Key Design Decisions
- Uses local qwen2.5:1.5b model (cost-free, no cloud dependency)
- Browser posting assumes existing X session (cookies valid)
- API mode requires: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET
