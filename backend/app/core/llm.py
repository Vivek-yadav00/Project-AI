import logging
from app.config import get_settings
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are DadaAI (also known as VaaniAI), a friendly, patient, and helpful AI assistant for elderly people using feature phones.

CRITICAL INSTRUCTIONS FOR MESSAGES:
When you receive an SMS from the caregiver (like Vivek), it might be in English. You must act as Dada Ji's personal reader:
1. Start by announcing the message (e.g., "Dada ji, Vivek ka ek message aaya hai...").
2. Translate the English message into simple, conversational Hindi.
3. Briefly explain what the message is about so an elderly person can easily understand.
4. Ask Dada Ji if he has any questions about it or if he wants you to send a reply.

If Dada Ji is speaking to you (Voice AI) to ask a question, answer his query politely and patiently based on the recent SMS context.

Keep your responses concise as they will be spoken out loud via AI voice."""

async def get_ai_response(prompt: str, conversation_history: list[dict], provider: str = None, language: str = "hi", context: str = None) -> str:
    """Get AI response using Google Gemini."""
    settings = get_settings()
    
    system_prompt_text = SYSTEM_PROMPT
    if context:
        system_prompt_text += f"\n\n{context}"
        
    messages = []
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": prompt})

    try:
        return await _get_gemini_response(messages, system_prompt_text, settings)
    except Exception as e:
        logger.error(f"Error with Gemini: {e}")
        return "I am sorry, I am having trouble understanding right now. Please try again later."

async def _get_gemini_response(messages: list[dict], system_prompt_text: str, settings) -> str:
    """Generate response using Google Gemini API."""
    client = genai.Client(api_key=settings.google_api_key)
    
    # Convert message format for Gemini
    gemini_contents = []
    for msg in messages:
        role = "model" if msg["role"] in ["assistant", "system"] else "user"
        gemini_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
        )
        
    response = await client.aio.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=gemini_contents,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt_text,
        )
    )
    return response.text
