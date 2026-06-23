import streamlit as st
import subprocess
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# 1. Configurações Iniciais da Página
st.set_page_config(page_title="RAG INPI Chatbot", page_icon="🤖", layout="centered")

# 2. Funções em cache para não carregar o banco de dados e modelo a cada mensagem
@st.cache_data
def get_windows_ip():
    try:
        output = subprocess.check_output(["ip", "route"]).decode()
        for line in output.split("\n"):
            if "default via" in line:
                return line.split()[2]
    except Exception:
        pass
    return "localhost"

@st.cache_resource
def load_rag_pipeline():
    # Carrega Embeddings e Banco FAISS
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # Carrega o Ollama
    host_ip = get_windows_ip()
    llm = Ollama(model="gemma", base_url=f"http://{host_ip}:11434", temperature=0)
    
    template = """Você é um assistente especialista do INPI. Use APENAS o contexto abaixo para responder à pergunta. 
Seja claro e responda em português.

Contexto:
{context}

Pergunta: {question}

Resposta:"""
    
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    
    return retriever, llm, prompt

# Carregar tudo
with st.spinner("Carregando base de dados do INPI..."):
    retriever, llm, prompt = load_rag_pipeline()

# 3. Interface de Usuário
st.title("🤖 Chatbot do INPI - Registro de Software")
st.markdown("Bem-vindo! Este chatbot responde a perguntas usando um sistema RAG baseado no Manual de Registro Eletrônico de Programas de Computador do INPI.")

st.divider()

# Campo de pergunta
pergunta = st.text_input("Faça sua pergunta sobre o registro de software:")

if st.button("Buscar Resposta") and pergunta:
    with st.spinner("Buscando informações nos documentos e gerando resposta..."):
        try:
            # Busca os chunks relevantes no banco de dados
            docs = retriever.invoke(pergunta)
            contexto = "\n\n".join([doc.page_content for doc in docs])
            
            # Formata o prompt e chama o modelo
            prompt_final = prompt.format(context=contexto, question=pergunta)
            resposta = llm.invoke(prompt_final)
            
            # Exibe a resposta
            st.success("Resposta gerada com sucesso!")
            st.markdown(f"**Resposta:** \n\n {resposta}")
            
            # Exibe as Fontes Expandidas
            with st.expander("📚 Ver Fontes Utilizadas"):
                for i, doc in enumerate(docs):
                    fonte = doc.metadata.get('fonte', 'Desconhecida')
                    pagina = doc.metadata.get('pagina', 'N/A')
                    st.markdown(f"**Fonte {i+1}:** Arquivo `{fonte}` - Página `{pagina}`")
                    st.caption(f"*Trecho recuperado:* {doc.page_content[:200]}...")
        except Exception as e:
            st.error(f"Erro ao gerar a resposta: {str(e)}")
            st.info("Verifique se o aplicativo Ollama está aberto no Windows (ícone perto do relógio) e a chave 'Expose to Network' está ativada.")
