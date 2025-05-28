#!/usr/bin/env python3
"""
Script para testar a API usando o arquivo test_input.json
(similar ao comportamento do Runpod)
"""

import requests
import json
import sys
import os


def load_test_input():
    """Carrega o arquivo test_input.json"""
    try:
        with open('test_input.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo test_input.json não encontrado!")
        print("💡 Certifique-se de estar no diretório correto (api/)")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        return None


def test_with_input_file():
    """Testa a API usando o test_input.json"""
    print("🧪 Testando API com test_input.json")
    print("=" * 50)

    # Carregar dados de teste
    test_data = load_test_input()
    if not test_data:
        return False

    print("📁 Dados carregados do test_input.json:")
    print(json.dumps(test_data, ensure_ascii=False, indent=2))
    print()

    # URL da API
    url = "http://localhost:8000/chat"

    # Extrair mensagens do formato Runpod
    messages = test_data.get("input", {}).get("messages", [])

    # Preparar payload para FastAPI
    payload = {"messages": messages}

    print("📤 Enviando requisição para:", url)
    print("📦 Payload:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print()

    try:
        # Fazer requisição
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )

        print("📥 Resposta recebida:")
        print(f"🔢 Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Sucesso!")
            print("📋 Resposta completa:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

            # Extrair conteúdo da resposta para exibição mais limpa
            if result.get("success") and "response" in result:
                bot_response = result["response"]
                print("\n🤖 Resposta do Chatbot:")
                print(f"   {bot_response.get('content', 'Sem conteúdo')}")

                # Mostrar memória se disponível
                if "memory" in bot_response:
                    print("\n🧠 Memória/Metadata:")
                    print(json.dumps(
                        bot_response["memory"], ensure_ascii=False, indent=2))

            return True
        else:
            print("❌ Erro na requisição!")
            print("📄 Resposta:")
            print(response.text)
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão!")
        print("💡 Certifique-se de que a API está rodando:")
        print("   python main.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout na requisição!")
        print("💡 O servidor pode estar sobrecarregado ou com problemas")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def test_direct_agent_controller():
    """Testa diretamente o AgentController (sem API)"""
    print("\n🔧 Teste direto do AgentController (sem API)")
    print("=" * 50)

    try:
        # Importar o AgentController
        from agent_controller import AgentController

        # Carregar dados de teste
        test_data = load_test_input()
        if not test_data:
            return False

        print("📁 Dados de teste:", json.dumps(
            test_data, ensure_ascii=False, indent=2))

        # Instanciar controlador
        print("🔄 Instanciando AgentController...")
        agent_controller = AgentController()

        # Chamar método get_response diretamente
        print("🚀 Executando get_response...")
        response = agent_controller.get_response(test_data)

        print("📥 Resposta do AgentController:")
        if response:
            print(json.dumps(response, ensure_ascii=False, indent=2))

            # Extrair conteúdo da resposta
            print(f"\n🤖 Conteúdo: {response.get('content', 'Sem conteúdo')}")

            if "memory" in response:
                print("\n🧠 Memória:")
                print(json.dumps(response["memory"],
                      ensure_ascii=False, indent=2))

            return True
        else:
            print("❌ Resposta vazia (provavelmente bloqueada pelo Guard Agent)")
            return False

    except ImportError as e:
        print(f"❌ Erro ao importar AgentController: {e}")
        print("💡 Certifique-se de estar no diretório correto")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def check_api_status():
    """Verifica se a API está rodando"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ API está rodando!")
            return True
        else:
            print(f"⚠️ API respondeu com status {response.status_code}")
            return False
    except:
        print("❌ API não está respondendo")
        print("💡 Inicie a API com: python main.py")
        return False


def main():
    """Função principal"""
    print("🧪 Teste usando test_input.json")
    print("=" * 60)

    # Verificar se estamos no diretório correto
    if not os.path.exists('test_input.json'):
        print("❌ Arquivo test_input.json não encontrado!")
        print("💡 Execute este script no diretório api/:")
        print("   cd python_code/api")
        print("   python test_with_json.py")
        return

    print("📍 Diretório atual:", os.getcwd())
    print()

    # Verificar status da API
    print("🔍 Verificando status da API...")
    api_running = check_api_status()
    print()

    if api_running:
        # Testar via API
        success = test_with_input_file()

        if not success:
            print("\n🔄 Tentando teste direto...")
            test_direct_agent_controller()
    else:
        print("🔄 Testando diretamente o AgentController...")
        test_direct_agent_controller()

    print("\n" + "=" * 60)
    print("✨ Teste concluído!")


if __name__ == "__main__":
    main()
