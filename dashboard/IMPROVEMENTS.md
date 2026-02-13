# OpenClaw Improvements Plan

**Created:** 2026-02-12  
**Status:** In Progress  
**Priority:** High

---

## 📋 Master TODO List

### 1. Browser Stability Fixes
- [ ] Create stable browser launcher using CDP port 9222
- [ ] Add auto-restart watchdog script
- [ ] Create systemd service template for browser
- [ ] Document setup in README

### 2. Model Fallback System
- [ ] Configure main agent to use local Ollama when cloud fails
- [ ] Add fallback chain: MiniMax → qwen2.5:1.5b → llama3.1:8b
- [ ] Test failover works

### 3. Free Web Search Integration
- [ ] Already have web-search.py using Wikipedia/GitHub/HN APIs
- [ ] Make it accessible via dashboard command /web
- [ ] Add more sources (Reddit, Stack Overflow, DuckDuckGo)

### 4. Usage Dashboard
- [ ] Create stats command showing token usage per model
- [ ] Add cron job success/failure tracking
- [ ] Display health scores

### 5. Cron Job Improvements
- [ ] Add retry logic with exponential backoff
- [ ] Add browser fallback (use web APIs if browser fails)
- [ ] Smart scheduling (run only when system healthy)

### 6. Repair Agent Enhancements
- [ ] Add common fix scripts to agent-repair
- [ ] Create auto-diagnose command
- [ ] Add health check crons

### 7. New Skills
- [ ] Install and configure coding-agent skill
- [ ] Test github skill integration
- [ ] Add nano-pdf for PDF editing

---

## 📝 Implementation Details

### Research Results

#### AI Agent Frameworks 2025 Trends
- Multi-model orchestration becoming standard
- Local-first AI agents gaining popularity
- Claude Computer Use style browser automation is emerging
- Terminal-based assistants evolving with better tool integration

#### Claude Computer Use Model
- Browser automation via CDP (Chrome DevTools Protocol)
- Visual grounding and screen understanding
- Autonomous task completion in browser
- Security sandboxing for safe automation

#### OpenClaw Alternatives
- Continue development for local-first approach
- Focus on stability and reliability improvements
- Enhanced browser automation features

#### Terminal AI Assistants Trends
- Integration with system APIs
- Better context awareness
- Multi-modal input support
- Improved reliability for production use

---

## 🔧 Implementation Progress

### 1. Browser Stability Fixes

#### 1.1 Browser Launcher Script (browser-launcher.sh)
```bash
#!/bin/bash
# Stable browser launcher using CDP port 9222
# Usage: ./browser-launcher.sh [profile]

BROWSER_PROFILE="${1:-default}"
CDP_PORT=9222
LOG_FILE="/tmp/browser-$BROWSER_PROFILE.log"

# Kill any existing browser on port
lsof -ti:$CDP_PORT | xargs kill -9 2>/dev/null

# Launch browser with remote debugging
google-chrome \
  --remote-debugging-port=$CDP_PORT \
  --user-data-dir=/tmp/chrome-$BROWSER_PROFILE \
  --no-first-run \
  --no-default-browser-check \
  --disable-default-apps \
  --disable-popup-blocking \
  --disable-translate \
  --disable-background-networking \
  --disable-sync \
  --disable-device-discovery-notifications \
  --headless=new \
  --virtual-time-budget=5000 \
  > $LOG_FILE 2>&1 &

echo "Browser launched on CDP port $CDP_PORT"
echo "Log: $LOG_FILE"
```

