# DadaAI Web Simulator (Integrated)

> Interactive dual-device web prototype simulating an AI-powered voice assistant system for elderly users on 2G / feature phones, with live FastAPI backend connectivity!

---

## 📖 Overview

**DadaAI (VaaniAI)** is an assistive technology solution designed to bridge the digital divide for elderly users relying on basic 2G feature phones. 

This **Web Simulator** is a standalone, interactive dashboard (`index.html`) that simulates the communication flow between:
1. **A modern 4G Smartphone UI** (used by family members or caregivers to send SMS messages/reminders).
2. **A retro 2G Keypad Feature Phone UI** (used by the elderly recipient to view SMS, listen to voice responses, and interact with the AI assistant).

### Two Operating Modes:
- **Local Mock Mode**: Run entirely offline inside the browser using client-side mock translations and browser-native text-to-speech.
- **Live Backend Mode**: Connect directly to your local FastAPI backend server. Sends real SMS triggers, streams backend TTS voices, and uses browser microphone recording to test the full end-to-end **Voice AI (STT → LLM → TTS)** pipeline!

---

## 🚀 How to Run

### Step 1: Open the Frontend Simulator
1. Navigate to the `simulator` directory.
2. Open `index.html` directly in a supported modern browser (**Google Chrome** or **Microsoft Edge** are highly recommended for full Web Speech and media recording support).

### Step 2: Start the FastAPI Backend (Optional for Live Mode)
To use the live AI processing, text-to-speech, and speech-to-text features, run the backend server:

1. Open PowerShell or command prompt and navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create and activate a python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your API keys (e.g., `OPENAI_API_KEY`, `GOOGLE_API_KEY`, and/or `ELEVENLABS_API_KEY` for live LLM, STT, and TTS services):
   ```powershell
   copy .env.example .env
   ```
5. Launch the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *The server will start on `http://127.0.0.1:8000`.*

### Step 3: Connect Frontend to Backend
1. In the simulator's **System Controls** panel on the web page, change **API Integration Mode** to **Live Backend Mode (FastAPI)**.
2. Ensure the Backend URL is set to `http://127.0.0.1:8000`.
3. Click the **Test** button. The status indicator in the top right will turn green: **Backend Status: Online**.

---

## ✨ Features

- **📱 Dual-Device Interactive UI**:
  - **4G Smartphone**: Type and send messages to Dada Ji.
  - **2G Keypad Phone**: Realistic retro display, clickable keypad, signal and battery status, and navigation controls.
- **🗣️ Live Voice Assistant (STT & TTS)**:
  - **Text-to-Speech (TTS)**: In Live Mode, the browser fetches and plays the actual `audio/mpeg` stream synthesized by your backend.
  - **Speech-to-Text (STT) & Microphone Recording**: Click the **VOICE AI** button, speak into your mic, and click **STOP**. The browser records your voice and sends it to the backend's `/api/v1/voice/process` endpoint. The backend transcribes it (Whisper), gets LLM replies (Gemini/GPT), and streams the spoken response back!
- **⚙️ Environment Simulation Toggles**:
  - Simulates offline/online states and server outages to demonstrate robust **graceful degradation** (silent text fallback).
- **📋 Live Action Log Console**:
  - Shows real-time request/response cycles, API endpoints hit, and system operations.

---

## 🧪 Test Scenarios

| Scenario | Mode | Internet/AI Switch | Expected Behavior |
| :--- | :---: | :---: | :--- |
| **1. Happy Path (Mock)** | Mock | ON / ON | Receives SMS, shows translation, and speaks aloud using browser's Hindi voice. |
| **2. Fallback Path (Mock)** | Mock | OFF / OFF | Gracefully falls back to plain text display with no audio. |
| **3. Live SMS Processing** | Live | N/A | Sending SMS calls the backend's `/incoming` endpoint. Real LLM translates/explains the message. |
| **4. Live E2E Voice AI** | Live | N/A | Click **VOICE AI**, record voice request, and hear the real backend TTS voice streaming back. |

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, Tailwind CSS (CDN), FontAwesome Icons, Vanilla JS.
- **APIs Used**: Browser MediaRecorder API, HTML5 Audio, Web Speech API.
- **Backend (FastAPI)**: Python, SQLAlchemy (SQLite), OpenAI (GPT/Whisper), Google Gemini, ElevenLabs.
