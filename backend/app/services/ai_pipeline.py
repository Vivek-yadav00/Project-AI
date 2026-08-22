from sqlalchemy.orm import Session
from app.db import crud
from app.core.llm import get_ai_response
from app.core.tts import text_to_speech
from app.core.stt import speech_to_text
from app.db.models import ChannelType, MessageRole

async def process_sms(phone_number: str, text: str, db: Session) -> str:
    # Get or create user
    user = crud.get_or_create_user(db, phone_number=phone_number)
    
    # Get or create active conversation
    conversation = crud.get_active_conversation(db, user_id=user.id, channel=ChannelType.SMS)
    if not conversation:
        conversation = crud.create_conversation(db, user_id=user.id, channel=ChannelType.SMS)
        
    # Get conversation history BEFORE adding the new message
    history_messages = crud.get_conversation_history(db, conversation_id=conversation.id, limit=10)
    history_messages.reverse() # Fix chronological order
    history = [{"role": msg.role, "content": msg.content} for msg in history_messages if msg.role != MessageRole.SYSTEM]
    
    # Add user message
    crud.add_message(db, conversation_id=conversation.id, role=MessageRole.USER, content=text, audio_url=None)
    
    # Get LLM response
    response_text = await get_ai_response(
        prompt=text,
        conversation_history=history,
        language=user.language_preference
    )
    
    # Add assistant message
    crud.add_message(db, conversation_id=conversation.id, role=MessageRole.ASSISTANT, content=response_text, audio_url=None)
    
    return response_text

async def process_voice(phone_number: str, audio_data: bytes, language: str, db: Session) -> bytes:
    # 1. Speech to Text
    transcribed_text = await speech_to_text(audio_data=audio_data, language=language)
    if not transcribed_text:
        return b"" # Handle gracefully
        
    # 2. Process as SMS (LLM interaction)
    user = crud.get_or_create_user(db, phone_number=phone_number)
    
    # Get recent SMS context so Voice AI knows what messages arrived
    sms_conv = crud.get_active_conversation(db, user_id=user.id, channel=ChannelType.SMS)
    sms_context = ""
    if sms_conv:
        recent_sms = crud.get_conversation_history(db, conversation_id=sms_conv.id, limit=3)
        if recent_sms:
            sms_context = "Recent SMS interaction:\n"
            for msg in reversed(recent_sms):
                sms_context += f"- {msg.role}: {msg.content}\n"
                
    conversation = crud.get_active_conversation(db, user_id=user.id, channel=ChannelType.VOICE)
    if not conversation:
        conversation = crud.create_conversation(db, user_id=user.id, channel=ChannelType.VOICE)
        
    # Get conversation history BEFORE adding the new message
    history_messages = crud.get_conversation_history(db, conversation_id=conversation.id, limit=10)
    history_messages.reverse() # Fix chronological order
    history = [{"role": msg.role, "content": msg.content} for msg in history_messages if msg.role != MessageRole.SYSTEM]
    
    crud.add_message(db, conversation_id=conversation.id, role=MessageRole.USER, content=transcribed_text, audio_url=None)
    
    response_text = await get_ai_response(
        prompt=transcribed_text,
        conversation_history=history,
        language=language,
        context=sms_context
    )
    
    crud.add_message(db, conversation_id=conversation.id, role=MessageRole.ASSISTANT, content=response_text, audio_url=None)
    
    # 3. Text to Speech
    audio_bytes = await text_to_speech(text=response_text, language=language)
    
    return audio_bytes