#### 1.2 Auto-Restart Watchdog (browser-watchdog.sh)
```bash
#!/bin/bash
# Browser auto-restart watchdog
# Run as: ./browser-watchdog.sh &

CDP_PORT=9222
MAX_RESTARTS=5
RESTART_WINDOW=300  # 5 minutes
RESTART_COUNT=0
LAST_RESTART=0

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

check_browser() {
    # Check if browser is responding on CDP port
    if ! curl -s http://localhost:$CDP_PORT/json/version > /dev/null 2>&1; then
        log "Browser not responding on port $CDP_PORT"
        return 1
    fi
    return 0
}

restart_browser() {
    CURRENT_TIME=$(date +%s)
    
    # Check restart window
    if [ $((CURRENT_TIME - LAST_RESTART)) -lt $RESTART_WINDOW ]; then
        RESTART_COUNT=$((RESTART_COUNT + 1))
    else
        RESTART_COUNT=1
    fi
    
    if [ $RESTART_COUNT -gt $MAX_RESTARTS ]; then
        log "ERROR: Too many restarts ($MAX_RESTARTS in $RESTART_WINDOW seconds)"
        log "Manual intervention required"
        return 1
    fi
    
    LAST_RESTART=$CURRENT_TIME
    log "Restarting browser (restart #$RESTART_COUNT)"
    
    # Kill existing browser
    lsof -ti:$CDP_PORT | xargs kill -9 2>/dev/null
    sleep 2
    
    # Launch new browser
    cd /home/vbai/.openclaw/workspace/dashboard
    ./browser-launcher.sh > /tmp/browser-restart.log 2>&1 &
    
    # Wait for browser to be ready
    sleep 5
    
    if check_browser; then
        log "Browser restarted successfully"
        return 0
    else
        log "Browser restart failed"
        return 1
    fi
}

log "Browser watchdog started"
while true; do
    if ! check_browser; then
        restart_browser
    fi
    sleep 30
done
```

#### 1.3 Systemd Service Template (openclaw-browser.service)
```ini
[Unit]
Description=OpenClaw Browser Service
After=network.target
Wants=network.target

[Service]
Type=simple
User=vbai
WorkingDirectory=/home/vbai/.openclaw/workspace/dashboard
ExecStart=/home/vbai/.openclaw/workspace/dashboard/browser-launcher.sh
Restart=always
RestartSec=10
Environment=DISPLAY=:0
Environment=HOME=/home/vbai

# Resource limits
MemoryMax=2G
CPUQuota=80%

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-browser

[Install]
WantedBy=multi-user.target
```

#### 1.4 README.md Update
```markdown
# Browser Stability Setup

## Quick Start

1. Make scripts executable:
```bash
chmod +x browser-launcher.sh browser-watchdog.sh
```

2. Start browser service:
```bash
# Manual (for testing)
./browser-launcher.sh

# Or with watchdog
./browser-watchdog.sh &
```

3. Systemd service (for production):
```bash
sudo cp openclaw-browser.service /etc/systemd/system/
sudo systemctl enable openclaw-browser
sudo systemctl start openclaw-browser
```

## CDP Port
- Default port: 9222
- Access: http://localhost:9222/json/version

## Troubleshooting
- Check logs: `journalctl -u openclaw-browser -f`
- Restart service: `sudo systemctl restart openclaw-browser`
```

---

### 2. Model Fallback System

#### 2.1 Fallback Configuration (model-fallback.sh)
```bash
#!/bin/bash
# Model fallback system for OpenClaw

# Fallback chain (in order of preference)
PRIMARY_MODEL="minimax-portal/MiniMax-M2.1"
FALLBACK_1="qwen2.5:1.5b"
FALLBACK_2="llama3.1:8b"
FALLBACK_3="deepseek-r1:14b"

# API endpoints
OLLAMA_URL="http://localhost:11434"
MINIMAX_API="https://api.minimax.chat/v1/text/chatcompletion_v2"

# Test function for each model
test_model() {
    local model=$1
    local provider=$2
    
    case $provider in
        "ollama")
            curl -s --max-time 5 "$OLLAMA_URL/api/tags" | grep -q "$model"
            return $?
            ;;
        "minimax")
            # MiniMax API test (requires valid API key)
            curl -s --max-time 5 -o /dev/null -w "%{http_code}" "$MINIMAX_API" | grep -q "200\|400\|401"
            return $?
            ;;
    esac
}

# Get available model with fallback
get_available_model() {
    log "Testing primary model: $PRIMARY_MODEL"
    if test_model "$PRIMARY_MODEL" "minimax"; then
        echo "$PRIMARY_MODEL"
        return 0
    fi
    
    log "Primary unavailable, trying fallback: $FALLBACK_1"
    if test_model "$FALLBACK_1" "ollama"; then
        echo "$FALLBACK_1"
        return 0
    fi
    
    log "Trying fallback: $FALLBACK_2"
    if test_model "$FALLBACK_2" "ollama"; then
        echo "$FALLBACK_2"
        return 0
    fi
    
    log "Trying fallback: $FALLBACK_3"
    if test_model "$FALLBACK_3" "ollama"; then
        echo "$FALLBACK_3"
        return 0
    fi
    
    log "ERROR: No models available"
    return 1
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [MODEL-FALLBACK] $1"
}

# Run if called directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    get_available_model
fi
```

