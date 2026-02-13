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

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [MODEL-FALLBACK] $1"
}

test_model() {
    local model=$1
    local provider=$2
    
    case $provider in
        "ollama")
            curl -s --max-time 5 "$OLLAMA_URL/api/tags" 2>/dev/null | grep -q "$model"
            return $?
            ;;
        "minimax")
            # MiniMax API test (requires valid API key)
            curl -s --max-time 5 -o /dev/null -w "%{http_code}" "$MINIMAX_API" 2>/dev/null | grep -q "200\|400\|401"
            return $?
            ;;
    esac
}

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

# Run if called directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    get_available_model
fi
