<pre>
product_requirements_document:
  title: "YouTube Transcriber App"
  version: 0.1
  owner: "BMAD-FullStack Team"
  updated: "2025-09-29"

  overview:
    description: >
      A modular application with a Streamlit frontend and a FastAPI backend.
      Users provide a YouTube link, the backend downloads audio, transcribes
      up to 60 minutes, and optionally translates into English or Brazilian Portuguese.
    goals:
      - Provide simple, free, and multilingual transcription
      - Deliver TXT files formatted with one sentence per line
      - Maintain modular separation: frontend, backend, SQLite (optional)
    non_goals:
      - Multi-speaker diarization
      - Advanced captioning (SRT/VTT not in MVP scope)
      - Large-scale multi-user concurrency

  functional_requirements:
    - id: FR-01
      desc: Input YouTube URL via frontend
    - id: FR-02
      desc: Validate duration ≤ 60 minutes
    - id: FR-03
      desc: Download audio with retries and timeout
    - id: FR-04
      desc: Transcribe multilingual audio using Whisper small (CPU)
    - id: FR-05
      desc: Optional translation to English (Whisper translate) or PT-BR (Argos Translate)
    - id: FR-06
      desc: Format transcript with one sentence per line
    - id: FR-07
      desc: Download TXT file from frontend
    - id: FR-08
      desc: Reset session (frontend button + backend /reset endpoint)
    - id: FR-09
      desc: Optional persistence with SQLite

  non_functional_requirements:
    - NFR-01: Synchronous response for ≤ 60 min input within reasonable time on CPU
    - NFR-02: Memory footprint ≤ ~2GB with Whisper small model
    - NFR-03: Minimal logging, no PII stored
    - NFR-04: Easy local and containerized deployment (Docker)
    - NFR-05: Automatic cleanup of temp files older than 1h

  acceptance_criteria:
    - AC-01: Reject > 60 min videos with explicit error
    - AC-02: Transcription of PT → EN works correctly
    - AC-03: Transcription of EN → PT-BR returns translated text or fallback with warning if Argos missing
    - AC-04: TXT output contains line breaks per sentence
    - AC-05: Reset clears session, tmpdirs, and cache
    - AC-06: When store=true, transcript is saved in SQLite and retrievable by ID
</pre>