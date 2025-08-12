import os
from huggingface_hub import snapshot_download
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VECTOR_STORE_DIR = BASE_DIR / "data" / "vector_store"
HF_REPO_ID = "WArbiol/gnostic-chat"

DATA_DIR = BASE_DIR / "data"

PDF_DIR = DATA_DIR / "pdfs"
VECTOR_STORE_DIR = DATA_DIR / "vector_store" 

EMBEDDING_MODEL_NAME = "BAAI/bge-m3"

def download_vector_store_if_needed():
    """Baixa o vector store do Hugging Face Hub se não existir localmente."""
    if not os.path.exists(VECTOR_STORE_DIR) or not os.listdir(VECTOR_STORE_DIR):
        print(f"Baixando base de dados vetorial de {HF_REPO_ID}...")
        snapshot_download(
            repo_id=HF_REPO_ID,
            repo_type="dataset",
            local_dir=VECTOR_STORE_DIR
        )
        print("Download concluído.")