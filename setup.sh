#!/bin/bash
set -e

echo "→ Criando virtual environment..."
python3 -m venv venv

echo "→ Ativando venv e instalando dependências..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "→ Copiando .env.example para .env (se ainda não existir)..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   .env criado — edite com as credenciais do seu MySQL."
fi

echo ""
echo "✓ Setup concluído!"
echo ""
echo "Próximos passos:"
echo "  1. Edite o arquivo .env com as credenciais do MySQL"
echo "  2. source venv/bin/activate"
echo "  3. uvicorn app.main:app --reload"
