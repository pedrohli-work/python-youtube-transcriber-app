from typing import Optional
import os
from pathlib import Path

def _bool(envval: Optional[str], default: bool = False) -> bool:
    if envval is None:
        return default
    return str(envval).strip().lower() in ("1", "true", "yes", "y", "on")

def _int(name: str, default: int) -> int:
    val = os.getenv(name, None)
    try:
        return int(val) if val is not None else default
    except (TypeError, ValueError):
        return int(default)

# Configs
MAX_MINUTES = _int("MAX_MINUTES", 60)
TTL_DAYS = _int("TTL_DAYS", 3)
CACHE_TTL_HOURS = _int("CACHE_TTL_HOURS", 72)
RATE_LIMIT_RPM = _int("RATE_LIMIT_RPM", 30)

MODEL_SIZE = os.getenv("MODEL_SIZE", "small").strip().lower()
if MODEL_SIZE not in {"small", "medium"}:
    MODEL_SIZE = "small"

STORE_DEFAULT = _bool(os.getenv("STORE_DEFAULT"), default=False)
PREFER_CAPTIONS_DEFAULT = _bool(os.getenv("PREFER_CAPTIONS_DEFAULT"), default=True)

# Default amigável (relativo à raiz onde roda o processo)
DB_PATH = os.getenv("TRANSCRIBER_DB", str(Path.cwd() / "data" / "transcripts.db"))
