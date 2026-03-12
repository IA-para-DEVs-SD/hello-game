# Docker Best Practices — Guia de Boas Práticas

> **Público-alvo:** Este documento é destinado a agentes de IA e desenvolvedores que precisam criar, manter e fazer deploy de containers Docker. Siga estas regras **sempre**, salvo indicação explícita do mantenedor do projeto. O objetivo é garantir imagens seguras, enxutas, reproduzíveis e prontas para produção.

---

## 1. Estrutura do Dockerfile

### Ordem das instruções (otimização de cache)

A ordem das instruções importa. O Docker invalida o cache a partir da primeira instrução que muda. Coloque o que muda **menos** no topo e o que muda **mais** no final.

```dockerfile
# ✅ Ordem correta — aproveita cache ao máximo
FROM python:3.11-slim

# 1. Metadados (raramente mudam)
LABEL maintainer="team@company.com"
LABEL version="1.0.0"

# 2. Dependências do sistema (mudam pouco)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 3. Dependências da aplicação (mudam às vezes)
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

# 4. Código-fonte (muda com frequência — sempre por último)
COPY src/ ./src/

# 5. Comando de execução
CMD ["python", "-m", "myproject.main"]
```

```dockerfile
# ❌ Errado — copia tudo antes de instalar deps, invalida cache a cada mudança de código
FROM python:3.11
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

---

## 2. Imagem Base

### Regras de escolha

| Situação                          | Imagem recomendada              |
|-----------------------------------|---------------------------------|
| Aplicação Python padrão           | `python:3.11-slim`              |
| ML com dependências nativas       | `python:3.11-slim` + build deps |
| Máxima leveza (sem shell)         | `python:3.11-alpine`            |
| Multi-arch / produção crítica     | `python:3.11-slim-bookworm`     |
| Base genérica Linux               | `debian:bookworm-slim`          |

### Regras obrigatórias

- **Sempre** fixar a versão da imagem base — nunca usar `latest`.
- **Sempre** usar variantes `slim` ou `alpine` em produção.
- **Nunca** usar imagens sem procedência (usuários aleatórios do Docker Hub).

```dockerfile
# ✅ Correto — versão fixada, variante slim
FROM python:3.11.9-slim-bookworm

# ❌ Errado — latest não é reproduzível
FROM python:latest
FROM ubuntu:latest
```

---

## 3. Multi-stage Build

Use multi-stage builds para separar o ambiente de build do ambiente de execução. Resultado: imagem final muito menor e sem ferramentas de build expostas.

```dockerfile
# ── Stage 1: Builder ──────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Instala uv e dependências
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ── Stage 2: Runtime ──────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Usuário não-root (segurança)
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copia apenas o virtualenv gerado no builder
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/

# Garante que o venv seja usado
ENV PATH="/app/.venv/bin:$PATH"

USER appuser

CMD ["python", "-m", "myproject.main"]
```

---

## 4. Segurança

### Nunca rodar como root

```dockerfile
# ✅ Criar e usar usuário não-root
RUN useradd --uid 1001 --create-home appuser
USER appuser

# ❌ Rodar como root (padrão se não especificado)
# FROM python:3.11-slim
# CMD ["python", "main.py"]  ← roda como root
```

### Nunca embutir segredos na imagem

```dockerfile
# ❌ NUNCA — segredo fica gravado nas layers da imagem
ENV DATABASE_PASSWORD="supersecret123"
RUN curl -H "Authorization: Bearer hardcoded_token" https://api.example.com

# ✅ Usar variáveis de ambiente em runtime
ENV DATABASE_URL=""  # valor vazio como placeholder de documentação
# Passar em runtime: docker run -e DATABASE_URL="..." myimage
```

### Verificar vulnerabilidades

```bash
# Escanear imagem com trivy (recomendado no CI)
trivy image myproject:latest

