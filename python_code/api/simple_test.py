#!/usr/bin/env python3
"""
Script SIMPLES para testar a API com test_input.json
"""

import requests
import json


def main():
    print("🧪 Teste SIMPLES usando test_input.json")
    print("=" * 50)

    # 1. Carregar test_input.json
    try:
        with open('test_input.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        print("✅ test_input.json carregado!")
        print(f"📄 Conteúdo: {json.dumps(test_data, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Erro ao carregar test_input.json: {e}")
        return

    # 2. Extrair mensagens (formato Runpod -> FastAPI)
    messages = test_data["input"]["messages"]
    payload = {"messages": messages}

    print(f"\n📤 Enviando para API: {json.dumps(payload, ensure_ascii=False)}")

    # 3. Fazer requisição
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=payload,
            timeout=60  # 60 segundos para o LLM responder
        )

        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCESSO!")

            if result.get("success") and "response" in result:
                bot_response = result["response"]
                print(
                    f"🤖 Resposta: {bot_response.get('content', 'Sem conteúdo')}")

                if "memory" in bot_response:
                    memory = bot_response["memory"]
                    print(f"🧠 Agente usado: {memory.get('agent', 'N/A')}")
                    if "order" in memory:
                        print(f"🛒 Pedido: {memory['order']}")
            else:
                print(f"❌ Erro na resposta: {result}")
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")

    except requests.exceptions.Timeout:
        print("⏰ Timeout - O LLM está demorando para responder")
        print("💡 Isso é normal na primeira execução ou se a API key estiver lenta")
    except requests.exceptions.ConnectionError:
        print("❌ Conexão falhou - API não está rodando?")
        print("💡 Execute: python main.py")
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
