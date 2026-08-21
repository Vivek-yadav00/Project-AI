# DadaAI / VaaniAI

AI-powered voice assistant for feature phones.

## Team
- **Susanta**: Backend
- **Vivek**: SMS Gateway & ESP32 Hardware

## Tech Stack
- **Backend Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **LLM Integration**: OpenAI / Gemini
- **TTS**: ElevenLabs
- **Others**: Redis, Celery

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd Project-AI
```

### 2. Set up virtual environment
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Copy `.env.example` to `.env` and fill in the values:
```bash
cp .env.example .env
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

## API Endpoints Overview
- `POST /api/v1/sms`: Handle incoming SMS
- `POST /api/v1/voice`: Handle incoming voice calls/audio
- `GET /api/v1/health`: Health check

## Git Branching Strategy
- `main`: Production-ready code
- `dev`: Development branch
- Feature branches: `feature/your-feature-name`
