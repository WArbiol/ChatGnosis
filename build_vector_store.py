import os
import shutil
from src.ingestion_pipeline import run_ingestion_for_file
from config import PDF_DIR, VECTOR_STORE_DIR

def main():
    """
    Script para construir ou reconstruir o banco de dados vetorial do zero.
    Ele lê todos os PDFs da pasta 'data/pdfs' e os processa.
    """

    # Passo 1: Limpar o banco de dados antigo para garantir consistência
    if os.path.exists(VECTOR_STORE_DIR):
        shutil.rmtree(VECTOR_STORE_DIR)

    os.makedirs(VECTOR_STORE_DIR)
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith('.pdf')]

    if not pdf_files:
        return

    for pdf_file in pdf_files:
        file_path = os.path.join(PDF_DIR, pdf_file)
        try:
            run_ingestion_for_file(file_path)
        except Exception as e:
            print(f"!!!!!! Erro ao processar o arquivo {pdf_file}: {e} !!!!!!")

if __name__ == "__main__":
    main()