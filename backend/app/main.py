from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.db.session import init_db
from app.api import health, sms, voice, call, users

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database
    init_db()
    yield

app = FastAPI(
    title="DadaAI API",
    description="AI-powered voice assistant backend for feature phones",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(sms.router, prefix="/api/v1/sms")
app.include_router(voice.router, prefix="/api/v1/voice")
app.include_router(call.router, prefix="/api/v1/call")
app.include_router(users.router, prefix="/api/v1/users")

@app.get("/")
async def root():
    return {"message": "Welcome to DadaAI API"}
