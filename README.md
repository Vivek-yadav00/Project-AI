# DadaAI / VaaniAI

An AI-powered voice and SMS assistant designed specifically to empower elderly users on feature phones (2G) and bridge the communication gap with their caregivers. 

## 👥 Team
- **Susanta**: Backend & Frontend Web (FastAPI, Next.js)
- **Vivek**: SMS Gateway & ESP32 Hardware Integration

---

## 🏗️ System Architecture & Tech Stack

The project is split into two main components: an AI backend and a Next.js frontend simulator.

### Backend (FastAPI)
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite with SQLAlchemy ORM
- **LLM Integration**: Google Gemini (`gemini-3.1-flash-lite`)
- **Speech-to-Text (STT)**: Google Gemini Multimodal Audio (via inline byte injection)
- **Text-to-Speech (TTS)**: ElevenLabs (Hindi voice generation)

### Frontend (Next.js)
- **Framework**: Next.js 15+ (App Router)
- **Styling**: Tailwind CSS v4 + Custom Retro CSS
- **State Management**: React Hooks + `BroadcastChannel` API for cross-tab communication
- **Language**: TypeScript

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Vivek-yadav00/Project-AI.git
cd Project-AI
```

### 2. Backend Setup
Navigate to the root directory where the python virtual environment is typically managed, or go to the backend folder:

```bash
# Activate your virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Set up Environment Variables
cp backend/.env.example backend/.env
# Edit backend/.env and add your GEMINI_API_KEY and ELEVENLABS_API_KEY
```

Run the FastAPI Server:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API will be running at `http://127.0.0.1:8000`.

### 3. Frontend Setup
Open a new terminal window and navigate to the `frontend/` directory.

```bash
cd frontend

# Install Node dependencies
npm install

# Run the Next.js development server
npm run dev
```
The frontend simulator will be running at `http://localhost:3000`.

---

## 📱 Using the Frontend Simulator

The frontend acts as a simulator to test the AI capabilities without needing the physical ESP32 hardware.

1. **Dashboard (`http://localhost:3000/`)**: Control panel to toggle between "Mock" and "Live FastAPI" mode. Allows simulating 5G/2G network constraints.
2. **Caregiver Phone (`http://localhost:3000/sender`)**: A modern 4G smartphone UI where caregivers can send text messages to Dada Ji.
3. **Dada Ji's Phone (`http://localhost:3000/receiver`)**: A retro Nokia-style 2G feature phone UI.
   - Incoming messages from the Caregiver are automatically translated to Hindi and read aloud via AI Voice.
   - Click the **Voice AI** button to speak a reply through your microphone, which is processed by the backend STT and LLM pipelines.

---

## 🔌 API Endpoints Overview

The FastAPI backend exposes the following core endpoints:
- `GET /api/v1/health`: Returns system health and database connectivity status.
- `POST /api/v1/sms/incoming`: Handles incoming text messages (Caregiver to Dada Ji) and triggers AI summarization.
- `POST /api/v1/voice/process`: Receives raw `audio/webm` bytes from Dada Ji's microphone, converts it to text (STT), generates an AI reply, and returns synthesized Hindi audio (TTS).
- `POST /api/v1/voice/tts`: Standalone endpoint for Text-to-Speech conversion.

---

## 🌿 Git Branching Strategy
- `main`: Production-ready code and stable releases.
- `dev`: Development integration branch.
- Feature branches: `susanta` (Backend/Web), `vivek` (Hardware/SMS).
