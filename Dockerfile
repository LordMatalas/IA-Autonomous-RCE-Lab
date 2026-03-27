# Base image
FROM python:3.11-slim-bookworm

# Metadata
LABEL maintainer="ur.s3c Research Team"
LABEL description="Lab de ataque a LLMs - OWASP Top 10 for LLMs"

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends 
    curl 
    ca-certificates 
    && rm -rf /var/lib/apt/lists/*

# Ollama Integration: Install official binary directly
RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama 
    && chmod +x /usr/bin/ollama

# Set working directory
WORKDIR /app

# App Setup: Copy requirements.txt and install dependencies
COPY ctf-llm/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code and RAG documents
COPY ctf-llm/main.py .
COPY ctf-llm/prompts.py .
COPY ctf-llm/tools.py .
COPY ctf-llm/docs/ ./docs/
COPY ctf-llm/static/ ./static/
COPY ctf-llm/secret/ ./secret/

# Orchestration script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Expose Streamlit port (as specified by user, though app is FastAPI)
EXPOSE 8501

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
