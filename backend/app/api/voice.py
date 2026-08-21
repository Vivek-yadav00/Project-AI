from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import io

from app.db.session import get_db
from app.core import stt, tts
from app.services import ai_pipeline

router = APIRouter(tags=["voice"])

class TTSRequest(BaseModel):
    text: str
    language: str = "hi"
    voice_id: str | None = None

@router.post("/stt")
async def process_stt(audio: UploadFile = File(...), language: str = Form("hi")):
    try:
        audio_data = await audio.read()
        text = await stt.speech_to_text(audio_data, language=language)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts")
async def process_tts(request: TTSRequest):
    try:
        audio_bytes = await tts.text_to_speech(
            request.text, 
            language=request.language, 
            voice_id=request.voice_id
        )
        return StreamingResponse(
            io.BytesIO(audio_bytes), 
            media_type="audio/mpeg"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process")
async def process_voice_interaction(
    phone_number: str = Form(...),
    audio: UploadFile = File(...),
    language: str = Form("hi"),
    db: Session = Depends(get_db)
):
    try:
        audio_data = await audio.read()
        response_audio = await ai_pipeline.process_voice(phone_number, audio_data, language, db)
        
        return StreamingResponse(
            io.BytesIO(response_audio), 
            media_type="audio/mpeg"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
