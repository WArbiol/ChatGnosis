from litellm.google_genai import generate_content_stream
from google.genai.types import ContentDict, PartDict
from src.vector_db_manager import VectorDBManager
import streamlit as st
import json

class RAGEngine:
    def __init__(self):
        self.db_manager = VectorDBManager()
        self.api_key = st.secrets["GOOGLE_API_KEY"]

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

        contents = ContentDict(parts=[PartDict(text=prompt)], role="user")

        try:
            stream = generate_content_stream(
                model="gemini/gemini-2.0-flash",  # ou "gemini/gemini-1.5-flash" se preferir
                contents=contents,
                max_output_tokens=1500,
                api_key=self.api_key
            )

            # 5. Itera sobre cada pedaço recebido
            for chunk in stream:
                data = json.loads(chunk[len(b"data: "):])
                if "candidates" in data:
                    text = data["candidates"][0]["content"]["parts"][0].get("text", "")
                    if text:
                        yield {"type": "response_chunk", "content": text}

            # 6. Ao final, retorna também as fontes
            yield {"type": "sources", "content": context_docs}

        except Exception as e:
            yield {"type": "error", "content": f"Erro ao contatar a API do Google via LiteLLM: {e}"}