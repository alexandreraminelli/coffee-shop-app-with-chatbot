from openai import ChatCompletion

# Função para obter uma resposta do chatbot.


def get_chatbot_response(messages, model_name, temperature=0):
    # Type check do messages
    if not isinstance(messages, list):
        raise TypeError("messages deve ser uma lista")

    # Lista de mensagens enviadas para o LLM
    input_messages = []
    for message in messages:
        # Adicionar dicionário à lista
        input_messages.append({
            "role": message["role"],  # Quem está falando (usuário ou sistema)
            "content": message["content"]  # Conteúdo da mensagem
        })

    # Chamada à API do OpenAI para obter a resposta do modelo
    response = ChatCompletion.create(
        model=model_name,  # Modelo de IA
        # Lista de mensagens
        messages=input_messages,
        # Temperatura: quantidade de aleatoriedade na resposta
        temperature=temperature,  # 0 pois queremos resultados concretos
        top_p=0.8,
        max_tokens=2_000,  # Limite de tokens na resposta
        # Token: unidade de medida do modelo de IA (palavras, sub-palavras, caracteres, ...)
    ).choices[0].message.content.strip()

    return response  # Retornar resposta ao usuário

# Função para obter os embeddings


def get_embedding(embedding_client, text_input):
    # Data check: Se for uma string, transforma em lista
    if isinstance(text_input, str):
        text_input = [text_input]

    # Gerar embeddings usando o cliente | retorna um numpy array
    embeddings = embedding_client.encode(text_input, convert_to_numpy=True)
    # Retornar embeddings
    return embeddings
