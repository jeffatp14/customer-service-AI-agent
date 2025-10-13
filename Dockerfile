#Python base
FROM python:3.11-slim

#Install Ollama
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.ai/install.sh | bash && \
    rm -rf /var/lib/apt/lists/*

#Set working directory
WORKDIR /app

#Copy your project files
COPY . /app

#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Download models
RUN ollama pull llama3.2 && ollama pull mxbai-embed-large

#Command to start ollama and AI agenf
CMD ollama serve & sleep 8 && python main.py
