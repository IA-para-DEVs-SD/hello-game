# PyBlaze — Especificações Técnicas v1.0

> Guia técnico completo do projeto PyBlaze. Define stack, ferramentas, configurações, estrutura de código e padrões de desenvolvimento. Destinado a desenvolvedores e agentes de IA que vão implementar o projeto.

---

## Metadados

| Campo            | Valor                        |
|------------------|------------------------------|
| Projeto          | PyBlaze                      |
| Versão do guia   | 1.0                          |
| Data             | 2025-03-11                   |
| Python alvo      | **3.12**                     |
| Gerenciador      | **uv**                       |
| Testes           | **pytest**                   |
| Requisito chave  | Apenas Python para rodar     |

---

## 1. Escolha da Engine — Bibliotecas para Jogos em Python

### Comparativo de opções

| Biblioteca       | Tipo              | Instalação    | Ideal para                          | Obs                                          |
|------------------|-------------------|---------------|-------------------------------------|----------------------------------------------|
| **pygame-ce**    | 2D / SDL2         | `pip install` | Jogos 2D completos, controle total  | ✅ **Escolha do projeto** — madura e ativa   |
| `arcade`         | 2D / OpenGL       | `pip install` | Jogos 2D modernos, API mais simples | Boa para iniciantes, menos controle fino     |
| `pyxel`          | 2D retro          | `pip install` | Jogos pixel art com limites retro   | Limita resolução/cores intencionalmente      |
| `pyglet`         | 2D/3D / OpenGL    | `pip install` | Jogos com áudio/vídeo avançado      | Mais verboso, sem abstrações prontas         |
| `panda3d`        | 3D                | `pip install` | Jogos 3D completos                  | Pesado para um jogo 2D                       |
| `wasabi2d`       | 2D / ModernGL     | `pip install` | Efeitos visuais modernos em 2D      | Menos community, API experimental            |

### Por que `pygame-ce`?

- Fork oficial e ativo do `pygame` clássico (Community Edition)
- Suporte nativo a Python 3.12 e wheels binários para Windows/Linux/macOS
- **Instalação via pip — sem dependências de sistema** (SDL2 já vem embutido no wheel)
- API estável com 20+ anos de documentação e exemplos
- Suporte a tilemaps, spritesheets, áudio, joystick e texto
- Roda com `python main.py` — zero configuração extra para o usuário final

---

## 2. Stack Técnica Completa

```
Linguagem:        Python 3.12
Engine:           pygame-ce 2.5+
Gerenciador:      uv 0.4+
Linting:          ruff
Formatação:       black
Tipagem:          mypy (strict)
Testes:           pytest + pytest-cov
Mapas:            pytmx (carrega arquivos .tmx do Tiled)
Assets:           assets/ com sprites CC0
CI:               GitHub Actions
```

---

## 3. Gerenciamento de Ambiente com `uv`

### Por que `uv`?

- Substitui `pip` + `venv` + `pip-tools` em um único binário
- 10–100x mais rápido que pip para resolução e instalação
- Lockfile determinístico (`uv.lock`) — ambiente idêntico em qualquer máquina
- Não requer instalação de Python separada — `uv` gerencia versões

### Instalação do `uv`

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Inicialização do projeto

```bash
# Criar projeto novo com Python 3.12
uv init pyblaze --python 3.12
cd pyblaze

# Adicionar dependências de produção
uv add pygame-ce pytmx

# Adicionar dependências de desenvolvimento
uv add --dev pytest pytest-cov black ruff mypy

# Instalar tudo (cria .venv automaticamente)
uv sync

# Rodar o jogo
uv run python src/pyblaze/main.py

# Rodar testes
uv run pytest
```

### Estrutura gerada pelo `uv init`

```
pyblaze/
├── .python-version     # "3.12" — força a versão do Python
├── pyproject.toml      # toda configuração do projeto
├── uv.lock             # lockfile — SEMPRE commitar no git
├── .venv/              # ambiente virtual — NO .gitignore
├── src/
│   └── pyblaze/
│       └── __init__.py
└── tests/
```

---

## 4. `pyproject.toml` — Configuração Completa

