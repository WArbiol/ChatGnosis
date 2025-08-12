import google.generativeai as genai
from src.vector_db_manager import VectorDBManager
import streamlit as st

class RAGEngine:
    def __init__(self):
        self.db_manager = VectorDBManager()
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def _build_prompt(self, query: str, context: list[dict]) -> str:
        """
        Constrói o prompt para o LLM com base na pergunta e no contexto recuperado.
        """
        context_text = "\n\n---\n\n".join([f"Fonte: {doc['metadata']['source']}\n\nTrecho: {doc['text']}" for doc in context])

        prompt_template = f"""
        Você é um assistente especialista nos documentos fornecidos. Sua tarefa é responder à pergunta do usuário de forma clara e concisa, baseando-se ESTRITAMENTE no contexto abaixo.

        CONTEXTO FORNECIDO:
        {context_text}

        PERGUNTA DO USUÁRIO:
        {query}

        INSTRUÇÕES:
        - Se o contexto não contiver a resposta, diga "Com base nos documentos fornecidos, não encontrei uma resposta para essa pergunta."
        - Não invente informações.
        - Responda em português.
        - Ao final da sua resposta, cite as fontes que utilizou no formato [Fonte: nome_do_arquivo.pdf].

        RESPOSTA:
        """
        return prompt_template

    def query_stream(self, query: str):
        """
        Executa o pipeline completo de RAG: busca -> construção de prompt -> geração.
        """
        context_docs = self.db_manager.query(query_text=query, top_k=4)

        if not context_docs:
            yield {"type": "error", "content": "Não foi possível encontrar informações relevantes nos documentos."}
            return
        
        prompt = self._build_prompt(query, context_docs)

        try:
            stream = self.model.generate_content(prompt, stream=True)

            for chunk in stream:
                yield {"type": "response_chunk", "content": chunk.text}
            
            yield {"type": "sources", "content": context_docs}

        except Exception as e:
            yield {"type": "error", "content": f"Erro ao contatar a API do Google: {e}"}