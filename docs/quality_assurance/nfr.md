<pre>
# --- NON-FUNCTIONAL REQUIREMENTS (Extended) ---
  nfr:
    - id: NFR-01
      desc: Transcription completes within 2h for 60-min input on CPU (Whisper small)
    - id: NFR-02
      desc: Peak memory ≤ ~2GB during transcription
    - id: NFR-03
      desc: App runs locally via pip; containerization optional
    - id: NFR-04
      desc: Auto-cleanup removes temp files/dirs older than 1h
    - id: NFR-05
      desc: Minimal logs; no PII persisted by default (store=false)
    - id: NFR-06
      desc: Support 3–5 concurrent sessions without data loss (graceful slowdown allowed)
    - id: NFR-07
      desc: UI remains responsive; progress updated at least every 10s during long jobs
    - id: NFR-08
      desc: Docker image builds reproducibly in < 10 minutes (if used)
    - id: NFR-09
      desc: Frontend meets basic accessibility (keyboard navigation, labels, contrast)
    - id: NFR-10
      desc: Error messages are clear, actionable, and available in EN/PT-BR

  # --- COVERAGE & EXIT CRITERIA ---
  coverage:
    functional_coverage_target: "≥ 90% of FRs mapped to at least 1 passing FT"
    nfr_coverage_target: "≥ 80% of NFRs validated by NFT or inspection"
    risk_mitigation_status: "All high-severity risks have at least one active mitigation"
  exit_criteria:
    - "All must-have features pass FT and related NFT benchmarks"
    - "No open high-severity defects"
    - "Docs updated (README, usage, limitations, privacy note)"
</pre>