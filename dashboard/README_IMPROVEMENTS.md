# OpenClaw Dashboard Improvements

**Created:** 2026-02-12  
**Status:** Implemented  
**Location:** `/home/vbai/.openclaw/workspace/dashboard/`

---

## 📁 New Scripts Created

### 1. Browser Stability

| Script | Purpose |
|--------|---------|
| `browser-launcher.sh` | Stable browser launcher using CDP port 9222 |
| `browser-watchdog.sh` | Auto-restart watchdog for browser |
| `openclaw-browser.service` | Systemd service template |

**Usage:**
```bash
# Manual launch
./browser-launcher.sh

# With watchdog (runs in background)
./browser-watchdog.sh &

# Systemd service (production)
sudo cp openclaw-browser.service /etc/systemd/system/
sudo systemctl enable openclaw-browser
sudo systemctl start openclaw-browser
```

### 2. Model Fallback System

| Script | Purpose |
|--------|---------|
| `model-fallback.sh` | Automatic model switching with fallback chain |

**Fallback Chain:**
1. MiniMax (cloud primary)
2. qwen2.5:1.5b (Ollama local)
3. llama3.1:8b (Ollama local)
4. deepseek-r1:14b (Ollama local)

**Usage:**
```bash
./model-fallback.sh
# Returns available model name
```

### 3. Free Web Search

| Script | Purpose |
|--------|---------|
| `web-search-enhanced.py` | Multi-source web search |

**Sources:** Wikipedia, GitHub, HN, Reddit, Stack Overflow, DuckDuckGo

**Usage:**
```bash
# Search all sources
./web-search-enhanced.py "artificial intelligence"

# Search specific source
./web-search-enhanced.py "python tutorial" --source wikipedia

# Multiple sources
./web-search-enhanced.py "machine learning" --source github,stackoverflow
```

### 4. Usage Dashboard

| Script | Purpose |
|--------|---------|
| `stats.py` | Token usage, cron tracking, health scores |

**Usage:**
```bash
./stats.py
```

**Tracks:**
- Model usage (tokens, requests)
- Cron job success/failure rates
- Health scores over time

### 5. Cron Job Improvements

| Script | Purpose |
|--------|---------|
| `cron-manager.sh` | Retry logic, health checks, smart scheduling |

**Features:**
- Exponential backoff retry
- System health checks before running
- Browser fallback for failed jobs
- Smart scheduling (skips when system overloaded)

**Usage:**
```bash
# Run with retry
./cron-manager.sh run <job_name> <command>

# Check system health
./cron-manager.sh health

# Smart schedule (runs in loop)
./cron-manager.sh schedule <job_name> <interval_seconds>
```

### 6. Repair Agent

| Script | Purpose |
|--------|---------|
| `agent-repair.sh` | Auto-diagnose and fix common issues |

**Commands:**
```bash
# Diagnose system
./agent-repair.sh diagnose

# Fix permissions
./agent-repair.sh fix-permissions

# Restart Ollama
./agent-repair.sh restart-ollama

# Restart browser
./agent-repair.sh restart-browser

# Run all fixes
./agent-repair.sh fix-all
```

---

## 📋 Quick Reference

### CDP Browser Port
- **Port:** 9222
- **API:** http://localhost:9222/json/version
- **Status Check:** `curl http://localhost:9222/json/version`

### Model Endpoints
- **Ollama:** http://localhost:11434
- **MiniMax:** https://api.minimax.chat/v1/text/chatcompletion_v2

### Health Checks
```bash
# Browser
curl http://localhost:9222/json/version

# Ollama
curl http://localhost:11434/api/tags

# System
./cron-manager.sh health
```

---

## 🔧 Configuration

### Systemd Service Setup
```bash
# Install browser service
sudo cp openclaw-browser.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable openclaw-browser
sudo systemctl start openclaw-browser

# Check status
sudo systemctl status openclaw-browser

# View logs
journalctl -u openclaw-browser -f
```

### Crontab Setup
```bash
# Add health check cron
echo "*/5 * * * * /home/vbai/.openclaw/workspace/dashboard/cron-manager.sh health" | crontab -

# Add repair auto-check
echo "0 * * * * /home/vbai/.openclaw/workspace/dashboard/agent-repair.sh diagnose >> /var/log/openclaw-repair.log 2>&1" | crontab -
```

---

## 📊 Monitoring

### View Logs
```bash
# Browser logs
tail -f /tmp/browser-default.log

# Cron history
tail -f ~/.openclaw/logs/cron-history.log

# Repair logs
tail -f /var/log/openclaw-repair.log
```

### Stats File
- **Location:** `~/.openclaw/stats/usage.json`
- **Format:** JSON
- **Contents:** Model usage, cron stats, health scores

---

## 🚨 Troubleshooting

### Browser Won't Start
```bash
# Kill existing processes
lsof -ti:9222 | xargs kill -9

# Check port
ss -tlnp | grep 9222

# Launch manually
./browser-launcher.sh
```

### Ollama Not Responding
```bash
# Check status
curl http://localhost:11434/api/tags

# Restart Ollama
./agent-repair.sh restart-ollama

# Manual restart
pkill -f ollama
ollama serve &
```

### Model Fallback Not Working
```bash
# Test Ollama directly
curl http://localhost:11434/api/tags

# Test MiniMax
curl https://api.minimax.chat/v1/text/chatcompletion_v2

# Run fallback manually
./model-fallback.sh
```

---

## 📈 Performance

### Expected Resource Usage
- **Browser:** ~1-2GB RAM (headless)
- **Ollama:** ~2-8GB RAM (depends on model)
- **CPU:** <50% typical, spikes during model inference

### Optimization Tips
1. Use smaller models (qwen2.5:1.5b) for routine tasks
2. Reserve llama3.1:8b for complex reasoning
3. Monitor with `./cron-manager.sh health`
4. Use watchdog for browser stability

---

## 🔒 Security Notes

- Browser runs headless with minimal permissions
- CDP port exposed locally only
- Local models keep data on your machine
- No external API keys required for basic operation

---

## 📝 Changelog

### 2026-02-12
- Initial implementation of all improvement scripts
- Created IMPROVEMENTS.md with full documentation
- Added systemd service template
- Implemented multi-source web search
- Added usage statistics tracking
- Created repair and diagnostic tools
