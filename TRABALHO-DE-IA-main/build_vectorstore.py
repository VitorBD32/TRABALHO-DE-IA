import json
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def main():
    # 1. Carregar os documentos do JSON criado
    print("Carregando documentos...")
    with open("data/base_conhecimento.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Converter para objetos Document do Langchain
    docs = []
    for item in dados:
        docs.append(Document(
            page_content=item["page_content"],
            metadata=item["metadata"]
        ))

    # 2. Dividir os textos em Chunks (Pedaços menores)
    print("Dividindo textos em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Total de {len(chunks)} chunks gerados.")

    # 3. Gerar Embeddings (Usando modelo local gratuito do HuggingFace)
    # 'all-MiniLM-L6-v2' é um modelo pequeno, leve e muito rápido para português/inglês
    print("Iniciando geração de Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Criar e armazenar o Vector Store com FAISS
    print("Criando o Vector Store FAISS...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Salvar localmente
    vectorstore.save_local("faiss_index")
    print("Vector Store salvo com sucesso na pasta 'faiss_index'.")

if __name__ == "__main__":
    main()
