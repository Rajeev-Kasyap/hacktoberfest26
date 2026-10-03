#!/bin/bash
set -e

mkdir -p ~/.ollama-bin
cd ~/.ollama-bin

echo "Downloading Ollama binary resiliently (will resume if dropped)..."
wget -c --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 100 https://github.com/ollama/ollama/releases/download/v0.35.1/ollama-linux-amd64.tar.zst -O ollama.tar.zst

echo "Extracting Ollama..."
tar -I zstd -xf ollama.tar.zst

echo "Starting Ollama server..."
./bin/ollama serve > ollama_serve.log 2>&1 &
SERVER_PID=$!

echo "Waiting for server to start..."
sleep 5

echo "Pulling gemma4:e2b (Ollama handles retries automatically)..."
./bin/ollama pull gemma4:e2b

echo "Model downloaded successfully!"
kill $SERVER_PID
echo "Local AI setup complete."
