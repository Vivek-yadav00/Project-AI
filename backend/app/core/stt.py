import logging
from app.config import get_settings
import openai
import tempfile
import os

logger = logging.getLogger(__name__)

async def speech_to_text(audio_data: bytes, language: str = "hi", provider: str = None) -> str:
    settings = get_settings()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(audio_data)
        temp_path = temp_file.name
        
    try:
        client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        
        with open(temp_path, "rb") as audio_file:
            response = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language
            )
            return response.text
    except Exception as e:
        logger.error(f"STT error: {e}")
        return ""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
