FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .

# 7. Instalação de dependências
# O uso de --no-cache-dir evita que o pip armazene pacotes baixados em cache na imagem
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 8. Copiando o restante do código da aplicação
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]