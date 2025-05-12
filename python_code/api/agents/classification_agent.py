from openai import OpenAI
import os
import dotenv
from .utils import get_chatbot_response, double_check_json_output  # utilitários
import json
from copy import deepcopy

dotenv.load_dotenv()  # Carregar variáveis de ambiente


class ClassificationAgent():
    # Método construtor
    def __init__(self):
        # Inicializar o cliente OpenAI com a chave de API e a URL base
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("CHATBOT_URL")
        )
        # Carregar o modelo a partir das variáveis de ambiente
        self.model_name = os.getenv("MODEL_NAME")

    # Método para obter a resposta do modelo
    def get_response(self, messages):
        # Deepcopy das mensagens para evitar mutações indesejadas
        messages = deepcopy(messages)

        # System prompt do classificador: determinar qual agente deve lidar com a entrada do usuário
        system_prompt = """
            Você é um assistente de IA prestativo para um aplicativo de cafeteria.
            Sua tarefa é determinar qual agente deve lidar com a entrada do usuário. Você tem 3 agentes para escolher:
            1. details_agent: Este agente é responsável por responder perguntas sobre a cafeteria, como localização, locais de entrega, horários de funcionamento, detalhes sobre itens do menu. Ou listar itens no menu. Ou ao perguntar o que temos.
            2. order_taking_agent: Este agente é responsável por receber pedidos do usuário. Ele é responsável por ter uma conversa com o usuário sobre o pedido até que esteja completo.
            3. recommendation_agent: Este agente é responsável por dar recomendações ao usuário sobre o que comprar. Se o usuário pedir uma recomendação, este agente deve ser usado.

            Sua saída deve estar em um formato JSON estruturado como este. cada chave é uma string e cada valor é uma string. Certifique-se de seguir exatamente o formato JSON abaixo:
            {
            "chain of thought": "percorra cada um dos agentes acima e escreva alguns de seus pensamentos sobre a qual agente esta entrada é relevante.",
            "decision": "details_agent" ou "order_taking_agent" ou "recommendation_agent". Escolha um desses dois valores e escreva apenas a palavra,
            "message": deixe a mensagem vazia
        }
        """

        # Lista de mensagens que serão enviadas para o modelo
        input_messages = [
            # Adiciona o prompt_system
            {"role": "system", "content": system_prompt}
        ]
        # Adiciona as últimas 3 mensagens do usuário
        input_messages += messages[-3:]

        # Resposta do chatbot

        chatbot_output = get_chatbot_response(
            self.client, self.model_name, input_messages)
        chatbot_output = double_check_json_output(
            self.client, self.model_name, chatbot_output)
        # Processa a saída do chatbot
        output = self.postprocess(chatbot_output)
        return output  # Retorna a saída processada

    # Método para processar a saída do chatbot
    # O método verifica se a saída é válida e retorna um dicionário com as chaves "chain of thought", "decision" e "message"
    def postprocess(self, output):
        print("Saída do classificador: ", output)  # Debugging

        output = json.loads(output)  # Converte a string JSON em um dicionário

        # Criar dicionário estruturado que contém a saída processada
        dict_output = {
            "role": "assistant",  # Papel do agente
            "content": output["message"],  # Mensagem do agente
            "memory": {  # Memória do agente
                'agent': 'classification_agent',  # Nome do agente
                # Decisão de classificação
                'classification_decision': output['decision']
            }
        }

        return dict_output  # Retorna o dicionário com a saída processada
