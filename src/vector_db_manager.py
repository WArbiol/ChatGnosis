import chromadb
from sentence_transformers import SentenceTransformer
from config import VECTOR_STORE_DIR, EMBEDDING_MODEL_NAME
import streamlit as st
from google import genai
from google.genai.types import EmbedContentConfig
import time

class VectorDBManager:
    def __init__(self):
        self.device = 'cpu'
        self.client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
        self.collection = self.client.get_or_create_collection(
            name="documentos",
            embedding_function=None # Vamos gerar os embeddings manualmente
        )
        self.genai_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Gera embeddings para um lote de textos usando a API do Google."""
        try:
            result = self.genai_client.models.embed_content(
                model=EMBEDDING_MODEL_NAME,
                contents=texts,
                config=EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
            )
            return [item.values for item in result.embeddings]
        except Exception as e:
            print(f"Erro na API de embedding: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)
            return self._embed_batch(texts)

    def add_document(self, chunks_with_metadata):
        """Adiciona os chunks de um documento ao banco de dados vetorial."""
        if not chunks_with_metadata:
            return

        texts = [item['text'] for item in chunks_with_metadata]
        metadatas = [item['metadata'] for item in chunks_with_metadata]
        ids = [f"{item['metadata']['source']}_chunk{item['metadata']['chunk_num']}" for item in chunks_with_metadata]
        
        # A API do Google tem um limite de 100 textos por chamada
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]

            print(f"Processando lote {i//batch_size + 1}...")
            batch_embeddings = self._embed_batch(batch_texts)

            self.collection.add(
                embeddings=batch_embeddings,
                documents=batch_texts,
                metadatas=batch_metadatas,
                ids=batch_ids
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
        result = self.genai_client.models.embed_content(
            model=EMBEDDING_MODEL_NAME,
            contents=query_text,
            config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        query_embedding = result.embeddings[0].values
        # 2. Realiza a busca no ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_docs = [
            {
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i]
            }
            for i in range(len(results['ids'][0]))
        ]

        return retrieved_docs
