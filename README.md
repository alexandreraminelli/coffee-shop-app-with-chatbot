# Coffee Shop App com Chatbot

Este projeto implementa uma aplicação de cafeteria com um chatbot de atendimento ao cliente integrado, usando embeddings locais com SentenceTransformer e a API OpenRouter para acesso a modelos de linguagem.

## Configuração

### Pré-requisitos

- Python 3.8+ instalado
- Conexão com a Internet para baixar os pacotes e o modelo de embeddings

### Variáveis de ambiente

Copie o arquivo `.env.example` para um arquivo chamado `.env` e preencha as variáveis:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

- `OPENROUTER_API_KEY`: Chave da API do OpenRouter
- `CHATBOT_URL`: URL base da API do OpenRouter (normalmente https://openrouter.ai/api/v1)
- `MODEL_NAME`: Nome do modelo de linguagem a ser usado (ex: "meta-llama/llama-3.1-8b-instruct:free")
- `EMBEDDING_MODEL_NAME`: Nome do modelo de embeddings local (ex: "fabiochiu/multilingual-e5-small-instruct")
- `PINECONE_API_KEY`: Chave da API do Pinecone (banco de dados vetorial)
- `PINECONE_INDEX_NAME`: Nome do índice Pinecone para armazenar os vetores

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/coffee-shop-app-with-chatbot.git
cd coffee-shop-app-with-chatbot/python_code/api
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando a aplicação

1. Inicie o backend:

```bash
python main.py
```

2. O servidor estará disponível em:

```
http://localhost:8000
```

## Estrutura do Projeto

- `api/`: Diretório do backend
  - `agents/`: Agentes do chatbot
    - `classification_agent.py`: Classifica a intenção do usuário
    - `details_agent.py`: Responde perguntas sobre a cafeteria
    - `guard_agent.py`: Filtra consultas não relacionadas à cafeteria
    - `order_taking_agent.py`: Processa pedidos
    - `recommendation_agent.py`: Oferece recomendações de produtos
    - `utils.py`: Funções utilitárias
  - `main.py`: Ponto de entrada da aplicação
  - `requirements.txt`: Dependências do projeto

## Características principais

- Embeddings locais usando SentenceTransformer
- Integração com a API OpenRouter para acesso a modelos de linguagem modernos
- Sistema de recomendação baseado em produtos populares e regras de associação
- Base de conhecimento vetorial usando Pinecone
