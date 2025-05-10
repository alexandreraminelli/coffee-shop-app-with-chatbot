import json
import pandas as pd
import numpy as np
import os
from copy import deepcopy
import dotenv
from openai import OpenAI
# Importar funções utilitárias
from .utils import get_chatbot_response, get_embedding
from pinecone import Pinecone  # Importar o cliente Pinecone
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
            base_url="https://openrouter.ai/api/v1"  # URL base do OpenRouter
        )

        # Ler arquivo de recomendações Apriori (.json)
        with open(apriori_recommendation_path, 'r') as file:
            self.apriori_recommendations = json.load(file)

        # Ler arquivo de recomendações populares (.csv)
        self.popular_recommendations = pd.read_csv(popular_recommendation_path)
        # Lista de produtos
        self.products = self.popular_recommendations['product'].tolist()
        # Categorias dos produtos
        self.product_categories = self.popular_recommendations['product_category'].tolist(
        )

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

    def get_popular_recommendations(self, product_categories=None, top_k=5):
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
