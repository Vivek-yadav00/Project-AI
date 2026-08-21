from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = ""
    google_api_key: str = ""
    elevenlabs_api_key: str = ""
    database_url: str = "sqlite:///./dadaai.db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-me-in-production"
    allowed_origins: str = "*"
    debug: bool = True
    default_llm_provider: str = "gemini"  # "openai" or "gemini"
    default_tts_provider: str = "elevenlabs"
    default_language: str = "hi"  # Hindi default

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()
