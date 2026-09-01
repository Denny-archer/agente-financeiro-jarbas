import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Limites de alerta por categoria (ajuste conforme necessário)
LIMITES_POR_CATEGORIA = {
    "Supermercado": float(os.getenv("LIMITE_SUPERMERCADO", 500)),
    "Streaming": float(os.getenv("LIMITE_STREAMING", 100)),
}