#### 2.2 OpenClaw Configuration Update
```yaml
# Add to openclaw config
models:
  primary: minimax-portal/MiniMax-M2.1
  fallbacks:
    - qwen2.5:1.5b
    - llama3.1:8b
    - deepseek-r1:14b
  
fallback:
  enabled: true
  health_check_interval: 60
  auto_switch: true
```

---

### 3. Free Web Search Integration

#### 3.1 Enhanced Web Search Script (web-search-enhanced.py)
```python
#!/usr/bin/env python3
"""
Enhanced Free Web Search for OpenClaw
Sources: Wikipedia, GitHub, HN, Reddit, Stack Overflow, DuckDuckGo
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from typing import List, Dict, Optional

class FreeWebSearch:
    def __init__(self):
        self.user_agent = "OpenClaw/1.0 (Terminal AI Assistant)"
        self.results = []
    
    def search_wikipedia(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Wikipedia API"""
        try:
            url = f"https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "utf8": 1,
                "srlimit": max_results
            }
            url += "?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            results = []
            for item in data.get("query", {}).get("search", []):
                results.append({
                    "source": "Wikipedia",
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(item.get('title', ''))}",
                    "timestamp": item.get("timestamp", "")
                })
            return results
        except Exception as e:
            return [{"error": f"Wikipedia search failed: {str(e)}"}]
    
    def search_github(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search GitHub API"""
        try:
            url = f"https://api.github.com/search/code"
            params = {"q": query, "per_page": max_results}
            url += "?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            results = []
            for item in data.get("items", []):
                results.append({
                    "source": "GitHub",
                    "title": item.get("full_name", ""),
                    "snippet": item.get("path", ""),
                    "url": item.get("html_url", ""),
                    "description": item.get("description", "")
                })
            return results
        except Exception as e:
            return [{"error": f"GitHub search failed: {str(e)}"}]
    
    def search_hn(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Hacker News"""
        try:
            # First get story IDs
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                story_ids = json.loads(response.read().decode())[:30]
            
            # Search in first 30 stories
            results = []
            for story_id in story_ids[:30]:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                req = urllib.request.Request(story_url, headers={"User-Agent": self.user_agent})
                with urllib.request.urlopen(req, timeout=10) as response:
                    story = json.loads(response.read().decode())
                
                if story and query.lower() in (story.get("title", "") + story.get("text", "")).lower():
                    results.append({
                        "source": "Hacker News",
                        "title": story.get("title", ""),
                        "url": f"https://news.ycombinator.com/item?id={story_id}",
                        "score": story.get("score", 0)
                    })
                    if len(results) >= max_results:
                        break
            return results
        except Exception as e:
            return [{"error": f"HN search failed: {str(e)}"}]
    
    def search_reddit(self, query: str, subreddit: str = None, max_results: int = 3) -> List[Dict]:
        """Search Reddit (via pushshift API)"""
        try:
            url = "https://api.pushshift.io/reddit/search/submission"
            params = {"q": query, "size": max_results, "sort": "desc", "sort_type": "created_utc"}
            if subreddit:
                params["subreddit"] = subreddit
            url += "?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            results = []
            for item in data.get("data", []):
                results.append({
                    "source": "Reddit",
                    "title": item.get("title", ""),
                    "subreddit": f"r/{item.get('subreddit', '')}",
                    "url": f"https://reddit.com{item.get('permalink', '')}",
                    "score": item.get("score", 0)
                })
            return results
        except Exception as e:
            return [{"error": f"Reddit search failed: {str(e)}"}]
    
    def search_stackoverflow(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Stack Overflow"""
        try:
            url = "https://api.stackexchange.com/2.3/search/advanced"
            params = {
                "order": "desc",
                "sort": "activity",
                "q": query,
                "site": "stackoverflow",
                "pagesize": max_results
            }
            url += "?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            results = []
            for item in data.get("items", []):
                results.append({
                    "source": "Stack Overflow",
                    "title": item.get("title", ""),
                    "tags": item.get("tags", []),
                    "url": item.get("link", ""),
                    "score": item.get("score", 0),
                    "answer_count": item.get("answer_count", 0)
                })
            return results
        except Exception as e:
            return [{"error": f"Stack Overflow search failed: {str(e)}"}]
    
    def search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search DuckDuckGo (HTML scraping)"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}&kl=us-en"
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode()
            
            # Simple HTML parsing for results
            import re
            results = []
            # Look for result blocks
            pattern = r'<a class="result__a" href="([^"]*)"[^>]*>([^<]*)</a>'
            matches = re.findall(pattern, html)
            
            for url, title in matches[:max_results]:
                results.append({
                    "source": "DuckDuckGo",
                    "title": title.strip(),
                    "snippet": "",
                    "url": url
                })
            return results
        except Exception as e:
            return [{"error": f"DuckDuckGo search failed: {str(e)}"}]
    
    def search_all(self, query: str, sources: List[str] = None) -> Dict[str, List[Dict]]:
        """Search all sources"""
        if sources is None:
            sources = ["wikipedia", "github", "hn", "reddit", "stackoverflow", "duckduckgo"]
        
        all_results = {}
        for source in sources:
            source = source.lower()
            if source == "wikipedia":
                all_results["Wikipedia"] = self.search_wikipedia(query)
            elif source == "github":
                all_results["GitHub"] = self.search_github(query)
            elif source == "hn":
                all_results["Hacker News"] = self.search_hn(query)
            elif source == "reddit":
                all_results["Reddit"] = self.search_reddit(query)
            elif source == "stackoverflow":
                all_results["Stack Overflow"] = self.search_stackoverflow(query)
            elif source == "duckduckgo":
                all_results["DuckDuckGo"] = self.search_duckduckgo(query)
        
        return all_results

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: web-search-enhanced.py <query> [--source <source>]")
        print("Sources: wikipedia, github, hn, reddit, stackoverflow, duckduckgo (default: all)")
        sys.exit(1)
    
    query = sys.argv[1]
    sources = None
    
    if "--source" in sys.argv:
        idx = sys.argv.index("--source")
        if idx + 1 < len(sys.argv):
            sources = sys.argv[idx + 1].split(",")
    
    search = FreeWebSearch()
    results = search.search_all(query, sources)
    
    print(f"\n{'='*60}")
    print(f"Search Results for: {query}")
    print(f"{'='*60}\n")
    
    for source, items in results.items():
        print(f"\n### {source}")
        if not items or "error" in items[0]:
            print(f"  Error or no results")
            continue
            
        for i, item in enumerate(items, 1):
            print(f"\n{i}. {item.get('title', 'N/A')}")
            print(f"   URL: {item.get('url', 'N/A')}")
            if item.get('snippet'):
                snippet = item['snippet'][:150] + "..." if len(item.get('snippet', '')) > 150 else item['snippet']
                print(f"   Snippet: {snippet}")
            if item.get('score'):
                print(f"   Score: {item.get('score', 0)}")

if __name__ == "__main__":
    main()
```

