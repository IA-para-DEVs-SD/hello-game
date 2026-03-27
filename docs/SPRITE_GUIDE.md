# Guia de Criação de Sprites para PyBlaze

Este guia explica como criar e integrar sprites visuais no PyBlaze.

## Visão Geral

O PyBlaze usa um sistema de sprites flexível que suporta:
- Sprites estáticos (imagens únicas)
- Spritesheets (múltiplos frames em uma imagem)
- Animações baseadas em frames
- Fallback para formas geométricas

## Sistema de Assets

### AssetManager

O `AssetManager` (`src/pyblaze/utils/assets.py`) gerencia o carregamento e cache de todos os sprites:

```python
from pyblaze.utils.assets import get_asset_manager

# Obter instância global
asset_manager = get_asset_manager()

# Carregar sprites
player_sprite = asset_manager.get_player_sprite(frame=0)
enemy_sprite = asset_manager.get_enemy_sprite()
```

### Estrutura de Diretórios

```
assets/
└── sprites/
    ├── player.png           # Spritesheet 160x50 (4 frames)
    ├── enemy.png            # Sprite único 40x40
    ├── ring.png             # Sprite único 20x20
    ├── checkpoint.png       # Sprite único 50x80
    ├── checkpoint_active.png # Sprite único 50x80
    └── platform_tile.png    # Tile 32x32
```

## Criando Sprites Programaticamente

### Script Gerador

O arquivo `tools/generate_sprites.py` cria sprites usando pygame:

```python
def create_custom_sprite(width: int, height: int) -> pygame.Surface:
    """Cria um sprite customizado."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Desenha formas
    pygame.draw.circle(surface, (255, 0, 0), (width//2, height//2), 10)
    pygame.draw.rect(surface, (0, 255, 0), (0, 0, width, height), 2)
    
    return surface

# Salvar
sprite = create_custom_sprite(32, 32)
pygame.image.save(sprite, "assets/sprites/custom.png")
```

### Técnicas de Desenho

#### Formas Básicas

```python
# Círculo
pygame.draw.circle(surface, color, (x, y), radius)

# Retângulo
pygame.draw.rect(surface, color, (x, y, width, height))

# Elipse
pygame.draw.ellipse(surface, color, (x, y, width, height))

# Polígono
points = [(x1, y1), (x2, y2), (x3, y3)]
pygame.draw.polygon(surface, color, points)

# Linha
pygame.draw.line(surface, color, (x1, y1), (x2, y2), thickness)
```

#### Gradientes Simples

```python
def create_gradient(width: int, height: int, color1: tuple, color2: tuple):
    """Cria gradiente vertical."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    
    return surface
```

#### Sombras e Brilhos

```python
# Sombra (círculo semi-transparente)
shadow = pygame.Surface((width, height), pygame.SRCALPHA)
pygame.draw.circle(shadow, (0, 0, 0, 100), (x, y), radius)

# Brilho (círculo branco semi-transparente)
highlight = pygame.Surface((width, height), pygame.SRCALPHA)
pygame.draw.circle(highlight, (255, 255, 255, 150), (x-3, y-3), 5)
```

## Criando Spritesheets

### Layout de Spritesheet

```
Frame 0    Frame 1    Frame 2    Frame 3
[40x50]    [40x50]    [40x50]    [40x50]
┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
│      │   │      │   │      │   │      │
│  🧍  │   │  🏃  │   │  🏃  │   │  ⚽  │
│      │   │      │   │      │   │      │
└──────┘   └──────┘   └──────┘   └──────┘
0px        40px       80px       120px
```

### Código para Spritesheet

```python
def create_player_spritesheet() -> pygame.Surface:
    """Cria spritesheet com 4 frames."""
    frame_width = 40
    frame_height = 50
    num_frames = 4
    
    sheet = pygame.Surface(
        (frame_width * num_frames, frame_height),
        pygame.SRCALPHA
    )
    
    for i in range(num_frames):
        frame = create_player_frame(i)  # Função que cria cada frame
        sheet.blit(frame, (i * frame_width, 0))
    
    return sheet
```

## Integrando Sprites nas Entidades

### Passo 1: Adicionar ao AssetManager

Edite `src/pyblaze/utils/assets.py`:

```python
def _load_sprites(self) -> None:
    # ... código existente ...
    
    # Novo sprite
    custom_path = SPRITES_DIR / "custom.png"
    if custom_path.exists():
        self.sprites["custom"] = pygame.image.load(
            str(custom_path)
        ).convert_alpha()
        logger.info("Loaded custom sprite")

def get_custom_sprite(self) -> pygame.Surface | None:
    """Retorna sprite customizado."""
    return self.sprites.get("custom")
```

### Passo 2: Usar na Entidade

Edite a entidade (ex: `src/pyblaze/entities/player.py`):

