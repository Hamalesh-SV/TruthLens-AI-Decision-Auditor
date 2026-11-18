import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = "llama3.1:8b"

# Construct absolute paths to avoid directory execution issues
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'sql_db', 'company_metrics.db')}"
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")