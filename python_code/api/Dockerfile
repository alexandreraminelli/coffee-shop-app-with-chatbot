# Configuração do container do Docker para a API

# Definir a imagem base
FROM python:3.13.4-slim

# Abrir e definir o diretório de trabalho
RUN mkdir /app
WORKDIR /app

# Copiar o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt requirements.txt
# Instalar as dependências do Python
RUN pip install -r requirements.txt

# Copiar o restante do código necessário da API para o diretório de trabalho
COPY recommendation_objects/ recommendation_objects/
COPY agents/ agents/
COPY agent_controller.py agent_controller.py 
COPY main.py main.py

# Testar o Docker (remover na produção)
# COPY test_input.json test_input.json

# Executar código
ENTRYPOINT [ "python", "main.py" ]
