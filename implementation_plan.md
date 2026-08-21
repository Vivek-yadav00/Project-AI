# Implementation Plan: DadaAI / VaaniAI Project Initialization

This plan establishes the directory structure for the **DadaAI / VaaniAI** project (an AI-powered voice assistant feature phone system) and outlines how two team members can collaborate simultaneously using version control and mock API interfaces.

## Collaborative Git & Branching Strategy

To enable both team members to work concurrently without merge conflicts, we will use the following approach:

1. **Monorepo Architecture**: All code (backend, Android/gateway app, ESP32 firmware) is kept in a single repository but separated into clean subfolders. This keeps code and API contracts aligned.
2. **API Contract First**: Before writing logic, both members agree on the JSON request/response formats. We will build mock endpoints in FastAPI first so the client developer can test immediately.
3. **Feature Branching**:
   - `main`: Production-ready, stable code.
   - `feature/backend-core` (Member A): Database, LLM processing, TTS/STT, FastAPI routers.
   - `feature/gateway-client` (Member B): Android SMS gateway app or ESP32 GSM module controller.
4. **Local Exposing (`ngrok`)**: Since telephony/SMS services require public webhooks, Member B (developing the client) can use `ngrok` to expose Member A's local FastAPI server for end-to-end testing.

---

## Proposed Project Structure

We will initialize the following structure in the workspace:

```text
quirky-curie/
├── backend/                   # FastAPI Backend Server (Member A)
│   ├── app/
│   │   ├── api/               # API Router endpoints (SMS, Voice, Call Webhooks)
│   │   ├── core/              # Config, security, and LLM/TTS/STT wrappers
│   │   ├── db/                # SQLite database session and models
│   │   ├── services/          # Business logic (AI pipelines, audio converters)
│   │   └── main.py            # FastAPI entrypoint
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Container configuration
│   └── .env.example           # Example environment variables (git-tracked)
├── sms_gateway/               # Android Companion SMS Gateway (Member B)
│   └── (Flutter / Kotlin app template)
├── hardware/                  # ESP32 Matrix Keypad & GSM Code (Member B)
│   └── dada_ai_esp32/         # Arduino IDE/PlatformIO C++ project
├── docker-compose.yml         # Dev database and FastAPI container runner
├── .gitignore                 # Excludes venvs, local configs, credentials
└── README.md                  # Team instructions & onboarding guide
```

---

## Proposed Changes

### [DadaAI Root Directory]

#### [NEW] [README.md](file:///c:/Users/hp/Documents/antigravity/quirky-curie/README.md)
Contains team onboarding instructions, division of responsibilities, and how to start the app.

#### [NEW] [.gitignore](file:///c:/Users/hp/Documents/antigravity/quirky-curie/.gitignore)
Standard ignore patterns for Python, Android, ESP32, and `.env` credentials.

#### [NEW] [docker-compose.yml](file:///c:/Users/hp/Documents/antigravity/quirky-curie/docker-compose.yml)
Compose file to orchestrate FastAPI, database, and Redis.

### [Backend Component (FastAPI)]

#### [NEW] [backend/requirements.txt](file:///c:/Users/hp/Documents/antigravity/quirky-curie/backend/requirements.txt)
FastAPI, Uvicorn, SQLAlchemy, OpenAI, ElevenLabs, etc.

#### [NEW] [backend/.env.example](file:///c:/Users/hp/Documents/antigravity/quirky-curie/backend/.env.example)
Template variables (e.g., `OPENAI_API_KEY`, `TELEPHONY_PROVIDER`).

#### [NEW] [backend/app/main.py](file:///c:/Users/hp/Documents/antigravity/quirky-curie/backend/app/main.py)
Entry point setting up mock endpoints so Member B can immediately run integration tests.

### [Client / Gateway Components]

#### [NEW] [sms_gateway/README.md](file:///c:/Users/hp/Documents/antigravity/quirky-curie/sms_gateway/README.md)
Instructions for Android app setup.

#### [NEW] [hardware/README.md](file:///c:/Users/hp/Documents/antigravity/quirky-curie/hardware/README.md)
Instructions for ESP32/SIM800L/Keypad connections and libraries.

---

## Verification Plan

### Automated Verification
- We will write a check script to verify the file structure is created correctly.
- Run `uvicorn app.main:app` to ensure the FastAPI mock endpoints start correctly.

### Manual Verification
- Verify the mock routes are accessible via curl requests.
- Verify Git repository has correct folder setup.
