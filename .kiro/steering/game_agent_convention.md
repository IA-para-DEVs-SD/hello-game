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

## DEBUGGING DE JOGOS 2D (LIÇÕES CRÍTICAS)

### 1. Sistema de Física e Colisão

#### ❌ NUNCA faça colisão baseada apenas em posição
```python
# ERRADO - Causa teletransporte aleatório
if entity.vx > 0 and entity_rect.right > platform.left:
    entity.x = platform.left - entity.width  # BUG!
```

**Problema**: Isso reposiciona o player SEMPRE que ele está à direita da plataforma, mesmo sem colisão real!

#### ✅ Use SAT (Separating Axis Theorem) correto
```python
# CORRETO - Calcula sobreposição real
if entity_rect.colliderect(platform):
    overlap_left = entity_rect.right - platform.left
    overlap_right = platform.right - entity_rect.left
    overlap_top = entity_rect.bottom - platform.top
    overlap_bottom = platform.bottom - entity_rect.top

    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

    if min_overlap == overlap_left and entity.vx > 0:
        entity.x = platform.left - entity.width
        entity.vx = 0.0
```

**Lição**: Sempre verifique QUAL lado está colidindo baseado na menor sobreposição.

---

### 2. Sistema de Spawn/Respawn

#### ❌ NUNCA calcule spawn como `checkpoint.y + height`
```python
# ERRADO - Spawna no AR
self.spawn_y = y + CHECKPOINT_HEIGHT  # BUG!
```

**Problema**: Isso coloca o spawn ABAIXO do checkpoint, não em cima de uma plataforma!

#### ✅ Calcule spawn baseado na plataforma
```python
# CORRETO - Spawna em cima da plataforma
# Se plataforma.top = 500 e player.height = 50
spawn_y = platform_top - player_height - 5  # -5 = margem de segurança
# spawn_y = 500 - 50 - 5 = 445
```

**Lição Crítica**: Sempre subtraia a altura da entidade do topo da plataforma, nunca adicione!

#### ⚠️ Loop Infinito de Queda - O Bug Mais Comum

**Sintomas**:
- Player cai infinitamente após respawn
- Centenas de warnings "Player fell off the map" em segundos
- Player perde todas as vidas instantaneamente

**Causa Raiz**:
```python
# Player spawna em y=400
# Gravidade é aplicada ANTES da colisão
# Player.y se torna 400.6 (gravidade 0.6)
# Sistema de colisão reseta on_ground = False no início
# Player nunca colide porque já passou da plataforma!
```

**Soluções Aplicadas** (use TODAS juntas):

1. **Margem de segurança no spawn** (-5 pixels)
2. **Desabilitar gravidade durante cooldown**:
```python
if player.respawn_cooldown == 0:
    physics.apply_gravity(player)
```
3. **Setar `on_ground = True` no respawn**
4. **Cooldown longo** (120 frames = 2 segundos)
5. **Desabilitar detecção de queda durante cooldown**:
```python
if player.y > DEATH_Y and player.respawn_cooldown == 0:
    player.take_damage()
```

---

### 3. Controle de Movimento

#### ❌ NUNCA use aceleração acumulativa pura
```python
# ERRADO - Player continua se movendo após soltar tecla
if keys[K_LEFT]:
    self.vx -= ACCELERATION  # Acumula infinitamente!
```

**Problema**: Movimento impreciso e difícil de controlar.

#### ✅ Use target velocity com aceleração suave
```python
# CORRETO - Controle direto e responsivo
target_vx = 0.0
if keys[K_LEFT]:
    target_vx = -PLAYER_SPEED
elif keys[K_RIGHT]:
    target_vx = PLAYER_SPEED

# Acelera suavemente em direção ao alvo
if moving:
    if abs(target_vx - self.vx) > ACCELERATION:
        self.vx += ACCELERATION if target_vx > self.vx else -ACCELERATION
    else:
        self.vx = target_vx
```

**Lição**: Defina velocidade alvo e acelere em direção a ela, não acumule indefinidamente.

---

### 4. Posicionamento de Objetivos

#### ❌ NUNCA posicione goals/checkpoints sem verificar plataformas
```python
# ERRADO
self.goal_rect = pygame.Rect(5800, 400, 80, 120)
# Goal.bottom = 520, mas plataforma.top = 360
# Gap de 160 pixels - IMPOSSÍVEL DE ALCANÇAR!
```