---

### 4. Usage Dashboard

#### 4.1 Stats Command (stats.py)
```python
#!/usr/bin/env python3
"""
Usage statistics for OpenClaw
Tracks: Token usage, cron success/failure, health scores
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

STATS_DIR = Path.home() / ".openclaw" / "stats"
STATS_FILE = STATS_DIR / "usage.json"

class UsageStats:
    def __init__(self):
        STATS_DIR.mkdir(parents=True, exist_ok=True)
        if not STATS_FILE.exists():
            self.data = self._init_data()
            self.save()
        else:
            self.load()
    
    def _init_data(self):
        return {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "models": {},
            "crons": {
                "total_runs": 0,
                "successes": 0,
                "failures": 0,
                "by_job": {}
            },
            "health_scores": []
        }
    
    def load(self):
        with open(STATS_FILE) as f:
            self.data = json.load(f)
    
    def save(self):
        self.data["last_updated"] = datetime.now().isoformat()
        with open(STATS_FILE, "w") as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def log_model_usage(self, model: str, prompt_tokens: int, completion_tokens: int):
        if model not in self.data["models"]:
            self.data["models"][model] = {
                "requests": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "first_used": datetime.now().isoformat(),
                "last_used": datetime.now().isoformat()
            }
        
        self.data["models"][model]["requests"] += 1
        self.data["models"][model]["prompt_tokens"] += prompt_tokens
        self.data["models"][model]["completion_tokens"] += completion_tokens
        self.data["models"][model]["total_tokens"] += prompt_tokens + completion_tokens
        self.data["models"][model]["last_used"] = datetime.now().isoformat()
        self.save()
    
    def log_cron_run(self, job_name: str, success: bool, duration_ms: int = 0):
        self.data["crons"]["total_runs"] += 1
        if success:
            self.data["crons"]["successes"] += 1
        else:
            self.data["crons"]["failures"] += 1
        
        if job_name not in self.data["crons"]["by_job"]:
            self.data["crons"]["by_job"][job_name] = {
                "total_runs": 0,
                "successes": 0,
                "failures": 0,
                "avg_duration_ms": 0
            }
        
        job = self.data["crons"]["by_job"][job_name]
        job["total_runs"] += 1
        if success:
            job["successes"] += 1
        else:
            job["failures"] += 1
        
        if duration_ms > 0:
            job["avg_duration_ms"] = int((job["avg_duration_ms"] * (job["total_runs"] - 1) + duration_ms) / job["total_runs"])
        
        self.save()
    
    def log_health_score(self, score: float, details: dict = None):
        self.data["health_scores"].append({
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "details": details or {}
        })
        self.data["health_scores"] = self.data["health_scores"][-100:]
        self.save()
    
    def get_summary(self) -> dict:
        """Get usage summary"""
        crons = self.data["crons"]
        success_rate = (crons["successes"] / crons["total_runs"] * 100) if crons["total_runs"] > 0 else 0
        
        avg_health = 0
        if self.data["health_scores"]:
            scores = [s["score"] for s in self.data["health_scores"]]
            avg_health = sum(scores) / len(scores)
        
        return {
            "models": self.data["models"],
            "crons": {
                "total_runs": crons["total_runs"],
                "successes": crons["successes"],
                "failures": crons["failures"],
                "success_rate": f"{success_rate:.1f}%",
                "by_job": crons["by_job"]
            },
            "health": {
                "average_score": f"{avg_health:.1f}",
                "recent_checks": len(self.data["health_scores"])
            }
        }
    
    def display(self):
        """Display stats in terminal-friendly format"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("OPENCLAW USAGE STATISTICS")
        print("="*60)
        print(f"Last Updated: {self.data['last_updated']}")
        
        print("\n### Model Usage")
        if summary["models"]:
            print(f"{'Model':<30} {'Requests':<10} {'Prompt Tokens':<15} {'Completion':<12} {'Total':<10}")
            print("-" * 77)
            for model, stats in summary["models"].items():
                print(f"{model:<30} {stats['requests']:<10} {stats['prompt_tokens']:<15} {stats['completion_tokens']:<12} {stats['total_tokens']:<10}")
        else:
            print("No model usage recorded yet.")
        
        print("\n### Cron Jobs")
        crons = summary["crons"]
        print(f"Total Runs: {crons['total_runs']}")
        print(f"Successes:  {crons['successes']}")
        print(f"Failures:   {crons['failures']}")
        print(f"Success Rate: {crons['success_rate']}")
        
        if crons["by_job"]:
            print(f"\n{'Job Name':<25} {'Runs':<8} {'Success':<8} {'Fail':<8} {'Avg Duration':<15}")
            print("-" * 70)
            for job, stats in crons["by_job"].items():
                print(f"{job:<25} {stats['total_runs']:<8} {stats['successes']:<8} {stats['failures']:<8} {stats['avg_duration_ms']:<15}ms")
        
        print("\n### Health Scores")
        health = summary["health"]
        print(f"Average Score: {health['average_score']}/100")
        print(f"Recent Checks: {health['recent_checks']}")
        
        print("\n" + "="*60)

def main():
    stats = UsageStats()
    stats.display()

if __name__ == "__main__":
    main()
```

