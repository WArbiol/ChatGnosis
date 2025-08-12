import fitz 
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import re

def clean_extracted_text(text: str) -> str:
    """
    Aplica uma série de limpezas em um bloco de texto extraído de um PDF.
    """
    # 1. Juntar palavras hifenizadas que foram quebradas no final da linha
    text = re.sub(r"-\n", "", text)

    # 2. Remover quebras de linha que não terminam um parágrafo.
    # Esta é a parte mais complexa. A lógica é: junte uma linha com a próxima
    # se a linha atual NÃO terminar com um ponto final ou pontuação similar.
    # Exceções são feitas para títulos e cabeçalhos.
    # Usamos re.VERBOSE para comentar o regex e torná-lo legível.
    paragraph_merge_pattern = re.compile(r"""
        ( # Início do grupo de captura
        [^\n] # Captura qualquer caractere que não seja uma quebra de linha
        (?<![.!?:]) # Lookbehind negativo: garante que o caractere anterior NÃO seja ., !, ?, :
        ) # Fim do grupo de captura
        \n # A quebra de linha que queremos potencialmente remover
        (?![A-ZÁÉÍÓÚ]) # Lookahead negativo: garante que a próxima linha NÃO comece com maiúscula (indicando novo parágrafo)
        (?!\s*•) # Garante que a próxima linha não seja um item de lista
    """, re.VERBOSE)
    text = paragraph_merge_pattern.sub(r"\1 ", text)


    # 3. Remover numeração de páginas ou linhas (ex: "123 - texto" ou "123. texto")
    # Remove números no início da linha, seguidos opcionalmente por ponto ou hífen.
    line_number_pattern = re.compile(r"^\s*\d+[\s.-]*", re.MULTILINE)
    text = line_number_pattern.sub("", text)
    
    # 4. Remover linhas que são apenas cabeçalhos ou rodapés repetitivos (heurística)
    # Remove linhas curtas (até 5 palavras) que aparecem com frequência.
    # Esta é uma limpeza mais avançada e opcional. (varia muito de pdf para pdf)

    # 5. Normalizar espaços em branco
    # Substitui múltiplos espaços/quebras de linha por um único espaço/quebra de linha.
    text = re.sub(r"[ \t]+", " ", text) # Múltiplos espaços por um só
    text = re.sub(r"\n{3,}", "\n\n", text) # Múltiplas quebras de linha por duas

    return text.strip()

def load_and_chunk_pdf(file_path):
    filename = os.path.basename(file_path)
    
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Erro ao abrir o arquivo {filename}: {e}")
        return []

    chunks_with_metadata = []

    # Configura o divisor de texto
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )

    full_text = ""
    for page_num, page in enumerate(doc):
        full_text += page.get_text() + "\n"

    cleaned_text = clean_extracted_text(full_text)
    chunks = text_splitter.split_text(cleaned_text)

    for i, chunk in enumerate(chunks):
        chunks_with_metadata.append({
            "text": chunk,
            "metadata": {
                "source": filename,
                "chunk_num": i
            }
        })
    
    doc.close()
    return chunks_with_metadata