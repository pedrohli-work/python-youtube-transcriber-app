<pre>
roadmap:
  mvp:
    sprint_1:
      - Setup modular repository structure (frontend/backend/db/utils)
      - Implement /transcribe endpoint with Whisper small
      - Streamlit UI: YouTube input, preview, and TXT download
      - Duration validation up to 60 minutes
    sprint_2:
      - English translation via Whisper translate
      - PT-BR translation via Argos (optional, offline)
      - Reset button (frontend) and /reset endpoint (backend)
      - Optional persistence using SQLite with TTL
  next:
    sprint_3:
      - Export to SRT/VTT in backend
      - Playlist support (multiple videos sequentially)
      - Docker Compose deployment (frontend + backend)
    sprint_4:
      - Whisper model caching
      - Async worker (Celery or rq-lite)
      - Basic job status endpoint for multi-user support
  future:
    - Enhanced UI with transcript history
    - Speaker diarization (pyannote or similar)
    - Pluggable ASR backends (Cloud ASR providers, custom models)
</pre>

youtube-transcriber/
├─ backend/
│  ├─ __init__.py
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ db/
│  │  └─ models.py
│  ├─ middleware/
│  │  └─ metrics.py
│  ├─ services/
│  │  ├─ asr.py
│  │  ├─ cache.py
│  │  ├─ downloader.py
│  │  ├─ errors.py
│  │  ├─ formatters.py
│  │  └─ translate.py
│  └─ utils/
│     ├─ config.py
│     └─ temp.py
├─ frontend/
│  ├─ app.py
│  ├─ requirements.txt
│  └─ i18n/
│     ├─ en.json
│     └─ pt.json
├─ tools/
│  └─ batch_client.py
├─ docker/
│  ├─ Dockerfile.backend
│  ├─ Dockerfile.frontend
│  └─ docker-compose.yml
├─ .env.example
└─ README.md