---

### 5. Cron Job Improvements

#### 5.1 Enhanced Cron Manager (cron-manager.sh)
```bash
#!/bin/bash
# Enhanced cron manager with retry logic, fallback, and smart scheduling

CRON_DIR="$HOME/.openclaw/crons"
LOG_DIR="$HOME/.openclaw/logs"
MAX_RETRIES=3
RETRY_DELAY=30  # seconds
HEALTH_CHECK_URL="http://localhost:8080/health"
SYSTEM_LOAD_THRESHOLD=80  # percentage

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [CRON-MGR] $1"
}

check_system_health() {
    # Check CPU load
    load=$(uptime | grep -oP '\d+\.\d+' | head -1)
    load_int=${load%.*}
    
    # Check memory
    mem_used=$(free | grep Mem | awk '{print $3/$2 * 100}')
    
    # Check disk
    disk_used=$(df / | grep / | awk '{print $5}' | tr -d '%')
    
    # Check if health endpoint responds
    health_ok=false
    if curl -s --max-time 5 "$HEALTH_CHECK_URL" > /dev/null 2>&1; then
        health_ok=true
    fi
    
    echo "$load_int $mem_used $disk_used $health_ok"
}

is_system_healthy() {
    read load mem disk health <<< $(check_system_health)
    
    if [ "$health" != "true" ]; then
        log "System unhealthy: health endpoint not responding"
        return 1
    fi
    
    if [ "$load" -gt "$SYSTEM_LOAD_THRESHOLD" ]; then
        log "System overloaded: CPU load $load%"
        return 1
    fi
    
    if [ "$mem_used" -gt 90 ]; then
        log "Memory critical: $mem_used% used"
        return 1
    fi
    
    if [ "$disk_used" -gt 90 ]; then
        log "Disk critical: $disk_used% used"
        return 1
    fi
    
    return 0
}

run_cron_with_retry() {
    local job_name=$1
    local command=$2
    local max_retries=${3:-$MAX_RETRIES}
    local retry_delay=${4:-$RETRY_DELAY}
    
    local attempt=1
    local success=false
    local start_time=$(date +%s)
    
    while [ $attempt -le $max_retries ]; do
        log "Running $job_name (attempt $attempt/$max_retries)"
        
        # Check system health before running
        if ! is_system_healthy; then
            log "Skipping $job_name - system unhealthy"
            return 1
        fi
        
        # Execute command with timeout
        timeout 300 $command > "$LOG_DIR/$job_name.log" 2>&1
        
        if [ $? -eq 0 ]; then
            success=true
            log "$job_name completed successfully"
            break
        else
            log "$job_name failed (exit code: $?)"
            
            if [ $attempt -lt $max_retries ]; then
                # Exponential backoff
                sleep $((retry_delay * (2 ** (attempt - 1))))
            fi
        fi
        
        attempt=$((attempt + 1))
    done
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # Log result
    if [ "$success" = true ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') $job_name SUCCESS $duration" >> "$LOG_DIR/cron-history.log"
        return 0
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') $job_name FAILED $duration" >> "$LOG_DIR/cron-history.log"
        
        # Try browser fallback if available
        if [ -f "$HOME/.openclaw/workspace/dashboard/web-search-enhanced.py" ]; then
            log "Attempting web API fallback for $job_name"
            python3 "$HOME/.openclaw/workspace/dashboard/web-search-enhanced.py" "fallback check" > /dev/null 2>&1
        fi
        
        return 1
    fi
}

# Smart scheduler - only run if system healthy
smart_schedule() {
    local job_name=$1
    local interval=${2:-300}  # seconds
    
    while true; do
        if is_system_healthy; then
            run_cron_with_retry "$job_name"
        else
            log "Postponing $job_name - system unhealthy"
        fi
        sleep $interval
    done
}

# Usage
case "${1:-help}" in
    "run")
        run_cron_with_retry "$2" "$3" "${4:-$MAX_RETRIES}" "${5:-$RETRY_DELAY}"
        ;;
    "health")
        check_system_health
        ;;
    "schedule")
        smart_schedule "$2" "$3"
        ;;
    *)
        echo "Usage: $0 {run|health|schedule} <job_name> <command> [max_retries] [retry_delay]"
        ;;
esac
```

