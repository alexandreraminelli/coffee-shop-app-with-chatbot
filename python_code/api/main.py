from agent_controller import AgentController
# import runpod


def main():
    # Instanciar o controlador de agentes
    agent_controller = AgentController()

    # RUNPOD: executar o servidor serverless
    # runpod.serverless.start({'handler': agent_controller.get_response})

    # SEM RUNPOD: usar backend próprio (ex: FastAPI)
    # React Native envia mensagens para endpoint (ex: /chat) que chamará o AgentController.get_response


# Garantir que script seja executado diretamente (não importado como módulo)
if __name__ == "__main__":
    main()
