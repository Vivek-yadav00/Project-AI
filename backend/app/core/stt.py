import logging
import tempfile
import os
from app.config import get_settings
import google.generativeai as genai

logger = logging.getLogger(__name__)

async def speech_to_text(audio_data: bytes, language: str = "hi", provider: str = None) -> str:
    """Transcribe audio to text using Google Gemini."""
    settings = get_settings()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(audio_data)
        temp_path = temp_file.name
        
    try:
        genai.configure(api_key=settings.google_api_key)
        model = genai.GenerativeModel('gemini-3.5-flash')
        
        # Upload audio file to Gemini
        audio_file = genai.upload_file(temp_path)
        
        response = await model.generate_content_async([
            f"Transcribe this audio to text. The audio is in {language} language. Return only the transcribed text, nothing else.",
            audio_file
        ])
        
        return response.text.strip()
    except Exception as e:
        logger.error(f"STT error: {e}")
        return ""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
