# OpenClaw - Complete File Inventory & Improvement Guide

**Generated:** 2026-02-13  
**Purpose:** Document every key file, its purpose, and how to improve

---

## Quick Stats

| Category | Count |
|----------|-------|
| Total Files | ~14,000+ (includes node_modules) |
| Key Files | ~200 (Python, Markdown, JSON, Shell) |
| Configs | ~50 JSON files |
| Scripts | ~15 Python scripts |

---

## CORE FILES

### /home/vbai/.openclaw/

| File/Folder | Purpose | Status | Improvements Needed |
|-------------|---------|--------|---------------------|
| `openclaw.json` | Main configuration (models, agents, crons) | ✅ Working | Backup before any changes, add validation |
| `openclawbroken.json` | Broken config backup | ⚠️ Reference | Keep for debugging, delete when stable |
| `telegram-bot-token.txt` | Telegram bot token | ✅ Working | Secure, no changes needed |
| `gateway.token` | Gateway auth token | ✅ Working | Secure |

---

## AGENTS

### ~/.openclaw/agents/

| Agent | File | Purpose | Status | Improvements |
|-------|------|---------|--------|--------------|
| **main** | N/A (OpenClaw default) | Primary assistant | ✅ Working | Add memory persistence |
| **qwen** | N/A | Fast local backup | ✅ Working | None |
| **llama** | N/A | Complex tasks | ✅ Working | None |
| **thinking** | N/A | Reasoning | ✅ Working | None |
| **repair** | N/A | Fixer agent | ✅ Working | None |
| **research-agent** | `research_agent.py` | Auto-improvement search | ✅ Working | Add AI analysis of findings |
| **project-manager** | `project_manager.py` | Project tracking | ✅ Working | Add progress visualization |
| **communications** | `communications.py` | Email/Telegram reports | ✅ Working | Add SMS support |
| **test-agent** | `test_agent.py` | Automated testing | ✅ Working | Add unit test generation |
| **staratlas** | `staratlas_skill.py` | Star Atlas queries | ⚠️ Needs update | Update to new API |
| **solana** | `solana_skill.py` | Solana/DeFi | ⚠️ Needs update | Add Raydium/Orca |
| **holosim** | `holosim_agent.py` | Holosim automation | 🔄 Paused | Wait for game launch |
| **game-tester** | `agent.py` | Game testing | ✅ Working | Add automated play |
| **gamedev** | `agent.py` | Game development | ✅ Working | Add feature templates |
| **gemini** | `agent.py` | Placeholder | ❌ Not configured | Skip, use main |
| **grok** | `agent.py` | Placeholder | ❌ No API key | Skip, use main |

### Priority Agents to Improve
1. **research-agent** - Add AI-powered analysis of findings
2. **project-manager** - Add Gantt chart visualization
3. **communications** - Add SMS/matrix support

---

## PROJECTS

### ~/.openclaw/projects/

#### fleet-alerts/
| File | Purpose | Status | Improvements |
|------|---------|--------|--------------|
| `fleet_alerts.py` | Fleet monitoring + Telegram alerts | ✅ Done | Add SMS, webhooks |
| `tracked_fleets.json` | Fleet list | ✅ Working | Add more ships |
| `install_cron.sh` | Cron installer | ✅ Working | None |
| `test_alerts.sh` | Test script | ✅ Working | None |
| `README.md` | Documentation | ✅ Working | None |

#### portfolio-tracker/
| File | Purpose | Status | Improvements |
|------|---------|--------|--------------|
| `portfolio_tracker.py` | SOL/ATLAS/POLIS tracking | 🔄 In Progress | Add live price feeds |
| N/A | LP position tracking | ❌ Missing | Add Raydium/Orca integration |

### New Projects Needed
1. **DEX Tracker** - Raydium/Orca integration
2. **SAGE Fleet Parser** - Anchor/Borsh decoding
3. **Game Metrics** - Track Flappy/SideScroller scores

---

## SCRIPTS

### ~/.openclaw/scripts/

| Script | Purpose | Status | Improvements |
|--------|---------|--------|--------------|
| `db.py` | Database utilities | ✅ Working | Add encryption |
| `staratlas_tv_check.py` | Twitter agent (Star Atlas TV) | ✅ Working | Add video thumbnails |
| `get_transcript.py` | YouTube transcript fetcher | ✅ Working | Add caching, error handling |
| `youtube_transcript.py` | YouTube Data API v3 | ⚠️ Needs API key | User must set up |
| `setup-youtube-api.sh` | API setup script | ✅ Working | None |
| `autopush.sh` | Auto-commit to GitHub | ✅ Working | Add conflict resolution |

### Priority Script Improvements
1. **staratlas_tv_check.py** - Add hashtag optimization, image generation
2. **get_transcript.py** - Add Redis caching, retry logic
3. **autopush.sh** - Add PR creation, branch management

---

## SKILLS

### ~/.openclaw/skills/

