import json
import pandas as pd
import os
from copy import deepcopy
import dotenv
from openai import OpenAI
# Importar funções utilitárias
from .utils import get_chatbot_response, double_check_json_output  # utilitários
# Importar SentenceTransformer para embeddings locais
from sentence_transformers import SentenceTransformer

dotenv.load_dotenv()  # Carregar variáveis de ambiente

# Classe do Agente de Recomendação


class RecommendationAgent():
    # Método construtor
    def __init__(self, apriori_recommendation_path, popular_recommendation_path):
        # Inicializar o cliente OpenAI com a chave de API e a URL base
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("CHATBOT_URL")
        )
        self.model_name = os.getenv("MODEL_NAME")  # Modelo LLM

        # Cliente de embeddings usando SentenceTransformer (processamento local)
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
        self.embedding_client = SentenceTransformer(self.embedding_model_name)

        # Ler arquivo de recomendações Apriori (.json)
        with open(apriori_recommendation_path, 'r') as file:
            self.apriori_recommendations = json.load(file)

        # Ler arquivo de recomendações populares (.csv)
        self.popular_recommendations = pd.read_csv(popular_recommendation_path)
        # Lista de produtos
        self.products = self.popular_recommendations['product'].tolist()
        # Categorias dos produtos
        self.product_categories = list(set(  # transformar em set para evitar duplicatas
            self.popular_recommendations['product_category'].tolist()
        ))

    # Método para obter recomendações Apriori
    def get_apriori_recommendation(self, products, top_k=5):
        # DataFrame com as recomendações Apriori
        recommendation_list = []
        for product in products:
            if product in self.apriori_recommendations:
                recommendation_list += self.apriori_recommendations[product]
        # Ordenar lista de recomendações pela confiança
        recommendation_list = sorted(
            recommendation_list, key=lambda x: x['confidence'], reverse=True)

        # Criar lista de recomendações
        recommendations = []  # Alterado de 'recommendation' para 'recommendations'
        recommendation_per_category = {}
        for recommendation_item in recommendation_list:
            # Se o produto desta recomendação já estiver na lista, ignora
            if recommendation_item['product'] in recommendations:
                continue

            # Limitar 2 recomendações por categoria
            product_category = recommendation_item['product_category']
            if product_category not in recommendation_per_category:
                # inicializa contagem de recomendações por categoria
                recommendation_per_category[product_category] = 0
            # Se já houver 2 recomendações por categoria, ignora
            if recommendation_per_category[product_category] >= 2:
                continue
            # incrementa contagem
            recommendation_per_category[product_category] += 1

            # Adicionar produto da recomendação à lista
            recommendations.append(recommendation_item['product'])

            if len(recommendations) >= top_k:
                # parar se já atingir o limite de recomendações
                break

        # Retornar as recomendações
        return recommendations

    # Método para obter recomendações Populares (não Apriori)

    def get_popular_recommendation(self, product_categories=None, top_k=5):
        # DataFrame com as recomendações populares
        recommendations_df = self.popular_recommendations

        # Type Check
        # se argumento for uma string, transforma em lista
        if isinstance(product_categories, str):  # Alterado de type() para isinstance()
            product_categories = [product_categories]
        # se argumento não for None
        if product_categories is not None:
            recommendations_df = self.popular_recommendations[self.popular_recommendations['product_category'].isin(
                product_categories)]

        # Ordenar DataFrame por número de transações
        recommendations_df = recommendations_df.sort_values(
            'number_of_transactions', ascending=False)
        # Se não houver recomendações retorna uma lista vazia
        if recommendations_df.shape[0] == 0:
            return []
        # Se houver recomendações, retorna as mais populares
        recommendations = recommendations_df['product'].tolist()[:top_k]
        return recommendations

    # Método para obter recomendações de produtos semelhantes
    def recommendation_classification(self, message):
        system_prompt = """ Você é um assistente de IA útil para um aplicativo de cafeteria que serve bebidas e doces. Temos 3 tipos de recomendações:

        1. Recomendações Apriori: Estas são recomendações baseadas no histórico de pedidos do usuário. Recomendamos itens que são frequentemente comprados junto com os itens do pedido do usuário.
        2. Recomendações Populares: Estas são recomendações baseadas na popularidade dos itens na cafeteria. Recomendamos itens que são populares entre os clientes.
        3. Recomendações Populares por Categoria: Aqui o usuário pede para recomendar um produto em uma categoria. Como, qual café você me recomenda pegar? Recomendamos itens que são populares na categoria solicitada pelo usuário.

        Aqui está a lista de itens na cafeteria:
        """ + ",".join(self.products) + """
        Aqui está a lista de Categorias que temos na cafeteria:
        """ + ",".join(self.product_categories) + """

        Sua tarefa é determinar qual tipo de recomendação fornecer com base na mensagem do usuário.

        Sua saída deve estar em um formato json estruturado como este. Cada chave é uma string e cada valor é uma string. Certifique-se de seguir exatamente o formato:
        {
        "chain of thought": Escreva seu raciocínio crítico sobre a qual tipo de recomendação esta entrada é relevante.
        "recommendation_type": "apriori" ou "popular" ou "popular by category". Escolha um desses e escreva apenas a palavra.
        "parameters": Esta é uma lista em python. É uma lista de itens para recomendações apriori ou uma lista de categorias para recomendações populares por categoria. Deixe vazio para recomendações populares. Certifique-se de usar as strings exatas da lista de itens e categorias acima.
        }        """
        # Mensagens que serão enviadas para o LLM: system prompt + 3 últimas mensagens do chat
        input_messages = [
            {'role': 'system', 'content': system_prompt}] + message[-3:]
        # Obter resposta do LLM
        chatbot_output = get_chatbot_response(
            self.client, self.model_name, input_messages)
        chatbot_output = double_check_json_output(  # verificar se o JSON está correto
            self.client, self.model_name, chatbot_output)

        output = self.postprocess_classification(chatbot_output)
        return output  # retornar resposta do LLM    # Método para pós-processar a resposta do LLM

    def postprocess_classification(self, output):
        try:
            # converter resposta do LLM (string) para JSON/dict
            output = json.loads(output)
            dict_output = {
                "recommendation_type": output.get('recommendation_type', 'popular'),
                "parameters": output.get('parameters', []),
            }
            return dict_output
        except json.JSONDecodeError as e:
            # Se houver erro ao analisar o JSON, retornar valores padrão
            print(f"Erro ao analisar JSON: {e}")
            return {
                "recommendation_type": "popular",
                "parameters": []
            }  # Método para obter recomendações a partir de um pedido que o usuário fez ou está fazendo

    def get_recommendations_from_order(self, messages, order):
        messages = deepcopy(messages)  # evitar alterações

        products = []  # lista de produtos no pedido
        for product in order:
            products.append(product['item'])

        # obter recomendações apriori para os produtos do pedido
        recommendations = self.get_apriori_recommendation(products)
        # Resposta ao usuário: converter lista em string e separar por vírgula
        recommendations_str = ", ".join(recommendations)

        # System prompt
        system_prompt = """
        Você é um assistente de IA útil para um aplicativo de cafeteria que serve bebidas e doces.
        Sua tarefa é recomendar itens ao usuário com base no pedido dele.

        Fornecerei quais itens você deve recomendar ao usuário com base no pedido dele na mensagem do usuário.
        """
        # Adicionar recomendações ao final da mensagem
        prompt = f"""
        {messages[-1]['content']}

        Por favor, me recomende exatamente os seguintes itens: {recommendations_str}
        """
        messages[-1]['content'] = prompt
        # Mensagens que serão enviadas para o LLM: system prompt + 3 últimas mensagens do chat
        input_messages = [
            {'role': 'system', 'content': system_prompt}] + messages[-3:]
        # Obter resposta do LLM
        chatbot_output = get_chatbot_response(
            self.client, self.model_name, input_messages)
        output = self.postprocess(chatbot_output)
        return output

    # Método para obter recomendações a partir de uma pergunta que o usuário fez
    def get_response(self, messages):
        messages = deepcopy(messages)  # evitar alterações
        #
        recommendation_classification = self.recommendation_classification(
            messages)
        recommendation_type = recommendation_classification['recommendation_type']

        recommendations = []
        # Adicionar recomendações com base no tipo de recomendação
        if recommendation_type == 'apriori':
            recommendations = self.get_apriori_recommendation(
                recommendation_classification['parameters']
            )
        elif recommendation_type == 'popular':
            recommendations = self.get_popular_recommendation()
        elif recommendation_type == 'popular by category':
            recommendations = self.get_popular_recommendation(
                recommendation_classification['parameters'])
        # Se recomendações estiver vazia, retorna uma mensagem padrão
        if recommendations == []:
            return {
                'role': 'assistant',
                'content': 'Desculpe, eu não posso te ajudar com essa recomendação. Posso te ajudar com outra coisa?',
            }
        # Resposta ao usuário
        recommendations_str = ', '.join(recommendations)

        system_prompt = """
        Você é um assistente de IA útil para um aplicativo de cafeteria que serve bebidas e doces.
        Sua tarefa é recomendar itens ao usuário com base na mensagem inserida. Responda de forma amigável, porém concisa. Crie uma lista não ordenada com uma descrição bem curta.
        
        Eu fornecerei os itens que você deve recomendar ao usuário com base no pedido feito na mensagem.
        """
        prompt = f"""
        {messages[-1]['content']}

        Por favor, me recomende exatamente os seguintes itens: {recommendations_str}
        """
        messages[-1]['content'] = prompt
        # Mensagens pro LLM: system prompt + 3 últimas mensagens do chat
        input_messages = [
            {'role': 'system', 'content': system_prompt}] + messages[-3:]
        # Obter resposta do LLM
        chatbot_output = get_chatbot_response(
            self.client, self.model_name, input_messages)
        # pós-processamento da resposta (converter string para JSON)
        output = self.postprocess(chatbot_output)
        return output

    # Método para pós-processar a resposta do LLM

    def postprocess(self, output):
        # converter resposta do LLM (string) para JSON/dict
        output = {
            'role': 'assistant',
            'content': output,
            'memory': {'agent': 'recommendation_agent'}
        }
        return output
