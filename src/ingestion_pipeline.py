from src.data_ingestion import load_and_chunk_pdf
from src.vector_db_manager import VectorDBManager

def run_ingestion_for_file(file_path):
    chunks = load_and_chunk_pdf(file_path)
    
    if not chunks:
        print(f"Nenhum texto extraído de {file_path}. Pulando.")
        return

    db_manager = VectorDBManager()
    db_manager.add_document(chunks)