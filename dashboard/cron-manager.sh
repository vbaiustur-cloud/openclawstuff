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
