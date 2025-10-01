<pre>
features_prioritization:
  must_have:
    - YouTube URL input
    - Duration validation up to 60 minutes
    - Robust audio download (yt-dlp with retries/timeout)
    - Multilingual transcription via Whisper small
    - Translation to English via Whisper translate
    - TXT output with one sentence per line
    - TXT download button in frontend
    - Reset functionality (frontend + backend)
  should_have:
    - PT-BR translation via Argos
    - Optional SQLite persistence with TTL
    - SRT/VTT export
  could_have:
    - Transcript history in frontend
    - Playlist support (multi-video)
    - Docker Compose deployment
  wont_have:
    - Multi-speaker diarization in MVP
    - Massive scale multi-user concurrency
</pre>