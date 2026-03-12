# PyBlaze

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![pygame-ce](https://img.shields.io/badge/pygame--ce-2.5+-green?logo=pygame&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-26%20passing-brightgreen?logo=pytest&logoColor=white)
![Type Check](https://img.shields.io/badge/mypy-strict-blue?logo=python&logoColor=white)
![Ruff](https://img.shields.io/badge/code%20style-ruff-000000?logo=ruff&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-orange)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)

</div>

Jogo de plataforma 2D de alta velocidade inspirado no Sonic the Hedgehog, desenvolvido em Python com pygame-ce.

## Características

- Personagem com movimento acelerado e mecânicas de alta velocidade
- Sistema de pulo variável (curto/longo baseado no tempo de pressão)
- Spin attack para destruir inimigos
- Sistema de anéis e vidas
- State machine completa do personagem
- Fase jogável com 4 zonas:
  - Zona 1: Introdução com plataformas baixas
  - Zona 2: Rampa de aceleração e corredor de alta velocidade
  - Zona 3: Plataformas aéreas com abismos
  - Zona 4: Sprint final até a meta
- Checkpoints de respawn
- Câmera com suavização (lerp)
- HUD com contador de anéis, vidas e timer

## Requisitos

- Python 3.12+
- `uv` (gerenciador de pacotes)

## Instalação

### 1. Instalar o `uv`

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clonar e instalar dependências

```bash
cd pyblaze
uv sync
```

## Como Jogar

### Executar o jogo

```bash
uv run python src/pyblaze/main.py
```

### Controles

**Menu:**
- `W/S` ou `Setas` - Navegar opções
- `Enter` ou `Espaço` - Selecionar

**Jogo:**
- `A/D` ou `Setas Esquerda/Direita` - Mover
- `Espaço` - Pular (segurar para pulo alto)
- `Shift Esquerdo` - Spin attack (no ar)
- `ESC` - Voltar ao menu

**Game Over / Vitória:**
- `Espaço` - Reiniciar fase
- `ESC` - Voltar ao menu

## Desenvolvimento

### Comandos Rápidos (Makefile)

O projeto inclui um Makefile com comandos de conveniência:

```bash
make help          # Mostra todos os comandos disponíveis
make install       # Instala dependências
make test          # Executa testes
make test-cov      # Testes com cobertura (relatório HTML)
make format        # Formata código automaticamente
make lint          # Verifica qualidade do código
make type-check    # Verifica tipos com mypy
make check         # Executa TODAS as verificações
make run           # Executa o jogo
make clean         # Remove arquivos temporários
make build-exe     # Cria executável standalone
make ci            # Simula pipeline de CI localmente
```

### Comandos Manuais

Se preferir executar os comandos diretamente:

#### Executar testes

```bash
uv run pytest -v
```

#### Verificar cobertura de testes

```bash
uv run pytest --cov=src/pyblaze --cov-report=html
```

#### Verificar tipos com mypy

```bash
uv run mypy src/
```

#### Formatar código

```bash
uv run ruff format src/ tests/
```

#### Lint com ruff

```bash
uv run ruff check src/ tests/ --fix
```

#### Executar todas as verificações

```bash
make check
# ou manualmente:
uv run ruff format src/ tests/ && uv run ruff check src/ tests/ --fix && uv run mypy src/ && uv run pytest
```

## Estrutura do Projeto

```
pyblaze/
├── docs/                      # Documentação completa
│   ├── INDEX.md              # Índice de toda documentação
│   ├── LESSONS_LEARNED.md    # Lições aprendidas
│   ├── guidelines/           # Padrões e best practices
│   │   ├── git_convection.md
│   │   ├── python_best_practices.md
│   │   ├── docker_best_practices.md
│   │   ├── product_requirements_document.md
│   │   ├── tech_spec.md
│   │   └── readme_writing_guide.md
│   └── prompts/              # Prompts para IA
│       └── game_agent.md
├── src/
│   └── pyblaze/
│       ├── entities/          # Entidades do jogo
│       │   ├── base_entity.py
│       │   ├── player.py
│       │   ├── enemy.py
│       │   ├── ring.py
│       │   └── checkpoint.py
│       ├── scenes/            # Cenas do jogo
│       │   ├── base_scene.py
│       │   ├── menu.py
│       │   ├── game.py
│       │   └── game_over.py
│       ├── systems/           # Sistemas de jogo
│       │   ├── physics.py
│       │   ├── camera.py
│       │   └── hud.py
│       ├── utils/             # Utilitários
│       │   ├── spritesheet.py
│       │   └── audio.py
│       ├── settings.py        # Constantes globais
│       └── main.py            # Entry point
└── tests/                     # Testes
    ├── conftest.py
    └── unit/
        ├── test_physics.py
        ├── test_player.py
        ├── test_camera.py
        ├── test_enemy.py
        └── test_ring.py
```

### Arquitetura de Módulos

O diagrama abaixo mostra a organização e relacionamento entre os módulos do projeto:

```mermaid
graph TB
    subgraph "Camada de Apresentação"
        Main[main.py]
        Menu[scenes/menu.py]
        Game[scenes/game.py]
        GameOver[scenes/game_over.py]
    end

    subgraph "Camada de Entidades"
        Player[entities/player.py]
        Enemy[entities/enemy.py]
        Ring[entities/ring.py]
        Checkpoint[entities/checkpoint.py]
        BaseEntity[entities/base_entity.py]
    end

    subgraph "Camada de Sistemas"
        Physics[systems/physics.py]
        Camera[systems/camera.py]
        HUD[systems/hud.py]
    end

    subgraph "Camada de Configuração"
        Settings[settings.py]
        Utils[utils/]
    end

    Main --> Menu
    Main --> Game
    Main --> GameOver

    Game --> Player
    Game --> Enemy
    Game --> Ring
    Game --> Checkpoint

    Player --> BaseEntity
    Enemy --> BaseEntity
    Ring --> BaseEntity
    Checkpoint --> BaseEntity

    Game --> Physics
    Game --> Camera
    Game --> HUD

    Player --> Physics
    Enemy --> Physics

    BaseEntity --> Settings
    Physics --> Settings
    Camera --> Settings
```

## Fluxo do Jogo

O diagrama abaixo ilustra o fluxo de navegação entre as diferentes cenas do jogo:

```mermaid
graph TD
    A[Iniciar Aplicação] --> B[Menu Principal]
    B --> C{Opção Escolhida}
    C -->|Iniciar Jogo| D[Cena de Jogo]
    C -->|Sair| E[Fechar Aplicação]

    D --> F{Resultado}
    F -->|Completar Fase| G[Tela de Vitória]
    F -->|Perder Todas Vidas| H[Tela de Game Over]
    F -->|Pressionar ESC| B

    G --> I{Ação do Jogador}
    H --> I

    I -->|Espaço| D
    I -->|ESC| B
```

## Mecânicas de Jogo

### Estados do Personagem

O personagem possui uma state machine completa que gerencia seus diferentes estados:

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> Running: Pressionar A/D
    Running --> Idle: Soltar teclas

    Running --> Sprinting: Correr 1s na mesma direção
    Sprinting --> Running: Mudar direção ou soltar

    Idle --> Jumping: Pressionar Espaço
    Running --> Jumping: Pressionar Espaço
    Sprinting --> Jumping: Pressionar Espaço

    Jumping --> Falling: Velocidade Y > 0
    Falling --> Idle: Tocar no chão
    Falling --> Running: Tocar no chão com tecla pressionada

    Jumping --> SpinAttack: Pressionar Shift
    Falling --> SpinAttack: Pressionar Shift
    SpinAttack --> Falling: Continuar no ar

    Running --> Hurt: Colidir com inimigo
    Sprinting --> Hurt: Colidir com inimigo
    Hurt --> Invincible: Perder anéis/vida
    Invincible --> Idle: Após 2s

    Hurt --> Dead: Sem vidas
    Dead --> [*]
```

### Sistema de Dano
- **Com anéis:** Jogador perde todos os anéis mas não perde vida
- **Sem anéis:** Jogador perde 1 vida e reaparece no último checkpoint
- **Sem vidas:** Game Over

### Velocidade
- **Corrida normal:** Velocidade base
- **Sprint:** Após 1 segundo correndo na mesma direção sem parar
- **Rampas:** Aumentam a velocidade automaticamente

### Inimigos
- Patrulham horizontalmente em suas plataformas
- Podem ser destruídos com spin attack vindo de cima
- Causam dano ao toque lateral ou frontal

## Build e Distribuição

### Criar Executável Standalone

Para distribuir o jogo sem necessidade de Python instalado:

```bash
# Usando Makefile
make build-exe

# Ou manualmente
python build/build.py
```

O executável será criado em `dist/PyBlaze.exe` (Windows) ou `dist/PyBlaze` (Linux/Mac).

### CI/CD com GitHub Actions

O projeto inclui pipeline automatizado que executa em cada push/PR:

- ✅ Verificação de formatação (Ruff)
- ✅ Linting (Ruff)
- ✅ Type checking (MyPy)
- ✅ Testes unitários (pytest)
- ✅ Cobertura de código (Codecov)
- ✅ Build em múltiplas plataformas

Ver configuração em [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

## Licença

Este projeto foi desenvolvido como material educacional.

## Documentação

Para informações detalhadas sobre o desenvolvimento, padrões e lições aprendidas, consulte:

- **[docs/INDEX.md](docs/INDEX.md)** - Índice completo da documentação
- **[docs/PROJETO_COMPLETO.md](docs/PROJETO_COMPLETO.md)** - Resumo executivo e métricas
- **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Guia de contribuição
- **[docs/LESSONS_LEARNED.md](docs/LESSONS_LEARNED.md)** - Problemas encontrados e soluções
- **[docs/guidelines/](docs/guidelines/)** - Padrões de código e arquitetura
- **[docs/prompts/](docs/prompts/)** - Prompts utilizados no desenvolvimento
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de versões e mudanças

## Qualidade de Código

✅ **100% de conformidade com:**
- Type hints completos (mypy strict)
- Testes unitários (26 testes passando)
- Code quality (ruff + black)
- Logging estruturado (sem prints)
- Arquitetura modular

## Métricas do Projeto

- **Código:** ~1500 linhas
- **Testes:** 26 (100% passing)
- **Módulos:** 21
- **FPS:** 60 (estável)
- **Dependências runtime:** 1 (pygame-ce)
- **Tempo de fase:** 3-5 minutos

## Créditos

Desenvolvido seguindo as melhores práticas de Python moderno e documentado extensivamente para servir como referência educacional.