#### ✅ Calcule posição baseada nas plataformas existentes
```python
# CORRETO
# Plataforma: Rect(5450, 360, 500, 40) => top=360
# Goal.height = 120
# Goal.bottom deve estar em 360
goal_y = platform_top - goal_height  # 360 - 120 = 240
self.goal_rect = pygame.Rect(5800, 240, 80, 120)
```

---

### 5. Debugging Sistemático

#### Checklist de Debugging para Bugs de Física:

1. **Identifique o padrão nos logs**:
   - Loop infinito? → Problema de spawn/respawn
   - Teletransporte? → Problema de colisão
   - Movimento errado? → Problema de input/aceleração

2. **Verifique SEMPRE as coordenadas**:
   ```python
   logger.info("Player spawned at (%.1f, %.1f)", self.x, self.y)
   ```

3. **Desenhe retângulos de debug**:
   ```python
   # Visualize hitboxes
   pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
   pygame.draw.rect(screen, (0, 255, 0), goal_rect, 2)
   ```

4. **Teste com timeout**:
   ```bash
   timeout 30 uv run python main.py
   ```

5. **Analise a ordem de execução**:
   ```
   Input → Física → Update → Colisão → Detecção de Queda
   ```

#### Perguntas Críticas para Qualquer Bug:

- ❓ A entidade está na posição correta ANTES da física?
- ❓ A gravidade está sendo aplicada quando não deveria?
- ❓ A colisão verifica DIREÇÃO ou só POSIÇÃO?
- ❓ O spawn está em cima ou abaixo da plataforma?
- ❓ Há cooldown/proteção suficiente após eventos especiais?

---

### 6. Valores de Referência que Funcionam

**Velocidade e Física**:
```python
PLAYER_SPEED = 8.0           # Velocidade base
PLAYER_SPRINT_SPEED = 15.0   # Sprint (quase 2x)
ACCELERATION = 0.8           # Aceleração suave
FRICTION = 0.88              # Desaceleração
GRAVITY = 0.6                # Gravidade realista
MAX_FALL_SPEED = 20.0        # Terminal velocity
```

**Timers e Cooldowns**:
```python
INVINCIBILITY_FRAMES = 120      # 2 segundos base
RESPAWN_INVINCIBILITY = 360     # 6 segundos (3x)
RESPAWN_COOLDOWN = 120          # 2 segundos sem gravidade
```

**Margens de Segurança**:
```python
SPAWN_MARGIN = 5                # Pixels acima da plataforma
COLLISION_TOLERANCE = 10        # Tolerância para colisão de cima
```

---

### 7. Padrão de Respawn Robusto (Copy-Paste Ready)

```python
def respawn(self) -> None:
    """Reaparece no último checkpoint de forma segura."""
    # 1. Teleporta para posição segura
    self.x = self.last_checkpoint_x
    self.y = self.last_checkpoint_y

    # 2. Zera velocidades
    self.vx = 0.0
    self.vy = 0.0

    # 3. CRÍTICO: Força on_ground
    self.on_ground = True

    # 4. Proteção tripla
    self.invincibility_timer = INVINCIBILITY_FRAMES * 3
    self.respawn_cooldown = 120  # 2s sem gravidade

    # 5. Estado inicial (não INVINCIBLE, para permitir movimento)
    self.state = PlayerState.IDLE

    logger.info("Player respawned at (%.1f, %.1f)", self.x, self.y)
```

```python
# No game loop, ANTES da física:
if player.respawn_cooldown == 0:
    physics.apply_gravity(player)
else:
    player.respawn_cooldown -= 1

# Na detecção de queda:
if player.y > DEATH_Y and player.respawn_cooldown == 0:
    player.take_damage()
```

---

### 8. Resumo das Lições Mais Importantes

1. ⚠️ **Spawn = plataforma.top - entidade.height - 5** (NUNCA +)
2. ⚠️ **Colisão deve calcular overlap, não apenas posição**
3. ⚠️ **Desabilite gravidade durante respawn_cooldown**
4. ⚠️ **Use target velocity, não aceleração pura acumulativa**
5. ⚠️ **Goals devem ter .bottom = plataforma.top**
6. ⚠️ **Sempre adicione margens de segurança (5px)**
7. ⚠️ **Logs são seus melhores amigos - use liberalmente**
8. ⚠️ **Teste com timeout para identificar loops infinitos**

**Regra de Ouro**: Se algo teleporta, cai infinitamente ou não responde, o problema está SEMPRE na ordem de execução ou nos cálculos de coordenadas Y.

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