```toml
[project]
name = "pyblaze"
version = "1.0.0"
description = "Jogo de plataforma 2D de alta velocidade inspirado no Sonic"
requires-python = ">=3.12"
dependencies = [
    "pygame-ce>=2.5.0",
    "pytmx>=3.32",
]

[project.scripts]
pyblaze = "pyblaze.main:main"   # permite rodar com `uv run pyblaze`

[dependency-groups]
dev = [
    "pytest>=8.2.0",
    "pytest-cov>=5.0.0",
    "black>=24.0.0",
    "ruff>=0.5.0",
    "mypy>=1.10.0",
]

# ── Black ─────────────────────────────────────────────────────
[tool.black]
line-length = 88
target-version = ["py312"]

# ── Ruff ──────────────────────────────────────────────────────
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "ANN"]
ignore = ["ANN101", "ANN102"]

# ── MyPy ──────────────────────────────────────────────────────
[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true   # pygame-ce não tem stubs completos

# ── Pytest ────────────────────────────────────────────────────
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short --cov=src/pyblaze --cov-report=term-missing"

[tool.coverage.report]
fail_under = 70
omit = ["src/pyblaze/main.py"]  # entry point não precisa de cobertura unitária
```

---

## 5. Estrutura de Pastas do Projeto

```
pyblaze/
├── .python-version
├── pyproject.toml
├── uv.lock                          # lockfile — commitar sempre
├── README.md
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml                   # GitHub Actions
│
├── assets/
│   ├── sprites/
│   │   ├── player/
│   │   │   ├── idle.png             # spritesheet do estado idle
│   │   │   ├── run.png              # spritesheet da corrida
│   │   │   ├── jump.png
│   │   │   └── hurt.png
│   │   ├── enemies/
│   │   │   └── patroller.png
│   │   └── items/
│   │       └── ring.png
│   ├── tiles/
│   │   ├── tileset.png              # tileset principal
│   │   └── phase_01.tmx             # mapa da fase (Tiled)
│   └── audio/
│       ├── music/
│       │   └── phase_01.ogg
│       └── sfx/
│           ├── jump.wav
│           ├── ring_collect.wav
│           ├── hurt.wav
│           └── victory.wav
│
├── src/
│   └── pyblaze/
│       ├── __init__.py
│       ├── main.py                  # entry point — inicializa e roda o jogo
│       ├── settings.py              # constantes globais
│       │
│       ├── scenes/
│       │   ├── __init__.py
│       │   ├── base_scene.py        # classe base abstrata para cenas
│       │   ├── menu.py
│       │   ├── game.py
│       │   └── game_over.py
│       │
│       ├── entities/
│       │   ├── __init__.py
│       │   ├── base_entity.py
│       │   ├── player.py
│       │   ├── enemy.py
│       │   ├── ring.py
│       │   └── checkpoint.py
│       │
│       ├── systems/
│       │   ├── __init__.py
│       │   ├── physics.py
│       │   ├── camera.py
│       │   └── hud.py
│       │
│       └── utils/
│           ├── __init__.py
│           ├── spritesheet.py       # carregamento e fatiamento de spritesheets
│           ├── tilemap.py           # carregamento via pytmx
│           └── audio.py             # gerenciamento de sons e música
│
└── tests/
    ├── conftest.py                  # fixtures compartilhadas
    ├── unit/
    │   ├── test_player.py
    │   ├── test_enemy.py
    │   ├── test_physics.py
    │   ├── test_camera.py
    │   └── test_ring.py
    └── integration/
        └── test_game_scene.py
```

---

## 6. Arquivos Essenciais — Código Base

### `settings.py`

```python
# src/pyblaze/settings.py
from typing import Final

# Janela
SCREEN_WIDTH: Final = 1280
SCREEN_HEIGHT: Final = 720
FPS: Final = 60
TITLE: Final = "PyBlaze"

# Física
GRAVITY: Final = 0.6
MAX_FALL_SPEED: Final = 20.0
PLAYER_SPEED: Final = 5.0
PLAYER_SPRINT_SPEED: Final = 12.0
JUMP_FORCE: Final = -14.0

# Jogador
PLAYER_LIVES: Final = 3
INVINCIBILITY_FRAMES: Final = 120   # 2 segundos a 60 FPS
SPRINT_THRESHOLD_FRAMES: Final = 60 # 1 segundo em linha reta

# Câmera
CAMERA_LERP: Final = 0.1

# Cores (fallback sem sprites)
COLOR_BG: Final = (30, 120, 200)
COLOR_PLAYER: Final = (0, 180, 80)
COLOR_ENEMY: Final = (200, 50, 50)
COLOR_RING: Final = (255, 215, 0)
COLOR_PLATFORM: Final = (100, 70, 40)
```

