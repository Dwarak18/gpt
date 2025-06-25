# 🔧 Ollama Docker Troubleshooting Guide

This guide helps you resolve common issues with the Ollama Docker setup.

## 🚨 Common Issues & Solutions

### 1. "Docker is not running" Error

**Problem**: `❌ Docker is not running. Please start Docker first.`

**Solutions**:
- Install Docker Desktop from https://www.docker.com/products/docker-desktop
- Start Docker Desktop application
- Wait for Docker to fully initialize (check the system tray icon)
- Run the setup script again

### 2. Container Won't Start

**Problem**: Ollama container fails to start

**Solutions**:
```bash
# Check if port 11434 is already in use
netstat -an | findstr :11434

# Stop any existing containers
docker stop ollama-server
docker rm ollama-server

# Restart with docker-compose
docker-compose down
docker-compose up -d ollama
```

### 3. Model Download Issues

**Problem**: `❌ Failed to pull model 'llama3.2:1b-instruct-q4_K_M'`

**Solutions**:
- Check internet connection
- Try pulling manually:
  ```bash
  docker exec ollama-server ollama pull llama3.2:1b-instruct-q4_K_M
  ```
- Alternative model names to try:
  - `llama3.2:1b`
  - `llama3.2:latest`
  - `llama3.1:8b` (larger but more capable)

### 4. API Connection Issues

**Problem**: Flask app shows "Unable to connect to AI service"

**Solutions**:
```bash
# Check if Ollama is responding
curl http://localhost:11434/api/tags

# Check container logs
docker-compose logs ollama

# Restart the container
docker-compose restart ollama
```

### 5. Slow Response Times

**Problem**: AI takes a long time to respond

**Solutions**:
- First response is always slow (model loading)
- Increase timeout in `config.py`:
  ```python
  OLLAMA_TIMEOUT = 60  # Increase from 30 to 60 seconds
  ```
- Consider using a smaller model for faster responses:
  ```python
  OLLAMA_MODEL = "llama3.2:1b"  # Smaller, faster model
  ```

### 6. Memory Issues

**Problem**: Docker runs out of memory

**Solutions**:
- Increase Docker Desktop memory allocation:
  - Open Docker Desktop
  - Go to Settings → Resources → Memory
  - Increase to at least 8GB
  - Apply & Restart
- Use a smaller model:
  ```python
  OLLAMA_MODEL = "llama3.2:1b"  # Uses less memory
  ```

## 🔍 Diagnostic Commands

### Check Docker Status
```bash
docker info
docker ps
docker-compose ps
```

### Check Ollama Container
```bash
# View container logs
docker-compose logs ollama

# Access container shell
docker exec -it ollama-server bash

# Check available models inside container
docker exec ollama-server ollama list
```

### Test Ollama API
```bash
# Test basic connectivity
curl http://localhost:11434/api/tags

# Test model generation
curl -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d "{\"model\": \"llama3.2:1b-instruct-q4_K_M\", \"prompt\": \"Hello!\", \"stream\": false}"
```

## 🏃‍♂️ Quick Recovery Steps

If everything fails, try these steps in order:

1. **Complete Reset**:
   ```bash
   docker-compose down
   docker system prune -f
   docker volume prune -f
   docker-compose up -d ollama
   ```

2. **Re-run Setup**:
   ```bash
   setup-ollama.bat
   ```

3. **Check Health**:
   ```bash
   python ollama_health_check.py
   ```

4. **Start App**:
   ```bash
   start-with-ollama.bat
   ```

## 📞 Getting Help

If you're still having issues:

1. **Check the logs**: Run `docker-compose logs ollama` and look for error messages
2. **Check system resources**: Ensure you have enough RAM and disk space
3. **Try a different model**: Some models may not be available or may be corrupted
4. **Check firewall**: Ensure port 11434 is not blocked
5. **Update Docker**: Make sure you have the latest version of Docker Desktop

## 🔧 Advanced Configuration

### Custom Ollama Configuration

Create a `.env` file in your project directory:
```env
OLLAMA_HOST=0.0.0.0
OLLAMA_PORT=11434
OLLAMA_DEBUG=1
```

### Performance Tuning

Edit `docker-compose.yml` to add resource limits:
```yaml
services:
  ollama:
    # ... existing configuration ...
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G
```

### Alternative Models

If the default model doesn't work, try these alternatives:
- `llama3.2:1b` (smaller, faster)
- `llama3.1:8b` (larger, more capable)
- `phi3:mini` (very small and fast)
- `codellama:7b` (good for code-related tasks)

Remember to update `config.py` with your chosen model name!
