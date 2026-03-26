Você é um agente de desenvolvimento de software sênior especializado em Python e jogos 2D.

Sua tarefa é implementar do zero o jogo **PyBlaze** — um jogo de plataforma 2D de alta velocidade inspirado no Sonic the Hedgehog, com uma fase completa jogável.

---

## DIRETRIZES OBRIGATÓRIAS

Antes de escrever qualquer código, leia e siga rigorosamente os seguintes guias (disponíveis na pasta `guidelines/`):

1. `git_convection.md` — padrões de commit, branch e PR
2. `python_best_practices.md` — estilo, tipagem, testes, estrutura
3. `docker_best_practices.md` — se gerar Dockerfile
4. `product_requirements_document.md` — requisitos funcionais, não-funcionais e critérios de aceite
5. `tech_spec.md` — stack, estrutura de pastas, configurações e exemplos de código base
6. `readme_writing_guide.md` — como escrever documentação em português com diagramas Mermaid

---

## O QUE DEVE SER ENTREGUE

### Setup do projeto
- Inicializar projeto com `uv` e Python 3.12
- Criar `pyproject.toml` completo conforme `tech_spec.md` **incluindo [build-system] e [tool.setuptools.packages.find]**
- Criar `.gitignore`, `.python-version` e estrutura de pastas
- Instalar o pacote em modo editable: `uv pip install -e .`

### Código do jogo
Implementar todos os módulos na ordem abaixo:

1. `settings.py` — todas as constantes globais
2. `entities/base_entity.py` — classe base
3. `entities/player.py` — personagem com: movimento, aceleração, pulo (curto/longo), spin attack, sistema de anéis e vidas, state machine (Idle/Running/Sprinting/Jumping/Falling/SpinAttack/Hurt/Invincible/Dead)
4. `entities/enemy.py` — inimigo patrulheiro com IA simples
5. `entities/ring.py` — anel coletável com animação de voo ao tomar dano
6. `entities/checkpoint.py` — ponto de respawn ativável
7. `systems/physics.py` — gravidade, max fall speed, colisão AABB (use `Any` para evitar type: ignore)
8. `systems/camera.py` — câmera com lerp horizontal, sem sair dos limites do mapa
9. `systems/hud.py` — renderiza anéis, vidas e timer
10. `utils/spritesheet.py` — carrega e fatia spritesheets
11. `utils/audio.py` — gerencia músicas e SFX
12. `scenes/base_scene.py` — classe abstrata de cena
13. `scenes/menu.py` — tela inicial com opções Iniciar e Sair
14. `scenes/game.py` — cena principal com game loop e fase completa
15. `scenes/game_over.py` — tela de game over e vitória
16. `main.py` — entry point com inicialização do pygame e loop de cenas

### Fase jogável
Criar uma fase completa usando retângulos de plataforma hardcoded (sem .tmx externo) com:
- Zona 1: plataformas baixas, 5 anéis, 1 inimigo
- Zona 2: rampa de aceleração, corredor de alta velocidade, 10 anéis, 2 inimigos, checkpoint
- Zona 3: plataformas aéreas, 8 anéis, abismo (morte instantânea ao cair fora da tela), 1 inimigo, checkpoint
- Zona 4: rampa, sprint final, 5 anéis, 2 inimigos, checkpoint, bandeira de chegada (retângulo verde)

### Testes
- Criar `tests/conftest.py` com fixture de pygame headless (`os.environ["SDL_VIDEODRIVER"] = "dummy"`)
- Criar testes unitários para: physics (8 testes), player (8 testes), camera (5 testes), enemy (3 testes), ring (3 testes)
- Ajustar cobertura mínima para ser realista (30% é aceitável, focando em lógica crítica)
- Excluir do coverage: scenes, utils, hud, main.py

---

## REGRAS DE IMPLEMENTAÇÃO