### `main.py`

```python
# src/pyblaze/main.py
import sys
import pygame
from pyblaze.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from pyblaze.scenes.menu import MenuScene


def main() -> None:
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    current_scene = MenuScene(screen)

    while current_scene is not None:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            current_scene.handle_event(event)

        current_scene.update(dt)
        current_scene.draw()
        pygame.display.flip()

        current_scene = current_scene.next_scene


if __name__ == "__main__":
    main()
```

### `scenes/base_scene.py`

```python
# src/pyblaze/scenes/base_scene.py
from abc import ABC, abstractmethod
import pygame


class BaseScene(ABC):
    """Classe base para todas as cenas do jogo."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.next_scene: "BaseScene | None" = self  # None = encerra o jogo

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None: ...

    @abstractmethod
    def update(self, dt: int) -> None: ...

    @abstractmethod
    def draw(self) -> None: ...
```

### `entities/base_entity.py`

```python
# src/pyblaze/entities/base_entity.py
import pygame


class BaseEntity:
    """Entidade base com posição, tamanho e rect de colisão."""

    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt: int) -> None:
        pass

    def draw(self, surface: pygame.Surface, camera_x: float = 0.0) -> None:
        pass
```

---

## 7. Testes com `pytest`

### Filosofia de testes no projeto

- **Sistemas de física e lógica de jogo** → cobertura alta (≥ 80%)
- **Rendering e pygame.Surface** → não testar diretamente (depende de display)
- **Cenas** → testes de integração leves com mocks de pygame
- **Entidades** → testar comportamento, não pixels

### `conftest.py` — fixtures compartilhadas

```python
# tests/conftest.py
import pytest
import pygame


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Inicializa o pygame sem abrir janela — necessário para testes."""
    pygame.display.init()
    pygame.display.set_mode((1, 1))   # janela mínima invisível
    yield
    pygame.quit()


@pytest.fixture
def mock_player():
    """Player em posição padrão para testes."""
    from pyblaze.entities.player import Player
    return Player(x=100, y=400)


@pytest.fixture
def mock_platform_rect():
    """Retângulo de plataforma padrão."""
    return pygame.Rect(0, 500, 800, 32)
```

### Exemplos de testes unitários

```python
# tests/unit/test_physics.py
import pytest
import pygame
from pyblaze.systems.physics import PhysicsSystem
from pyblaze.entities.player import Player
from pyblaze.settings import GRAVITY, MAX_FALL_SPEED


class TestGravity:
    def test_apply_gravity_increases_vy(self, mock_player: Player):
        system = PhysicsSystem()
        mock_player.vy = 0.0
        system.apply_gravity(mock_player)
        assert mock_player.vy == pytest.approx(GRAVITY)

    def test_gravity_capped_at_max_fall_speed(self, mock_player: Player):
        system = PhysicsSystem()
        mock_player.vy = MAX_FALL_SPEED
        system.apply_gravity(mock_player)
        assert mock_player.vy == MAX_FALL_SPEED


class TestCollision:
    def test_player_lands_on_platform(
        self, mock_player: Player, mock_platform_rect: pygame.Rect
    ):
        system = PhysicsSystem()
        mock_player.y = 470.0
        mock_player.vy = 8.0
        system.resolve_collision(mock_player, [mock_platform_rect])
        assert mock_player.on_ground is True

    def test_player_does_not_fall_through_platform(
        self, mock_player: Player, mock_platform_rect: pygame.Rect
    ):
        system = PhysicsSystem()
        mock_player.y = 470.0
        mock_player.vy = 8.0
        system.resolve_collision(mock_player, [mock_platform_rect])
        assert mock_player.rect.bottom <= mock_platform_rect.top + 1
```

```python
# tests/unit/test_player.py
from pyblaze.entities.player import Player
from pyblaze.settings import PLAYER_LIVES


class TestPlayerDamage:
    def test_take_damage_with_rings_loses_rings_not_life(self, mock_player: Player):
        mock_player.rings = 10
        mock_player.take_damage()
        assert mock_player.rings == 0
        assert mock_player.lives == PLAYER_LIVES

    def test_take_damage_without_rings_loses_life(self, mock_player: Player):
        mock_player.rings = 0
        mock_player.take_damage()
        assert mock_player.lives == PLAYER_LIVES - 1

    def test_collect_ring_increments_counter(self, mock_player: Player):
        initial = mock_player.rings
        mock_player.collect_ring()
        assert mock_player.rings == initial + 1

    def test_player_dead_when_no_lives(self, mock_player: Player):
        mock_player.lives = 0
        assert mock_player.is_dead is True
```

