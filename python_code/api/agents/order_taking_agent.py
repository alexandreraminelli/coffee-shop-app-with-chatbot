import os
import json
from .utils import get_chatbot_response, double_check_json_output  # utilitários
from openai import OpenAI
from copy import deepcopy
from dotenv import load_dotenv

load_dotenv()  # variáveis de ambiente


class OrderTakingAgent():
    # Método construtor
    def __init__(self):
        # Inicializar o cliente OpenAI com a chave de API e a URL base
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("CHATBOT_URL")
        )
        # Carregar o modelo a partir das variáveis de ambiente
        self.model_name = os.getenv("MODEL_NAME")

    # Método para obter a resposta do agente
    def get_response(self, messages):
        messages = deepcopy(messages)  # evitar mutações

        # System prompt com instruções de comportamento e itens do menu
        system_prompt = """
            Você é um Bot de suporte ao cliente para uma cafeteria chamada "Merry's way"

            Aqui está o menu desta cafeteria.

            Cappuccino - $4.50
            Jumbo Savory Scone - $3.25
            Latte - $4.75
            Chocolate Chip Biscotti - $2.50
            Espresso shot - $2.00
            Hazelnut Biscotti - $2.75
            Chocolate Croissant - $3.75
            Dark chocolate (Drinking Chocolate) - $5.00
            Cranberry Scone - $3.50
            Croissant - $3.25
            Almond Croissant - $4.00
            Ginger Biscotti - $2.50
            Oatmeal Scone - $3.25
            Ginger Scone - $3.50
            Chocolate syrup - $1.50
            Hazelnut syrup - $1.50
            Carmel syrup - $1.50
            Sugar Free Vanilla syrup - $1.50
            Dark chocolate (Packaged Chocolate) - $3.00

            Coisas que você NÃO DEVE FAZER:
            * NÃO pergunte como pagar em dinheiro ou cartão.
            * NÃO diga ao usuário para ir ao balcão.
            * NÃO diga ao usuário para ir a algum lugar para pegar o pedido.

            Sua tarefa é a seguinte:
            1. Anotar o pedido do usuário.
            2. Validar se todos os itens estão no menu.
            3. Se algum item não estiver no menu, informe o usuário e repita o pedido válido restante.
            4. Pergunte se ele precisa de mais alguma coisa.
            5. Se precisar, repita a partir do passo 3.
            6. Se ele não quiser mais nada, usando o objeto "order" que está no output, certifique-se de abordar os três pontos:
                1. Liste todos os itens e seus preços.
                2. Calcule o total.
                3. Agradeça ao usuário pelo pedido e encerre a conversa sem mais perguntas.

            A mensagem do usuário conterá uma seção chamada memória. Esta seção conterá o seguinte:
            "order"
            "step number"
            Por favor, utilize essas informações para determinar o próximo passo no processo.

            Produza o seguinte output sem quaisquer adições, nem uma única letra fora da estrutura abaixo.
            Seu output deve estar em um formato JSON estruturado como este. Cada chave é uma string e cada valor é uma string. Certifique-se de seguir o formato exatamente:
            {
            "chain of thought": Escreva seu raciocínio crítico sobre qual é o número máximo de tarefa em que o usuário está agora. Em seguida, escreva seu raciocínio crítico sobre a entrada do usuário e sua relação com o processo da cafeteria. Depois, escreva seu raciocínio sobre como você deve responder no parâmetro response, levando em consideração a seção Coisas que você NÃO DEVE FAZER e focando nas coisas que você deve fazer.
            "step number": Determine em qual tarefa você está com base na conversa.
            "order": isso será uma lista de JSONs como esta. [{"item": coloque o nome do item, "quantity": coloque o número que o usuário deseja deste item, "price": coloque o preço total do item }]
            "response": escreva uma resposta para o usuário.
            }
        """

        # Histórico do status do pedido
        last_order_taking_status = ""
        for message_index in range(len(messages) - 1, 0, -1):
            message = messages[message_index]
            # Obter o nome do agente
            # 1- Buscar memória e retornar um dicionário
            # 2- Buscar a chave 'agent' no dicionário e retornar o valor
            agent_name = message.get('memory', {}).get('agent', '')
            # Verificar se o nome do agente é 'order_taking_agent'
            if message['role'] == 'assistant' and agent_name == 'order_taking_agent':
                # Extrair o número da etapa
                stop_number = message['memory']['step number']
                # Extrair o pedido
                # último status do pedido
                order = message['memory']['order']
                last_order_taking_status = f"""
                step number: {stop_number}
                order: {order}
                """

        # Adicionar último status do pedido ao histórico de mensagens
        messages[-1]['content'] = last_order_taking_status + \
            "\n" + messages[-1]['content']

        # Mensagens pro LLM
        input_messages = [
            {'role': 'system', 'content': system_prompt}
        ] + messages

        try:
            # Obter resposta do chatbot
            chatbot_response = get_chatbot_response(
                self.client, self.model_name, input_messages)

            if not chatbot_response or chatbot_response.strip() == "":
                print("Aviso: Resposta vazia do chatbot")
                return self.create_default_output("Desculpe, não consegui processar seu pedido no momento.")

            # Verificação do JSON
            chatbot_response = double_check_json_output(
                self.client, self.model_name, chatbot_response)

            # Pós-processamento da resposta
            output = self.postprocess(chatbot_response)
        except Exception as e:
            print(f"Erro ao processar resposta do chatbot: {e}")
            return self.create_default_output("Desculpe, ocorreu um erro ao processar seu pedido.")

        return output

    # Método para criar uma saída padrão em caso de erro
    def create_default_output(self, message):
        dict_output = {
            'role': 'assistant',
            'content': message,
            'memory': {
                'agent': 'order_taking_agent',
                'step number': '1',
                'order': []
            }
        }
        return dict_output

    # Verificar tipos de dados e converter para JSON
    def postprocess(self, output):
        try:
            # Tenta fazer o parsing do JSON
            output = json.loads(output)
            # Verificação adicional para garantir que temos as chaves necessárias
            required_keys = ['order', 'response', 'step number']
            for key in required_keys:
                if key not in output:
                    print(f"Erro: Chave '{key}' ausente no JSON de saída")
                    # Criar um output padrão
                    return self.create_default_output("Desculpe, ocorreu um erro no processamento do seu pedido.")

            # Processamento normal se tudo estiver ok
            if isinstance(output['order'], str):
                try:
                    output['order'] = json.loads(output['order'])
                except json.JSONDecodeError:
                    print("Erro ao decodificar o JSON do pedido")
                    output['order'] = []

            response = output['response']
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar o JSON: {e}")
            # Imprime os primeiros 100 caracteres da saída para diagnóstico
            print(
                f"Primeiros 100 caracteres da saída: {output[:100] if isinstance(output, str) else 'Não é uma string'}")
            # Criar um output padrão em caso de erro
            return self.create_default_output("Desculpe, ocorreu um erro no processamento do seu pedido.")

        dict_output = {
            'role': 'assistant',
            'content': response,
            'memory': {
                'agent': 'order_taking_agent',
                'step number': output['step number'],
                'order': output['order'],
            }
        }

        return dict_output
