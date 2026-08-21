from sqlalchemy.orm import Session
from app.db import models
from datetime import datetime

def create_user(db: Session, phone_number: str, name: str = None, language: str = "hi") -> models.User:
    db_user = models.User(phone_number=phone_number, name=name, language_preference=language)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_phone(db: Session, phone_number: str) -> models.User | None:
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def get_or_create_user(db: Session, phone_number: str) -> models.User:
    user = get_user_by_phone(db, phone_number)
    if user:
        return user
    return create_user(db, phone_number=phone_number)

def create_conversation(db: Session, user_id: int, channel: models.ChannelType) -> models.Conversation:
    db_conversation = models.Conversation(user_id=user_id, channel=channel)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_active_conversation(db: Session, user_id: int, channel: models.ChannelType) -> models.Conversation | None:
    return db.query(models.Conversation).filter(
        models.Conversation.user_id == user_id,
        models.Conversation.channel == channel,
        models.Conversation.ended_at == None
    ).order_by(models.Conversation.started_at.desc()).first()

def get_conversation_history(db: Session, conversation_id: int, limit: int = 10) -> list[models.Message]:
    return db.query(models.Message).filter(
        models.Message.conversation_id == conversation_id
    ).order_by(models.Message.timestamp.desc()).limit(limit).all()

def add_message(db: Session, conversation_id: int, role: models.MessageRole, content: str, audio_url: str = None) -> models.Message:
    db_message = models.Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        audio_url=audio_url
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def log_call(db: Session, user_id: int, call_sid: str, direction: models.CallDirection, status: models.CallStatus) -> models.CallLog:
    db_call_log = models.CallLog(
        user_id=user_id,
        call_sid=call_sid,
        direction=direction,
        status=status
    )
    db.add(db_call_log)
    db.commit()
    db.refresh(db_call_log)
    return db_call_log

def update_call_status(db: Session, call_id: int, status: models.CallStatus, duration: int = None) -> models.CallLog | None:
    call_log = db.query(models.CallLog).filter(models.CallLog.id == call_id).first()
    if not call_log:
        return None
    
    call_log.status = status
    if duration is not None:
        call_log.duration = duration
    
    if status in [models.CallStatus.COMPLETED, models.CallStatus.FAILED]:
        call_log.ended_at = datetime.utcnow()
        
    db.commit()
    db.refresh(call_log)
    return call_log
