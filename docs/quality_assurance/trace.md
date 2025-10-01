<pre>
# --- TRACEABILITY (US ↔ FR ↔ Tests) ---
  traceability:
    mapping:
      US-01: { functional_requirements: [FR-01], tests: [FT-01] }
      US-02: { functional_requirements: [FR-02], tests: [FT-02] }
      US-03: { functional_requirements: [FR-06], tests: [FT-03, FT-06] }
      US-04: { functional_requirements: [FR-05], tests: [FT-04, FT-05] }
      US-05: { functional_requirements: [FR-07], tests: [FT-06] }
      US-06: { functional_requirements: [FR-08], tests: [FT-07] }
      US-07: { functional_requirements: [FR-09], tests: [FT-08] }
      US-08: { functional_requirements: [FR-SRT], tests: [FT-09] }
      US-09: { functional_requirements: [FR-Playlist], tests: [FT-10] }
      US-10: { functional_requirements: [FR-History], tests: [FT-11] }
      US-11: { functional_requirements: [FR-Diarization], tests: [FT-12] }
      US-12: { functional_requirements: [FR-L10n], tests: [FT-13] }
      US-14: { functional_requirements: [FR-Progress], tests: [FT-14] }
      US-15: { functional_requirements: [FR-Privacy], tests: [FT-15] }
    notes:
      FR-01: "YouTube URL input (frontend)"
      FR-02: "Duration validation ≤ 60 minutes"
      FR-05: "Optional translation EN/PT-BR"
      FR-06: "One sentence per line formatting"
      FR-07: "TXT download"
      FR-08: "Reset (frontend + /reset)"
      FR-09: "SQLite optional"
      FR-SRT: "SRT/VTT export (extended)"
      FR-Playlist: "Playlist sequential processing (extended)"
      FR-History: "History UI/API (extended)"
      FR-Diarization: "Speaker diarization (extended)"
      FR-L10n: "Bilingual UI (extended)"
      FR-Progress: "Progress feedback (extended)"
      FR-Privacy: "No PII storage by default (extended)"
</pre>