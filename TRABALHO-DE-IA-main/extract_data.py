import json
from pypdf import PdfReader

def extract_pages():
    reader = PdfReader("docs/manual-e-software-2022.pdf")
    
    # Páginas 8 a 15 (índices 7 a 14, já que começa no 0)
    start_page = 7
    end_page = 14
    
    documentos = []
    
    for i in range(start_page, end_page + 1):
        page = reader.pages[i]
        text = page.extract_text()
        
        # Limpar um pouco o cabeçalho/rodapé se quiser, mas o Langchain também lidará bem
        # Vamos estruturar como Dicionário com metadados para cumprir os requisitos
        
        doc = {
            "page_content": text,
            "metadata": {
                "fonte": "Manual_e-Software_2022.pdf",
                "pagina": i + 1,
                "assunto": "Regras de Registro e Segurança Jurídica"
            }
        }
        documentos.append(doc)
        
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/base_conhecimento.json", "w", encoding="utf-8") as f:
        json.dump(documentos, f, ensure_ascii=False, indent=4)
        
    print(f"Extraídas {len(documentos)} páginas com sucesso e salvas em data/base_conhecimento.json")

if __name__ == "__main__":
    extract_pages()
