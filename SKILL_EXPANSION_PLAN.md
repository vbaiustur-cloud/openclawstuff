# 🛠️ SKILL EXPANSION PLAN
## Adding More Capabilities to Your Autonomy System

---

## CURRENT STATE (9 Skills)

| Skill | Purpose | Status |
|-------|---------|--------|
| Web Researcher | Research + browse | ✅ |
| Code Assistant | Write + debug code | ✅ |
| Task Automation | Run workflows | ✅ |
| Summarizer | Summarize URLs/text | ✅ |
| File Manager | Organize + search | ✅ |
| Browser Runner | Deterministic automation | ✅ |
| Self-Diagnostics | Auto-fix issues | ✅ |
| Preference Learner | Memory + learning | ✅ |
| Monitoring Dashboard | Real-time stats | ✅ |

---

## 🚀 NEW SKILLS TO ADD

### Priority 1: High Value, Low Effort

#### 1.1 Git & GitHub Skill
```bash
# Commands it would handle:
- "Create a git repo"
- "Commit my changes"
- "Push to GitHub"
- "Create a PR"
- "Check status"
```

**Implementation:** Use `gh` CLI (already installed!)

**Files needed:**
```
~/.openclaw/skills/github/
├── skill.json
├── github.py
└── README.md
```

---

#### 1.2 System Monitor Skill
```bash
# Commands:
- "Check disk space"
- "Show CPU usage"
- "List running processes"
- "Check memory"
```

**Implementation:** Python psutil + subprocess

**Files needed:**
```
~/.openclaw/skills/system-monitor/
├── skill.json
├── monitor.py
└── README.md
```

---

#### 1.3 Calculator Skill
```bash
# Commands:
- "Calculate 15% of 200"
- "Convert 100 EUR to USD"
- "What is 2^16?"
```

**Implementation:** Python eval + forex API

**Files needed:**
```
~/.openclaw/skills/calculator/
├── skill.json
├── calculator.py
└── README.md
```

---

### Priority 2: Medium Effort, High Value

#### 2.1 Music Player Skill
```bash
# Commands:
- "Play some music"
- "Next track"
- "Pause"
- "What's playing?"
```

**Implementation:** mpc (MPD client) or Spotify API

---

#### 2.2 Note Taker Skill
```bash
# Commands:
- "Note: buy milk"
- "Add todo: call mom"
- "What's on my list?"
```

**Implementation:** Simple JSON file storage

---

#### 2.3 Weather Skill
```bash
# Commands:
- "What's the weather?"
- "Will it rain tomorrow?"
```

**Implementation:** wttr.in (free, no API key!)

---

#### 2.4 Calculator Plus
```bash
# Commands:
- "Calculate 15% of 200"
- "What is 50 USD in EUR?"
- "Convert 100 MB to GB"
```

**Implementation:** Python + forex API

---

### Priority 3: Advanced Features

#### 3.1 Smart Home Skill
```bash
# Commands:
- "Turn on the lights"
- "Set thermostat to 22"
```

**Implementation:** Home Assistant API

---

#### 3.2 Calendar Skill
```bash
# Commands:
- "What's on my calendar?"
- "Schedule meeting for tomorrow"
```

**Implementation:** Already have gog! Just need wrapper

---

#### 3.3 Email Skill
```bash
# Commands:
- "Check my emails"
- "Send email to Oliver"
```

**Implementation:** gog mail integration

---

## 📋 IMPLEMENTATION ORDER

```
Week 1: Foundation
├── 1. Git & GitHub (use existing 'gh' CLI)
├── 2. System Monitor (psutil)
├── 3. Calculator (eval + forex)
└── 4. Weather (wttr.in)

Week 2: Lifestyle
├── 5. Note Taker (JSON storage)
├── 6. Music Player (mpc)
└── 7. Reminder System

Week 3: Integration
├── 8. Calendar (gog integration)
├── 9. Email (gog integration)
└── 10. Smart Home (Home Assistant)

Week 4: Advanced
├── 11. Data Analytics (pandas)
├── 12. Image Processing (PIL)
└── 13. PDF Tools (PyPDF2)
```

---

## 🎯 QUICK WINS (Today)

### Git & GitHub Skill (Most Useful!)

