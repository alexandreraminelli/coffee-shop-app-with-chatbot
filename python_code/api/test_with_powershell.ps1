# Script PowerShell para testar a API usando test_input.json
# Execute no diretório api/: .\test_with_powershell.ps1

# Função para verificar se a API está rodando
function Test-ApiStatus {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get -TimeoutSec 5
        Write-Host "✅ API está rodando!" -ForegroundColor Green
        Write-Host "📋 Status: $($response.message)" -ForegroundColor Cyan
        return $true
    }
    catch {
        Write-Host "❌ API não está respondendo" -ForegroundColor Red
        Write-Host "💡 Inicie a API com: python main.py" -ForegroundColor Yellow
        return $false
    }
}

# Função para carregar test_input.json
function Get-TestInput {
    if (-not (Test-Path "test_input.json")) {
        Write-Host "❌ Arquivo test_input.json não encontrado!" -ForegroundColor Red
        Write-Host "💡 Certifique-se de estar no diretório api/" -ForegroundColor Yellow
        return $null
    }
    
    try {
        $content = Get-Content "test_input.json" -Raw | ConvertFrom-Json
        Write-Host "📁 Dados carregados do test_input.json:" -ForegroundColor Cyan
        Write-Host ($content | ConvertTo-Json -Depth 10) -ForegroundColor Gray
        return $content
    }
    catch {
        Write-Host "❌ Erro ao carregar test_input.json: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Função para testar o endpoint /chat
function Test-ChatEndpoint {
    param($TestData)
    
    Write-Host "`n🧪 Testando endpoint /chat..." -ForegroundColor Cyan
    Write-Host "=" * 50
    
    # Extrair mensagens do formato Runpod
    $messages = $TestData.input.messages
    
    # Preparar payload para FastAPI
    $payload = @{
        messages = $messages
    } | ConvertTo-Json -Depth 10
    
    Write-Host "📤 Enviando requisição para: http://localhost:8000/chat" -ForegroundColor Cyan
    Write-Host "📦 Payload:" -ForegroundColor Cyan
    Write-Host $payload -ForegroundColor Gray
    Write-Host ""
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 30
        
        Write-Host "📥 Resposta recebida:" -ForegroundColor Green
        Write-Host "✅ Sucesso!" -ForegroundColor Green
        Write-Host "📋 Resposta completa:" -ForegroundColor Cyan
        Write-Host ($response | ConvertTo-Json -Depth 10) -ForegroundColor Gray
        
        # Extrair conteúdo da resposta
        if ($response.success -and $response.response) {
            Write-Host "`n🤖 Resposta do Chatbot:" -ForegroundColor Green
            Write-Host "   $($response.response.content)" -ForegroundColor White
            
            if ($response.response.memory) {
                Write-Host "`n🧠 Memória/Metadata:" -ForegroundColor Cyan
                Write-Host ($response.response.memory | ConvertTo-Json -Depth 5) -ForegroundColor Gray
            }
        }
        
        return $true
    }
    catch {
        Write-Host "❌ Erro na requisição!" -ForegroundColor Red
        Write-Host "📄 Erro: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Função para testar endpoint legacy /chatbot
function Test-ChatbotLegacy {
    param($TestData)
    
    Write-Host "`n📱 Testando endpoint legacy /chatbot..." -ForegroundColor Cyan
    Write-Host "=" * 50
    
    # Usar mensagens diretamente
    $payload = @{
        messages = $TestData.input.messages
    } | ConvertTo-Json -Depth 10
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/chatbot" -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 30
        
        Write-Host "📥 Resposta do endpoint legacy:" -ForegroundColor Green
        Write-Host ($response | ConvertTo-Json -Depth 10) -ForegroundColor Gray
        
        # Extrair conteúdo
        if ($response.content) {
            Write-Host "`n🤖 Conteúdo: $($response.content)" -ForegroundColor White
        }
        
        return $true
    }
    catch {
        Write-Host "❌ Erro no endpoint legacy!" -ForegroundColor Red
        Write-Host "📄 Erro: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Script principal
function Main {
    Write-Host "🧪 Teste da API usando test_input.json" -ForegroundColor Cyan
    Write-Host "=" * 60
    Write-Host "📍 Diretório atual: $(Get-Location)" -ForegroundColor Cyan
    Write-Host ""
    
    # Verificar se a API está rodando
    Write-Host "🔍 Verificando status da API..." -ForegroundColor Cyan
    $apiRunning = Test-ApiStatus
    Write-Host ""
    
    if (-not $apiRunning) {
        Write-Host "💡 Para iniciar a API, execute em outro terminal:" -ForegroundColor Yellow
        Write-Host "   python main.py" -ForegroundColor White
        return
    }
    
    # Carregar dados de teste
    $testData = Get-TestInput
    if (-not $testData) {
        return
    }
    
    # Testar endpoints
    $chatSuccess = Test-ChatEndpoint -TestData $testData
    $legacySuccess = Test-ChatbotLegacy -TestData $testData
    
    # Resumo
    Write-Host "`n" + "=" * 60
    Write-Host "📊 RESUMO DOS TESTES:" -ForegroundColor Cyan
    
    $chatStatus = if ($chatSuccess) { "✅ PASSOU" } else { "❌ FALHOU" }
    $legacyStatus = if ($legacySuccess) { "✅ PASSOU" } else { "❌ FALHOU" }
    
    Write-Host "  Endpoint /chat: $chatStatus"
    Write-Host "  Endpoint /chatbot: $legacyStatus"
    Write-Host "`n✨ Teste concluído!" -ForegroundColor Green
}

# Executar script principal
Main
