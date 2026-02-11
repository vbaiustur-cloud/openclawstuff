#!/bin/bash
# Run OpenClaw Dashboard

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if gateway is running
if ! curl -s http://127.0.0.1:18789/status &>/dev/null; then
    echo "⚠️  OpenClaw gateway doesn't seem to be running."
    echo "Start it with: openclaw gateway start"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run dashboard
cd "$SCRIPT_DIR"
python3 dashboard.py
