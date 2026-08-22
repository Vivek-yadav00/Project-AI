# DadaAI / VaaniAI: Complete Project Documentation

## 1. Project Overview & How It Works
**DadaAI (VaaniAI)** is an AI-powered communication assistant designed specifically to empower elderly users on 2G feature phones. It bridges the digital divide by allowing elderly users (like "Dada Ji") to interact seamlessly with their tech-savvy caregivers without needing to learn how to use a smartphone or read English.

**Core Workflow:**
1. **Inbound SMS (Caregiver ➔ Dada Ji):** When a caregiver sends a text message (e.g., in English) from their smartphone, the message reaches Dada Ji's feature phone. The system intercepts this message, translates it into simple conversational Hindi using our AI backend, and reads it aloud through Text-to-Speech (TTS). 
2. **Outbound Voice (Dada Ji ➔ Caregiver):** Dada Ji can press a button and speak his reply in Hindi. The system captures the audio, transcribes it using Speech-to-Text (STT), formulates a context-aware response or translates the reply, and sends it back to the caregiver.
3. **Offline Fallback:** If the API or internet is down, the system gracefully falls back to a standard 2G feature phone, bypassing the AI and simply displaying the raw SMS text on the screen.

To test and demonstrate this without the physical ESP32 hardware, we built a comprehensive **Next.js Web Simulator** that mimics the hardware constraints, featuring a Caregiver Smartphone UI, a Retro Nokia Phone UI, and a network condition toggler.

---

## 2. Team Structure & Contributions

Our team consisted of two members, dividing the workload across backend architecture, AI pipeline integration, and rigorous API testing.

### Susanta (Backend & Frontend Web)
* **Backend Architecture:** Built a high-performance, asynchronous Python backend using **FastAPI** and **SQLite/SQLAlchemy** to manage conversations, users, and API routing.
* **AI Pipeline Orchestration:** Developed the core AI logic (`ai_pipeline.py`). Integrated **Google Gemini (3.1-flash-lite)** for LLM text processing and Multimodal Audio STT, alongside **ElevenLabs** for highly natural Hindi Text-to-Speech.
* **Frontend Web Simulator:** Built the Next.js 15+ frontend from scratch using Tailwind CSS v4. Implemented cross-tab communication using the `BroadcastChannel` API so the Caregiver UI and Retro Phone UI could interact in real-time.
* **Deployment Ops:** Configured Docker files and the `render.yaml` infrastructure-as-code for 1-click cloud deployment on Render and Vercel.

### Vivek (API Testing & QA Integration)
* **API Testing & Quality Assurance:** Extensively tested the FastAPI endpoints and STT/TTS pipelines under simulated low-bandwidth environments to ensure they meet the constraints of a 2G feature phone.
* **Bug Tracking & Edge Cases:** Identified critical edge cases in the AI conversation history and latency issues in the audio streaming pipeline, ensuring high reliability and robustness for production use.

---

## 3. Key Features
* **Zero Learning Curve:** The end-user (elderly) interacts entirely via voice in their native language; the technology is completely invisible to them.
* **Context-Aware AI:** The LLM retains conversation history. When Dada Ji speaks a question (e.g., "What time?"), the AI knows he is referring to the specific SMS he just received from the caregiver.
* **Cross-Tab Web Simulator:** Allows judges and testers to simulate 5G/2G network environments and test the hardware flow purely through a browser without needing physical microcontrollers.

---

## 4. Technical Decisions
* **FastAPI:** Chosen for its native `async/await` support which is crucial for handling slow, I/O-bound AI API calls without blocking the server.
* **Gemini 3.1 Flash-Lite over Whisper:** We initially considered OpenAI Whisper for STT, but switched to Gemini's Multimodal Audio API by passing raw audio bytes directly inline. This drastically reduced transcription latency and cost while providing excellent Hindi recognition.
* **Next.js App Router:** Chosen for the frontend simulator to easily manage state and utilize modern React server components where necessary.

---

## 5. Challenges and Solutions

1. **AI Role Confusion in Context Window**
   * **Challenge:** Our database saved both the Caregiver's incoming SMS and Dada Ji's spoken voice inputs under the same role (`"user"`). When feeding this history to the LLM, Gemini became confused, thinking Dada Ji was the one who sent the English flight update SMS.
   * **Solution:** A context-injection wrapper was created in the backend that intercepts the database history and explicitly labels the roles before sending them to the prompt (e.g., prefixing messages with `[Received SMS (Caregiver)]` and `[Your AI Translation]`). This completely resolved the hallucination.

2. **Audio Processing Latency**
   * **Challenge:** Processing Voice ➔ Text ➔ AI ➔ Voice resulted in heavy latency. Initially, we were using API file upload methods to send the audio to Gemini.
   * **Solution:** We bypassed the upload step entirely by injecting the raw `audio/webm` bytes directly into the Gemini prompt payload. This cut our processing time significantly.

3. **Offline Graceful Degradation**
   * **Challenge:** We needed to ensure the phone wouldn't "brick" if the 2G internet dropped.
   * **Solution:** We designed a robust hardware/software fallback. If the API ping fails, the system bypasses the STT/TTS pipeline entirely and routes the raw SMS directly to the LCD screen, preserving base feature-phone functionality.
