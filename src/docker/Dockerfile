# Etapa 1: Imagem base Python
FROM python:3.10-slim AS base

# Etapa 2: Definir diretório de trabalho
WORKDIR /app

# Etapa 3: Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Etapa 4: Instalar dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiar código do projeto
COPY . .

# Etapa 6: Configurar variável de ambiente para FastAPI (opcional)
ENV UVICORN_CMD="uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

# Etapa 7: Expor a porta do FastAPI
EXPOSE 8000

# Etapa 8: Rodar o servidor FastAPI
CMD ["sh", "-c", "$UVICORN_CMD"]
