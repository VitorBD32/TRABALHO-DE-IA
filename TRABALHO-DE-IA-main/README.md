# Sistema RAG - Registro de Software (INPI) 🤖📚

Este projeto é um sistema de **RAG (Retrieval-Augmented Generation)** desenvolvido como avaliação final para a disciplina de Tópicos em Inteligência Artificial. Ele utiliza documentos oficiais do INPI (Manual do Usuário para Registro Eletrônico de Programas de Computador) como base de conhecimento para responder perguntas de forma precisa, evitando alucinações.

## 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando um pipeline 100% gratuito e executável localmente:
- **Langchain:** Framework principal para orquestração da cadeia (Chain) do RAG.
- **FAISS:** Banco de dados vetorial para armazenamento dos embeddings e busca semântica (Retriever).
- **HuggingFace (`all-MiniLM-L6-v2`):** Modelo de Embeddings eficiente para a criação dos vetores de texto.
- **Ollama (`gemma`):** Modelo de Linguagem (LLM) do Google executado localmente para geração de respostas.
- **Streamlit:** Framework para a construção da interface gráfica (Web App).
- **PyPDF:** Biblioteca para extração e processamento de textos do PDF.

## 📁 Estrutura do Projeto

- `data/`: Contém a base de conhecimento estruturada em JSON (`base_conhecimento.json`), com os pedaços de texto (chunks) e seus metadados (fonte, página e assunto).
- `docs/`: Documentação de planejamento do projeto, roteiro, e os arquivos PDF originais.
- `faiss_index/`: Pasta gerada automaticamente que armazena os índices vetoriais salvos.
- `extract_data.py`: Script responsável por raspar as páginas do PDF original e criar o JSON.
- `build_vectorstore.py`: Script que lê a base de conhecimento, realiza a quebra dos textos (Text Splitter), gera os Embeddings e salva no FAISS.
- `rag_app.py`: Script de teste para rodar o RAG e exibir as respostas e fontes no próprio terminal.
- `app.py`: Interface Gráfica interativa desenvolvida com Streamlit.

## 🚀 Como Executar

**1. Instalar as Dependências:**
Certifique-se de instalar as bibliotecas necessárias do Python:
```bash
pip install langchain langchain-community faiss-cpu sentence-transformers streamlit pypdf langchain-huggingface
```

**2. Instalar e Rodar o Ollama:**
Baixe o [Ollama](https://ollama.com/) e instale o modelo utilizado no projeto:
```bash
ollama run gemma
```

**3. Gerar o Banco Vetorial:**
```bash
python build_vectorstore.py
```
*(Isso criará a pasta `faiss_index` na raiz do projeto)*.

**4. Executar a Interface Gráfica:**
```bash
python -m streamlit run app.py
```
Acesse o endereço local fornecido no terminal (geralmente `http://localhost:8501`) para interagir com o Chatbot!

---
**Disciplina:** Tópicos em Inteligência Artificial  
**Professor:** Aldir Silva Sousa, Dsc.
