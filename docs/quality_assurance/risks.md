<pre>
# --- RISKS (MVP + Extended) ---
  risks:
    - id: R-01
      desc: YouTube throttling/site changes break downloads
      severity: high
      likelihood: medium
      mitigation: yt-dlp updates; retries/timeouts; clear error paths
      owner: backend
    - id: R-02
      desc: CPU resource exhaustion on long videos
      severity: medium
      likelihood: medium
      mitigation: enforce 60-min cap; model=small; document perf
      owner: backend
    - id: R-03
      desc: Argos not installed for PT-BR
      severity: low
      likelihood: high
      mitigation: warning + guided install; fallback text
      owner: backend
    - id: R-04
      desc: Disk fills with temp files
      severity: medium
      likelihood: low
      mitigation: auto-cleanup >1h; Reset button
      owner: both
    - id: R-05
      desc: User accuracy expectations too high
      severity: medium
      likelihood: medium
      mitigation: set expectations in UI/README; note limits
      owner: PM/UX
    - id: R-06
      desc: Deployment friction for non-technical users
      severity: medium
      likelihood: medium
      mitigation: pip path + optional Docker; guides
      owner: PM
    - id: R-07
      desc: Legal/TOS issues when downloading content
      severity: high
      likelihood: low
      mitigation: disclaimers; user responsibility; avoid private content
      owner: PM/Legal
    - id: R-08
      desc: SQLite corruption under concurrency
      severity: medium
      likelihood: low
      mitigation: WAL mode; single-writer policy; backups
      owner: backend
    - id: R-09
      desc: Streamlit Cloud resource/time limits
      severity: medium
      likelihood: medium
      mitigation: shorter samples; offline/local usage guidance
      owner: PM
    - id: R-10
      desc: Container disk quota overflow (if Docker)
      severity: medium
      likelihood: low
      mitigation: prune images; store outside container; quotas
      owner: DevOps
</pre>