from fastapi import HTTPException

class AppError(HTTPException):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        super().__init__(status_code=status_code, detail={"error": {"code": code, "message": message}})

URL_INVALID = lambda: AppError("URL_INVALID", "Invalid YouTube URL.", 400)
RATE_LIMITED = lambda: AppError("RATE_LIMITED", "Rate limit exceeded.", 429)
DURATION_EXCEEDED = lambda cap: AppError("DURATION_EXCEEDED", f"Video exceeds {cap} minutes.", 400)
CAPTIONS_FETCH_ERROR = lambda: AppError("CAPTIONS_FETCH_ERROR", "Could not fetch captions.", 502)
DOWNLOAD_ERROR = lambda: AppError("DOWNLOAD_ERROR", "Failed to download audio.", 502)
ASR_FAILED = lambda: AppError("ASR_FAILED", "ASR processing failed.", 500)
TRANSLATION_MISSING = lambda: AppError("TRANSLATION_MISSING", "PT-BR translation not available.", 400)
