# Dockerfile para PyBlaze
# Jogo de plataforma 2D desenvolvido em Python com pygame-ce

FROM python:3.14-slim

# Metadados
LABEL maintainer="PyBlaze Team"
LABEL description="PyBlaze - High-speed 2D platformer game"
LABEL version="1.7.1"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema para pygame e SDL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libfreetype6 \
    libportmidi0 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar UV (gerenciador de pacotes rápido)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos de configuração primeiro (cache de layers)
COPY pyproject.toml ./
COPY README.md ./

# Instalar dependências Python
RUN uv sync

# Copiar código-fonte
COPY src/ ./src/
COPY assets/ ./assets/

# Expor porta para possível servidor web futuro
EXPOSE 8000

# Healthcheck (verifica se pygame pode inicializar)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import pygame; pygame.init(); print('OK')" || exit 1

# Comando padrão: executar o jogo em modo headless (para testes)
# Para rodar com display, use docker run com -e DISPLAY=$DISPLAY
CMD ["uv", "run", "python", "src/pyblaze/main.py"]
