<pre>
qa_pack:
  meta:
    project: "YouTube Transcriber App"
    version: "0.2-extended"
    updated: "2025-09-29"
    scope: "MVP + next/future roadmap coverage"

  # --- USER STORIES (MVP + Extended) ---
  user_stories:
    - id: US-01
      role: user
      need: input a YouTube link
      goal: generate a transcript
    - id: US-02
      role: user
      need: reject videos longer than 60 minutes
      goal: avoid wasting time/resources
    - id: US-03
      role: user
      need: transcript with one sentence per line
      goal: improve readability and reuse
    - id: US-04
      role: user
      need: translate transcript to PT-BR or EN
      goal: consume content in my preferred language
    - id: US-05
      role: user
      need: download transcript as .txt
      goal: save and share
    - id: US-06
      role: user
      need: reset button
      goal: clear temporary files and restart
    - id: US-07
      role: user
      need: optional SQLite storage
      goal: retrieve transcripts later

    # Extended (next/future)
    - id: US-08
      role: user
      need: export subtitles (.srt/.vtt)
      goal: sync transcript with video players
    - id: US-09
      role: user
      need: process playlists (batch)
      goal: transcribe multiple videos sequentially
    - id: US-10
      role: user
      need: view transcript history
      goal: re-download past files
    - id: US-11
      role: user
      need: multi-speaker diarization
      goal: identify who is speaking
    - id: US-12
      role: user
      need: bilingual UI (EN/PT-BR)
      goal: navigate more easily
    - id: US-13
      role: maintainer
      need: containerized deployment (optional)
      goal: reproducible environment across machines
    - id: US-14
      role: user
      need: progress feedback during long jobs
      goal: understand current status and ETA-ish
    - id: US-15
      role: user
      need: privacy-safe processing
      goal: avoid storing personal data or links unnecessarily
</pre>