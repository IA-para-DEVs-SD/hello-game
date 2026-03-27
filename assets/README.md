# Assets do PyBlaze

Este diretório contém todos os assets visuais e sonoros do jogo.

## Estrutura

```
assets/
├── sprites/          # Sprites visuais das entidades
│   ├── player.png           # Spritesheet do player (160x50, 4 frames)
│   ├── enemy.png            # Sprite do inimigo (40x40)
│   ├── ring.png             # Sprite do anel (20x20)
│   ├── checkpoint.png       # Checkpoint inativo (50x80)
│   ├── checkpoint_active.png # Checkpoint ativo (50x80)
│   └── platform_tile.png    # Tile de plataforma (32x32)
└── README.md         # Este arquivo
```

## Sprites Disponíveis

### Player (player.png)
- **Dimensões:** 160x50 pixels (spritesheet)
- **Frames:** 4 frames de 40x50 cada
  - Frame 0 (0-39px): Idle
  - Frame 1 (40-79px): Running 1
  - Frame 2 (80-119px): Running 2
  - Frame 3 (120-159px): Jumping/Spin
- **Estilo:** Personagem azul inspirado no Sonic
- **Características:** Corpo azul, olhos brancos, sapatos vermelhos

### Enemy (enemy.png)
- **Dimensões:** 40x40 pixels
- **Estilo:** Inimigo vermelho com olhos amarelos malvados
- **Características:** Corpo vermelho escuro, espinhos no topo

### Ring (ring.png)
- **Dimensões:** 20x20 pixels
- **Estilo:** Anel dourado com buraco no centro
- **Características:** Cor dourada com brilho, transparência no centro

### Checkpoint (checkpoint.png / checkpoint_active.png)
- **Dimensões:** 50x80 pixels
- **Variantes:**
  - `checkpoint.png`: Bandeira azul (inativo)
  - `checkpoint_active.png`: Bandeira verde com brilho (ativo)
- **Características:** Poste cinza com bandeira

### Platform Tile (platform_tile.png)
- **Dimensões:** 32x32 pixels
- **Estilo:** Tile de terra com grama no topo
- **Características:** Base marrom, grama verde, textura de terra

## Gerando Sprites

Para regenerar os sprites, execute:

```bash
uv run python tools/generate_sprites.py
```

Este script cria todos os sprites programaticamente usando pygame.

## Customização

### Modificando Cores

Edite o arquivo `tools/generate_sprites.py` e ajuste as cores RGB nas funções de criação:

```python
# Exemplo: Mudar cor do player de azul para verde
pygame.draw.circle(surface, (0, 255, 120), (20, 15), 12)  # Verde
```

### Adicionando Novos Sprites

1. Crie uma função `create_<nome>_sprite()` em `generate_sprites.py`
2. Salve o sprite com `pygame.image.save()`
3. Adicione o carregamento em `src/pyblaze/utils/assets.py`
4. Use o sprite nas entidades

### Usando Sprites Externos

Se preferir usar sprites de artistas:

1. Coloque os arquivos PNG em `assets/sprites/`
2. Mantenha os mesmos nomes e dimensões
3. O jogo carregará automaticamente

**Fontes recomendadas para sprites CC0:**
- [OpenGameArt.org](https://opengameart.org/)
- [Kenney.nl](https://kenney.nl/assets)
- [itch.io](https://itch.io/game-assets/free)

## Fallback

Se os sprites não forem encontrados, o jogo usa retângulos coloridos como fallback:
- Player: Retângulo verde
- Enemy: Retângulo vermelho
- Ring: Círculo dourado
- Checkpoint: Retângulo azul/verde com bandeira
- Platform: Retângulo marrom

## Formato dos Arquivos

- **Formato:** PNG com transparência (RGBA)
- **Compressão:** Sem perdas
- **Transparência:** Canal alpha para áreas transparentes

## Performance

Os sprites são carregados uma vez no início do jogo e mantidos em cache pelo `AssetManager`. Não há impacto significativo na performance.

## Licença

Os sprites gerados pelo script são de domínio público (CC0). Você pode usá-los livremente em seus projetos.
