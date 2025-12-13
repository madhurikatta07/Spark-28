# Voice Bridge

## Tech Stack
- Python 3.11
- FastAPI (Backend APIs)
- OpenAI / Gemini (LLM Reasoning)
- FAISS (Retrieval Augmented Generation)
- Whisper (Speech to Text)
- gTTS (Text to Speech)

## Architecture
Voice Input → STT → Intent Detection → Agent Orchestrator → RAG → LLM → TTS → Voice Output
