# 🤖 Chat Gnosis: Uma Aplicação de RAG com LLMs na Nuvem

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red.svg)](https://streamlit.io)
[![Google Gemini API](https://img.shields.io/badge/Google_Gemini-API-4285F4.svg)](https://ai.google.dev/)
[![Licença: MIT](https://img.shields.io/badge/Licença-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- LLMs (Large Language Models)
- Busca Vetorial (Vector Search)
- Bancos de Dados Vetoriais (ChromaDB)
- Engenharia de Prompt (Prompt Engineering)
- Hugging Face Hub
- Deploy em Nuvem (Serverless)
- Streamlit

---

Uma aplicação inteligente de Q&A que permite conversar com uma grande coleção de documentos PDF, utilizando um pipeline de **Retrieval-Augmented Generation (RAG)** para fornecer respostas fiéis, rápidas e com fontes citadas, com todo o processamento de IA executado na nuvem.

---

## 🎥 Demonstração

![Image](https://github.com/user-attachments/assets/1e5b1765-30c7-4cc4-8a5f-03a232c49b70)

&rarr; Acesse o site: [https://chatgnosis.streamlit.app/](https://chatgnosis.streamlit.app/)

---

## 💡 Sobre o Projeto

Este projeto busca responder as perguntas do usuário com base em um banco de dados alimentado por livros Gnósticos. Foi arquitetado como uma aplicação web completa, modular e pronta para deploy, demonstrando práticas modernas de engenharia de software para sistemas de IA. O objetivo é criar uma ferramenta de pesquisa semântica robusta, onde um usuário pode fazer perguntas complexas em linguagem natural e receber respostas sintetizadas a partir de uma base de conhecimento privada.

A arquitetura foi cuidadosamente planejada para separar as responsabilidades, garantindo que a aplicação seja escalável, de fácil manutenção e flexível.

## 🚀 Tecnologias e Arquitetura

A aplicação é construída sobre um stack tecnológico moderno e eficiente, otimizado para uma arquitetura "serverless" e escalável.

### **Frontend**

- **Streamlit:** Utilizado para a criação de uma interface de usuário reativa e interativa com código Python puro, ideal para o desenvolvimento rápido de aplicações de dados.

### **Backend & Lógica de IA (Pipeline RAG na Nuvem)**

O coração da aplicação é um pipeline de RAG que orquestra serviços de IA na nuvem, tornando a aplicação extremamente leve e eficiente.

#### 1. **Indexação (A Memória da IA)**

Este processo offline transforma os documentos PDF em uma base de conhecimento vetorial.

- **Extração de Texto:** `PyMuPDF` foi escolhido por sua alta performance e eficiência.
- **Fragmentação Semântica:** `langchain-text-splitters` é utilizado para quebrar os textos em "chunks" de forma inteligente, preservando o contexto.
- **Vetorização (Embeddings via API):** A criação dos vetores semânticos é feita através de chamadas à **API do Google Gemini (`text-embedding-004`)**. Isso garante embeddings de altíssima qualidade sem a necessidade de carregar modelos pesados localmente.
- **Banco de Dados Vetorial:** `ChromaDB` atua como nosso banco de dados vetorial local e persistente.

#### 2. **Recuperação e Geração (O Raciocínio da IA na Nuvem)**

Este processo online é ativado a cada pergunta do usuário.

- **Motor de Geração (LLM via API):** Toda a geração de texto é realizada pela **API do Google Gemini (`gemini-1.5-flash`)**. A aplicação envia o contexto recuperado e a pergunta do usuário, recebendo uma resposta de alta qualidade gerada pela infraestrutura massiva do Google.
- **Prompt Engineering:** Uma estratégia de prompt robusta é utilizada para instruir o LLM a basear suas respostas estritamente no contexto recuperado, garantindo a fidelidade da informação.

## ✨ Funcionalidades

- [x] **Arquitetura Serverless:** Todo o processamento pesado de IA (embeddings e geração de texto) é terceirizado para APIs de nuvem, resultando em uma aplicação leve e com baixo consumo de recursos.
- [x] **Interface Reativa e Moderna:** Tema escuro customizável com CSS.
- [x] **Chat em Tempo Real:** Respostas geradas por streaming diretamente da API, com efeito de "digitação".
- [x] **Fidelidade e Citação de Fontes:** A IA exibe os trechos exatos dos documentos originais que usou para formular a resposta.
- [x] **Pipeline de Ingestão Desacoplado:** Um script dedicado para processar e indexar os documentos, separando o "modo admin" do "modo usuário".
- [x] **Pronto para Deploy:** A aplicação foi projetada e implementada para deploy na nuvem, com gerenciamento de segredos e artefatos de dados.

## 🔧 Instalação e Execução

Para executar este projeto localmente, siga os passos abaixo:

**1. Pré-requisitos:**

- Python 3.9 ou superior
- Git

**2. Clone o Repositório:**

```bash
git clone [https://github.com/WArbiol/ChatGnosis.git](https://github.com/WArbiol/ChatGnosis.git)
cd ChatGnosis
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

**5. Configure suas Chaves de API:**

- Crie o arquivo `.streamlit/secrets.toml` e adicione sua chave da API do Google Gemini:
  ```toml
  GOOGLE_API_KEY = "SUA_CHAVE_API_AQUI"
  ```

**6. Prepare a Base de Conhecimento:**

- Coloque seus arquivos PDF na pasta `data/pdfs/`.
- Execute o script de ingestão uma única vez (requer a chave de API configurada):
  ```bash
  python scripts/build_vector_store.py
  ```

**7. Execute a Aplicação:**

- Inicie a aplicação Streamlit:
  ```bash
  streamlit run app.py
  ```

## ☁️ Arquitetura de Deploy

Esta aplicação foi implantada usando um padrão "serverless" moderno e eficiente:

- **Frontend:** Implantado gratuitamente no **Streamlit Community Cloud**.
- **Base de Conhecimento:** A pasta `vector_store` gerada é hospedada como um "dataset" no **Hugging Face Hub**, mantendo o repositório Git leve e desacoplado dos dados.
- **LLM Backend:** Toda a lógica de IA é gerenciada pela **API do Google Gemini**, permitindo um deploy de baixo custo (dentro do nível gratuito) e altíssima escalabilidade, sem a necessidade de gerenciar servidores de GPU.

## 👨‍💻 Autor

**Walter Melhado Arbiol Forné**

- **LinkedIn:** [linkedin.com/in/walter-melhado-arbiol-forne-818656211/](https://www.linkedin.com/in/walter-melhado-arbiol-forne-818656211/)
- **GitHub:** [github.com/WArbiol](https://github.com/WArbiol)
- **Email:** [walterarbiol@gmail.com](mailto:walterarbiol@gmail.com)

## 📜 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
