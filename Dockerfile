# Imagem base oficial do Python (versão slim baseada em Debian)
FROM python:3.11-slim

# Instala dependências de sistema necessárias para compilar pacotes (como Rust/Tapo se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contentor
WORKDIR /app

# Copia os requisitos e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o script Python para dentro do contentor
COPY main.py .

# Variável de ambiente para garantir que os prints do Python aparecem logo no log do Docker
ENV PYTHONUNBUFFERED=1

# Comando para executar o script
CMD ["python", "main.py"]