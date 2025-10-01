import sqlite3, uuid, json, datetime
from pathlib import Path
from backend.utils.config import DB_PATH, TTL_DAYS

def _conn():
    # Garante diretório do DB
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def _expires_at(days: int = TTL_DAYS):
    # Compatível com CURRENT_TIMESTAMP (usa espaço)
    return (datetime.datetime.utcnow() + datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

def _migrate_if_needed(con: sqlite3.Connection):
    cur = con.cursor()

    # transcripts
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transcripts(
      id TEXT PRIMARY KEY,
      youtube_url TEXT, title TEXT, duration_sec INTEGER,
      detected_lang TEXT, target_lang TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      expires_at DATETIME,
      text_joined TEXT, status TEXT DEFAULT 'done'
    );""")

    # cache (assegura colunas)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cache(
      key TEXT PRIMARY KEY,
      video_id TEXT,
      target_lang TEXT,
      payload TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      expires_at DATETIME
    );""")
    cols = {r[1] for r in cur.execute("PRAGMA table_info(cache)").fetchall()}
    if "payload" not in cols:
        cur.execute("ALTER TABLE cache ADD COLUMN payload TEXT")
    if "created_at" not in cols:
        cur.execute("ALTER TABLE cache ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
    if "expires_at" not in cols:
        cur.execute("ALTER TABLE cache ADD COLUMN expires_at DATETIME")

    # metrics
    cur.execute("""
    CREATE TABLE IF NOT EXISTS metrics(
      id TEXT PRIMARY KEY,
      video_id TEXT,
      step TEXT,
      duration_sec REAL,
      outcome TEXT,
      error_code TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );""")

def init_db():
    con = _conn()
    con.execute("PRAGMA journal_mode=WAL;")
    _migrate_if_needed(con)
    con.commit(); con.close()

def store_transcript(info: dict, target_lang: str, text: str, detected: str) -> str:
    tid = str(uuid.uuid4())
    con = _conn()
    con.execute("""INSERT INTO transcripts
      (id, youtube_url, title, duration_sec, detected_lang, target_lang, expires_at, text_joined)
      VALUES (?,?,?,?,?,?,?,?)""",
      (tid, info.get("webpage_url"), info.get("title"),
       int(info.get("duration") or 0), detected or "", target_lang, _expires_at(), text))
    con.commit(); con.close()
    return tid

def get_transcript_text(tid: str):
    con = _conn()
    row = con.execute("SELECT text_joined FROM transcripts WHERE id=?", (tid,)).fetchone()
    con.close()
    return row["text_joined"] if row else None

def purge_expired():
    con = _conn()
    con.execute("DELETE FROM transcripts WHERE expires_at IS NOT NULL AND datetime(expires_at) < CURRENT_TIMESTAMP")
    con.execute("DELETE FROM cache WHERE expires_at IS NOT NULL AND datetime(expires_at) < CURRENT_TIMESTAMP")
    con.commit(); con.close()

# Cache
def cache_get(key: str):
    con = _conn()
    row = con.execute(
        "SELECT payload FROM cache WHERE key=? AND (expires_at IS NULL OR datetime(expires_at) >= CURRENT_TIMESTAMP)",
        (key,)
    ).fetchone()
    con.close()
    return json.loads(row["payload"]) if row and row["payload"] else None

def cache_put(key: str, video_id: str, target_lang: str, payload: dict, ttl_hours: int):
    expires = (datetime.datetime.utcnow() + datetime.timedelta(hours=ttl_hours)).strftime("%Y-%m-%d %H:%M:%S")
    con = _conn()
    con.execute("""INSERT OR REPLACE INTO cache(key, video_id, target_lang, payload, expires_at)
                   VALUES (?,?,?,?,?)""",
                (key, video_id, target_lang, json.dumps(payload), expires))
    con.commit(); con.close()

# Metrics
def log_metric(video_id: str, step: str, duration_sec: float, outcome: str, error_code: str | None):
    mid = str(uuid.uuid4())
    con = _conn()
    con.execute("""INSERT INTO metrics(id, video_id, step, duration_sec, outcome, error_code)
                   VALUES (?,?,?,?,?,?)""",
                (mid, video_id, step, duration_sec, outcome, (error_code or "")))
    con.commit(); con.close()
