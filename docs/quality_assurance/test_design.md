<pre>
# --- TEST DESIGN (Functional + Non-Functional) ---
  test_design:
    functional_tests:
      - id: FT-01
        desc: Accept valid YouTube URL and start transcription
        pre: backend up; network available
        steps:
          - open UI; paste valid URL
          - click Transcribe
        expected: job runs; preview appears
        covers: [US-01]
      - id: FT-02
        desc: Reject video > 60 min with clear message
        steps: [submit URL for a video > 60 min]
        expected: HTTP 400 + UI error message
        covers: [US-02]
      - id: FT-03
        desc: Multilingual transcription (PT input)
        steps: [submit PT video ~2-5 min]
        expected: detected_lang=pt; text produced
        covers: [US-03]
      - id: FT-04
        desc: EN → PT-BR translation (Argos installed)
        steps: [select PT-BR target; submit EN video]
        expected: text in PT-BR; sentences per line
        covers: [US-04, US-03]
      - id: FT-05
        desc: EN translation without Argos installed
        steps: [uninstall Argos; select PT-BR; submit EN video]
        expected: warning + fallback (original text or guided install)
        covers: [US-04]
      - id: FT-06
        desc: TXT download content/encoding
        steps: [download .txt; open in UTF-8]
        expected: one sentence per line; no garbling
        covers: [US-05, US-03]
      - id: FT-07
        desc: Reset clears tmp/session
        steps: [run a job; click Reset; check temp dirs]
        expected: tmp removed; UI cleared
        covers: [US-06]
      - id: FT-08
        desc: SQLite store & retrieve by ID
        steps: [store=true; capture id; GET /download/{id}]
        expected: exact same text returned
        covers: [US-07]

      # Extended features
      - id: FT-09
        desc: Export SRT/VTT with correct timestamps
        steps: [enable export; transcribe short video; download SRT/VTT]
        expected: monotonic timestamps; no overlaps; utf-8
        covers: [US-08]
      - id: FT-10
        desc: Playlist sequential processing
        steps: [submit playlist (3 items)]
        expected: 3 transcripts in order; per-item error isolation
        covers: [US-09]
      - id: FT-11
        desc: History list and re-download
        steps: [store=true for 2 jobs; open history; download past]
        expected: items visible; downloads match originals
        covers: [US-10]
      - id: FT-12
        desc: Basic diarization visible in output (if enabled)
        steps: [enable diarization; transcribe 2 speakers sample]
        expected: speaker turns labeled; no crash without GPU
        covers: [US-11]
      - id: FT-13
        desc: Bilingual UI (EN/PT-BR) language switch
        steps: [toggle language; verify labels/tooltips]
        expected: strings localized; no truncation
        covers: [US-12]
      - id: FT-14
        desc: Progress feedback during long job
        steps: [submit ~30-45 min video]
        expected: progress increments (download/transcribe/format)
        covers: [US-14]
      - id: FT-15
        desc: Privacy-safe default behavior
        steps: [inspect logs/DB after job with store=false]
        expected: no PII/URL stored; minimal logs
        covers: [US-15]
        
      non_functional_tests:
      - id: NFT-01
        desc: Runtime for 30 min input on CPU with Whisper small
        metric: total_time_minutes
        threshold: <= 120
        covers: [NFR-01]
      - id: NFT-02
        desc: Memory footprint during transcription
        metric: peak_rss_mb
        threshold: <= 2048
        covers: [NFR-02]
      - id: NFT-03
        desc: Auto-cleanup of temp dirs > 1h
        method: simulate aged dirs; run cleanup
        expected: dirs removed; no residuals
        covers: [NFR-05]
      - id: NFT-04
        desc: Concurrency smoke (3–5 parallel sessions)
        expected: no DB lock errors; graceful slowdown only
        covers: [NFR-06]
      - id: NFT-05
        desc: Cold start model load latency
        metric: seconds_to_first_transcribe
        threshold: <= 45 (CPU baseline)
        covers: [NFR-07]
      - id: NFT-06
        desc: Container image build reproducibility (optional)
        metric: build_success; duration_minutes
        threshold: <= 10
        covers: [NFR-08]
      - id: NFT-07
        desc: Accessibility quick check (keyboard nav, labels)
        expected: focus order logical; aria labels on controls
        covers: [NFR-09]
      - id: NFT-08
        desc: Error message clarity/bilingual
        expected: actionable, concise, EN/PT-BR
        covers: [NFR-10]
</pre>