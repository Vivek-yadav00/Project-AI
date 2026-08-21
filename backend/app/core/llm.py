import logging
from app.config import get_settings
import openai
import google.generativeai as genai

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are DadaAI (also known as VaaniAI), a friendly, patient, and helpful AI assistant for elderly people using feature phones.
Keep your responses concise as they will be delivered via SMS or voice.
Respond in the user's preferred language."""

async def get_ai_response(prompt: str, conversation_history: list[dict], provider: str = None, language: str = "hi") -> str:
    settings = get_settings()
    if provider is None:
        provider = settings.default_llm_provider
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": prompt})

    try:
        if provider == "openai":
            return await _get_openai_response(messages, settings)
        elif provider == "gemini":
            return await _get_gemini_response(messages, settings)
        else:
            logger.warning(f"Unknown provider {provider}, falling back to openai")
            return await _get_openai_response(messages, settings)
    except Exception as e:
        logger.error(f"Error with provider {provider}: {e}")
        fallback = "gemini" if provider == "openai" else "openai"
        logger.info(f"Falling back to {fallback}")
        try:
            if fallback == "openai":
                return await _get_openai_response(messages, settings)
            else:
                return await _get_gemini_response(messages, settings)
        except Exception as fallback_error:
            logger.error(f"Fallback error: {fallback_error}")
            return "I am sorry, I am having trouble understanding right now. Please try again later."

async def _get_openai_response(messages: list[dict], settings) -> str:
    client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=150
    )
    return response.choices[0].message.content

async def _get_gemini_response(messages: list[dict], settings) -> str:
    genai.configure(api_key=settings.google_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Convert format
    gemini_messages = []
    for msg in messages:
        role = "model" if msg["role"] in ["assistant", "system"] else "user"
        gemini_messages.append({"role": role, "parts": [msg["content"]]})
        
    response = await model.generate_content_async(gemini_messages)
    return response.text
