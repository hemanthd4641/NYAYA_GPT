# tools/voice_handler.py

import os
import io
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(audio_bytes):
    """
    Transcribes audio bytes using Groq's Whisper-large-v3 model.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not found in environment."

    try:
        client = Groq(api_key=api_key)
        
        # Groq's API expects a file-like object with a name
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav" # Placeholder name for the API

        transcription = client.audio.transcriptions.create(
            file=("audio.wav", audio_file.read()),
            model="whisper-large-v3",
            response_format="json",
        )
        
        return transcription.text
    except Exception as e:
        return f"Error during transcription: {str(e)}"
