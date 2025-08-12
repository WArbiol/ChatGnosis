# 🤖 Chat Gnosis: Uma Aplicação de RAG com LLMs

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red.svg)](https://streamlit.io)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2-orange.svg)](https://pytorch.org/)
[![Licença: MIT](https://img.shields.io/badge/Licença-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma aplicação inteligente de Q&A que permite conversar com uma grande coleção de documentos PDF, utilizando um pipeline de **Retrieval-Augmented Generation (RAG)** para fornecer respostas fiéis, rápidas e com fontes citadas.

---

## 🎥 Demonstração

![Placeholder para o GIF da aplicação](https://i.imgur.com/your-gif-placeholder.gif)

---

## 💡 Sobre o Projeto

Este projeto busca responder as perguntas do usuário com base em um banco de dados alimentado por livros Gnóstico, possui uma aplicação web completa, modular e pronta para deploy, demonstrando práticas modernas de engenharia de software para sistemas de IA. O objetivo é criar uma ferramenta de pesquisa semântica robusta, onde um usuário pode fazer perguntas complexas em linguagem natural e receber respostas sintetizadas a partir de uma base de conhecimento privada de dezenas (ou centenas) de documentos.

A arquitetura foi cuidadosamente planejada para separar as responsabilidades, garantindo que a aplicação seja escalável, de fácil manutenção e flexível para futuras expansões.

## 🚀 Tecnologias e Arquitetura

A aplicação é construída sobre um stack tecnológico moderno e eficiente, escolhido para otimizar tanto a performance quanto a experiência de desenvolvimento.

### **Frontend**

- **Streamlit:** Utilizado para a criação de uma interface de usuário reativa, bonita e interativa com poucas linhas de código Python. A escolha ideal para prototipagem rápida e desenvolvimento de aplicações de dados.

### **Backend & Lógica de IA (Pipeline RAG)**

O coração da aplicação é um pipeline de Retrieval-Augmented Generation (RAG) customizado, dividido em duas fases principais:

#### 1. **Indexação (A Memória da IA)**

Este processo offline transforma os documentos PDF em uma base de conhecimento vetorial otimizada para buscas rápidas.

- **Extração de Texto:** `PyMuPDF` foi escolhido por sua alta performance e eficiência na extração de texto bruto de PDFs.
- **Fragmentação Semântica:** `langchain-text-splitters` é utilizado para quebrar os textos em "chunks" de forma inteligente, preservando o contexto ao evitar quebras no meio de sentenças ou parágrafos.
- **Vetorização (Embeddings):** `sentence-transformers` é usado para carregar e executar modelos de embedding de última geração (`BAAI/bge-m3`). Esta etapa converte os chunks de texto em vetores numéricos que capturam seu significado semântico.
- **Banco de Dados Vetorial:** `ChromaDB` atua como nosso banco de dados vetorial local e persistente, armazenando os embeddings e metadata para permitir buscas por similaridade em milissegundos.

#### 2. **Recuperação e Geração (O Raciocínio da IA)**

Este processo online é ativado a cada pergunta do usuário.

- **Motor de Geração (LLM):** O motor é desacoplado, permitindo o uso de LLMs locais via **Ollama** (como `Qwen2`, `Llama 3`, `Phi-3`) para desenvolvimento e privacidade, ou a integração com APIs de nuvem (**Google Gemini API**) para um deploy escalável e de baixo custo. Esta flexibilidade arquitetural é um dos pontos fortes do projeto.
- **Prompt Engineering:** Uma estratégia de prompt robusta é utilizada para instruir o LLM a basear suas respostas estritamente no contexto recuperado, citar as fontes e evitar "alucinações", garantindo a fidelidade da informação.

## ✨ Funcionalidades

- [x] **Interface Reativa e Moderna:** Tema escuro customizável com CSS.
- [x] **Chat em Tempo Real:** Respostas geradas por streaming, com efeito de "digitação".
- [x] **Fidelidade e Citação de Fontes:** A IA exibe os trechos exatos dos documentos originais que usou para formular a resposta.
- [x] **Pipeline de Ingestão Desacoplado:** Um script dedicado para processar e indexar os documentos, separando o "modo admin" do "modo usuário".
- [x] **Suporte a GPU:** O código é capaz de detectar e utilizar GPUs NVIDIA para uma aceleração massiva no processamento dos modelos, tanto para embeddings quanto para a geração de texto.
- [x] **Pronto para Deploy:** Arquitetura projetada com deploy em mente, separando o código-fonte dos artefatos de dados.

## 🔧 Instalação e Execução

Para executar este projeto localmente, siga os passos abaixo:

**1. Pré-requisitos:**

- Python 3.9 ou superior
- Git
- (Opcional, para rodar LLM local) [Ollama](https://ollama.com/) instalado.
- (Opcional, para aceleração) GPU NVIDIA com drivers e CUDA Toolkit configurados.

**2. Clone o Repositório:**

```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_SEU_REPOSITORIO.git)
cd NOME_DO_SEU_REPOSITORIO
```

**3. Crie e Ative um Ambiente Virtual:**

```bash
python -m venv venv
source venv/bin/activate  # No macOS/Linux
# ou
.\venv\Scripts\activate  # No Windows
```

**4. Instale as Dependências:**

```bash
pip install -r requirements.txt
```

_(Lembre-se: para suporte a GPU, instale a versão do PyTorch com CUDA, conforme o site oficial)._

**5. Configure suas Chaves de API (se aplicável):**

- Se for usar a API do Google Gemini, crie o arquivo `.streamlit/secrets.toml` e adicione sua chave:
  ```toml
  GOOGLE_API_KEY = "SUA_CHAVE_API_AQUI"
  ```

**6. Prepare a Base de Conhecimento:**

- Coloque seus arquivos PDF na pasta `data/pdfs/`.
- Execute o script de ingestão uma única vez:
  ```bash
  python scripts/build_vector_store.py
  ```

**7. Execute a Aplicação:**

- (Se usar Ollama) Certifique-se de que o Ollama está rodando com o modelo desejado (ex: `ollama run qwen2`).
- Inicie a aplicação Streamlit:
  ```bash
  streamlit run app.py
  ```

## ☁️ Preparado para Deploy

Esta aplicação foi projetada para ser facilmente implantada usando padrões modernos:

- **Frontend:** Pode ser implantado gratuitamente no **Streamlit Community Cloud**.
- **Base de Conhecimento:** A pasta `vector_store` gerada pode ser hospedada em um serviço de armazenamento de artefatos como o **Hugging Face Hub**, mantendo o repositório Git leve.
- **LLM Backend:** A arquitetura suporta a troca do Ollama por uma chamada de API (como a do Gemini), permitindo um deploy "serverless" de baixo custo e alta escalabilidade.

## 👨‍💻 Autor

**Walter Melhado Arbiol Forné**

- **LinkedIn:** [linkedin.com/in/walter-melhado-arbiol-forne-818656211/](https://www.linkedin.com/in/walter-melhado-arbiol-forne-818656211/)
- **GitHub:** [github.com/WArbiol](https://https://github.com/WArbiol)
- **Email:** [walterarbiol@gmail.com](mailto:walterarbiol@gmail.com)

## 📜 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
