# ==========================================
# STAGE 1: Extractor del Binario de Ollama
# ==========================================
FROM ollama/ollama:latest as ollama_bin

# ==========================================
# STAGE 2: Imagen Final (Ultra Ligera)
# ==========================================
FROM python:3.11-slim-bookworm

# Metadata para HTB Colombia y ur.s3c
LABEL maintainer="ur.s3c Research Team"
LABEL description="Lab de ataque a LLMs - OWASP Top 10 for LLMs"

# Instalar utilidades básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Magia negra: Copiar SOLO el ejecutable (pesa megas, no gigas)
COPY --from=ollama_bin /usr/bin/ollama /usr/bin/ollama

# Variables de entorno críticas
ENV OLLAMA_MODELS=/root/.ollama/models
ENV OLLAMA_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Configurar el entorno de trabajo
WORKDIR /app

# Instalar dependencias de Python (Aprovechando la caché de Docker)
COPY ctf-llm/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del CTF
COPY ctf-llm/main.py .
COPY ctf-llm/prompts.py .
COPY ctf-llm/tools.py .
COPY ctf-llm/docs/ ./docs/
COPY ctf-llm/static/ ./static/
COPY ctf-llm/secret/ ./secret/

# Configurar el script de arranque
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Exponer el puerto de tu FastAPI
EXPOSE 8501

ENTRYPOINT ["/app/entrypoint.sh"]