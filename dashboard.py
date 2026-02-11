#!/usr/bin/env python3
"""
OpenClaw Dashboard - Live status + Agent terminal (Rich TUI)
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import requests
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich import box

console = Console()

# Gateway config - use environment variable
GATEWAY_URL = os.environ.get("OPENCLAW_GATEWAY_URL", "http://127.0.0.1:18789")
GATEWAY_TOKEN = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")

# To-Do storage
TODO_FILE = Path.home() / ".openclaw" / "dashboard-todos.json"


def load_todos():
    if TODO_FILE.exists():
        try:
            return json.loads(TODO_FILE.read_text())
        except:
            return []
    return []


def save_todos(todos):
    TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    TODO_FILE.write_text(json.dumps(todos, indent=2))


class GatewayClient:
    def _headers(self):
        token = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")
        if token:
            return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        return {"Content-Type": "application/json"}
    
    def get_status(self):
        try:
            r = requests.get(f"{GATEWAY_URL}/status", headers=self._headers(), timeout=2)
            return r.json() if r.status_code == 200 else {}
        except:
            return {}

    def get_agents(self):
        try:
            r = requests.get(f"{GATEWAY_URL}/agents/list", headers=self._headers(), timeout=2)
            return r.json().get("agents", []) if r.status_code == 200 else []
        except:
            return []

    def get_crons(self):
        try:
            r = requests.get(f"{GATEWAY_URL}/cron/list", headers=self._headers(), timeout=2)
            return r.json().get("jobs", []) if r.status_code == 200 else []
        except:
            return []

    def send_message(self, session_key: str, message: str):
        try:
            r = requests.post(
                f"{GATEWAY_URL}/sessions/{session_key}/send",
                headers=self._headers(),
                json={"message": message},
                timeout=5
            )
            return r.json()
        except Exception as e:
            return {"error": str(e)}


def create_status_panel(gateway):
    status = gateway.get_status()
    text = Text()
    text.append("🦞 OPENCLAW STATUS\n\n", style="bold green")

    if status:
        text.append(f"Version: {status.get('version', 'unknown')}\n", style="cyan")
        text.append(f"Runtime: {status.get('runtime', 'direct')}\n", style="cyan")
        text.append(f"Model: {status.get('model', 'unknown')}\n", style="cyan")
        text.append(f"Context: {status.get('context', 'N/A')}\n", style="magenta")
        text.append(f"Queue: {status.get('queue', {}).get('depth', 0)} pending\n", style="magenta")
    else:
        text.append("Gateway: ❌ unreachable\n", style="red")
        text.append("Run: openclaw gateway start", style="dim")

    return Panel(text, title="📊 System", box=box.ROUNDED, style="on dark_blue")


def create_agents_panel(gateway):
    agents = gateway.get_agents()
    table = Table(title="🤖 Agents", box=box.ROUNDED)
    table.add_column("ID", style="cyan", width=22)
    table.add_column("Model", style="green", width=32)

    for agent in agents:
        table.add_row(
            agent.get("id", "?"),
            agent.get("model", "?")
        )

    if not agents:
        table.add_row("No agents", "-")

    return Panel(table, title="Agents", box=box.ROUNDED, style="on dark_green")


def create_todos_panel():
    todos = load_todos()
    table = Table(title="📋 To-Do", box=box.ROUNDED)
    table.add_column("Done", style="green", width=6)
    table.add_column("Task", style="white")

    for todo in todos[:15]:
        status = "✅" if todo.get("done") else "⬜"
        task = todo.get("task", "?")
        style = "dim" if todo.get("done") else "white"
        table.add_row(status, task, style=style)

    if not todos:
        table.add_row("-", "No tasks. Use /todo add <task>")

    return Panel(table, title="Tasks", box=box.ROUNDED, style="on dark_cyan")


def create_crons_panel(gateway):
    crons = gateway.get_crons()
    table = Table(title="⏰ Cron Jobs", box=box.ROUNDED)
    table.add_column("Name", style="cyan", width=30)
    table.add_column("Schedule", style="magenta", width=12)
    table.add_column("Status", style="green", width=8)

    for cron in crons:
        name = cron.get("name", "?")[:28]
        sched = cron.get("schedule", {})
        if isinstance(sched, dict):
            mins = sched.get("everyMs", 0) // 60000
            schedule_str = f"{mins}m" if mins else "?"
        else:
            schedule_str = "?"
        enabled = "✅" if cron.get("enabled") else "❌"
        table.add_row(name, schedule_str, enabled)

    if not crons:
        table.add_row("-", "-", "-")

    return Panel(table, title="Crons", box=box.ROUNDED, style="on dark_orange")


def create_terminal_panel(messages, current_agent):
    text = Text()
    text.append(f"💬 TERMINAL — @{current_agent}\n\n", style="bold yellow")

    # Recent messages
    for msg in messages[-12:]:
        time = msg.get("time", "")
        source = msg.get("source", "")
        content = msg.get("text", "")

        if source == "user":
            text.append(f"[{time}] ", style="dim")
            text.append("You: ", style="bold red")
            text.append(f"{content}\n", style="white")
        elif source == "system":
            text.append(f"[{time}] ", style="dim")
            text.append(f"• {content}\n", style="dim white")
        else:
            text.append(f"[{time}] ", style="dim")
            text.append(f"Bot: {content}\n", style="white")

    text.append("\n" + "─" * 50 + "\n", style="dim")
    text.append("Type message or command (/help): ", style="bold yellow")

    return Panel(
        text,
        title="🖥️ Terminal",
        box=box.ROUNDED,
        style="on black",
        height=16
    )


def create_help_panel():
    text = Text()
    text.append("📖 COMMANDS\n\n", style="bold yellow")
    text.append("/agents      List all agents\n", style="cyan")
    text.append("/use <id>    Switch to agent\n", style="cyan")
    text.append("/todo add    Add task\n", style="cyan")
    text.append("/todo done   Mark task done\n", style="cyan")
    text.append("/status      Show status\n", style="cyan")
    text.append("/crons       Show crons\n", style="cyan")
    text.append("/voice <txt> Send voice msg\n", style="cyan")
    text.append("/clear       Clear history\n", style="cyan")
    text.append("/quit        Exit\n", style="cyan")
    return Panel(text, title="Help", box=box.ROUNDED, style="on dark_blue")


def main():
    gateway = GatewayClient()
    messages = []
    current_agent = "main"
    session_key = "agent:main:main"
    running = True

    console.clear()
    print("🚀 Starting OpenClaw Dashboard...")

    def get_layout():
        layout = Layout()
        layout.split_column(
            Layout(Panel(
                Text("🦞 OPENCLAW DASHBOARD", style="bold white on black", justify="center"),
                style="on black",
                box=box.HEAVY
            ), size=3),
            Layout(name="main")
        )
        layout["main"].split_row(
            Layout(create_status_panel(gateway), size=28),
            Layout(create_agents_panel(gateway), size=32),
            Layout(create_todos_panel(), size=28),
            Layout(create_terminal_panel(messages, current_agent))
        )
        return layout

    def log(msg, source="system"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        messages.append({"time": timestamp, "source": source, "text": msg})
        if len(messages) > 100:
            messages.pop(0)

    def process_input(inp):
        nonlocal current_agent, session_key
        inp = inp.strip()
        if not inp:
            return

        log(inp[:60], "user")

        if inp.startswith("/"):
            cmd = inp.lower().split()[0]
            args = inp.split()[1:]

            if cmd == "/help":
                log("Commands: /agents, /use <id>, /todo, /status, /crons, /voice <txt>, /clear, /quit")
            elif cmd == "/agents":
                agents = gateway.get_agents()
                for a in agents:
                    log(f"  - {a.get('id')} ({a.get('model')})")
            elif cmd == "/use" and args:
                agent_id = args[0]
                agents = gateway.get_agents()
                for a in agents:
                    if a.get("id") == agent_id:
                        current_agent = agent_id
                        session_key = f"agent:{agent_id}:{agent_id}"
                        log(f"Switched to {agent_id}")
                        return
                log(f"Agent '{agent_id}' not found")
            elif cmd == "/status":
                status = gateway.get_status()
                log(f"Version: {status.get('version', '?')}")
                log(f"Model: {status.get('model', '?')}")
            elif cmd == "/crons":
                crons = gateway.get_crons()
                for c in crons:
                    log(f"  - {c.get('name', '?')}")
            elif cmd == "/clear":
                messages.clear()
                log("History cleared")
            elif cmd == "/quit":
                running = False
                console.clear()
                print("👋 Goodbye!")
                sys.exit(0)
            elif cmd == "/todo":
                if args:
                    sub = args[0]
                    if sub == "add" and len(args) > 1:
                        task = " ".join(args[1:])
                        todos = load_todos()
                        todos.append({"task": task, "done": False, "added": datetime.now().strftime("%Y-%m-%d")})
                        save_todos(todos)
                        log(f"Added: {task}")
                    elif sub == "done" and len(args) > 1:
                        try:
                            idx = int(args[1]) - 1
                            todos = load_todos()
                            if 0 <= idx < len(todos):
                                todos[idx]["done"] = True
                                save_todos(todos)
                                log(f"Done: {todos[idx]['task'][:50]}")
                            else:
                                log(f"Invalid task #{args[1]}")
                        except ValueError:
                            log("Invalid task number")
                    else:
                        log("Usage: /todo add <task> | done <num>")
                else:
                    log("Usage: /todo add <task> | done <num>")
            elif cmd == "/voice":
                if len(args) > 0:
                    voice_text = " ".join(args)
                    import subprocess
                    audio_file = f"/tmp/voice_dash_{os.getpid()}.wav"
                    try:
                        subprocess.run(['espeak-ng', '-w', audio_file, '-v', 'en', voice_text], check=True, capture_output=True)
                        if os.path.exists(audio_file):
                            subprocess.run(['openclaw', 'message', 'send', '--channel', 'telegram', '--target', '6703664422', '--media', audio_file, '--message', '🎤 Voice'], capture_output=True)
                            os.remove(audio_file)
                            log("Voice message sent!")
                        else:
                            log("Failed to generate audio")
                    except Exception as e:
                        log(f"Voice error: {str(e)}")
                else:
                    log("Usage: /voice <text to speak>")
            else:
                log(f"Unknown command: {cmd}")
        else:
            result = gateway.send_message(session_key, inp)
            if "error" in result:
                log(f"Error: {result['error']}")
            else:
                log(f"→ Sent to {current_agent}")

    try:
        with Live(get_layout(), refresh_per_second=2, transient=True) as live:
            while running:
                live.update(get_layout())
                try:
                    inp = input()
                    if inp:
                        process_input(inp)
                except (EOFError, KeyboardInterrupt):
                    running = False
                    console.clear()
                    print("👋 Dashboard closed.")
                    break
    except Exception as e:
        console.clear()
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
