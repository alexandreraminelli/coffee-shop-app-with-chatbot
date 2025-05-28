#!/usr/bin/env python3
"""
Script de teste para a API do chatbot usando FastAPI.
Este script testa os endpoints da API e mostra como fazer requisições.
"""

import requests
import json

# URL base da API (ajuste conforme necessário)
BASE_URL = "http://localhost:8000"


def test_root_endpoint():
    """Testa o endpoint raiz da API."""
    print("🔍 Testando endpoint raiz...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False


def test_chat_endpoint():
    """Testa o endpoint principal de chat."""
    print("\n🤖 Testando endpoint /chat...")

    # Dados de teste
    test_data = {
        "messages": [
            {
                "role": "user",
                "content": "Eu gostaria de um latte, por favor"
            }
        ]
    }

    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        print(f"Status: {response.status_code}")
        print(
            f"Resposta: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False


def test_chatbot_legacy_endpoint():
    """Testa o endpoint legacy /chatbot."""
    print("\n📱 Testando endpoint legacy /chatbot...")

    # Dados de teste no formato legacy
    test_data = {
        "messages": [
            {
                "role": "user",
                "content": "Quais são as opções de café disponíveis?"
            }
        ]
    }

    try:
        response = requests.post(
            f"{BASE_URL}/chatbot",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        print(f"Status: {response.status_code}")
        print(
            f"Resposta: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False


def interactive_chat():
    """Modo de chat interativo para testar a API."""
    print("\n💬 Modo chat interativo (digite 'sair' para encerrar):")

    messages = []

    while True:
        user_input = input("\nVocê: ").strip()

        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("👋 Encerrando chat...")
            break

        if not user_input:
            continue

        # Adicionar mensagem do usuário
        messages.append({"role": "user", "content": user_input})

        # Fazer requisição para a API
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                headers={"Content-Type": "application/json"},
                json={"messages": messages}
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    bot_response = result.get("response", {})
                    bot_content = bot_response.get(
                        "content", "Desculpe, não consegui processar sua mensagem.")
                    print(f"Bot: {bot_content}")

                    # Adicionar resposta do bot ao histórico
                    messages.append(
                        {"role": "assistant", "content": bot_content})
                else:
                    print(f"Erro: {result.get('error', 'Erro desconhecido')}")
            else:
                print(f"Erro HTTP {response.status_code}: {response.text}")

        except Exception as e:
            print(f"Erro na requisição: {e}")


def main():
    """Função principal que executa todos os testes."""
    print("🧪 Testando Coffee Shop Chatbot API\n")

    # Verificar se a API está rodando
    print("📡 Verificando se a API está rodando...")
    try:
        requests.get(f"{BASE_URL}/", timeout=5)
        print("✅ API está rodando!")
    except Exception as e:
        print(f"❌ API não está respondendo: {e}")
        print("\n💡 Para iniciar a API, execute:")
        print("   python main.py")
        return

    # Executar testes
    tests = [
        ("Endpoint raiz", test_root_endpoint),
        ("Endpoint /chat", test_chat_endpoint),
        ("Endpoint /chatbot", test_chatbot_legacy_endpoint),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        result = test_func()
        results.append((test_name, result))

    # Resumo dos testes
    print(f"\n{'='*50}")
    print("📊 RESUMO DOS TESTES:")
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {test_name}: {status}")

    # Oferecer chat interativo
    print(f"\n{'='*50}")
    response = input(
        "Deseja testar o chat interativo? (s/n): ").strip().lower()
    if response in ['s', 'sim', 'y', 'yes']:
        interactive_chat()


if __name__ == "__main__":
    main()
