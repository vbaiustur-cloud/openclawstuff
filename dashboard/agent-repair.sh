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
    ping -c 3 8.8.8.8 2>/dev/null
    curl -s --max-time 5 https://api.minimax.chat > /dev/null 2>&1 && echo "MiniMax API: OK" || echo "MiniMax API: FAIL"
    curl -s --max-time 5 http://localhost:11434 > /dev/null 2>&1 && echo "Ollama: OK" || echo "Ollama: FAIL"
}

test_browser() {
    log "Testing browser CDP..."
    curl -s http://localhost:9222/json/version > /dev/null 2>&1 && echo "Browser CDP: OK" || echo "Browser CDP: FAIL"
}

fix_permissions() {
    log "Fixing permissions..."
    chmod +x "$HOME/.openclaw/workspace/dashboard/"*.sh 2>/dev/null
    chmod +x "$HOME/.openclaw/workspace/dashboard/"*.py 2>/dev/null
}

restart_ollama() {
    log "Restarting Ollama..."
    pkill -f ollama 2>/dev/null
    sleep 2
    ollama serve > /dev/null 2>&1 &
    sleep 5
}

restart_browser() {
    log "Restarting browser..."
    pkill -f "chrome.*remote-debugging" 2>/dev/null
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
