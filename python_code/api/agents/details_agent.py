import json
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

# Classe do Agente de Detalhes


class DetailsAgent():
    # Método construtor
    def __init__(self):
        # Inicializar o cliente OpenAI com a chave de API e a URL base
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("CHATBOT_URL")
        )
        # Carregar o modelo a partir das variáveis de ambiente
        self.model_name = os.getenv("MODEL_NAME")

        # Cliente de embeddings usando SentenceTransformer (processamento local)
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
        self.embedding_client = SentenceTransformer(self.embedding_model_name)

        # Cliente Pinecone
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME")

    # Método para obter o resultado mais próximo segundo o embedding
    def get_closest_result(self, index_name, input_embeddings: list, top_k=2):
        # Certificar-se de que os embeddings estão no formato de lista
        if isinstance(input_embeddings, np.ndarray):
            input_embeddings = input_embeddings.tolist()

        # Obter o índice do Pinecone
        index = self.pc.Index(index_name)

        # Resultados: consulta no índice do Pinecone
        results = index.query(
            namespace="ns1",  # namespace do Pinecone
            vector=input_embeddings,  # embeddings de entrada
            top_k=top_k,  # número de resultados mais próximos
            # não incluir valores na resposta (os embeddings em si)
            include_values=False,
            # incluir metadados (texto legível para humanos)
            include_metadata=True,
        )
        return results

    # Método para obter a resposta do modelo
    def get_response(self, messages):
        # Deepcopy para evitar mutações indesejadas
        messages = deepcopy(messages)

        # Mensagem do usuário
        user_message = messages[-1]['content']
        # Obter embeddings da mensagem do usuário
        embeddings = get_embedding(self.embedding_client, user_message)[0]
        # Resultado mais próximo do Pinecone
        result = self.get_closest_result(self.index_name, embeddings)
        # Fonte de conhecimento: resultado mais próximo do Pinecone usado para alimentar o prompt do agente
        # Obter o texto legível para humanos (metadados) do resultado mais próximo
        source_knowledge = "\n".join(
            [x['metadata']['text'].strip()+"\n" for x in result['matches']])

        # Prompt enviado ao agente de detalhes
        # O prompt é a pergunta do usuário e o contexto (resultado mais próximo do Pinecone)
        prompt = f"""
            Usando os contextos abaixo, responda a pergunta:
            Contextos:
            {source_knowledge}

            Pergunta: {user_message}
        """

        # System prompt do Agente de Detalhes: responder perguntas sobre a cafeteria, como localização, locais de entrega, horários
        system_prompt = """
            Você é um agente de suporte ao cliente para um aplicativo de cafeteria chamada Merry's Way. Você deve responder a cada pergunta como se você fosse um garçom da cafeteria e deve fornecer as informações necessárias ao usuário em relação ao seus pedidos. 
        """
        # Adiciona o system prompt às mensagens
        messages[-1]['content'] = prompt
        input_messages = [
            {'role': 'system', 'content': system_prompt}] + messages[-3:]

        # Resposta do chatbot
        chatbot_output = get_chatbot_response(
            self.client, self.model_name, input_messages)
        # Processa a saída do chatbot e a retorna
        output = self.postprocess(chatbot_output)
        return output

    # Método para processar a saída do chatbot
    def postprocess(self, output):
        output = {
            "role": "assistant",  # Papel do agente
            "content": output,  # Resposta do agente
            "memory": {  # Memória do agente
                'agent': 'details_agent',  # Nome do agente
            }
        }
        return output
