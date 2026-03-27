# Implementação de Sprites no PyBlaze

## Resumo

Sistema completo de sprites visuais implementado no PyBlaze, substituindo os retângulos coloridos por sprites desenhados programaticamente.

## O que foi implementado

### 1. Sistema de Assets (AssetManager)

**Arquivo:** `src/pyblaze/utils/assets.py`

- Gerenciador centralizado de sprites
- Cache automático de assets
- Suporte a sprites únicos e spritesheets
- Fallback para formas geométricas se sprites não existirem

**Funcionalidades:**
```python
asset_manager = get_asset_manager()

# Carregar sprites
player_sprite = asset_manager.get_player_sprite(frame=0)  # 4 frames disponíveis
enemy_sprite = asset_manager.get_enemy_sprite()
ring_sprite = asset_manager.get_ring_sprite()
checkpoint_sprite = asset_manager.get_checkpoint_sprite(active=False)
platform_sprite = asset_manager.get_platform_sprite()
```

### 2. Sprites Criados

#### Sprites Básicos (tools/generate_sprites.py)

1. **player.png** (160x50 - spritesheet com 4 frames)
   - Frame 0: Idle
   - Frame 1: Running 1
   - Frame 2: Running 2
   - Frame 3: Jumping/Spin

2. **enemy.png** (40x40)
   - Inimigo vermelho com olhos amarelos
   - Espinhos no topo

3. **ring.png** (20x20)
   - Anel dourado com buraco central
   - Brilho destacado

4. **checkpoint.png** (50x80)
   - Poste cinza com bandeira azul (inativo)

5. **checkpoint_active.png** (50x80)
   - Poste cinza com bandeira verde (ativo)
   - Efeito de brilho

6. **platform_tile.png** (32x32)
   - Tile de terra com grama no topo
   - Textura de terra

#### Sprites Avançados (tools/generate_advanced_sprites.py)

Versões melhoradas com:
- Gradientes radiais
- Sombras projetadas
- Brilhos e highlights
- Efeitos de volume
- Texturas detalhadas

Arquivos criados:
- `player_advanced.png`
- `enemy_advanced.png`
- `ring_animated.png` (8 frames de animação)
- `checkpoint_advanced.png`
- `checkpoint_advanced_active.png`
- `platform_advanced.png`

### 3. Integração nas Entidades

Todas as entidades foram atualizadas para usar sprites:

#### Player (src/pyblaze/entities/player.py)
- Sistema de animação por estado
- 4 frames de animação
- Espelhamento horizontal baseado na direção
- Fallback para retângulo verde

#### Enemy (src/pyblaze/entities/enemy.py)
- Sprite único
- Espelhamento baseado na direção de patrulha
- Fallback para retângulo vermelho

#### Ring (src/pyblaze/entities/ring.py)
- Rotação contínua do sprite
- Animação de pulsação
- Fallback para círculo dourado

#### Checkpoint (src/pyblaze/entities/checkpoint.py)
- Dois sprites (ativo/inativo)
- Troca automática ao ativar
- Fallback para retângulo com bandeira

## Estrutura de Arquivos

```
hello-game/
├── assets/
│   ├── sprites/
│   │   ├── player.png                    # Spritesheet 160x50
│   │   ├── player_advanced.png           # Versão melhorada
│   │   ├── enemy.png                     # 40x40
│   │   ├── enemy_advanced.png            # Versão melhorada
│   │   ├── ring.png                      # 20x20
│   │   ├── ring_animated.png             # 160x20 (8 frames)
│   │   ├── checkpoint.png                # 50x80
│   │   ├── checkpoint_active.png         # 50x80
│   │   ├── checkpoint_advanced.png       # Versão melhorada
│   │   ├── checkpoint_advanced_active.png
│   │   ├── platform_tile.png             # 32x32
│   │   └── platform_advanced.png         # Versão melhorada
│   └── README.md                         # Documentação dos assets
├── src/pyblaze/
│   ├── entities/
│   │   ├── player.py                     # ✅ Atualizado
│   │   ├── enemy.py                      # ✅ Atualizado
│   │   ├── ring.py                       # ✅ Atualizado
│   │   └── checkpoint.py                 # ✅ Atualizado
│   └── utils/
│       └── assets.py                     # ✅ Novo arquivo
├── tools/
│   ├── generate_sprites.py               # ✅ Gerador básico
│   └── generate_advanced_sprites.py      # ✅ Gerador avançado
└── docs/
    ├── SPRITE_GUIDE.md                   # ✅ Guia completo
    └── SPRITES_IMPLEMENTATION.md         # ✅ Este arquivo
```

## Como Usar

### Executar o jogo com sprites

```bash
# O jogo já carrega os sprites automaticamente
uv run python src/pyblaze/main.py
```

### Regenerar sprites básicos

```bash
uv run python tools/generate_sprites.py
```

### Gerar sprites avançados

```bash
uv run python tools/generate_advanced_sprites.py
```

### Usar sprites avançados

```bash
# Opção 1: Renomear arquivos (Windows)
cd assets/sprites
ren player_advanced.png player.png
ren enemy_advanced.png enemy.png
# ... etc

# Opção 2: Renomear arquivos (Linux/Mac)
cd assets/sprites
mv player_advanced.png player.png
mv enemy_advanced.png enemy.png
# ... etc
```

## Sistema de Animação

### Player Animation

O player possui 4 estados de animação:

```python
# Frame 0: Idle (parado)
if self.state == PlayerState.IDLE:
    self.animation_frame = 0

# Frames 1-2: Running (correndo)
elif self.state in (PlayerState.RUNNING, PlayerState.SPRINTING):
    # Alterna entre frames 1 e 2 a cada 8 frames
    if self.animation_timer % 8 == 0:
        self.animation_frame = 1 if self.animation_frame == 2 else 2

# Frame 3: Jumping/Spin (pulando/girando)
elif self.state in (PlayerState.JUMPING, PlayerState.FALLING, PlayerState.SPIN_ATTACK):
    self.animation_frame = 3
```

### Ring Animation

O anel possui rotação contínua:

```python
def update(self, dt: int) -> None:
    # Rotação de 5 graus por frame
    self.rotation += 5.0
    if self.rotation >= 360:
        self.rotation = 0

def draw(self, surface: pygame.Surface, camera_x: float = 0.0) -> None:
    sprite = self.asset_manager.get_ring_sprite()
    if sprite:
        # Rotaciona sprite
        rotated_sprite = pygame.transform.rotate(sprite, self.rotation)
        sprite_rect = rotated_sprite.get_rect(center=rect.center)
        surface.blit(rotated_sprite, sprite_rect)
```

## Fallback System

Se os sprites não forem encontrados, o jogo usa formas geométricas:

| Entidade   | Sprite                | Fallback              |
|------------|----------------------|-----------------------|
| Player     | Sprite azul animado  | Retângulo verde       |
| Enemy      | Sprite vermelho      | Retângulo vermelho    |
| Ring       | Anel dourado         | Círculo dourado       |
| Checkpoint | Poste com bandeira   | Retângulo com bandeira|
| Platform   | Tile de terra        | Retângulo marrom      |

## Técnicas Utilizadas

### 1. Gradientes Radiais

```python
def create_gradient_circle(size, color1, color2):
    for radius in range(center, 0, -1):
        ratio = radius / center
        r = int(color1[0] * ratio + color2[0] * (1 - ratio))
        # ... calcula g e b
        pygame.draw.circle(surface, (r, g, b), center, radius)
```

### 2. Sombras Projetadas

```python
# Sombra semi-transparente no chão
shadow = pygame.Surface((width, height), pygame.SRCALPHA)
pygame.draw.ellipse(shadow, (0, 0, 0, 80), (x, y, w, h))
surface.blit(shadow, (0, 0))
```

### 3. Brilhos e Highlights

```python
# Brilho branco semi-transparente
pygame.draw.circle(surface, (255, 255, 255), (x, y), radius)

# Highlight em superfície
pygame.draw.rect(surface, lighter_color, (x, y, w, h))
```

### 4. Espelhamento Horizontal

```python
if not self.facing_right:
    sprite = pygame.transform.flip(sprite, True, False)
```

### 5. Rotação de Sprites

```python
rotated_sprite = pygame.transform.rotate(sprite, angle)
```

## Performance

- Sprites carregados uma vez no início (cache)
- Sem impacto significativo no FPS
- Transformações (flip, rotate) são rápidas
- Fallback garante que o jogo sempre funciona

## Próximos Passos

### Melhorias Sugeridas

1. **Mais frames de animação**
   - Adicionar animação de morte
   - Animação de dano (piscar vermelho)
   - Animação de vitória

2. **Efeitos visuais**
   - Partículas ao coletar anéis
   - Rastro de velocidade no sprint
   - Explosão ao destruir inimigos

3. **Sprites de cenário**
   - Tiles de fundo (nuvens, montanhas)
   - Decorações (árvores, pedras)
   - Tiles de rampa

4. **Sprites profissionais**
   - Importar de OpenGameArt.org
   - Contratar pixel artist
   - Usar Aseprite para criar sprites

5. **Sistema de temas**
   - Múltiplos skins para o player
   - Temas de cenário (floresta, deserto, neve)
   - Paletas de cores customizáveis

## Recursos Adicionais

### Documentação
- [assets/README.md](../assets/README.md) - Documentação dos assets
- [SPRITE_GUIDE.md](SPRITE_GUIDE.md) - Guia completo de criação

### Ferramentas
- **Aseprite** - Editor profissional de pixel art
- **Piskel** - Editor online gratuito
- **GIMP** - Editor de imagens gratuito
- **Krita** - Editor de arte digital

### Fontes de Sprites
- [OpenGameArt.org](https://opengameart.org/)
- [Kenney.nl](https://kenney.nl/assets)
- [itch.io](https://itch.io/game-assets/free)
- [Lospec](https://lospec.com/palette-list)

## Troubleshooting

### Sprites não aparecem
1. Verifique se os arquivos existem em `assets/sprites/`
2. Confira os logs: `INFO | Loaded player sprite`
3. Teste o fallback (deve aparecer formas coloridas)

### Animação travada
1. Verifique se `_update_animation()` é chamado
2. Confirme que `animation_timer` incrementa
3. Debug com `print(self.animation_frame)`

### Sprite aparece cortado
1. Verifique dimensões do sprite
2. Use `sprite.get_rect(center=rect.center)`
3. Ajuste o tamanho do rect da entidade

## Conclusão

Sistema de sprites totalmente funcional implementado com:
- ✅ 12 sprites criados (6 básicos + 6 avançados)
- ✅ AssetManager com cache
- ✅ Integração em todas as entidades
- ✅ Sistema de animação
- ✅ Fallback para formas geométricas
- ✅ Documentação completa
- ✅ Scripts de geração automatizados

O jogo agora possui identidade visual própria e pode ser facilmente customizado com novos sprites!
