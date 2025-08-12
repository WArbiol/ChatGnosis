import streamlit as st
from src.rag_engine import RAGEngine
import html

def load_custom_css():
    """
    Função para injetar nosso CSS customizado para cores e estilos.
    """
    st.markdown("""
        <style>
            /* --- ESTILO PARA A CAIXA DE FONTES --- */
            .source-text-box {
                background-color: #1c1f2b; /* Cor de fundo secundária do nosso tema */
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Source Code Pro', 'Monaco', 'courier', monospace;
                white-space: pre-wrap !important; 
                word-wrap: break-word !important; 
            }

            /* --- ADICIONANDO NOSSAS CORES ESPECIAIS --- */

            /* Título principal em AMARELO */
            h1 {
                color: #facc15; /* Um tom de amarelo/dourado */
            }

            /* Texto 'Fonte:' em VERMELHO */
            div[data-testid="stExpander"] strong {
                color: #ef4444; /* Um tom de vermelho */
            }

            /* Borda do st.info em AZUL (combinando com o tema) */
            div[data-testid="stAlert"] {
                border-color: #3b82f6 !important;
            }

        </style>
        """, unsafe_allow_html=True)

def build_interface():
    st.set_page_config(page_title="Chat - PDFs Gnosis", layout="wide")
    load_custom_css()

    @st.cache_resource
    def get_rag_engine():
        return RAGEngine()
    rag_engine = get_rag_engine()

    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("Chat Gnosis 💎")
    st.info("Olá! Sou seu assistente de pesquisa Gnóstica. Posso cometer erros, sempre leia as Fontes dos Mestres.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("Ver Fontes Utilizadas"):
                    for source in message["sources"]:
                        st.markdown(f"**Fonte:** `{source['metadata']['source']}`")
                        st.code(source['text'], language=None)


    if user_query := st.chat_input("Faça sua pergunta..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            sources_placeholder = st.empty()
            
            full_response = ""
            sources_content = []

            for chunk in rag_engine.query_stream(user_query):
                if chunk["type"] == "response_chunk":
                    full_response += chunk["content"]
                    response_placeholder.markdown(full_response + "▌") # Efeito de cursor
                elif chunk["type"] == "sources":
                    sources_content = chunk["content"]
                    with sources_placeholder.expander("Ver Fontes Utilizadas"):
                        for source in sources_content:
                            st.markdown(f"**Fonte:** `{source['metadata']['source']}`")
                            st.code(source['text'], language=None, wrap_lines=True)
                elif chunk["type"] == "error":
                    full_response = chunk["content"]
                    response_placeholder.error(full_response)
            
            # Remove o cursor no final
            response_placeholder.markdown(full_response)
        
        # Adiciona a resposta completa e as fontes ao histórico
        st.session_state.messages.append({
            "role": "assistant", 
            "content": full_response,
            "sources": sources_content
        })