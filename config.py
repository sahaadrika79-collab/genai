import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# API KEY
# ==========================

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# ==========================
# Paths
# ==========================

UPLOAD_FOLDER = "uploads"

CHROMA_PATH = "chroma_db"

# ==========================
# Chunk Settings
# ==========================

CHUNK_SIZE = 500

CHUNK_OVERLAP = 50

# ==========================
# Models
# ==========================

EMBEDDING_MODEL = "mistral-embed"

LLM_MODEL = "mistral-small-latest"

# ==========================
# Retriever
# ==========================

TOP_K = 3

FETCH_K = 5