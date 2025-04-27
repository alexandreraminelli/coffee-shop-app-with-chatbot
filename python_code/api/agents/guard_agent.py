from openai import OpenAI
import os
import dotenv
from .utils import get_chatbot_response  # Importar funções utilitárias
import json
from copy import deepcopy

dotenv.load_dotenv()  # Carregar variáveis de ambiente


class GuardAgent():
    def __init__(self):
        # Inicializar o cliente OpenAI com a chave de API e a URL base
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"  # URL base do OpenRouter
        )
        # Carregar o modelo a partir das variáveis de ambiente
        self.model_name = os.getenv("MODEL_NAME")

    # Método para obter a resposta do modelo
    def get_response(self, messages):
        # Deepcopy das mensagens para evitar mutações indesejadas
        messages = deepcopy(messages)

        # System prompt: Filtrar qualquer conteúdo não relacionado a finalizado do chatbot (ser um atendente de uma cafeteria)
        system_prompt = """
            Você é um assistente de IA prestativo para um aplicativo de cafeteria que serve bebidas e doces.
            Sua tarefa é determinar se o usuário está perguntando algo relevante para a cafeteria ou não.

            O usuário está autorizado a:
            1. Fazer perguntas sobre a cafeteria, como localização, horário de funcionamento, itens do cardápio e perguntas relacionadas à cafeteria.
            2. Fazer perguntas sobre os items do menu, eles podem perguntar por ingredientes em um item e mais detalhes sobre o item.
            3. Fazer um pedido.
            4. Pedir recomendações do que quer pedir.

            O usuário não está autorizado a:
            1. Fazer perguntas sobre qualquer outra coisa não relacionada à nossa cafeteria.
            2. Fazer perguntas sobre os funcionários ou como fazer um item do cardápio.

            Sua saída deve estar em um formato JSON estruturado como este. Cada chave é uma string e cada valor é uma string. Certifique-se de seguir o formato JSON exatamente como mostrado abaixo:
            {
            "chain of thought": Revise cada um dos pontos acima e veja se a mensagem se enquadra nesse ponto ou não. Em seguida, escreva algumas reflexões sobre qual ponto essa contribuição é relevante.
            "decision": "allowed" or "not allowed". Escolha um desses dois valores e apenas escreva a palavra.  
            "message": deixe a mensagem vazia (empty strings) se "decision" for "allowed", caso contrário, escreva "Desculpe, não posso ajudar com isso. Posso te ajudar com seu pedido?".
            }
        """
