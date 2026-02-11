#!/bin/bash
# Telegram Voice Message Sender
# Usage: ./send-voice.sh "Text to speak" [target_chat_id]

TEXT="$1"
TARGET="${2:-6703664422}"  # Default to vb's chat ID

if [ -z "$TEXT" ]; then
    echo "Usage: ./send-voice.sh \"Text to speak\" [chat_id]"
    exit 1
fi

# Create temp file
AUDIO_FILE="/tmp/voice_$(date +%s).wav"

# Generate speech using espeak-ng
echo "$TEXT" | espeak-ng -w "$AUDIO_FILE" -v en --stdin 2>/dev/null

if [ -f "$AUDIO_FILE" ]; then
    # Convert to OGG (Telegram prefers OGG for voice)
    OGG_FILE="${AUDIO_FILE%.wav}.ogg"
    if command -v ffmpeg &>/dev/null; then
        ffmpeg -y -i "$AUDIO_FILE" -acodec libopus -ab 128k "$OGG_FILE" 2>/dev/null
        rm "$AUDIO_FILE"
        AUDIO_FILE="$OGG_FILE"
    fi
    
    # Send via OpenClaw
    openclaw message send --channel telegram --target "$TARGET" --media "$AUDIO_FILE" --message "🎤 Voice message"
    
    echo "✅ Voice sent!"
    rm -f "$AUDIO_FILE"
else
    echo "❌ Failed to generate speech"
    exit 1
fi
