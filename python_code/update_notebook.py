import json
import os

# Caminho para o notebook
notebook_path = "c:/Users/aleju/Documentos (local)/Dev/Faculdade/Projeto Integrador/Chatbot/coffee-shop-app-with-chatbot/python_code/build_vector_database.ipynb"

# Ler o conteúdo do notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook_content = json.load(f)

# Procurar e atualizar células específicas
for cell in notebook_content["cells"]:
    if cell["cell_type"] == "code" and isinstance(cell.get("source"), list):
        # Célula 1 - RunPod comment
        if any("# Se usar RunPod: " in line for line in cell["source"]):
            # Atualizar para usar apenas SentenceTransformer
            new_source = []
            for line in cell["source"]:
                if "# Se usar RunPod: " in line:
                    new_source.append(
                        "# Código antigo (RunPod) foi substituído por SentenceTransformer:\n")
                elif "# output = client.embeddings.create" in line:
                    continue  # Remover esta linha
                elif "# embedding = output.data[0].embedding" in line:
                    continue  # Remover esta linha
                else:
                    new_source.append(line)
            cell["source"] = new_source

        # Célula 2 - RunPod embeddings comment
        if any("# Com RunPod: embeddings = output.data[0].embedding" in line for line in cell["source"]):
            new_source = []
            for line in cell["source"]:
                if "# Com RunPod: embeddings = output.data[0].embedding" in line:
                    new_source.append(
                        "# Usando SentenceTransformer para embeddings locais:\n")
                else:
                    new_source.append(line)
            cell["source"] = new_source

        # Célula 3 - RunPod client.embedding.create
        if any("# Com RunPod: output = client.embedding.create" in line for line in cell["source"]):
            new_source = []
            for line in cell["source"]:
                if "# Com RunPod: output = client.embedding.create" in line:
                    new_source.append(
                        "# Substituído código do RunPod por SentenceTransformer para embeddings locais:\n")
                elif "embedding = np.array(output.data)" in line:
                    new_source.append(
                        "embedding = output  # embedding já está no formato correto\n")
                else:
                    new_source.append(line)
            cell["source"] = new_source

# Salvar o notebook atualizado
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, ensure_ascii=False)

print("Notebook atualizado com sucesso!")