# Docker Scout (integrado ao Docker Desktop)
docker scout cves myproject:latest
```

### `.dockerignore` obrigatório

```dockerignore
# .dockerignore — sempre presente na raiz do projeto
.git
.gitignore
.env
.env.*
__pycache__
*.pyc
*.pyo
*.egg-info
.pytest_cache
.mypy_cache
.ruff_cache
dist/
build/
node_modules/
*.log
.DS_Store
README.md
docs/
tests/
notebooks/
```

---

## 5. Boas Práticas de RUN

### Agrupar comandos relacionados em uma única instrução

Cada `RUN` cria uma nova layer. Agrupar reduz o número de layers e o tamanho final.

```dockerfile
# ✅ Correto — uma layer, limpeza no mesmo RUN
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# ❌ Errado — múltiplas layers desnecessárias, cache de apt não limpo
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y libpq-dev
```

### Flags importantes do apt-get

```dockerfile
# --no-install-recommends → não instala pacotes recomendados desnecessários
# -y → não pede confirmação
# rm -rf /var/lib/apt/lists/* → limpa cache do apt após instalação
RUN apt-get update && apt-get install -y --no-install-recommends \
    pacote1 pacote2 \
    && rm -rf /var/lib/apt/lists/*
```

---

## 6. COPY vs ADD

```dockerfile
# ✅ Sempre preferir COPY — comportamento previsível
COPY src/ ./src/
COPY pyproject.toml ./

# ✅ ADD apenas quando necessário para extrair arquivos tar locais
ADD archive.tar.gz /app/data/

# ❌ Nunca usar ADD para copiar arquivos simples
ADD src/ ./src/         # COPY é correto aqui
ADD https://... /app/   # use RUN curl/wget em vez disso
```

---

## 7. Variáveis de Ambiente (ENV e ARG)

```dockerfile
# ARG → apenas em build time (não persiste na imagem final)
ARG PYTHON_VERSION=3.11
ARG BUILD_ENV=production

# ENV → persiste na imagem e fica disponível em runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ❌ Nunca usar ARG para segredos — aparecem no histórico do build
ARG SECRET_KEY="mysecret"  # NUNCA
```

### Variáveis Python recomendadas para produção

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1   # não gera arquivos .pyc
ENV PYTHONUNBUFFERED=1          # logs aparecem imediatamente (sem buffer)
ENV PYTHONFAULTHANDLER=1        # traceback em falhas de segfault
```

---

## 8. HEALTHCHECK

Todo serviço de longa duração deve ter HEALTHCHECK para orquestradores (Docker Compose, Kubernetes).

```dockerfile
# Para aplicações web (FastAPI, Flask)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Para workers ou processos que não expõem HTTP
HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD python -c "import myproject; myproject.healthcheck()" || exit 1
```

---

## 9. Docker Compose

### Estrutura padrão

```yaml
# docker-compose.yml
version: "3.9"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime          # aponta para o stage correto no multi-stage
    image: myproject-api:local
    container_name: myproject-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}   # lê do .env local
      - LOG_LEVEL=${LOG_LEVEL:-INFO}   # valor default
    env_file:
      - .env                           # alternativa ao environment acima
    volumes:
      - ./src:/app/src:ro              # :ro = read-only em dev
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Separar ambientes com override

```bash
docker-compose.yml           # base (produção)
docker-compose.override.yml  # dev (aplicado automaticamente)
docker-compose.test.yml      # testes

# Uso em CI
docker compose -f docker-compose.yml -f docker-compose.test.yml up
```

---

## 10. Nomenclatura e Tags de Imagem

### Convenção de tags

```
<registry>/<projeto>/<servico>:<versao>-<variante>

# Exemplos:
gcr.io/my-gcp-project/nbo-api:2.3.1
gcr.io/my-gcp-project/nbo-api:2.3.1-slim
gcr.io/my-gcp-project/nbo-worker:latest   # apenas em dev/staging, nunca prod
```

### Estratégia de tagging no CI/CD

```bash
# Em pipelines: sempre taguear com commit SHA + versão semântica
IMAGE="gcr.io/my-project/myservice"
TAG_SHA="${IMAGE}:$(git rev-parse --short HEAD)"
TAG_VERSION="${IMAGE}:v1.2.3"
TAG_LATEST="${IMAGE}:latest"

docker build -t "$TAG_SHA" -t "$TAG_VERSION" -t "$TAG_LATEST" .
docker push "$TAG_SHA"
docker push "$TAG_VERSION"
# latest apenas em staging/dev — nunca referenciar latest em manifests de produção
```

---

## 11. Otimização de Tamanho

### Checklist de redução de tamanho

```dockerfile
# 1. Imagem base slim/alpine
FROM python:3.11-slim

# 2. Multi-stage — copiar só o necessário para runtime
COPY --from=builder /app/.venv /app/.venv

# 3. Limpar cache em cada RUN de instalação
RUN pip install ... && pip cache purge
RUN apt-get install ... && rm -rf /var/lib/apt/lists/*

# 4. Não copiar arquivos desnecessários (.dockerignore)

# 5. Não instalar dependências de dev na imagem de produção
RUN uv sync --frozen --no-dev   # --no-dev é essencial
```

### Inspecionar tamanho das layers

```bash
docker images myproject:latest
docker history myproject:latest --human --format "{{.Size}}\t{{.CreatedBy}}"
dive myproject:latest   # ferramenta visual para análise de layers
```

---

## 12. Referência Rápida

```
IMAGEM BASE:    sempre fixar versão | usar slim/alpine | nunca latest em produção
CACHE:          dependências antes do código-fonte | agrupar RUN relacionados
MULTI-STAGE:    separar build de runtime | imagem final sem ferramentas de build
SEGURANÇA:      nunca root | nunca segredos em ENV/ARG | .dockerignore obrigatório
VARIÁVEIS:      ARG = build time | ENV = runtime | segredos sempre via -e ou secrets
HEALTHCHECK:    obrigatório em todo serviço de longa duração
COMPOSE:        um arquivo base + overrides por ambiente | depends_on com condition
TAGS:           SHA + versão semântica no CI | nunca latest em manifests de produção

NUNCA:
  - FROM python:latest
  - ENV SECRET_KEY="valor_real"
  - COPY . . antes de instalar dependências
  - Rodar processo principal como root
  - Imagem sem .dockerignore
  - apt-get sem rm -rf /var/lib/apt/lists/*
```