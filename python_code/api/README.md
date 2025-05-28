# Coffee Shop Chatbot API

Esta é uma API FastAPI que substitui a implementação Runpod do chatbot da cafeteria. A API usa o mesmo `AgentController` existente, mas agora roda em um servidor FastAPI local.

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o Servidor

```bash
cd .\python_code\api\ &&

python main.py
```

O servidor será iniciado em:

- **URL Principal**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 Endpoints Disponíveis

### GET `/`

Endpoint de verificação de status da API.

**Resposta:**

```json
{
  "message": "Coffee Shop Chatbot API",
  "status": "running"
}
```

### POST `/chat`

Endpoint principal para interação com o chatbot.

**Payload:**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Eu gostaria de um latte, por favor"
    }
  ]
}
```

**Resposta de Sucesso:**

```json
{
  "success": true,
  "response": {
    "role": "assistant",
    "content": "Resposta do chatbot...",
    "memory": {...}
  }
}
```

**Resposta de Erro:**

```json
{
  "success": false,
  "error": "Descrição do erro"
}
```

### POST `/chatbot`

Endpoint legacy para compatibilidade com implementações existentes.

**Payload:**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Quais são as opções de café disponíveis?"
    }
  ]
}
```

## 🧪 Testando a API

### Usando o Script de Teste

Execute o script de teste incluído:

```bash
python test_api.py
```

Este script irá:

1. ✅ Verificar se a API está rodando
2. 🧪 Testar todos os endpoints
3. 💬 Oferecer um modo de chat interativo

### Usando curl

```bash
# Testar endpoint raiz
curl http://localhost:8000/

# Testar chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Eu gostaria de um cappuccino"
      }
    ]
  }'
```

### Usando Python requests

```python
import requests

# Fazer uma requisição para o chatbot
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "messages": [
            {
                "role": "user",
                "content": "Quero fazer um pedido"
            }
        ]
    }
)

print(response.json())
```

## 🧪 Testando com test_input.json

O arquivo `test_input.json` contém dados de teste no formato original do Runpod. Aqui estão várias formas de testá-lo:

### Método 1: Script Python Simples

```bash
python simple_test.py
```

### Método 2: Script Python Completo

```bash
python test_with_json.py
```

### Método 3: PowerShell Script

```powershell
.\test_with_powershell.ps1
```

### Método 4: Curl (PowerShell)

```powershell
# Criar payload temporário
$testInput = Get-Content "test_input.json" | ConvertFrom-Json
$messages = $testInput.input.messages
$payload = @{ messages = $messages } | ConvertTo-Json -Depth 10
$payload | Out-File -FilePath "temp_payload.json" -Encoding utf8

# Testar API
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "@temp_payload.json"

# Limpar
Remove-Item "temp_payload.json"
```

### Método 5: Teste Direto (sem API)

Se a API estiver com problemas, você pode testar diretamente o AgentController:

```python
from agent_controller import AgentController
import json

# Carregar test_input.json
with open('test_input.json', 'r') as f:
    test_data = json.load(f)

# Testar diretamente
controller = AgentController()
response = controller.get_response(test_data)
print(response)
```

### Formato dos Dados

**test_input.json (formato Runpod):**

```json
{
  "input": {
    "messages": [{ "role": "user", "content": "Eu gostaria de um latte, por favor" }]
  }
}
```

**API FastAPI (formato esperado):**

```json
{
  "messages": [{ "role": "user", "content": "Eu gostaria de um latte, por favor" }]
}
```

A conversão é feita automaticamente pelos scripts de teste.

## 🔧 Integração com Frontend

Para integrar com seu app React Native ou qualquer frontend:

1. **URL Base**: `http://localhost:8000` (ou seu domínio em produção)
2. **Endpoint**: `POST /chat`
3. **Headers**: `Content-Type: application/json`
4. **Body**: Formato JSON com array de mensagens

### Exemplo React Native

```javascript
const sendMessage = async (messages) => {
  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: messages,
      }),
    })

    const data = await response.json()

    if (data.success) {
      return data.response.content
    } else {
      console.error("Erro:", data.error)
    }
  } catch (error) {
    console.error("Erro na requisição:", error)
  }
}
```

## 🛠️ Diferenças da Implementação Runpod

### Antes (Runpod)

```python
# Runpod serverless
runpod.serverless.start({'handler': agent_controller.get_response})
```

### Agora (FastAPI)

```python
# Servidor FastAPI local
app = FastAPI()

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    response = agent_controller.get_response(input_data)
    return {"success": True, "response": response}
```

## 🌟 Vantagens da Nova Implementação

1. **💰 Gratuita**: Não há custos de serverless
2. **🚀 Rápida**: Resposta mais rápida sem cold starts
3. **🔧 Flexível**: Fácil de personalizar e debug
4. **📚 Documentada**: Swagger UI automática
5. **🧪 Testável**: Scripts de teste incluídos
6. **🔗 Compatível**: Mantém a mesma lógica do `AgentController`

## 🐛 Troubleshooting

### Porta 8000 em uso

```bash
# Encontrar processo usando a porta
netstat -ano | findstr :8000

# Matar o processo (substitua PID)
taskkill /PID <PID> /F
```

### Erro de importação

Certifique-se de que todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
```

### Problemas de CORS

A API está configurada para aceitar requisições de qualquer origem. Em produção, configure `allow_origins` com domínios específicos.

## 📝 Logs e Debug

O servidor FastAPI mostra logs detalhados no terminal, incluindo:

- Requisições recebidas
- Erros de processamento
- Status de resposta

Para mais informações de debug, você pode adicionar prints no `agent_controller.py` ou nos agentes individuais.
