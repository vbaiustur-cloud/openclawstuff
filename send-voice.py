#!/usr/bin/env python3
"""
Telegram Voice Message Sender
Send text as voice to Telegram using OpenClaw
"""

import sys
import subprocess
import os
from pathlib import Path

# Try to import pyttsx3, fall back to espeak-ng
USE_PYTTSX3 = False

try:
    import pyttsx3
    USE_PYTTSX3 = True
except ImportError:
    pass

TARGET_CHAT = "6703664422"  # Default: vb


def speak_pyttsx3(text: str, output_path: str):
    """Use pyttsx3 for TTS."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.save_to_file(text, output_path)
    engine.runAndWait()


def speak_espeak(text: str, output_path: str):
    """Use espeak-ng for TTS."""
    subprocess.run([
        'espeak-ng', '-w', output_path, '-v', 'en', text
    ], check=True)


def send_voice(audio_path: str, target: str):
    """Send audio file via OpenClaw."""
    cmd = [
        'openclaw', 'message', 'send',
        '--channel', 'telegram',
        '--target', target,
        '--media', audio_path,
        '--message', '🎤 Voice message'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: ./send-voice.py \"Text to speak\" [chat_id]")
        sys.exit(1)
    
    text = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else TARGET_CHAT
    
    audio_file = f"/tmp/voice_{os.getpid()}.wav"
    
    try:
        print(f"🔊 Generating speech...")
        if USE_PYTTSX3:
            speak_pyttsx3(text, audio_file)
        else:
            speak_espeak(text, audio_file)
        
        if not os.path.exists(audio_file):
            print("❌ Failed to generate audio")
            sys.exit(1)
        
        print(f"📤 Sending to Telegram...")
        if send_voice(audio_file, target):
            print("✅ Voice message sent!")
        else:
            print("❌ Failed to send message")
    
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)


if __name__ == "__main__":
    main()
