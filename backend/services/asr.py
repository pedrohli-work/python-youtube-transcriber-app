from faster_whisper import WhisperModel
from backend.utils.config import MODEL_SIZE
from backend.services.translate import to_ptbr
from backend.services.errors import ASR_FAILED

_model = None

def _get_model():
    global _model
    if _model is None:
        # CPU, com quantização leve (int8)
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return _model

def transcribe(audio_path, target_lang="original"):
    try:
        model = _get_model()
        task = "translate" if target_lang == "en" else "transcribe"
        segs, info = model.transcribe(
            str(audio_path),
            task=task,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            beam_size=5, best_of=5
        )
        lines = [s.text.strip() for s in segs if s.text and s.text.strip()]
        if target_lang == "pt-BR":
            lines = to_ptbr(lines)
        return lines, info.language, segs
    except Exception:
        raise ASR_FAILED()
