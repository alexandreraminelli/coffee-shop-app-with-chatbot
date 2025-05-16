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


def main():
    # Instanciar agentes
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    recommendation_agent = RecommendationAgent(
        os.path.join(
            folder_path, "recommendation_objects/apriori_recommendation.json"),
        os.path.join(
            folder_path, "recommendation_objects/popularity_recommendation.csv")
    )
    # Dicionário com os agentes pós-classificação
    agent_dict: Dict[str, AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "recommendation_agent": recommendation_agent,
        "order_taking_agent": OrderTakingAgent(recommendation_agent)
    }

    # Lista de mensagens para armazenar as interações
    messages = []
    while True:
        # Limpar os inputs anteriores | ter um novo terminal limpo
        os.system('cls' if os.name == 'nt' else 'clear')

        # Exibir mensagens anteriores
        print("\n\n Print mensagens ............")
        for message in messages:
            print(f"{message['role']}: {message['content']}")

        # Obter mensagem do usuário e adiciona-a à lista de mensagens
        prompt = input("Usuário: ")
        messages.append({"role": "user", "content": prompt})

        # Executar Guard Agent
        guard_agent_response = guard_agent.get_response(messages)
        # print("Resposta do Guard Agent: ", guard_agent_response)
        if guard_agent_response['memory']['guard_decision'] == 'not allowed':
            # se a decisão não for permitida
            messages.append(guard_agent_response)
            continue  # continue para a próxima iteração do loop

        # Executar Classification Agent
        classification_agent_response = classification_agent.get_response(
            messages)
        # Agente escolhido pelo classificador
        chosen_agent = classification_agent_response["memory"]["classification_decision"]
        # print("Agente escolhido: ", chosen_agent)

        # Executar o agente escolhido
        agent = agent_dict[chosen_agent]  # usar instância do agente escolhido
        # Resposta do agente escolhido
        # acessar seu método `get_response`
        response = agent.get_response(messages)
        # Exibir metadados
        print("Agent output:", response)
        # adiciona a resposta do agente à lista de mensagens
        messages.append(response)


# Verificar se o script está sendo executado diretamente (não importado como módulo)
# Evita que o código seja executado ao importar o módulo em outro lugar
if __name__ == "__main__":
    main()
