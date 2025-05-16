# Documentação do Coffee Shop Chatbot

## Visão Geral do Projeto

Este projeto implementa um chatbot para uma cafeteria utilizando LLMs (Large Language Models) via OpenRouter API e embeddings locais com a biblioteca SentenceTransformer. O chatbot é capaz de responder perguntas sobre a cafeteria, fazer recomendações de produtos e processar pedidos dos clientes.

## Alterações Recentes

O projeto foi adaptado para:

- Usar a API OpenRouter em vez do RunPod
- Implementar embeddings locais usando SentenceTransformer em vez de serviços remotos
- Remover dependências desnecessárias como numpy e importações não utilizadas
- Melhorar a documentação e configuração do ambiente

## Arquitetura do Sistema

O sistema utiliza uma arquitetura baseada em agentes especializados:

1. **GuardAgent**: Filtra consultas não relacionadas à cafeteria
2. **ClassificationAgent**: Classifica a intenção do usuário
3. **DetailsAgent**: Responde perguntas sobre a cafeteria e produtos
4. **RecommendationAgent**: Oferece recomendações personalizadas
5. **OrderTakingAgent**: Processa pedidos dos clientes

## Configuração do Ambiente

### Pré-requisitos

- Python 3.8+ instalado
- Acesso à API OpenRouter (chave de API)
- Acesso ao Pinecone (chave de API)
- Conexão à Internet para baixar o modelo de embeddings

### Variáveis de Ambiente

Crie um arquivo `.env` no diretório `python_code/api/` com as seguintes variáveis:

```
# OpenRouter API
OPENROUTER_API_KEY=sua_chave_aqui
CHATBOT_URL=https://openrouter.ai/api/v1
MODEL_NAME=meta-llama/llama-3.1-8b-instruct:free

# Modelo de Embeddings Local
EMBEDDING_MODEL_NAME=BAAI/bge-small-en-v1.5

# Pinecone DB
PINECONE_API_KEY=sua_chave_pinecone_aqui
PINECONE_INDEX_NAME=nome_do_seu_indice
```

### Instalação de Dependências

Execute o script de instalação que utilizará binários pré-compilados para evitar problemas de compilação:

```bash
install_dependencies.bat
```

Ou, se preferir instalar manualmente:

```bash
cd "c:\Users\aleju\Documentos (local)\Dev\Faculdade\Projeto Integrador\Chatbot\coffee-shop-app-with-chatbot\python_code\api"
pip install --only-binary :all: pandas==2.0.3
pip install -r requirements.txt
```

## Etapas de Execução

### 1. Verificar a Configuração do Ambiente

Execute o script de diagnóstico para verificar se todas as dependências estão corretamente instaladas e se as variáveis de ambiente estão configuradas:

```bash
cd "c:\Users\aleju\Documentos (local)\Dev\Faculdade\Projeto Integrador\Chatbot\coffee-shop-app-with-chatbot\python_code\api"
python check_setup.py
```

### 2. Construir o Banco de Dados Vetorial

Abra e execute o notebook `build_vector_database.ipynb` para criar os vetores no Pinecone:

```bash
cd "c:\Users\aleju\Documentos (local)\Dev\Faculdade\Projeto Integrador\Chatbot\coffee-shop-app-with-chatbot\python_code"
jupyter notebook build_vector_database.ipynb
```

### 3. Executar a API do Chatbot

Você pode usar o script de execução:

```bash
run_api_server.bat
```

Ou manualmente:

```bash
cd "c:\Users\aleju\Documentos (local)\Dev\Faculdade\Projeto Integrador\Chatbot\coffee-shop-app-with-chatbot\python_code\api"
python main.py
```

A API estará disponível em `http://localhost:8000`.

## Testando o Chatbot

### Exemplo de requisição:

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "Me recomende algo para beber"}]}'
```

## Resolução de Problemas

### Problemas com o pandas

Se houver erros durante a instalação do pacote pandas, você pode tentar:

```bash
pip install --only-binary :all: pandas
```

ou

```bash
pip install --no-cache-dir pandas
```

### Problemas com o SentenceTransformer

Se o download do modelo de embeddings falhar:

1. Verifique sua conexão com a internet
2. Tente especificar um modelo menor: `"paraphrase-MiniLM-L3-v2"`
3. Certifique-se de que há espaço suficiente em disco

## Próximos Passos

- Implementar autenticação na API
- Adicionar suporte a mais idiomas
- Melhorar o sistema de recomendação com feedback dos usuários
- Implementar integração com sistema de pagamento
