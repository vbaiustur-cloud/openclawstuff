#!/bin/bash
# OpenClaw Dashboard - Install Script
# Run this to set up the dashboard

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Setting up OpenClaw Dashboard..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install --user rich requests --break-system-packages 2>/dev/null || \
    pip install rich requests --break-system-packages

# Make scripts executable
chmod +x dashboard.py
chmod +x run-dashboard.sh

# Install desktop launcher (to user home)
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"
cp openclaw-dashboard.desktop "$DESKTOP_DIR/"
echo "✅ Desktop launcher installed to $DESKTOP_DIR/openclaw-dashboard.desktop"

# Refresh desktop database if available
if command -v desktop-file-install &> /dev/null; then
    desktop-file-install "$DESKTOP_DIR/openclaw-dashboard.desktop" 2>/dev/null || true
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the dashboard:"
echo "  1. ./run-dashboard.sh"
echo "  2. Or find 'OpenClaw Dashboard' in your app launcher"
echo ""
echo "Tip: Make sure OpenClaw gateway is running first:"
echo "  openclaw gateway status"