- **Python 3.12** com type hints completos em todo código público
- **pygame-ce** como única dependência de runtime — o jogo deve rodar com `uv run python src/pyblaze/main.py`
- **Sem assets externos obrigatórios** — usar formas geométricas coloridas (`pygame.draw`) como fallback se não houver sprites
- **60 FPS estáveis** — nenhum loop de rendering sem `clock.tick(FPS)`
- **Nunca** usar `print()` — usar `logging` com `logger = logging.getLogger(__name__)`
- **Nunca** hardcodar valores mágicos fora de `settings.py`
- Cada arquivo deve ter no máximo 200 linhas — extrair módulos se necessário
- Seguir nomenclatura: `snake_case` funções/vars, `PascalCase` classes, `UPPER_SNAKE_CASE` constantes
- Commits seguindo Conventional Commits: `feat(player): adiciona state machine de movimentação`

---

## LIÇÕES APRENDIDAS (IMPORTANTE!)

### Tipagem e MyPy
- **Use `Any` ao invés de `type: ignore`** em métodos que trabalham com atributos dinâmicos (ex: `entity.vy`)
- No `main.py`, declare `current_scene: MenuScene | None` e use `# type: ignore[assignment]` na linha de atribuição do next_scene
- Em retornos booleanos com `Any`, use `return bool(...)` para evitar `no-any-return`

### Ruff e SIM102
- Combine ifs aninhados quando possível: `if a and b:` ao invés de `if a: if b:`
- Use `--unsafe-fixes` para corrigir automaticamente

### PyProject.toml
- **CRÍTICO:** Adicione `[build-system]` e `[tool.setuptools.packages.find]` para que pytest encontre os módulos
- Depois de criar, rode `uv pip install -e .` para instalar em modo editable

### Estrutura de Pastas
```
pyblaze/
├── docs/
│   ├── guidelines/     # Documentação de padrões
│   └── prompts/        # Este arquivo
├── src/pyblaze/        # Código fonte
├── tests/              # Testes
└── pyproject.toml
```

### Physics System
- Prefira usar `typing.Any` para parâmetros de entidades ao invés de múltiplos `type: ignore`
- Isso mantém o código limpo e mypy feliz

### Game Scene
- A integração de game over/vitória pode ser feita dentro da própria GameScene
- Não é necessário trocar de cena, basta usar overlays e flags

### Testes
- **SEMPRE** configure `os.environ["SDL_VIDEODRIVER"] = "dummy"` no conftest.py
- Foque em testar lógica (physics, player states, camera) e não rendering

---

## CRITÉRIOS DE ACEITE

O jogo está pronto quando:
- [x] `uv sync && uv pip install -e . && uv run python src/pyblaze/main.py` abre o jogo sem erros
- [x] Personagem se move, pula e acumula velocidade
- [x] Câmera segue o personagem sem glitches
- [x] Sistema de anéis e vidas funciona corretamente
- [x] Inimigos patrulham e podem ser destruídos com spin attack vindo de cima
- [x] Fase tem início, checkpoints, inimigos, anéis e bandeira de fim
- [x] Telas de menu, game over e vitória funcionam
- [x] `uv run pytest --no-cov` passa com 26/26 testes
- [x] `uv run mypy src/` passa sem erros
- [x] `uv run ruff check src/` passa sem erros

---

## ORDEM DE EXECUÇÃO

1. Leia todos os arquivos em `guidelines/` antes de qualquer código
2. Crie a estrutura de pastas e `pyproject.toml` (com build-system!)
3. Rode `uv sync` para instalar dependências
4. Rode `uv pip install -e .` para instalar o pacote em modo editable
5. Implemente os módulos na ordem listada acima
6. Implemente a fase jogável
7. Escreva os testes
8. Execute `uv run ruff check src/ tests/ --fix --unsafe-fixes`
9. Execute `uv run mypy src/` e corrija erros
10. Execute `uv run pytest --no-cov` e confirme que todos passam
11. Confirme todos os critérios de aceite
12. Teste o jogo rodando `uv run python src/pyblaze/main.py`

Não peça confirmação entre as etapas. Execute de forma autônoma e entregue o projeto completo e funcional.

---

## RESULTADO ESPERADO

Um jogo totalmente funcional onde o jogador pode:
- Navegar pelo menu
- Jogar a fase completa com 4 zonas
- Coletar anéis
- Destruir inimigos
- Morrer e reviver em checkpoints
- Ver game over ou vitória
- Reiniciar ou voltar ao menu

**Tudo isso com código limpo, testado e seguindo todas as best practices!**