#### solana/
| File | Purpose | Status | Improvements |
|------|---------|--------|--------------|
| `solana_skill.py` | Core Solana functionality | ⚠️ Basic | Add DeFi protocols |
| `portfolio_dashboard.py` | Portfolio visualization | ✅ Working | Add charts |
| `wallets.json` | Wallet addresses | ✅ Working | Add labels |
| `watched.json` | Watched tokens | ✅ Working | None |

**Needed:** Raydium integration, Orca whirlpools

#### staratlas/
| File | Purpose | Status | Improvements |
|------|---------|--------|--------------|
| `staratlas_skill.py` | Core Star Atlas | ⚠️ Basic | Update API |
| `sage_fleet_tracker.py` | SAGE fleet tracking | ⚠️ Basic | Add Anchor/Borsh |
| `staratlas_api.py` | API wrapper | ⚠️ Basic | Update endpoints |
| `realtime_tracker.py` | Real-time data | ✅ Working | None |
| `data.json` | Static data | ✅ Working | None |

**Needed:** New API integration, fleet parsing

#### github/
| File | Purpose | Status | Improvements |
|------|---------|--------|--------------|
| `github.py` | GitHub automation | ⚠️ Basic | Add PR review, issue tracking |
| `skill.json` | Skill config | ✅ Working | None |

**Needed:** PR merge automation, release notes

#### browser-runner/
| File | Purpose | Status | Improvements |
|------|---------|--------|--------------|
| `browser_runner.py` | Browser automation | ✅ Working | Add more actions |
| `SKILL.md` | Documentation | ✅ Working | None |

**Needed:** Screenshot comparison, form filling

---

## CONFIGURATIONS

### ~/.openclaw/

| Config | Purpose | Status | Improvements |
|--------|---------|--------|--------------|
| `openclaw.json` | Main config | ✅ Working | Add schema validation |
| `agents.json` | Agent database | ✅ Working | Add status field |
| `topics/` | Conversation topics | ✅ Working | Add search |
| `database/` | Agent database | ✅ Working | Add backup |

---

## DASHBOARD

### ~/openclaw-dashboard/

| File | Purpose | Status | Improvements |
|------|---------|--------|--------------|
| `dashboard.py` | Main TUI | ✅ Working | Add graphs |
| `stats.py` | Statistics | ✅ Working | Add trends |
| `web-search-enhanced.py` | Free web search | ✅ Working | Add more sources |
| `improvement-tracker.html` | Web dashboard | ✅ Working | Auto-refresh |
| `transcribe.py` | Voice transcription | ✅ Working | None |

### Needed Dashboard Features
1. **Live agent status** - Real-time updates
2. **Cost tracking** - Token usage graphs
3. **Project timeline** - Gantt chart
4. **Alert center** - All notifications in one place

---

## WORKSPACES

### ~/.openclaw/workspace*/
| Workspace | Purpose | Status | Improvements |
|-----------|---------|--------|--------------|
| `workspace` | Main agent workspace | ✅ Working | Add templates |
| `workspace-holosim` | Holosim agent | 🔄 Paused | Wait for launch |
| `workspace-ollama-test` | Testing | ✅ Working | None |
| `workspace-game-tester` | Game testing | ✅ Working | None |
| `workspace-qwen` | Qwen agent | ✅ Working | None |
| `workspace-llama` | Llama agent | ✅ Working | None |
| `workspace-thinking` | Thinking agent | ✅ Working | None |
| `workspace-repair` | Repair agent | ✅ Working | None |
| `workspace-gemini` | Gemini agent (empty) | ❌ Not used | Skip |
| `workspace-grok` | Grok agent (empty) | ❌ Not used | Skip |

---

## MEMORY FILES

### ~/.openclaw/workspace/memory/

| File | Purpose | Status |
|------|---------|--------|
| `2026-02-11.md` | Day 1 logs | ✅ Working |
| `2026-02-12.md` | Day 2 logs | ✅ Working |
| `2026-02-13.md` | Day 3 logs | ✅ Working |
| `MEMORY.md` | Long-term memory | ✅ Working |
| `HISTORY.md` | Complete timeline | ✅ New |

### Needed Memory Improvements
1. **Auto-summarization** - AI summarizes daily notes
2. **Cross-reference** - Link related memories
3. **Search** - Full-text search

---

## IMPROVEMENT ROADMAP

### Phase 1: Quick Wins (This Week)
| Item | Effort | Impact |
|------|--------|--------|
| Add schema validation to config | Low | High |
| Improve Twitter agent thumbnails | Low | Medium |
| Add error retry to transcripts | Low | High |
| Improve project-manager visualization | Medium | Medium |

### Phase 2: Medium Tasks (This Month)
| Item | Effort | Impact |
|------|--------|--------|
| Add Raydium/Orca to Solana skill | Medium | High |
| Update Star Atlas API integration | Medium | High |
| Add AI analysis to research agent | Medium | High |
| Create DEX tracking project | Medium | High |

### Phase 3: Long-term (Next Quarter)
| Item | Effort | Impact |
|------|--------|--------|
| Full Holosim automation | High | High |
| Complete SAGE fleet parsing | High | High |
| Cross-agent memory system | High | High |
| Self-improving agent | High | Very High |

