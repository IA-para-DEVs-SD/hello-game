# Makefile para PyBlaze
# Comandos de conveniência para desenvolvimento

.PHONY: help install test test-cov lint format type-check check run clean build-exe

# Cores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)PyBlaze - Comandos Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Instala dependências e o pacote
	@echo "$(BLUE)Instalando dependências...$(NC)"
	uv sync
	uv pip install -e .
	@echo "$(GREEN)✓ Instalação concluída!$(NC)"

test: ## Executa todos os testes
	@echo "$(BLUE)Executando testes...$(NC)"
	uv run pytest -v
	@echo "$(GREEN)✓ Testes concluídos!$(NC)"

test-cov: ## Executa testes com cobertura e gera relatório HTML
	@echo "$(BLUE)Executando testes com cobertura...$(NC)"
	uv run pytest --cov=src/pyblaze --cov-report=html --cov-report=term -v
	@echo "$(GREEN)✓ Relatório gerado em htmlcov/index.html$(NC)"

lint: ## Verifica qualidade do código com Ruff
	@echo "$(BLUE)Verificando código com Ruff...$(NC)"
	uv run ruff check src/ tests/
	@echo "$(GREEN)✓ Verificação concluída!$(NC)"

format: ## Formata código com Ruff
	@echo "$(BLUE)Formatando código...$(NC)"
	uv run ruff format src/ tests/
	uv run ruff check src/ tests/ --fix
	@echo "$(GREEN)✓ Código formatado!$(NC)"

type-check: ## Verifica tipos com MyPy
	@echo "$(BLUE)Verificando tipos com MyPy...$(NC)"
	uv run mypy src/
	@echo "$(GREEN)✓ Verificação de tipos concluída!$(NC)"

check: format lint type-check test ## Executa todas as verificações (format + lint + type + test)
	@echo "$(GREEN)✓ Todas as verificações passaram!$(NC)"

run: ## Executa o jogo
	@echo "$(BLUE)Iniciando PyBlaze...$(NC)"
	uv run python src/pyblaze/main.py

clean: ## Remove arquivos temporários e cache
	@echo "$(YELLOW)Limpando arquivos temporários...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info 2>/dev/null || true
	@echo "$(GREEN)✓ Limpeza concluída!$(NC)"

build-exe: ## Cria executável standalone com PyInstaller
	@echo "$(BLUE)Criando executável...$(NC)"
	@if [ ! -d "build" ]; then mkdir build; fi
	uv run python build/build.py
	@echo "$(GREEN)✓ Executável criado em dist/$(NC)"

dev: install ## Setup completo do ambiente de desenvolvimento
	@echo "$(BLUE)Configurando ambiente de desenvolvimento...$(NC)"
	@echo "$(GREEN)✓ Ambiente pronto! Use 'make run' para executar o jogo$(NC)"

ci: ## Simula o pipeline de CI localmente
	@echo "$(BLUE)Executando pipeline de CI...$(NC)"
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) type-check
	@$(MAKE) test-cov
	@echo "$(GREEN)✓ Pipeline de CI concluído com sucesso!$(NC)"

watch-test: ## Executa testes em modo watch (requer pytest-watch)
	@echo "$(BLUE)Modo watch ativado (Ctrl+C para sair)...$(NC)"
	uv run ptw -- -v

.DEFAULT_GOAL := help
