# Lume & Co Customer Service Agent

## Description
This repository contains customer service AI agent for small online retailer. This agent designed to reduce customer support load.

## Requirement & Specification
- An AI agent act as customer service to answer FAQ from users regarding order, product, and company's policy
- Receives input (understand questions) -> Decide action to take (get context from database) 
- Memorize conversation within session
- UI for interacting
- Calculate confidence -> Decides action

## Architecture
- Engine :Ollama 
  - Ollama allows running open-source LLMs locally without any API key or paid cloud service
- Models 
  - llama3.2 : Conversation & Reasoning 
  - mxbai-embed-large : document embedding
- Framework : LangChain
  - Connect LLM, data, and retriever
- Database : Vector Database (ChromaDB)
  - Retrieve data with semantic similarity adding context to the response

# Installation
Use the package manager pip to install requirements with the following command:
 > `pip install -r requirements.txt`

or can be installed each module

## Usage
You can run this AI customer service agent in a Docker container without installing Ollama.

- Build docker image
```bash
docker build -t lume-agent .
```

- Run docker 
```commandline
docker run -it --rm \
  -v $(pwd)/transaction_datamart.csv:/app/transaction_datamart.csv \
  -v $(pwd)/chrome_langchain_db:/app/chrome_langchain_db \
  -p 11434:11434 \
  lume-agent
```

- Once the container run you'll see:
```
Lume & Co Customer Service Center
User type here (D for Done):
```