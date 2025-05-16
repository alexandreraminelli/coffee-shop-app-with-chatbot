import os
import time
import dotenv
import importlib
import traceback
from openai import OpenAI


def check_module(name):
    """Verifica se um módulo está instalado"""
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False


def check_env_var(name):
    """Verifica se uma variável de ambiente está definida"""
    return os.getenv(name) is not None


def main():
    """Verificação principal da configuração do chatbot"""
    print("=== Verificação de Configuração do Coffee Shop Chatbot ===\n")

    # Verificar se o arquivo .env existe
    print("Verificando arquivo .env...")
    if os.path.exists(".env"):
        print("✅ Arquivo .env encontrado")
        dotenv.load_dotenv()
    else:
        print("❌ Arquivo .env não encontrado")
        return

    # Verificar variáveis de ambiente
    env_vars = [
        "OPENROUTER_API_KEY",
        "CHATBOT_URL",
        "MODEL_NAME",
        "EMBEDDING_MODEL_NAME",
        "PINECONE_API_KEY",
        "PINECONE_INDEX_NAME"
    ]

    print("\nVerificando variáveis de ambiente...")
    all_env_vars_exist = True
    for var in env_vars:
        if check_env_var(var):
            print(f"✅ {var} está definido")
        else:
            print(f"❌ {var} não está definido")
            all_env_vars_exist = False

    if not all_env_vars_exist:
        print("\n⚠️ Algumas variáveis de ambiente não estão definidas")

    # Verificar pacotes instalados
    dependencies = [
        "openai",
        "sentence_transformers",
        "fastapi",
        "uvicorn",
        "pinecone",
        "pandas",
        "numpy"
    ]

    print("\nVerificando dependências...")
    all_dependencies_installed = True
    for dep in dependencies:
        if check_module(dep):
            print(f"✅ {dep} está instalado")
        else:
            print(f"❌ {dep} não está instalado")
            all_dependencies_installed = False

    if not all_dependencies_installed:
        print("\n⚠️ Algumas dependências não estão instaladas")
        print("Por favor, execute: pip install -r requirements.txt")

    # Testar SentenceTransformer
    print("\nTestando SentenceTransformer...")
    try:
        from sentence_transformers import SentenceTransformer
        embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
        print(f"Carregando modelo: {embedding_model_name}")

        start = time.time()
        model = SentenceTransformer(embedding_model_name)
        load_time = time.time() - start
        print(f"✅ Modelo carregado em {load_time:.2f} segundos")

        # Testar embeddings
        start = time.time()
        embeddings = model.encode(
            ["Olá! Gostaria de um cappuccino."], convert_to_numpy=True)
        encode_time = time.time() - start
        print(f"✅ Embedding gerado com sucesso em {encode_time:.2f} segundos")
        print(f"   Dimensão do embedding: {embeddings.shape}")

    except Exception as e:
        print(f"❌ Erro ao testar SentenceTransformer: {e}")
        print("Detalhes do erro:")
        traceback.print_exc()
        # Testar OpenRouter API
    print("\nTestando OpenRouter API...")
    try:
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        chatbot_url = os.getenv("CHATBOT_URL")
        model_name = os.getenv("MODEL_NAME")

        if not all([openrouter_api_key, chatbot_url, model_name]):
            print("❌ Variáveis de ambiente para OpenRouter incompletas")
            return

        client = OpenAI(
            api_key=openrouter_api_key,
            base_url=chatbot_url
        )

        print(
            f"Enviando requisição para OpenRouter usando modelo: {model_name}")

        start = time.time()
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Diga olá!"}],
            temperature=0,
            max_tokens=50,
            headers={
                "HTTP-Referer": "https://coffee-shop-app-with-chatbot.example",
                "X-Title": "Coffee Shop App with Chatbot - Teste"
            }
        )
        request_time = time.time() - start

        print(
            f"✅ Resposta recebida do OpenRouter em {request_time:.2f} segundos")
        print(f"   Resposta: {response.choices[0].message.content}")

    except Exception as e:
        print(f"❌ Erro ao testar OpenRouter API: {e}")
        print("Detalhes do erro:")
        traceback.print_exc()

        if not all([openrouter_api_key, chatbot_url, model_name]):
            print("❌ Variáveis de ambiente para OpenRouter incompletas")
            return

        client = OpenAI(
            api_key=openrouter_api_key,
            base_url=chatbot_url
        )

        print(
            f"Enviando requisição para OpenRouter usando modelo: {model_name}")

        start = time.time()
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Diga olá!"}],
            temperature=0,
            max_tokens=50,
            headers={
                "HTTP-Referer": "https://coffee-shop-app-with-chatbot.example",
                "X-Title": "Coffee Shop App with Chatbot - Teste"
            }
        )
        request_time = time.time() - start

        print(
            f"✅ Resposta recebida do OpenRouter em {request_time:.2f} segundos")
        print(f"   Resposta: {response.choices[0].message.content}")

    except Exception as e:
        print(f"❌ Erro ao testar OpenRouter API: {e}")
        print("Detalhes do erro:")
        traceback.print_exc()

    print("\n=== Verificação concluída ===")


if __name__ == "__main__":
    main()
