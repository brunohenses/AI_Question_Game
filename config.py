import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# --- Configurações de Ambiente ---
# Chave de API do OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.warning("OPENAI_API_KEY não encontrada em variáveis de ambiente. Modo offline ativado.")

# Diretórios base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Arquivos de dados
PERGUNTAS_FILE = DATA_DIR / "perguntas.json"
CACHE_FILE = DATA_DIR / "cache.json"
STATS_FILE = DATA_DIR / "stats.json"
ENV_FILE = BASE_DIR / ".env"

# Configuração de Logging
LOG_FILE = BASE_DIR / "app.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Modelos e parâmetros de API
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.8))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 200))