```bash
# Create the skill
mkdir -p ~/.openclaw/skills/github
cat > ~/.openclaw/skills/github/skill.json << 'EOF'
{
  "name": "github",
  "version": "1.0.0",
  "description": "Git and GitHub operations",
  "author": "vb",
  "commands": [
    "create repo",
    "commit",
    "push",
    "pull",
    "status",
    "clone"
  ]
}
EOF

cat > ~/.openclaw/skills/github/github.py << 'PYEOF'
#!/usr/bin/env python3
"""
Git & GitHub Skill
Uses 'gh' CLI for GitHub operations
"""

import subprocess
import json
from pathlib import Path

class GitHubSkill:
    """Git and GitHub operations via gh CLI"""
    
    def __init__(self):
        self.gh_available = self._check_gh()
    
    def _check_gh(self) -> bool:
        """Check if gh CLI is installed"""
        try:
            subprocess.run(["gh", "--version"], capture_output=True, check=True)
            return True
        except:
            return False
    
    def status(self) -> str:
        """Show git status"""
        if not self.gh_available:
            return "❌ gh CLI not installed"
        
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        return result.stdout or "No git repository"
    
    def repo_status(self) -> str:
        """Show GitHub repo status"""
        if not self.gh_available:
            return "❌ gh CLI not installed"
        
        result = subprocess.run(["gh", "repo", "view", "--json"], capture_output=True, text=True)
        return result.stdout or "Not in a GitHub repository"
    
    def commit(self, message: str) -> str:
        """Create a git commit"""
        if not self.gh_available:
            return "❌ git not installed"
        
        # Add all files
        subprocess.run(["git", "add", "."], capture_output=True)
        
        # Create commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )
        
        return result.stdout or result.stderr
    
    def push(self) -> str:
        """Push to remote"""
        if not self.gh_available:
            return "❌ git not installed"
        
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        return result.stdout or result.stderr
    
    def pull(self) -> str:
        """Pull from remote"""
        if not self.gh_available:
            return "❌ git not installed"
        
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        return result.stdout or result.stderr
    
    def create_repo(self, name: str, description: str = "") -> str:
        """Create a new GitHub repository"""
        if not self.gh_available:
            return "❌ gh CLI not installed"
        
        args = ["gh", "repo", "create", name]
        if description:
            args.extend(["--description", description])
        args.extend(["--public", "--confirm"])
        
        result = subprocess.run(args, capture_output=True, text=True)
        return result.stdout or result.stderr
    
    def run(self, command: str, **kwargs) -> str:
        """Execute a command"""
        command = command.lower()
        
        if "status" in command:
            return self.status()
        elif "commit" in command:
            message = kwargs.get("message", "Auto commit")
            return self.commit(message)
        elif "push" in command:
            return self.push()
        elif "pull" in command:
            return self.pull()
        elif "create repo" in command:
            name = kwargs.get("name", "new-repo")
            desc = kwargs.get("description", "")
            return self.create_repo(name, desc)
        else:
            return f"Unknown command: {command}"


if __name__ == "__main__":
    skill = GitHubSkill()
    
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        print(f"Running: {cmd}")
    else:
        print("GitHub Skill - Available commands:")
        print("  python github.py status")
        print("  python github.py commit <message>")
        print("  python github.py push")
        print("  python github.py pull")
        print("  python github.py create_repo <name>")
PYEOF

chmod +x ~/.openclaw/skills/github/github.py

echo "✅ Created GitHub skill!"
echo ""
python3 ~/.openclaw/skills/github/github.py
```

---

### System Monitor Skill

