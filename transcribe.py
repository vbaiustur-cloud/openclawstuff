#!/usr/bin/env python3
"""Transcribe audio using faster-whisper."""

import sys
from faster_whisper import WhisperModel

def transcribe(audio_path: str, model_size: str = "base"):
    """Transcribe audio file."""
    model = WhisperModel(model_size, compute_type="int8")
    segments, info = model.transcribe(audio_path, language="en")
    
    print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")
    print("\nTranscription:")
    
    for segment in segments:
        print(segment.text.strip())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe.py <audio_file> [model_size]")
        sys.exit(1)
    
    audio = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    transcribe(audio, model)
