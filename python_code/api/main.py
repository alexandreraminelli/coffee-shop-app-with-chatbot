from agent_controller import AgentController
# import runpod  # Comentado para usar o OpenRouter em vez do RunPod
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Configuração para o OpenRouter:
# 1. O arquivo .env deve conter as seguintes variáveis:
#    - OPENROUTER_API_KEY: Chave de API do OpenRouter
#    - CHATBOT_URL: URL base da API do OpenRouter (https://openrouter.ai/api/v1)
#    - MODEL_NAME: Nome do modelo a ser usado (por exemplo, "meta-llama/llama-3.1-8b-instruct:free")
#    - EMBEDDING_MODEL_NAME: Nome do modelo de embeddings local (por exemplo, "BAAI/bge-small-en-v1.5")
# 2. Os agentes já estão configurados para usar o OpenRouter nas classes GuardAgent,
#    ClassificationAgent, DetailsAgent, RecommendationAgent e OrderTakingAgent
# 3. Para a geração de embeddings, usamos a biblioteca SentenceTransformer localmente em vez de
#    uma API externa, o que reduz custos e dependência de serviços externos


# Modelo de dados para a requisição
class ChatMessage(BaseModel):
    role: str
    content: str
    memory: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


# Instanciar o controlador de agentes
agent_controller = AgentController()

# Criar aplicação FastAPI
app = FastAPI()

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, liste apenas as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    """
    Endpoint para verificar se a API está funcionando.
    """
    return {
        "status": "online",
        "message": "API do Chatbot está funcionando!",
        "environment": "OpenRouter"
    }


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Converter a estrutura Pydantic para o formato esperado pelo AgentController
        input_format = {
            'input': {
                'messages': [dict(message) for message in request.messages]
            }
        }

        # Chamar o controlador de agentes
        response = agent_controller.get_response(input_format)

        # Se não houver resposta (ex: quando guard_decision é 'not allowed')
        if not response:
            return {"response": None}

        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar mensagem: {str(e)}")


def main():
    # RUNPOD: executar o servidor serverless (comentado)
    # runpod.serverless.start({'handler': agent_controller.get_response})

    # SEM RUNPOD: usar backend próprio com FastAPI
    # React Native envia mensagens para endpoint /chat que chamará o AgentController.get_response
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Garantir que script seja executado diretamente (não importado como módulo)
if __name__ == "__main__":
    main()
