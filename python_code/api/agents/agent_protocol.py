# permite usar tipagem opcional (igual ao TypeScript)
from typing import Protocol, List, Dict, Any


class AgentProtocol(Protocol):
    #
    def get_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Docstring
        '''
        Função para obter uma resposta do chatbot.

        Parameters:
        self (Any): ...
        messages (List[Dict[str, Any]]): Lista de mensagens enviadas para o LLM. Cada mensagem é um dicionário com as chaves "role" e "content".
        '''
        ...
