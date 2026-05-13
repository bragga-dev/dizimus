FROM python:3.12-slim

# Evita arquivos .pyc e ativa logs imediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências de sistema (psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements/base.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements/base.txt

# Copia o projeto
COPY . .