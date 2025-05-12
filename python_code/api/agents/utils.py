# Utilitários para agentes de chatbot

# Função para obter uma resposta do chatbot.


def get_chatbot_response(client, model_name, messages, temperature=0):
    # Type check do messages
    # if not isinstance(messages, list):
    #     raise TypeError("messages deve ser uma lista")

    try:
        # Lista de mensagens enviadas para o LLM
        input_messages = []
        for message in messages:
            # Adicionar dicionário à lista
            input_messages.append({
                # Quem está falando (usuário ou sistema)
                "role": message["role"],
                "content": message["content"]  # Conteúdo da mensagem
            })

        # Chamada à API do OpenAI para obter a resposta do modelo
        response = client.chat.completions.create(
            model=model_name,  # Modelo de IA
            # Lista de mensagens
            messages=input_messages,
            # Temperatura: quantidade de aleatoriedade na resposta
            temperature=temperature,  # 0 pois queremos resultados concretos
            top_p=0.8,
            max_tokens=2_000,  # Limite de tokens na resposta
            # Token: unidade de medida do modelo de IA (palavras, sub-palavras, caracteres, ...)
        ).choices[0].message.content

        # Verificar se a resposta está vazia
        if not response or response.strip() == "":
            print("Aviso: API retornou uma resposta vazia")
            return ""

        return response  # Retornar resposta ao usuário
    except Exception as e:
        print(f"Erro ao chamar a API: {e}")
        return ""  # Retornar string vazia em caso de erro

# Função para obter os embeddings


def get_embedding(embedding_client, text_input):
    # Data check: Se for uma string, transforma em lista
    if isinstance(text_input, str):
        text_input = [text_input]

    # Gerar embeddings usando o cliente | retorna um numpy array
    embeddings = embedding_client.encode(text_input, convert_to_numpy=True)
    # Retornar embeddings
    return embeddings

# Verificação de output JSON


def double_check_json_output(client, model_name, json_string):
    # Verificar se json_string está vazio ou é nulo
    if not json_string or json_string.strip() == "":
        # Retornar um JSON padrão para evitar erro
        return '{"recommendation_type": "popular", "chain of thought": "Não foi possível determinar o tipo de recomendação devido a um erro na resposta.", "parameters": []}'

    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    If there is any text before order after the json string, remove it.
    Do NOT return a single letter outside of the json string.
    The first thing you write should be open curly brace of the json and the last letter you write should be the closing curly brace of the json.

    You should check the json string for the following text between triple backticks:
    ```
    {json_string}
    ```
    """

    messages = [{'role': 'user', 'content': prompt}]
    response = get_chatbot_response(client, model_name, messages)
    # Remover triple backticks (indicadores de código)
    response = response.replace("```", "")

    # Verificar se a resposta está vazia
    if not response or response.strip() == "":
        # Retornar um JSON padrão para evitar erro
        return '{"recommendation_type": "popular", "chain of thought": "Não foi possível determinar o tipo de recomendação devido a um erro na resposta.", "parameters": []}'

    return response