```python
def __init__(self, x: float, y: float) -> None:
    # ... código existente ...
    self.asset_manager = get_asset_manager()

def draw(self, surface: pygame.Surface, camera_x: float = 0.0) -> None:
    rect = self.rect.copy()
    rect.x -= int(camera_x)
    
    # Tenta usar sprite
    sprite = self.asset_manager.get_player_sprite(self.animation_frame)
    
    if sprite:
        # Espelha se necessário
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        # Desenha
        sprite_rect = sprite.get_rect(center=rect.center)
        surface.blit(sprite, sprite_rect)
    else:
        # Fallback
        pygame.draw.rect(surface, COLOR_PLAYER, rect)
```

## Animações

### Sistema de Frames

```python
class AnimatedEntity:
    def __init__(self):
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8  # Frames entre mudanças
    
    def update_animation(self):
        self.animation_timer += 1
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
```

### Animações por Estado

```python
def _update_animation(self) -> None:
    """Atualiza frame baseado no estado."""
    if self.state == PlayerState.IDLE:
        self.animation_frame = 0
    elif self.state == PlayerState.RUNNING:
        # Alterna entre frames 1 e 2
        if self.animation_timer % 8 == 0:
            self.animation_frame = 1 if self.animation_frame == 2 else 2
    elif self.state == PlayerState.JUMPING:
        self.animation_frame = 3
```

## Usando Sprites Externos

### Fontes Recomendadas

1. **OpenGameArt.org** - Sprites CC0 e Creative Commons
2. **Kenney.nl** - Assets gratuitos de alta qualidade
3. **itch.io** - Marketplace com assets gratuitos e pagos

### Importando Sprites

1. Baixe o sprite (formato PNG com transparência)
2. Redimensione se necessário:
   ```bash
   # Usando ImageMagick
   convert input.png -resize 40x50 output.png
   ```
3. Coloque em `assets/sprites/`
4. Mantenha os nomes esperados pelo AssetManager

### Editando Sprites

Ferramentas recomendadas:
- **Aseprite** - Editor profissional de pixel art (pago)
- **Piskel** - Editor online gratuito
- **GIMP** - Editor de imagens gratuito
- **Krita** - Editor de arte digital gratuito

## Otimização

### Tamanho dos Arquivos

```python
# Comprimir PNG sem perda de qualidade
from PIL import Image

img = Image.open("sprite.png")
img.save("sprite_optimized.png", optimize=True)
```

### Cache de Sprites

O AssetManager já faz cache automático. Não carregue sprites repetidamente:

```python
# ❌ Ruim - carrega toda vez
def draw(self):
    sprite = pygame.image.load("sprite.png")
    
# ✅ Bom - usa cache
def draw(self):
    sprite = self.asset_manager.get_player_sprite()
```

## Troubleshooting

### Sprite não aparece

1. Verifique se o arquivo existe em `assets/sprites/`
2. Verifique os logs: `2026-03-26 | INFO | Loaded player sprite`
3. Confirme que o nome do arquivo está correto
4. Teste o fallback (deve aparecer retângulo colorido)

### Sprite aparece cortado

1. Verifique as dimensões do sprite
2. Confirme que o rect da entidade tem o tamanho correto
3. Use `sprite.get_rect(center=rect.center)` para centralizar

### Animação não funciona

1. Verifique se `_update_animation()` é chamado em `update()`
2. Confirme que `animation_timer` está incrementando
3. Teste com `print(self.animation_frame)` para debug

## Exemplos Avançados

### Sprite com Múltiplas Camadas

```python
def create_layered_sprite():
    base = pygame.Surface((40, 50), pygame.SRCALPHA)
    
    # Camada 1: Corpo
    pygame.draw.ellipse(base, (0, 120, 255), (5, 15, 30, 25))
    
    # Camada 2: Detalhes
    pygame.draw.circle(base, (255, 255, 255), (15, 20), 5)
    
    # Camada 3: Sombra
    shadow = pygame.Surface((40, 50), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 50), (10, 45, 20, 5))
    base.blit(shadow, (0, 0))
    
    return base
```

### Efeitos de Partículas

```python
def create_particle_effect(x, y, color):
    """Cria partícula para efeitos visuais."""
    particle = pygame.Surface((4, 4), pygame.SRCALPHA)
    pygame.draw.circle(particle, color, (2, 2), 2)
    return particle
```

## Recursos Adicionais

- [Pygame Drawing Documentation](https://www.pygame.org/docs/ref/draw.html)
- [Pixel Art Tutorial](https://lospec.com/pixel-art-tutorials)
- [Color Palette Generator](https://coolors.co/)
- [Sprite Animation Guide](https://www.gamedeveloper.com/design/pixel-art-animation-tutorial)

## Próximos Passos

1. Experimente modificar cores em `generate_sprites.py`
2. Crie novos frames de animação
3. Adicione efeitos visuais (partículas, brilhos)
4. Importe sprites profissionais de OpenGameArt
5. Crie tiles de cenário customizados
