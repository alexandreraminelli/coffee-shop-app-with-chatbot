from typing import List
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_controller import AgentController
import json

# Modelos para validação de dados


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# Criar aplicação FastAPI
app = FastAPI(title="Coffee Shop Chatbot API", version="1.0.0")

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciar o controlador de agentes globalmente
agent_controller = AgentController()


@app.get("/")
async def root():
    return {"message": "Coffee Shop Chatbot API", "status": "running"}


@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    """
    Endpoint principal para chat com o chatbot.
    Recebe mensagens e retorna a resposta do chatbot.
    """
    try:
        # Converter mensagens para o formato esperado pelo AgentController
        messages_dict = [{"role": msg.role, "content": msg.content}
                         for msg in chat_request.messages]

        # Simular o formato de input que o AgentController espera (similar ao Runpod)
        input_data = {
            "input": {
                "messages": messages_dict
            }
        }

        # Obter resposta do controlador de agentes
        response = agent_controller.get_response(input_data)

        if response is None:
            return {"error": "Mensagem não permitida pelo sistema de segurança"}

        return {
            "success": True,
            "response": response
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Erro interno do servidor: {str(e)}"
        }


@app.post("/chatbot")
async def chatbot_legacy(request: Request):
    """
    Endpoint legacy para compatibilidade com implementações existentes.
    """
    try:
        request_json = await request.json()

        # Se o body vier como string JSON (como no exemplo)
        if "body" in request_json:
            body = json.loads(request_json["body"])
        else:
            body = request_json

        # Extrair mensagens
        messages = body.get("messages", [])

        # Simular o formato de input que o AgentController espera
        input_data = {
            "input": {
                "messages": messages
            }
        }

        # Obter resposta do controlador de agentes
        response = agent_controller.get_response(input_data)

        if response is None:
            return {"message": "Mensagem não permitida pelo sistema de segurança"}

        return response

    except Exception as e:
        return {"error": f"Erro interno do servidor: {str(e)}"}


def main():
    """
    Função principal para executar o servidor FastAPI em modo de desenvolvimento.
    """
    import uvicorn

    print("🚀 Iniciando Coffee Shop Chatbot API...")
    print("📍 Acesse: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")

    # Executar servidor em modo de desenvolvimento
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Reinicia automaticamente quando há mudanças no código
        log_level="info"
    )


# Garantir que script seja executado diretamente (não importado como módulo)
if __name__ == "__main__":
    main()
