from pathlib import Path

# Carrega .env local automaticamente. Em Docker, variáveis vêm do compose.
try:
    from dotenv import load_dotenv  # requer 'python-dotenv' no requirements
    ROOT = Path(__file__).resolve().parents[1]
    load_dotenv(ROOT / ".env", override=False)
except Exception:
    pass