---

### 6. Repair Agent Enhancements

#### 6.1 Auto-Diagnose Script (agent-repair.sh)
```bash
#!/bin/bash
# Agent repair and auto-diagnose script

LOG_DIR="$HOME/.openclaw/logs"
DIAGNOSTIC_FILE="$HOME/.openclaw/diagnostics.json"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [REPAIR] $1"
}

check_disk_space() {
    log "Checking disk space..."
    df -h | grep -E "^/dev/" | awk '{print $5 " " $1}'
}

check_memory() {
    log "Checking memory..."
    free -h
}

check_processes() {
    log "Checking critical processes..."
    ps aux | grep -E "(openclaw|ollama|chrome)" | grep -v grep
}

check_ports() {
    log "Checking ports..."
    ss -tlnp | grep -E "(8080|11434|9222)"
}

test_network() {
    log "Testing network connectivity..."
    ping -c 3 8.8.8.8
    curl -s --max-time 5 https://api.minimax.chat > /dev/null && echo "MiniMax API: OK" || echo "MiniMax API: FAIL"
    curl -s --max-time 5 http://localhost:11434 > /dev/null && echo "Ollama: OK" || echo "Ollama: FAIL"
}

test_browser() {
    log "Testing browser CDP..."
    curl -s http://localhost:9222/json/version > /dev/null && echo "Browser CDP: OK" || echo "Browser CDP: FAIL"
}

fix_permissions() {
    log "Fixing permissions..."
    chmod +x "$HOME/.openclaw/workspace/dashboard/"*.sh
    chmod +x "$HOME/.openclaw/workspace/dashboard/"*.py
}

restart_ollama() {
    log "Restarting Ollama..."
    pkill -f ollama
    sleep 2
    ollama serve > /dev/null 2>&1 &
    sleep 5
}

restart_browser() {
    log "Restarting browser..."
    pkill -f "chrome.*remote-debugging"
    sleep 2
    "$HOME/.openclaw/workspace/dashboard/browser-launcher.sh"
}

auto_diagnose() {
    echo "=== OPENCLAW AUTO-DIAGNOSTIC ==="
    echo "Timestamp: $(date)"
    echo ""
    
    echo "## System Info"
    echo "Disk:"
    check_disk_space
    echo ""
    echo "Memory:"
    check_memory
    echo ""
    
    echo "## Network"
    test_network
    echo ""
    
    echo "## Services"
    test_browser
    echo ""
    
    echo "## Processes"
    check_processes
    echo ""
    
    echo "## Ports"
    check_ports
    echo ""
    
    echo "## Recommendations:"
    # Simple logic for recommendations
    if curl -s http://localhost:9222 > /dev/null 2>&1; then
        echo "- Browser: OK"
    else
        echo "- Browser: Not responding, try: ./browser-launcher.sh"
    fi
    
    if curl -s http://localhost:11434 > /dev/null 2>&1; then
        echo "- Ollama: OK"
    else
        echo "- Ollama: Not responding, try: ollama serve"
    fi
}

case "${1:-diagnose}" in
    "diagnose")
        auto_diagnose
        ;;
    "fix-permissions")
        fix_permissions
        ;;
    "restart-ollama")
        restart_ollama
        ;;
    "restart-browser")
        restart_browser
        ;;
    "fix-all")
        fix_permissions
        restart_ollama
        restart_browser
        ;;
    *)
        echo "Usage: $0 {diagnose|fix-permissions|restart-ollama|restart-browser|fix-all}"
        ;;
esac
```

#### 6.2 Health Check Cron (health-check-cron.sh)
```bash
#!/bin/bash
# Health check cron - runs every 5 minutes

CHECK_INTERVAL=300  # 5 minutes
STATS_FILE="$HOME/.openclaw/stats/usage.json"

log_health() {
    local score=$1
    local details=$2
    python3 -c "
import json
from datetime import datetime

stats = {'timestamp': datetime.now().isoformat(), 'score': $score, 'details': $details}
with open('$STATS_FILE', 'r') as f:
    data = json