# Comandos para testar a API usando curl no PowerShell
# Execute estes comandos no terminal PowerShell

# ===============================================
# 1. VERIFICAR SE A API ESTÁ RODANDO
# ===============================================

# Testar endpoint raiz
curl http://localhost:8000/

# ===============================================
# 2. TESTAR COM test_input.json (MÉTODO SIMPLES)
# ===============================================

# Enviar conteúdo do test_input.json diretamente
# Primeiro, extrair as mensagens do test_input.json e converter para o formato da API

curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Eu gostaria de um latte, por favor"
      }
    ]
  }'

# ===============================================
# 3. USANDO ARQUIVO test_input.json DIRETAMENTE
# ===============================================

# Método 1: Ler arquivo e reformatar (requer processamento manual)
# O test_input.json tem formato: {"input": {"messages": [...]}}
# A API espera formato: {"messages": [...]}

# Método 2: Usar PowerShell para extrair e reformatar
# Execute este bloco no PowerShell:

$testInput = Get-Content "test_input.json" | ConvertFrom-Json
$messages = $testInput.input.messages
$apiPayload = @{ messages = $messages } | ConvertTo-Json -Depth 10

# Salvar payload reformatado em arquivo temporário
$apiPayload | Out-File -FilePath "temp_payload.json" -Encoding utf8

# Usar curl com arquivo temporário
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d "@temp_payload.json"

# Limpar arquivo temporário
Remove-Item "temp_payload.json"

# ===============================================
# 4. TESTAR ENDPOINT LEGACY /chatbot
# ===============================================

# O endpoint legacy aceita o formato direto do test_input.json
curl -X POST http://localhost:8000/chatbot `
  -H "Content-Type: application/json" `
  -d '{
    "messages": [
      {
        "role": "user", 
        "content": "Eu gostaria de um latte, por favor"
      }
    ]
  }'

# ===============================================
# 5. EXEMPLOS DE DIFERENTES MENSAGENS
# ===============================================

# Testar recomendação
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "O que você recomenda para o café da manhã?"
      }
    ]
  }'

# Testar detalhes de produto
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Me fale mais sobre o cappuccino"
      }
    ]
  }'

# Testar fazer pedido
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Quero fazer um pedido de 2 lattes e 1 croissant"
      }
    ]
  }'

# ===============================================
# 6. TESTE COM CONVERSA COMPLETA
# ===============================================

# Simular uma conversa com histórico
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Olá!"
      },
      {
        "role": "assistant", 
        "content": "Olá! Bem-vindo à nossa cafeteria. Como posso ajudá-lo hoje?"
      },
      {
        "role": "user",
        "content": "Eu gostaria de um café"
      }
    ]
  }'
