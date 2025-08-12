import os
from huggingface_hub import snapshot_download
from pathlib import Path

EMBEDDING_MODEL_NAME = "BAAI/bge-m3"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"

VECTOR_STORE_DIR = Path("/tmp/vector_store")
HF_REPO_ID = "WArbiol/gnostic-chat"


def create_folders():
    """Garante que todas as pastas necessárias para o projeto existam."""
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)


def download_vector_store_if_needed():
    """Baixa o vector store do Hugging Face Hub se não existir localmente."""
    # Esta função continua perfeita. Agora ela fará o download para /tmp/vector_store.
    if not os.path.exists(VECTOR_STORE_DIR) or not os.listdir(VECTOR_STORE_DIR):
        print(f"Baixando base de dados vetorial de {HF_REPO_ID} para {VECTOR_STORE_DIR}...")
        from huggingface_hub import snapshot_download
        snapshot_download(
            repo_id=HF_REPO_ID,
            repo_type="dataset",
            local_dir=str(VECTOR_STORE_DIR) 
        )
        print("Download concluído.")