from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.db.session import get_db
from app.db import crud

router = APIRouter(tags=["users"])

class UserRegisterRequest(BaseModel):
    phone_number: str
    name: str | None = None
    language_preference: str = "hi"

class UserResponse(BaseModel):
    id: int
    phone_number: str
    name: str | None
    language_preference: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserPreferencesUpdate(BaseModel):
    name: str | None = None
    language_preference: str | None = None

@router.post("/register", response_model=UserResponse)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_phone(db, request.phone_number)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this phone number already exists")
        
    user = crud.create_user(
        db, 
        request.phone_number, 
        request.name, 
        request.language_preference
    )
    return user

@router.get("/{phone_number}", response_model=UserResponse)
def get_user_profile(phone_number: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_phone(db, phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{phone_number}/preferences", response_model=UserResponse)
def update_user_preferences(phone_number: str, request: UserPreferencesUpdate, db: Session = Depends(get_db)):
    user = crud.get_user_by_phone(db, phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if request.name is not None:
        user.name = request.name
    if request.language_preference is not None:
        user.language_preference = request.language_preference
        
    db.commit()
    db.refresh(user)
    return user
