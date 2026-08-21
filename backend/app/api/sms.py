from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.db import crud
from app.services import ai_pipeline

router = APIRouter(tags=["sms"])

class IncomingSMSRequest(BaseModel):
    from_number: str
    body: str

class SMSResponse(BaseModel):
    to: str
    body: str
    conversation_id: int | None = None

class SendSMSRequest(BaseModel):
    to_number: str
    body: str

@router.post("/incoming", response_model=SMSResponse)
async def incoming_sms(request: IncomingSMSRequest, db: Session = Depends(get_db)):
    try:
        response_text = await ai_pipeline.process_sms(request.from_number, request.body, db)
        
        user = crud.get_user_by_phone(db, request.from_number)
        conv = None
        if user:
            conv = crud.get_active_conversation(db, user.id, "sms")
            
        return SMSResponse(
            to=request.from_number,
            body=response_text,
            conversation_id=conv.id if conv else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send")
async def send_sms(request: SendSMSRequest, db: Session = Depends(get_db)):
    return {"status": "accepted", "to": request.to_number}

@router.get("/history/{phone_number}")
def get_sms_history(phone_number: str, limit: int = 50, db: Session = Depends(get_db)):
    user = crud.get_user_by_phone(db, phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    conv = crud.get_active_conversation(db, user.id, "sms")
    if not conv:
        return {"messages": []}
        
    messages = crud.get_conversation_history(db, conv.id, limit)
    return {"messages": [{"role": m.role, "content": m.content, "timestamp": m.timestamp} for m in messages]}
