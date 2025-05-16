from agents import (  # importação dos agentes
    GuardAgent,
    ClassificationAgent,
    DetailsAgent,
    AgentProtocol,
    RecommendationAgent,
    OrderTakingAgent)
import os
from typing import Dict  # tipagem
import pathlib
import sys

folder_path = pathlib.Path(__file__).parent.resolve()  # caminho do projeto
# adicionar o caminho do projeto ao sys.path
sys.path.append(os.path.join(folder_path, "../.."))


class AgentController():
    # Método construtor
    def __init__(self):
        # Instanciar agentes
        self.guard_agent = GuardAgent()
        self.classification_agent = ClassificationAgent()
        self.recommendation_agent = RecommendationAgent(
            os.path.join(
                folder_path, "recommendation_objects/apriori_recommendation.json"),
            os.path.join(
                folder_path, "recommendation_objects/popularity_recommendation.csv")
        )
        # Dicionário com os agentes pós-classificação
        self.agent_dict: Dict[str, AgentProtocol] = {
            "details_agent": DetailsAgent(),
            "recommendation_agent": self.recommendation_agent,
            "order_taking_agent": OrderTakingAgent(self.recommendation_agent)
        }

    # Método para obter uma resposta do LLM
    # Executa os agentes em sequência (Guard Agent -> Classification Agent -> Agente escolhido (Details, Recommendation ou Order Taking))
    def get_response(self, input):
        # Extrair input do usuário para ser usado com serverless
        job_input = input['input']
        messages = job_input['messages']

        # Executar Guard Agent
        guard_agent_response = self.guard_agent.get_response(messages)
        # Se o Guard Agent decidir que mensagem não é relevante pro contexto do negócio, retorna sua resposta ao usuário e encerra o método
        if guard_agent_response['memory']['guard_decision'] == 'not allowed':
            return  # encerrar método

        # Executar Classification Agent
        classification_agent_response = self.classification_agent.get_response(
            messages)
        # Agente escolhido pelo classificador
        chosen_agent = classification_agent_response["memory"]["classification_decision"]

        # Executar o agente escolhido (Details, Recommendation ou Order Taking)
        agent = self.agent_dict[chosen_agent]
        # Resposta do agente escolhido: acessar seu método `get_response`
        response = agent.get_response(messages)

        # Retornar mensagem ao usuário
        return response
