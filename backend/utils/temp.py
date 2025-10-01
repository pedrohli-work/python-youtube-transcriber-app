from __future__ import annotations

import logging
import os
import stat
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

log = logging.getLogger("backend.utils.temp")

def _rmtree_onerror(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
        func(path)
    except Exception:
        log.debug("Fail to force remove: %s", path, exc_info=exc_info)

@contextmanager
def session_tmpdir(prefix: str = "yt-transcript-") -> Iterator[Path]:
    import shutil
    p = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        yield p
    finally:
        try:
            shutil.rmtree(p, ignore_errors=False, onerror=_rmtree_onerror)
        except FileNotFoundError:
            pass
        except Exception:
            log.warning("Error removing temp directory: %s", p, exc_info=True)

def cleanup_old_tmp(
    prefix: str = "yt-transcript-",
    max_age_sec: int = 3600,
    base_dir: Optional[Path] = None,
) -> int:
    import shutil
    base = base_dir or Path(tempfile.gettempdir())
    now = time.time(); removed = 0
    for d in base.glob(prefix + "*"):
        try:
            if d.is_symlink() or not d.is_dir():
                continue
            age = now - d.stat().st_mtime
            if age > max_age_sec:
                shutil.rmtree(d, ignore_errors=False, onerror=_rmtree_onerror)
                removed += 1
        except FileNotFoundError:
            continue
        except Exception:
            log.warning("Failed cleaning %s", d, exc_info=True)
    return removed
