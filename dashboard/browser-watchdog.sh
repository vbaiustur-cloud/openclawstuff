#!/bin/bash
# Browser auto-restart watchdog
# Run as: ./browser-watchdog.sh &

CDP_PORT=9222
MAX_RESTARTS=5
RESTART_WINDOW=300  # 5 minutes
RESTART_COUNT=0
LAST_RESTART=0

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WATCHDOG] $1"
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
