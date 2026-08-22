import logging
from app.config import get_settings
import google.generativeai as genai

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are DadaAI (also known as VaaniAI), a friendly, patient, and helpful AI assistant for elderly people using feature phones.
Keep your responses concise as they will be delivered via SMS or voice.
Respond in the user's preferred language."""

async def get_ai_response(prompt: str, conversation_history: list[dict], provider: str = None, language: str = "hi", context: str = None) -> str:
    """Get AI response using Google Gemini."""
    settings = get_settings()
    
    system_prompt_text = SYSTEM_PROMPT
    if context:
        system_prompt_text += f"\n\n{context}"
        
    messages = [{"role": "system", "content": system_prompt_text}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": prompt})

    try:
        return await _get_gemini_response(messages, settings)
    except Exception as e:
        logger.error(f"Error with Gemini: {e}")
        return "I am sorry, I am having trouble understanding right now. Please try again later."

async def _get_gemini_response(messages: list[dict], settings) -> str:
    """Generate response using Google Gemini API."""
    genai.configure(api_key=settings.google_api_key)
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    # Convert message format for Gemini
    gemini_messages = []
    for msg in messages:
        role = "model" if msg["role"] in ["assistant", "system"] else "user"
        gemini_messages.append({"role": role, "parts": [msg["content"]]})
        
    response = await model.generate_content_async(gemini_messages)
    return response.text
