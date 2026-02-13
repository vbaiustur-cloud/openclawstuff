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
