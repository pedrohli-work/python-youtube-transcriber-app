from yt_dlp import YoutubeDL
from pathlib import Path
from backend.services.errors import DOWNLOAD_ERROR

def _opts(outtmpl):
    return {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "quiet": True, "no_warnings": True,
        "retries": 10, "fragment_retries": 10, "socket_timeout": 30,
        "user_agent": "Mozilla/5.0",
        "postprocessors": [{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}],
    }

def get_info(url: str):
    with YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True, "forcejson": True}) as ydl:
        return ydl.extract_info(url, download=False)

def has_captions(info: dict) -> bool:
    return bool(info.get("subtitles") or info.get("automatic_captions"))

def download_audio(url: str, outdir: Path):
    try:
        outdir.mkdir(parents=True, exist_ok=True)
        with YoutubeDL(_opts(str(outdir / "%(id)s.%(ext)s"))) as ydl:
            info = ydl.extract_info(url, download=True)
        vid = info.get("id")
        mp3 = list(outdir.glob(f"{vid}.mp3")) or list(outdir.glob("*.mp3"))
        if not mp3:
            raise DOWNLOAD_ERROR()
        return mp3[0], info
    except Exception:
        raise DOWNLOAD_ERROR()

def download_captions(url: str, outdir: Path, prefer_sub_lang: str | None = None) -> Path | None:
    """Tenta baixar VTT. Primeiro 'subtitles' (manuais), depois 'automatic_captions'.
       Em caso de erro, retorna None para permitir fallback ao ASR."""
    outdir.mkdir(parents=True, exist_ok=True)
    base = str(outdir / "%(id)s.%(ext)s")
    opts_primary = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": False,
        "subtitlesformat": "vtt",
        "subtitleslangs": [prefer_sub_lang] if prefer_sub_lang else ["en","pt","pt-BR","es","fr"],
        "outtmpl": base,
        "quiet": True, "no_warnings": True
    }
    opts_auto = dict(opts_primary); opts_auto["writesubtitles"]=False; opts_auto["writeautomaticsub"]=True

    def _try(opts):
        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
            vid = info.get("id")
            cand = list(outdir.glob(f"{vid}.vtt")) or list(outdir.glob("*.vtt"))
            return cand[0] if cand else None
        except Exception:
            return None

    return _try(opts_primary) or _try(opts_auto)
