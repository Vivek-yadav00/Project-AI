import logging
import tempfile
import os
from app.config import get_settings
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

async def speech_to_text(audio_data: bytes, language: str = "hi", provider: str = None) -> str:
    """Transcribe audio to text using Google Gemini."""
    settings = get_settings()
    
    try:
        client = genai.Client(api_key=settings.google_api_key)
        
        response = await client.aio.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=[
                types.Part.from_text(text=f"Transcribe this audio to text. The audio is in {language} language. Return ONLY the transcribed text, nothing else. If you cannot hear anything, return empty."),
                types.Part.from_bytes(data=audio_data, mime_type='audio/webm')
            ]
        )
        
        return response.text.strip()
    except Exception as e:
        logger.error(f"STT error: {e}")
        return ""
