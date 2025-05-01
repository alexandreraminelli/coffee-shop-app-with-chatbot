from agents import (GuardAgent, ClassificationAgent)  # importação dos agentes
import os


def main():
    pass


# Verificar se o script está sendo executado diretamente (não importado como módulo)
# Evita que o código seja executado ao importar o módulo em outro lugar
if __name__ == "__main__":
    # Instanciar agentes
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()

    # Lista de mensagens para armazenar as interações
    messages = []
    while True:
        # Limpar os inputs anteriores | ter um novo terminal limpo
        # os.system('cls' if os.name == 'nt' else 'clear')

        # Exibir mensagens anteriores
        print("\n\n Print mensagens ............")
        for message in messages:
            print(f"{message['role']}: {message['content']}")

        # Obter mensagem do usuário e adiciona-a à lista de mensagens
        prompt = input("Usuário: ")
        messages.append({"role": "user", "content": prompt})

        # Executar Guard Agent
        guard_agent_response = guard_agent.get_response(messages)
        print("Resposta do Guard Agent: ", guard_agent_response)
        if guard_agent_response['memory']['guard_decision'] == 'not allowed':
            # se a decisão não for permitida
            messages.append(guard_agent_response)
            continue  # continue para a próxima iteração do loop

        # Executar Classification Agent
        classification_agent_response = classification_agent.get_response(
            messages)
        # Agente escolhido pelo classificador
        chosen_agent = classification_agent_response["memory"]["classification_decision"]
        print("Agente escolhido: ", chosen_agent)