```python
# tests/unit/test_camera.py
from pyblaze.systems.camera import Camera
from pyblaze.settings import SCREEN_WIDTH


class TestCamera:
    def test_camera_follows_player_position(self):
        camera = Camera()
        camera.follow(target_x=500.0)
        # após lerp, câmera deve se aproximar do alvo
        assert camera.x > 0

    def test_camera_does_not_go_negative(self):
        camera = Camera()
        camera.follow(target_x=0.0)
        assert camera.x >= 0

    def test_apply_returns_offset_rect(self):
        import pygame
        camera = Camera()
        camera.x = 100.0
        original = pygame.Rect(200, 300, 32, 32)
        result = camera.apply(original)
        assert result.x == 100   # 200 - 100
```

### Executar testes

```bash
# Todos os testes com cobertura
uv run pytest

# Apenas testes unitários
uv run pytest tests/unit/

# Um arquivo específico
uv run pytest tests/unit/test_player.py -v

# Com relatório HTML de cobertura
uv run pytest --cov-report=html
# Abre: htmlcov/index.html

# Parar no primeiro erro
uv run pytest -x
```

---

## 8. Qualidade de Código

### Executar todas as verificações

```bash
# Formatar código
uv run black src/ tests/

# Lint + autofix
uv run ruff check src/ tests/ --fix

# Verificação de tipos
uv run mypy src/

# Tudo de uma vez (recomendado antes do commit)
uv run black src/ tests/ && uv run ruff check src/ tests/ --fix && uv run mypy src/ && uv run pytest
```

### `.gitignore` recomendado

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# uv
.venv/

# Testes e cobertura
.pytest_cache/
htmlcov/
.coverage

# MyPy
.mypy_cache/

# Ruff
.ruff_cache/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Assets gerados
assets/generated/
```

---

## 9. CI com GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
      - uses: actions/checkout@v4

      - name: Instalar uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"

      - name: Instalar dependências
        run: uv sync --frozen

      - name: Black
        run: uv run black src/ tests/ --check

      - name: Ruff
        run: uv run ruff check src/ tests/

      - name: MyPy
        run: uv run mypy src/

      - name: Pytest
        run: uv run pytest --cov-fail-under=70
        env:
          SDL_VIDEODRIVER: dummy    # roda pygame sem display real no CI
          SDL_AUDIODRIVER: dummy    # desabilita áudio no CI
```

---

## 10. Como Rodar o Projeto (README técnico)

```bash
# 1. Pré-requisito: apenas uv instalado
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clonar o repositório
git clone https://github.com/user/pyblaze.git
cd pyblaze

# 3. Instalar dependências (cria .venv com Python 3.12 automaticamente)
uv sync

# 4. Rodar o jogo
uv run python src/pyblaze/main.py

# --- Desenvolvimento ---

# Rodar testes
uv run pytest

# Verificar qualidade
uv run black src/ tests/ && uv run ruff check src/ && uv run mypy src/

# Adicionar nova dependência
uv add nome-da-lib

# Atualizar todas as dependências
uv lock --upgrade
```

---

## 11. Referência Rápida

```
PYTHON:       3.12 — fixado em .python-version
ENGINE:       pygame-ce (SDL2 embutido — sem deps de sistema)
GERENCIADOR:  uv — init, add, sync, run, lock
TESTES:       pytest + pytest-cov | cobertura mínima 70%
LINT:         ruff | FORMAT: black | TIPOS: mypy strict
CI:           GitHub Actions — matriz Win/Linux/macOS
              SDL_VIDEODRIVER=dummy para rodar pygame sem display

FLUXO DE DESENVOLVIMENTO:
  uv sync                          → instalar / atualizar ambiente
  uv run python src/pyblaze/main.py → rodar o jogo
  uv run pytest                    → rodar testes
  uv run black . && ruff check .   → formatar e lintar
  uv run mypy src/                 → checar tipos

NUNCA:
  - pip install diretamente (usar uv add)
  - commitar .venv/
  - NÃO commitar uv.lock (ele DEVE estar no git)
  - pygame.display chamadas dentro de testes unitários (usar SDL_VIDEODRIVER=dummy)
  - hardcodar valores mágicos fora de settings.py
```