import hashlib, json
from backend.db.models import cache_get, cache_put

def make_key(url: str, target_lang: str, export_format: list[str] | None, settings: dict | None) -> str:
    payload = {"url": url, "target_lang": target_lang, "export_format": export_format or ["txt"], "settings": settings or {}}
    raw = json.dumps(payload, sort_keys=True, separators=(",",":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def get_cached(key: str):
    return cache_get(key)

def put_cached(key: str, video_id: str, target_lang: str, payload: dict, ttl_hours: int):
    cache_put(key, video_id, target_lang, payload, ttl_hours)
