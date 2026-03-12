# PyBlaze - Referência Rápida

> Comandos e informações essenciais para trabalhar com o PyBlaze

---

## 🚀 Comandos Essenciais

### Setup Inicial
```bash
# Instalar UV (apenas uma vez)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# ou
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Clonar e configurar projeto
cd pyblaze
uv sync
uv pip install -e .
```

### Executar o Jogo
```bash
uv run python src/pyblaze/main.py
```

### Testes
```bash
# Rodar todos os testes
uv run pytest

# Sem cobertura (mais rápido)
uv run pytest --no-cov

# Com verbose
uv run pytest -v

# Apenas um arquivo
uv run pytest tests/unit/test_player.py
```

### Code Quality
```bash
# Formatar código
uv run black src/ tests/

# Lint
uv run ruff check src/ tests/

# Lint + autofix
uv run ruff check src/ tests/ --fix --unsafe-fixes

# Type checking
uv run mypy src/

# Tudo de uma vez
uv run black src/ tests/ && \
uv run ruff check src/ tests/ --fix --unsafe-fixes && \
uv run mypy src/ && \
uv run pytest --no-cov
```

---

## 🎮 Controles do Jogo

### Menu
- `W/S` ou `↑/↓` - Navegar
- `Enter` ou `Space` - Selecionar

### Gameplay
- `A/D` ou `←/→` - Mover
- `Space` - Pular (segurar = pulo alto)
- `Left Shift` - Spin attack (no ar)
- `ESC` - Menu

### Game Over / Vitória
- `Space` - Reiniciar
- `ESC` - Menu principal

---

## 📁 Estrutura Simplificada

```
pyblaze/
├── src/pyblaze/           # Código fonte
│   ├── entities/         # Player, Enemy, Ring, Checkpoint
│   ├── systems/          # Physics, Camera, HUD
│   ├── scenes/           # Menu, Game, GameOver
│   ├── utils/            # SpriteSheet, Audio
│   ├── settings.py       # TODAS as constantes
│   └── main.py           # Entry point
├── tests/                # Testes unitários
├── docs/                 # Documentação
└── pyproject.toml        # Configurações
```

---

## 🔧 Troubleshooting

### Problema: Testes não encontram módulos
```bash
# Solução: Instalar em modo editable
uv pip install -e .
```

### Problema: MyPy reclama de pygame
```toml
# pyproject.toml já tem:
[tool.mypy]
ignore_missing_imports = true
```

### Problema: Ruff muitos warnings
```bash
# Use unsafe-fixes para correção automática
uv run ruff check src/ tests/ --fix --unsafe-fixes
```

### Problema: Jogo não abre
```bash
# Verificar se pygame instalou corretamente
uv run python -c "import pygame; print(pygame.ver)"

# Reinstalar dependências
uv sync --reinstall
```

---

## 📊 Métricas Importantes

| Métrica | Valor | Comando |
|---------|-------|---------|
| Testes | 26 | `uv run pytest` |
| Cobertura | Focada em lógica | `uv run pytest --cov` |
| MyPy | 0 erros | `uv run mypy src/` |
| Ruff | 0 warnings | `uv run ruff check src/` |
| FPS | 60 (estável) | Rodar jogo |
| LOC | ~1500 | `find src -name "*.py" \| xargs wc -l` |

---

## 🎯 Checklist de Desenvolvimento

Antes de commit:
- [ ] `uv run black src/ tests/`
- [ ] `uv run ruff check src/ tests/ --fix`
- [ ] `uv run mypy src/`
- [ ] `uv run pytest --no-cov`
- [ ] Testar o jogo manualmente

Antes de release:
- [ ] Todos os testes passando
- [ ] README atualizado
- [ ] CHANGELOG atualizado (se aplicável)
- [ ] Versão atualizada no `pyproject.toml`
- [ ] Tag no git: `git tag v1.0.0`

---

## 💡 Dicas Rápidas

### Adicionar Nova Entidade
1. Criar arquivo em `src/pyblaze/entities/`
2. Herdar de `BaseEntity`
3. Implementar `update()` e `draw()`
4. Adicionar testes em `tests/unit/`
5. Usar em `scenes/game.py`

### Adicionar Nova Cena
1. Criar arquivo em `src/pyblaze/scenes/`
2. Herdar de `BaseScene`
3. Implementar `handle_event()`, `update()`, `draw()`
4. Usar `switch_to()` para transições

### Ajustar Gameplay
- Todas as constantes estão em `settings.py`
- Exemplos:
  - Velocidade: `PLAYER_SPEED`, `PLAYER_SPRINT_SPEED`
  - Física: `GRAVITY`, `JUMP_FORCE`
  - Player: `PLAYER_LIVES`, `INVINCIBILITY_FRAMES`

### Debugar
```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Variável: %s", variavel)  # Só em development
logger.info("Evento importante")        # Sempre visível
logger.warning("Algo inesperado")       # Warnings
logger.error("Erro!")                   # Erros
```

---

## 📚 Links Úteis

### Documentação do Projeto
- [INDEX.md](INDEX.md) - Índice completo
- [LESSONS_LEARNED.md](LESSONS_LEARNED.md) - Problemas e soluções
- [game_agent.md](prompts/game_agent.md) - Prompt de desenvolvimento

### Documentação Externa
- [Python 3.12](https://docs.python.org/3.12/)
- [pygame-ce](https://pyga.me/)
- [UV](https://github.com/astral-sh/uv)
- [Ruff](https://docs.astral.sh/ruff/)
- [MyPy](https://mypy.readthedocs.io/)

---

## 🔥 Comandos Mais Usados

```bash
# Desenvolvimento diário
uv run python src/pyblaze/main.py       # Testar jogo
uv run pytest --no-cov                  # Rodar testes
uv run ruff check src/ --fix            # Lint rápido

# Antes de commit
uv run black src/ tests/ && \
uv run ruff check src/ tests/ --fix && \
uv run mypy src/ && \
uv run pytest --no-cov

# Adicionar dependência
uv add nome-do-pacote                   # Runtime
uv add --dev nome-do-pacote             # Development

# Atualizar dependências
uv lock --upgrade
uv sync
```

---

## ⚡ Atalhos Úteis

### VSCode
- `F5` - Debug
- `Ctrl+Shift+P` → "Python: Run File in Terminal"
- `Ctrl+Shift+P` → "Python: Select Interpreter" (escolher .venv)

### Terminal
```bash
# Alias úteis (adicionar ao .bashrc ou .zshrc)
alias uvtest='uv run pytest --no-cov'
alias uvrun='uv run python src/pyblaze/main.py'
alias uvcheck='uv run black src/ tests/ && uv run ruff check src/ tests/ --fix && uv run mypy src/'
```

---

## 🎮 Easter Eggs

- O jogador pisca quando invencível (após tomar dano)
- Anéis perdidos voam em direções aleatórias
- Sprint ativa automaticamente após 1 segundo correndo
- Câmera usa lerp para movimento suave
- Logs mostram tudo que acontece no jogo

---

**Mantenha esta página favoritada para referência rápida!** 📌