---

## MISSING FILES

### Files That Should Exist But Don't

| File | Purpose | Priority |
|------|---------|----------|
| `backup-openclaw.sh` | Automated config backup | High |
| `health-check.sh` | System health check | Medium |
| `cleanup-zombies.sh` | Kill stuck processes | High |
| `update-all.sh` | Update all agents/skills | Medium |
| `migration-v1-v2.py` | Config migration | Low |
| `docs/API.md` | API documentation | Low |
| `docs/AGENTS.md` | Agent documentation | Low |
| `tests/` | Test suite | High |

---

## CRITICAL IMPROVEMENTS

### 1. Backup System
**Current:** Manual backup to `openclawbroken.json`  
**Needed:** Automated, dated backups
```bash
#!/bin/bash
# backup-openclaw.sh
DATE=$(date +%Y%m%d_%H%M%S)
cp ~/.openclaw/openclaw.json ~/.openclaw/backups/openclaw_$DATE.json
```

### 2. Health Check Script
**Current:** Manual `openclaw health`  
**Needed:** Automated with alerts
```bash
#!/bin/bash
# health-check.sh
openclaw health || notify_via_telegram "OpenClaw unhealthy!"
```

### 3. Config Validation
**Current:** JSON corruption undetected  
**Needed:** Pre-save validation
```python
import jsonschema
# Validate against schema before saving
```

### 4. Session Monitor
**Current:** Sessions hang, zombie processes  
**Needed:** Auto-restart on timeout
```bash
# Kill sessions older than 1 hour
pkill -9 -f "agent.*hung"
```

---

## QUICK COMMANDS REFERENCE

### System Status
```bash
openclaw status                    # Gateway status
openclaw agents list               # All agents
openclaw health                    # Health check
ps aux | grep openclaw            # Processes
```

### Dashboard
```bash
python3 ~/openclaw-dashboard/dashboard.py      # TUI
python3 ~/openclaw-dashboard/stats.py          # Stats
bash ~/openclaw-dashboard/improvement-status.sh # Projects
```

### Scripts
```bash
python3 ~/.openclaw/scripts/staratlas_tv_check.py --daily  # Tweet
python3 ~/.openclaw/scripts/get_transcript.py <video_id>  # Transcript
bash ~/.openclaw/scripts/autopush.sh                            # Git push
```

### GitHub
```bash
cd ~/openclaw-dashboard && git push origin main
cd ~/.openclaw && git add . && git commit -m "Update" && git push
```

---

## FILE COUNT SUMMARY

| Directory | Files | Purpose |
|-----------|-------|---------|
| `agents/` | 15 | Agent implementations |
| `projects/` | 2 | Major projects |
| `scripts/` | 6 | Automation scripts |
| `skills/` | 30+ | Domain skills |
| `workspace/memory/` | 8 | Daily logs |
| `workspace.old/` | 50+ | Legacy files |
| `dashboard/` | 15+ | Dashboard files |
| `node_modules/` | 13,000+ | Dependencies (ignore) |

---

*Document generated: 2026-02-13*
*Last updated: 2026-02-13*

---

## NEW: Critical Scripts (Created 2026-02-13)

| Script | Purpose | Status |
|--------|---------|--------|
| `backup-openclaw.sh` | Automated config/memory backup | ✅ New |
| `health-check.sh` | System health check with alerts | ✅ New |
| `cleanup-zombies.sh` | Kill stuck processes | ✅ New |
| `validate-config.py` | JSON validation before save | ✅ New |
| `update-all.sh` | Update all components | ✅ New |

### Usage

```bash
# Backup everything
~/.openclaw/scripts/backup-openclaw.sh "Optional commit message"

# Health check (add --notify for Telegram alert)
~/.openclaw/scripts/health-check.sh
~/.openclaw/scripts/health-check.sh --notify

# Cleanup stuck processes
~/.openclaw/scripts/cleanup-zombies.sh
~/.openclaw/scripts/cleanup-zombies.sh --restart

# Validate config before saving
python3 ~/.openclaw/scripts/validate-config.py
python3 ~/.openclaw/scripts/validate-config.py ~/.openclaw/openclaw.json

# Update all components
~/.openclaw/scripts/update-all.sh
```

### Auto-Add to Cron

```bash
# Backup daily at 2 AM
0 2 * * * ~/.openclaw/scripts/backup-openclaw.sh

# Health check every hour
0 * * * * ~/.openclaw/scripts/health-check.sh

# Cleanup every 30 minutes
*/30 * * * * ~/.openclaw/scripts/cleanup-zombies.sh
```

---

## CRON JOBS (Auto-Added 2026-02-13)

| Schedule | Job | Purpose |
|----------|-----|---------|
| `0 2 * * *` | Backup | Daily config/memory backup |
| `0 * * * *` | Health check | Hourly system health |
| `*/30 * * * *` | Cleanup | Kill zombie processes |

