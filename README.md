# 🎬 YouTube Transcriber App

A fullstack application (FastAPI + Streamlit) that **downloads, transcribes and translates YouTube videos** into text.  
Supports videos up to **60 minutes**, with optional translation to **Portuguese (Brazil)** or **English**.  
Users can **download the transcript** as `.txt`, `.srt`, or `.vtt` with clean sentence formatting.

---

## ✨ Features
- 🔗 Input any YouTube link
- 🎙️ Transcribe audio using [faster-whisper](https://github.com/guillaumekln/faster-whisper)
- 🌍 Optional translation (PT-BR / EN) via [Argos Translate](https://github.com/argosopentech/argos-translate)
- 📄 Download as `.txt`, `.srt`, or `.vtt`
- ⚡ Uses `yt-dlp` for robust YouTube audio download
- 🗑️ Temporary storage cleaned automatically
- 🧹 Reset option to avoid database bloat
- 🐳 Docker-ready (backend + frontend)

---

## 🏗️ Architecture
frontend/ → Streamlit app (user dashboard)
backend/ → FastAPI app (REST API for transcription/translation)
backend/utils/ → Helpers (config, temp files, formatters)
backend/db/ → SQLite (optional, for transcripts)
docker/ → Dockerfiles + docker-compose

yaml
Copiar código

- **Backend**: Python 3.10 (FastAPI + Uvicorn)  
- **Frontend**: Python 3.10 (Streamlit)  
- **FFmpeg**: required for audio extraction  
- **Optional**: Argos Translate for offline translations  

---

## ⚙️ Requirements
- Python **3.10+** (backend recommended at 3.10 for Torch stability)
- Python **3.10+ (frontend)
- [FFmpeg](https://ffmpeg.org/download.html) installed and in PATH
- Virtual environments (`venv`) or Docker

---

This app makes it easy to:
🔗 Paste a YouTube link  
🎙️ Transcribe the video (any language, up to 60 minutes)  
🌍 Translate to Brazilian Portuguese or English  
📄 Download clean transcripts as TXT, SRT, or VTT  

Tech stack:
⚡ FastAPI (backend)  
⚡ Streamlit (frontend dashboard)  
⚡ faster-whisper (speech-to-text)  
⚡ yt-dlp + FFmpeg (audio extraction)  
🐳 Docker-ready  

👉 Why I built it:  
I wanted a **modular, lightweight and educational project** to dive deeper into **FastAPI, Streamlit, and Whisper-based transcription pipelines** — while keeping it practical and user-friendly.  

💡 Next steps: improving UI/UX, handling longer videos, and deploying to the cloud.

## 🚀 Running Locally

### 1) Backend (FastAPI)
```bash
cd backend
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate      # Linux/macOS

pip install --upgrade pip wheel setuptools
pip install --index-url https://download.pytorch.org/whl/cpu torch
pip install -r requirements.txt

uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
Check: http://localhost:8000/health

2) Frontend (Streamlit)
bash
Copiar código
cd frontend
py -3.10 -m venv .venv   # or use 3.10 if you prefer
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

streamlit run app.py
Access: http://localhost:8501

🐳 Running with Docker
bash
Copiar código
cd docker
docker compose build
docker compose up
Frontend: http://localhost:8501

API health: http://localhost:8000/health

🧪 Testing
To validate metrics and DB logging:

bash
Copiar código
python -m backend.scripts.smoke_metrics
Expected output: success + error metrics recorded.

📦 Tech Stack
Backend: FastAPI, Uvicorn, faster-whisper, yt-dlp, Pydantic

Frontend: Streamlit

Database: SQLite (optional, lightweight)

Infra: Docker Compose

🛠️ Roadmap
 Support >1h videos with chunked transcription

 UI improvements (progress bar, subtitles preview)

 User authentication for persistent transcripts

 Deployment to cloud (Render, Railway, or Docker Swarm)

🤝 Contributing
PRs and suggestions are welcome. Please open an issue for bug reports or feature requests.

📜 License
MIT License © 2025 Pedro H. Lins

yaml
Copiar código
