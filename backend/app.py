import re, json, uuid, time, logging
from fastapi import FastAPI, Request
from pydantic import BaseModel, AnyUrl
from backend.utils.config import (MAX_MINUTES, STORE_DEFAULT, CACHE_TTL_HOURS,
                                  PREFER_CAPTIONS_DEFAULT, RATE_LIMIT_RPM, DB_PATH)
from backend.db.models import init_db, purge_expired, store_transcript, get_transcript_text
from backend.services import downloader as dl
from backend.services.asr import transcribe
from backend.services.formatters import join_sentences, vtt_to_lines, srt_to_lines, to_srt_from_segments, to_vtt_from_segments
from backend.services.errors import (AppError, URL_INVALID, RATE_LIMITED, DURATION_EXCEEDED)
from backend.services.cache import make_key, get_cached, put_cached
from backend.middleware.metrics import StepTimer
from backend.utils.temp import session_tmpdir, cleanup_old_tmp

app = FastAPI(title="YT Transcriber API (refined)")
log = logging.getLogger("uvicorn.error")

# -------- Rate Limit (in-memory simples) --------
BUCKET = {}
def _rl_ok(ip: str) -> bool:
    now = time.time()
    winsize = 60.0
    bucket = BUCKET.get(ip, [])
    bucket = [t for t in bucket if t > now - winsize]
    if len(bucket) >= RATE_LIMIT_RPM:
        BUCKET[ip] = bucket
        return False
    bucket.append(now)
    BUCKET[ip] = bucket
    return True

# -------- Validação de URL --------
YT_REGEX = re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+", re.I)

class TranscribeReq(BaseModel):
    youtube_url: AnyUrl
    target_lang: str = "original"    # original | pt-BR | en
    max_minutes: int = MAX_MINUTES
    export_format: list[str] = ["txt"]  # ["txt","srt","vtt"]
    prefer_captions: bool = PREFER_CAPTIONS_DEFAULT
    store: bool = STORE_DEFAULT

@app.on_event("startup")
def _init():
    log.info(f"USING DB_PATH={DB_PATH}")
    init_db()
    cleanup_old_tmp()
    purge_expired()

@app.get("/health")
def health():
    return {"ok": True, "max_minutes": MAX_MINUTES, "rate_limit_rpm": RATE_LIMIT_RPM}

@app.post("/transcribe")
def transcribe_ep(req: Request, body: TranscribeReq):
    ip = req.client.host if req.client else "0.0.0.0"
    if not _rl_ok(ip):
        raise RATE_LIMITED()
    if not YT_REGEX.match(str(body.youtube_url)):
        raise URL_INVALID()

    info = dl.get_info(str(body.youtube_url))
    duration = int(info.get("duration") or 0)
    if duration and duration > body.max_minutes * 60:
        raise DURATION_EXCEEDED(body.max_minutes)

    # Cache key
    settings = {"max_minutes": body.max_minutes}
    ckey = make_key(str(body.youtube_url), body.target_lang, body.export_format, settings)
    cached = get_cached(ckey)
    if cached:
        return {"cached": True, **cached}

    video_id = info.get("id") or ""

    with StepTimer(video_id, "total"):
        with session_tmpdir() as tmp:
            # 1) Captions (com fallback silencioso para ASR)
            if body.prefer_captions and dl.has_captions(info):
                with StepTimer(video_id, "captions"):
                    vtt_path = dl.download_captions(str(body.youtube_url), tmp)
                    if vtt_path:
                        vtt_txt = vtt_path.read_text(encoding="utf-8", errors="ignore")
                        lines = vtt_to_lines(vtt_txt)
                        detected = info.get("language") or ""
                        payload = _build_payload(info, detected, body, lines, segments=None)
                        put_cached(ckey, video_id, body.target_lang, payload, CACHE_TTL_HOURS)
                        return payload
            # 2) Download + ASR
            with StepTimer(video_id, "download"):
                audio_path, _ = dl.download_audio(str(body.youtube_url), tmp)
            with StepTimer(video_id, "asr"):
                lines, detected, segments = transcribe(audio_path, target_lang=body.target_lang)

            payload = _build_payload(info, detected, body, lines, segments)
            put_cached(ckey, video_id, body.target_lang, payload, CACHE_TTL_HOURS)
            return payload

def _build_payload(info: dict, detected: str, body: TranscribeReq, lines: list[str], segments):
    text = join_sentences(lines)
    resp = {
        "job_id": str(uuid.uuid4()),
        "title": info.get("title") or "youtube",
        "duration_sec": int(info.get("duration") or 0),
        "detected_lang": detected,
        "target_lang": body.target_lang,
        "text_lines": lines,
        "text_joined": text,
        "export": {}
    }
    # Export SRT/VTT se solicitado e se tivermos segments (ASR)
    if segments is not None:
        if "srt" in body.export_format:
            resp["export"]["srt"] = to_srt_from_segments(segments)
        if "vtt" in body.export_format:
            resp["export"]["vtt"] = to_vtt_from_segments(segments)
    if body.store:
        tid = store_transcript(info, body.target_lang, text, detected)
        resp["transcript_id"] = tid
    return resp

@app.get("/download/{transcript_id}")
def download_txt(transcript_id: str):
    txt = get_transcript_text(transcript_id)
    if not txt:
        raise AppError("NOT_FOUND", "Transcript not found.", 404)
    return {"id": transcript_id, "text_joined": txt}

@app.post("/reset")
def reset():
    cleanup_old_tmp(); purge_expired()
    return {"ok": True}
