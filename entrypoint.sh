#!/bin/bash
set -e

echo "=== [ur.s3c] Iniciando demonio de Ollama ==="
ollama serve &

echo "=== [ur.s3c] Esperando a Ollama (Healthcheck) ==="
# Esperar hasta que responda el API
until curl -s http://127.0.0.1:11434/api/tags > /dev/null; do
  sleep 2
done

echo "=== [ur.s3c] Cargando modelo llama3.2:1b (Optimizado) ==="
ollama pull llama3.2:1b

echo "=== [ur.s3c] Lanzando Aplicacion BogotaTrust CTF ==="
# Usamos uvicorn porque tu main.py es FastAPI
exec uvicorn main:app --host 0.0.0.0 --port 8501