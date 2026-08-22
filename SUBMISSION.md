# DadaAI / VaaniAI: Project Documentation

## 1. What We Built and How It Works
**DadaAI (VaaniAI)** is an AI-powered communication assistant designed specifically to empower elderly users on 2G feature phones. It bridges the digital divide by allowing elderly users (like "Dada Ji") to interact seamlessly with their tech-savvy caregivers without needing to learn how to use a smartphone or read English.

**How it works:**
1. **Inbound SMS (Caregiver ➔ Dada Ji):** When a caregiver sends a text message (e.g., in English) from their smartphone, the message reaches Dada Ji's feature phone. The system intercepts this message, translates it into simple conversational Hindi using our AI backend, and reads it aloud through Text-to-Speech (TTS). 
2. **Outbound Voice (Dada Ji ➔ Caregiver):** Dada Ji can press a button and speak his reply in Hindi. The system captures the audio, transcribes it using Speech-to-Text (STT), formulates a context-aware response or translates the reply, and sends it back to the caregiver.
3. **Offline Fallback:** If the API or internet is down, the system gracefully falls back to a standard 2G feature phone, bypassing the AI and simply displaying the raw SMS text on the screen.

To test and demonstrate this without the physical ESP32 hardware, we built a comprehensive **Next.js Web Simulator** that mimics the hardware constraints, featuring a Caregiver Smartphone UI, a Retro Nokia Phone UI, and a network condition toggler.

---

## 2. Team Members & Contributions

Our team consisted of two members, dividing the workload across software infrastructure and hardware integration.

### Susanta (Backend & Frontend Web) - *My Contribution*
I was responsible for architecting the entire software ecosystem:
* **Backend Development:** Built a high-performance, asynchronous Python backend using **FastAPI** and **SQLite/SQLAlchemy** to manage conversations, users, and API routing.
* **AI Pipeline Integration:** Orchestrated the core AI logic (`ai_pipeline.py`). I integrated **Google Gemini (3.1-flash-lite)** for LLM text processing and Multimodal Audio STT, and **ElevenLabs** for highly natural Hindi Text-to-Speech.
* **Frontend Web Simulator:** Built the Next.js 15+ frontend from scratch using Tailwind CSS v4. I implemented the cross-tab communication using the `BroadcastChannel` API so the Caregiver UI and Retro Phone UI could interact in real-time.
* **Deployment Ops:** Configured Docker files and the `render.yaml` infrastructure-as-code for 1-click cloud deployment.

### Vivek (Hardware & SMS Gateway)
* **ESP32 Hardware Integration:** Engineered the physical device logic using an ESP32 microcontroller.
* **Cellular Networking:** Integrated the SIM800L module to handle actual GSM cellular network SMS receiving and sending, acting as the bridge between the physical cellular network and our FastAPI webhook.
* **Hardware Interfacing:** Managed the physical microphone inputs and speaker outputs on the feature phone casing.

---

## 3. Key Features
* **Zero Learning Curve:** The end-user (elderly) interacts entirely via voice in their native language; the technology is completely invisible to them.
* **Context-Aware AI:** The LLM retains conversation history. When Dada Ji speaks a question (e.g., "What time?"), the AI knows he is referring to the specific SMS he just received from the caregiver.
* **Cross-Tab Web Simulator:** Allows judges and testers to simulate 5G/2G network environments and test the hardware flow purely through a browser.

---

## 4. Technical Decisions
* **FastAPI:** Chosen for its native `async/await` support which is crucial for handling slow, I/O-bound AI API calls without blocking the server.
* **Gemini 3.1 Flash-Lite over Whisper:** We initially considered OpenAI Whisper for STT, but switched to Gemini's Multimodal Audio API by passing raw audio bytes directly inline. This drastically reduced transcription latency and cost while providing excellent Hindi recognition.
* **Next.js App Router:** Chosen for the frontend simulator to easily manage state and utilize modern React server components where necessary.

---

## 5. Challenges and Solutions

1. **AI Role Confusion in Context Window**
   * **Challenge:** Our database saved both the Caregiver's incoming SMS and Dada Ji's spoken voice inputs under the same role (`"user"`). When feeding this history to the LLM, Gemini became confused, thinking Dada Ji was the one who sent the English flight update SMS.
   * **Solution:** I wrote a context-injection wrapper in the backend that intercepts the database history and explicitly labels the roles before sending them to the prompt (e.g., prefixing messages with `[Received SMS (Caregiver)]` and `[Your AI Translation]`). This completely resolved the hallucination.

2. **Audio Processing Latency**
   * **Challenge:** Processing Voice ➔ Text ➔ AI ➔ Voice resulted in heavy latency. Initially, we were using `client.aio.files.upload()` to upload the audio to Gemini.
   * **Solution:** We bypassed the upload step entirely by injecting the raw `audio/webm` bytes directly into the Gemini prompt payload. This cut our processing time significantly.

3. **Offline Graceful Degradation**
   * **Challenge:** We needed to ensure the phone wouldn't "brick" if the 2G internet dropped.
   * **Solution:** We designed a robust hardware/software fallback. If the API ping fails, the system bypasses the STT/TTS pipeline entirely and routes the raw SMS directly to the LCD screen, preserving base feature-phone functionality.
