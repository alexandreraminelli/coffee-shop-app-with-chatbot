@echo off
echo Instalando dependências do projeto com pacotes binários para evitar requisitos de compilação...
python -m pip install --upgrade pip
python -m pip install --only-binary :all: pandas==2.0.3
python -m pip install -r python_code\api\requirements.txt
echo.
echo Instalação concluída! Verifique se não ocorreram erros acima.
echo.
pause
