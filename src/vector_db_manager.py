import chromadb
from sentence_transformers import SentenceTransformer
from config import VECTOR_STORE_DIR, EMBEDDING_MODEL_NAME
import os
import torch

class VectorDBManager:
    def __init__(self):
        self.device = 'cpu'
        self.client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
        self.model = SentenceTransformer(
            model_name_or_path=EMBEDDING_MODEL_NAME,
            device=self.device,
        )
        self.collection = self.client.get_or_create_collection(
            name="documentos",
            embedding_function=None # Vamos gerar os embeddings manualmente
        )

    def add_document(self, chunks_with_metadata):
        """Adiciona os chunks de um documento ao banco de dados vetorial."""
        if not chunks_with_metadata:
            return

        texts = [item['text'] for item in chunks_with_metadata]
        metadatas = [item['metadata'] for item in chunks_with_metadata]
        
        embeddings = self.model.encode(texts, show_progress_bar=False).tolist()

        # Cria IDs únicos para cada chunk
        ids = [f"{item['metadata']['source']}_chunk{item['metadata']['chunk_num']}" for item in chunks_with_metadata]

        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def delete_document(self, filename):
        """Remove todos os vetores associados a um arquivo específico."""
        self.collection.delete(where={"source": filename})


    def query(self, query_text: str, top_k: int = 5) -> list[dict]:
        """
        Realiza uma busca por similaridade no banco de dados vetorial.
        Retorna os 'top_k' chunks mais relevantes para a consulta.
        """
        # 1. Gera o embedding para a pergunta do usuário
        query_embedding = self.model.encode(query_text, show_progress_bar=False).tolist()

        # 2. Realiza a busca no ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_docs = []
        for i in range(len(results['ids'][0])):
            retrieved_docs.append({
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i]
            })

        return retrieved_docs