```bash
mkdir -p ~/.openclaw/skills/system-monitor
cat > ~/.openclaw/skills/github/skill.json << 'EOF'
{
  "name": "system-monitor",
  "version": "1.0.0", 
  "description": "System monitoring (CPU, memory, disk)",
  "author": "vb"
}
EOF

cat > ~/.openclaw/skills/system-monitor/monitor.py << 'PYEOF'
#!/usr/bin/env python3
"""
System Monitor Skill
Shows CPU, memory, disk usage
"""

import shutil
import psutil
from datetime import datetime

class SystemMonitor:
    """System resource monitoring"""
    
    def cpu(self) -> str:
        """Show CPU usage"""
        return f"🖥️  CPU: {psutil.cpu_percent()}%"
    
    def memory(self) -> str:
        """Show memory usage"""
        mem = psutil.virtual_memory()
        return f"💾  RAM: {mem.percent}% ({mem.used/1024/1024/1024:.1f}GB / {mem.total/1024/1024/1024:.1f}GB)"
    
    def disk(self) -> str:
        """Show disk usage"""
        disk = shutil.disk_usage("/")
        return f"💿  Disk: {disk.used/1024/1024/1024:.1f}GB / {disk.total/1024/1024/1024:.1f}GB"
    
    def all(self) -> str:
        """Show all metrics"""
        return f"\n📊 SYSTEM STATUS - {datetime.now().strftime('%H:%M:%S')}\n\n{self.cpu()}\n{self.memory()}\n{self.disk()}"
    
    def processes(self, limit: int = 5) -> str:
        """Show top processes by CPU"""
        procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                      key=lambda x: x.info['cpu_percent'] or 0, 
                      reverse=True)[:limit]
        
        lines = ["\n🔝 TOP PROCESSES:"]
        for p in procs:
            lines.append(f"  {p.info['pid']} {p.info['name']} {p.info['cpu_percent']}%")
        
        return "\n".join(lines)
    
    def run(self, command: str = "all") -> str:
        """Execute monitoring command"""
        if command == "cpu":
            return self.cpu()
        elif command == "memory":
            return self.memory()
        elif command == "disk":
            return self.disk()
        elif command == "processes":
            return self.processes()
        else:
            return self.all()


if __name__ == "__main__":
    monitor = SystemMonitor()
    print(monitor.run())
PYEOF

chmod +x ~/.openclaw/skills/system-monitor/monitor.py

echo "✅ Created System Monitor skill!"
python3 ~/.openclaw/skills/system-monitor/monitor.py
```

---

## 🎯 RESULT: 11 Skills Total

| # | Skill | Purpose |
|---|-------|---------|
| 1 | Web Researcher | Research + browse |
| 2 | Code Assistant | Write + debug code |
| 3 | Task Automation | Run workflows |
| 4 | Summarizer | Summarize URLs/text |
| 5 | File Manager | Organize + search |
| 6 | Browser Runner | Deterministic automation |
| 7 | Self-Diagnostics | Auto-fix issues |
| 8 | Preference Learner | Memory + learning |
| 9 | Monitoring Dashboard | Real-time stats |
| **10** | **Git & GitHub** | **NEW - Version control** |
| **11** | **System Monitor** | **NEW - CPU/RAM/Disk** |

---

## ⚠️ SHARING: DANGERS & MITIGATION

### Risks of Sharing Skills

| Risk | Severity | Description |
|------|----------|-------------|
| **Credentials Exposed** | 🔴 High | API keys in code |
| **Security Vulnerabilities** | 🔴 High | Code injection points |
| **Malicious Code** | 🔴 High | Backdoors or data theft |
| **Reputation Damage** | 🟡 Medium | Bad code reflects on you |
| **IP Theft** | 🟡 Medium | Others copy without credit |
| **Dependency Issues** | 🟢 Low | Broken by external changes |

---

### What TO Share ✅

```
✅ OpenClaw skills (deterministic browser runner is UNIQUE!)
✅ Documentation
✅ Configuration examples
✅ Architecture patterns
✅ Learning experiences
```

### What NOT TO Share ❌

```
❌ API keys or credentials
❌ Passwords or tokens
❌ Personal data
❌ Unreviewed third-party code
❌ Security-sensitive operations
```

---

### Safe Sharing Checklist

Before publishing any skill:

- [ ] **Remove all credentials** (use env vars)
- [ ] **Code review** (read every line)
- [ ] **VirusTotal scan** (use their API)
- [ ] **Test in isolation** (not on production)
- [ ] **Document limitations** (what it can't do)
- [ ] **Add security notes** (what permissions it needs)
- [ ] **Use standard format** (OpenClaw skill convention)

---

### Our Unique Skills to Share 🎯

| Skill | Why Unique | Sharing Safe? |
|-------|------------|---------------|
| **Deterministic Browser Runner** | No one else has this! | ✅ Yes - pure logic |
| **Autonomy Pipeline** | Complete orchestration | ✅ Yes - architectural |
| **Multi-API Router** | Free + fallback | ✅ Yes - configuration |
| **Self-Diagnostics** | Auto-heal | ✅ Yes - patterns |

---

### Recommendation

**Safe approach:**
1. Share architecture patterns (not credentials)
2. Share deterministic browser runner (no keys needed)
3. Don't share skills with API integrations (unless configurable)
4. Always use environment variables for secrets

**Action:** I'll create a "shareable skills" directory with safe, credential-free skills that demonstrate our unique approach!

---

*Skill Expansion Plan - Created: 2026-02-12*
