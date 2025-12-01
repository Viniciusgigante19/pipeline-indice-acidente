FROM python:3.11-slim

WORKDIR /app

# Copia a pasta src do projeto para dentro do container
COPY ../../src ./src

# Copia o requirements.txt que agora está ao lado do Dockerfile
COPY docker/testes_python/requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Mantém o container em modo interativo Python
CMD ["python3"]
