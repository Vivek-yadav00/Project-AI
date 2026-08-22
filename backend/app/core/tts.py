import logging
from app.config import get_settings
from elevenlabs.client import AsyncElevenLabs
import base64
import json
import urllib.request
import asyncio

logger = logging.getLogger(__name__)

async def text_to_speech(text: str, language: str = "hi", voice_id: str = None, provider: str = None) -> bytes:
    settings = get_settings()
    if provider is None:
        provider = settings.default_tts_provider
        
    try:
        if provider == "elevenlabs":
            return await _elevenlabs_tts(text, voice_id, settings)
        else:
            return await _google_tts(text, language, settings)
    except Exception as e:
        logger.error(f"TTS error with provider {provider}: {e}")
        fallback = "google" if provider == "elevenlabs" else "elevenlabs"
        logger.info(f"Falling back to {fallback}")
        try:
            if fallback == "elevenlabs":
                return await _elevenlabs_tts(text, voice_id, settings)
            else:
                return await _google_tts(text, language, settings)
        except Exception as fallback_error:
            logger.error(f"Fallback TTS error: {fallback_error}")
            return b""

async def _elevenlabs_tts(text: str, voice_id: str, settings) -> bytes:
    client = AsyncElevenLabs(api_key=settings.elevenlabs_api_key)
    vid = voice_id or "JBFqnCBsd6RMkjVDRZzb"  # Default voice
    
    audio_stream = client.text_to_speech.convert(
        voice_id=vid,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    audio_bytes = b""
    async for chunk in audio_stream:
        if chunk:
            audio_bytes += chunk
    return audio_bytes

async def _google_tts(text: str, language: str, settings) -> bytes:
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={settings.google_api_key}"
    
    data = {
        "input": {"text": text},
        "voice": {"languageCode": language, "name": f"{language}-IN-Standard-A"},
        "audioConfig": {"audioEncoding": "MP3"}
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    loop = asyncio.get_event_loop()
    
    def _make_request():
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return base64.b64decode(result['audioContent'])
            
    return await loop.run_in_executor(None, _make_request)
