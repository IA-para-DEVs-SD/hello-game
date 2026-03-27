"""Gera todas as variações de sprites usando as máscaras customizadas."""

import pygame
import sys
from pathlib import Path

# Adiciona o diretório tools ao path para importar módulos
sys.path.insert(0, str(Path(__file__).parent))

from procedural_sprite_generator import (
    generate_sprite_from_mask,
    generate_color_palette,
    generate_variations,
    PLAYER_MASK,
    ENEMY_ROBOT_MASK,
    ENEMY_ALIEN_MASK,
    SPACESHIP_MASK,
    CRYSTAL_MASK,
    HEART_MASK,
)
from custom_masks import ALL_MASKS
import random

pygame.init()

ASSETS_DIR = Path(__file__).parent.parent / "assets"
SPRITES_DIR = ASSETS_DIR / "sprites" / "procedural"
SPRITES_DIR.mkdir(parents=True, exist_ok=True)

print("🎨 Gerando TODAS as variações de sprites...")
print(f"📁 Diretório: {SPRITES_DIR}\n")

total_sprites = 0

# Gera sprites das máscaras customizadas
print("🆕 Sprites customizados:")
for name, mask in ALL_MASKS.items():
    # Determina número de variações baseado no tipo
    if name in ["platform", "spike", "cloud"]:
        count = 2  # Menos variações para elementos de cenário
    elif name in ["coin", "star", "heart", "crystal"]:
        count = 4  # Mais variações para coletáveis
    else:
        count = 3  # Padrão
    
    # Determina tamanho do pixel baseado no tipo
    if name in ["tree", "chest", "portal"]:
        pixel_size = 3  # Menor para objetos grandes
    elif name in ["coin", "key", "butterfly"]:
        pixel_size = 5  # Maior para objetos pequenos
    else:
        pixel_size = 4  # Padrão
    
    generate_variations(mask, name, count=count, pixel_size=pixel_size)
    total_sprites += count

# Gera mais variações dos sprites originais
print("\n🔄 Variações extras dos sprites originais:")

# Players extras (mais cores)
print("  🧍 Players:")
player_hues = [0.1, 0.15, 0.6, 0.75, 0.85]  # Laranja, amarelo, ciano, roxo, rosa
for i, hue in enumerate(player_hues, start=4):
    palette = generate_color_palette(hue, 4)
    sprite = generate_sprite_from_mask(
        PLAYER_MASK,
        pixel_size=4,
        mirror=True,
        color_palette=palette,
        add_outline=True
    )
    filename = f"player_procedural_{i}.png"
    pygame.image.save(sprite, str(SPRITES_DIR / filename))
    print(f"    ✓ {filename}")
    total_sprites += 1

# Inimigos extras
print("  👾 Enemies:")
for i in range(4, 7):
    hue = random.random()
    palette = generate_color_palette(hue, 4)
    
    # Alterna entre robô e alien
    mask = ENEMY_ROBOT_MASK if i % 2 == 0 else ENEMY_ALIEN_MASK
    sprite_type = "robot" if i % 2 == 0 else "alien"
    
    sprite = generate_sprite_from_mask(
        mask,
        pixel_size=4,
        mirror=True,
        color_palette=palette,
        add_outline=True
    )
    filename = f"enemy_{sprite_type}_var{i}.png"
    pygame.image.save(sprite, str(SPRITES_DIR / filename))
    print(f"    ✓ {filename}")
    total_sprites += 1

# Naves extras
print("  🚀 Spaceships:")
for i in range(5, 9):
    hue = random.random()
    palette = generate_color_palette(hue, 4)
    sprite = generate_sprite_from_mask(
        SPACESHIP_MASK,
        pixel_size=3,
        mirror=True,
        color_palette=palette,
        add_outline=True
    )
    filename = f"spaceship_var{i}.png"
    pygame.image.save(sprite, str(SPRITES_DIR / filename))
    print(f"    ✓ {filename}")
    total_sprites += 1

# Cristais extras
print("  💎 Crystals:")
for i in range(5, 9):
    hue = random.random()
    palette = generate_color_palette(hue, 4)
    sprite = generate_sprite_from_mask(
        CRYSTAL_MASK,
        pixel_size=3,
        mirror=True,
        color_palette=palette,
        add_outline=True
    )
    filename = f"crystal_var{i}.png"
    pygame.image.save(sprite, str(SPRITES_DIR / filename))
    print(f"    ✓ {filename}")
    total_sprites += 1

# Corações extras
print("  ❤️  Hearts:")
for i in range(4, 7):
    # Corações em tons de vermelho/rosa
    hue = random.uniform(0.9, 1.0) if i % 2 == 0 else random.uniform(0.0, 0.1)
    palette = generate_color_palette(hue, 4)
    sprite = generate_sprite_from_mask(
        HEART_MASK,
        pixel_size=3,
        mirror=True,
        color_palette=palette,
        add_outline=True
    )
    filename = f"heart_var{i}.png"
    pygame.image.save(sprite, str(SPRITES_DIR / filename))
    print(f"    ✓ {filename}")
    total_sprites += 1

print(f"\n✅ Geração completa!")
print(f"📊 Total de sprites gerados nesta execução: {total_sprites}")
print(f"📁 Total de sprites no diretório: {len(list(SPRITES_DIR.glob('*.png')))}")
print(f"\n💡 Execute novamente para gerar novas variações com cores diferentes!")

pygame.quit()
