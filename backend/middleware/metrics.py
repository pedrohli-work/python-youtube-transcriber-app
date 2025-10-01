import time
from backend.db.models import log_metric

class StepTimer:
    def __init__(self, video_id: str, step: str):
        self.video_id = video_id
        self.step = step
        self.t0 = None
    def __enter__(self):
        self.t0 = time.perf_counter()
        return self  # garante 'as t' funcional
    def __exit__(self, exc_type, exc, tb):
        dt = max(0.0, time.perf_counter() - self.t0)
        outcome = "error" if exc else "success"
        err_code = getattr(exc, "code", None) if exc else None
        log_metric(self.video_id or "", self.step, dt, outcome, err_code)
        return False
