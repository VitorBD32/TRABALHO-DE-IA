from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

import subprocess

def get_windows_ip():
    try:
        output = subprocess.check_output(["ip", "route"]).decode()
        for line in output.split("\n"):
            if "default via" in line:
                return line.split()[2]
    except Exception:
        pass
    return "localhost"

def test_rag():
    # 1. Carregar os Embeddings e o FAISS
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    # 2. Configurar o Retriever (k=3)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # 3. Configurar a API do Ollama Local
    host_ip = get_windows_ip()
    llm = Ollama(model="gemma", base_url=f"http://{host_ip}:11434", temperature=0)
    
    # 4. Criar o Template de Prompt estrito
    template = """Você é um assistente prestativo. Responda à pergunta baseando-se EXCLUSIVAMENTE no contexto fornecido abaixo.
Se a resposta não estiver contida no contexto, responda: "Não há informação suficiente nos documentos fornecidos para responder a essa pergunta." Não tente inventar uma resposta.

Contexto:
{context}

Pergunta: {question}

Resposta:"""
    
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    
    # 5. Testar com uma pergunta do requisito
    print("--- Testando RAG ---")
    pergunta = "Qual a importância da função hash para o registro de software?"
    print(f"Pergunta: {pergunta}\n")
    
    # Busca manual dos documentos (Retrieval)
    docs = retriever.invoke(pergunta)
    
    # Prepara o contexto como uma string única
    contexto = "\n\n".join([doc.page_content for doc in docs])
    
    # Chama o LLM (Geração)
    prompt_final = prompt.format(context=contexto, question=pergunta)
    resposta = llm.invoke(prompt_final)
    
    print("RESPOSTA DO MODELO:")
    print(resposta)
    print("\nFONTES UTILIZADAS:")
    for i, doc in enumerate(docs):
        fonte = doc.metadata.get('fonte', 'Desconhecida')
        pagina = doc.metadata.get('pagina', 'N/A')
        print(f"[{i+1}] Fonte: {fonte} - Página: {pagina}")

if __name__ == "__main__":
    test_rag()
