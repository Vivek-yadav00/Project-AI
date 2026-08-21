from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.db import crud

router = APIRouter(tags=["call"])

class CallWebhookRequest(BaseModel):
    call_sid: str
    from_number: str
    to_number: str
    status: str
    direction: str

class CallInitiateRequest(BaseModel):
    to_number: str
    message: str | None = None

@router.post("/webhook")
def handle_webhook(request: CallWebhookRequest, db: Session = Depends(get_db)):
    try:
        user = crud.get_or_create_user(db, request.from_number)
        call_log = crud.log_call(
            db, 
            user.id, 
            request.call_sid, 
            request.direction, 
            request.status
        )
        return {"status": "success", "call_log_id": call_log.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/initiate")
def initiate_call(request: CallInitiateRequest, db: Session = Depends(get_db)):
    return {"status": "initiated", "to_number": request.to_number}

@router.get("/status/{call_id}")
def get_call_status(call_id: int, db: Session = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented")
