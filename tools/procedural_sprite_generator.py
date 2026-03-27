"""Gerador procedural de sprites usando máscaras 2D.

Inspirado no conceito de geração procedural de sprites, este script
cria sprites únicos usando máscaras, espelhamento e variações de cor.
"""

import pygame
import random
from pathlib import Path
from typing import List
import colorsys

pygame.init()

ASSETS_DIR = Path(__file__).parent.parent / "assets"
SPRITES_DIR = ASSETS_DIR / "sprites" / "procedural"
SPRITES_DIR.mkdir(parents=True, exist_ok=True)

print(f"📁 Criando sprites procedurais em: {SPRITES_DIR}")


def hsv_to_rgb(h: float, s: float, v: float) -> tuple:
    """Converte HSV para RGB."""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def generate_color_palette(base_hue: float, variations: int = 4) -> List[tuple]:
    """Gera paleta de cores baseada em um matiz base.
    
    Args:
        base_hue: Matiz base (0.0 a 1.0)
        variations: Número de variações de cor
        
    Returns:
        Lista de cores RGB
    """
    colors = []
    for i in range(variations):
        # Varia saturação e valor para criar profundidade
        saturation = 0.6 + (i * 0.1)
        value = 0.9 - (i * 0.15)
        colors.append(hsv_to_rgb(base_hue, saturation, value))
    return colors


def generate_sprite_from_mask(
    mask: List[List[int]],
    pixel_size: int = 4,
    mirror: bool = True,
    color_palette: List[tuple] = None,
    add_outline: bool = True
) -> pygame.Surface:
    """Gera sprite a partir de uma máscara 2D.
    
    Args:
        mask: Matriz 2D onde 0=transparente, 1+=cores
        pixel_size: Tamanho de cada pixel
        mirror: Se True, espelha horizontalmente
        color_palette: Paleta de cores a usar
        add_outline: Se True, adiciona contorno
        
    Returns:
        Surface do pygame com o sprite
    """
    height = len(mask)
    width = len(mask[0]) * (2 if mirror else 1)
    
    # Paleta padrão se não fornecida
    if color_palette is None:
        color_palette = [
            (100, 100, 100),  # Cinza escuro
            (150, 150, 150),  # Cinza médio
            (200, 200, 200),  # Cinza claro
            (255, 255, 255),  # Branco
        ]
    
    # Cria surface
    surface = pygame.Surface(
        (width * pixel_size, height * pixel_size),
        pygame.SRCALPHA
    )
    
    # Desenha pixels
    for y, row in enumerate(mask):
        for x, value in enumerate(row):
            if value > 0:
                # Escolhe cor baseada no valor
                color_idx = min(value - 1, len(color_palette) - 1)
                color = color_palette[color_idx]
                
                # Desenha pixel original
                rect = pygame.Rect(
                    x * pixel_size,
                    y * pixel_size,
                    pixel_size,
                    pixel_size
                )
                pygame.draw.rect(surface, color, rect)
                
                # Espelha se necessário
                if mirror:
                    mirror_x = (width - x - 1) * pixel_size
                    mirror_rect = pygame.Rect(
                        mirror_x,
                        y * pixel_size,
                        pixel_size,
                        pixel_size
                    )
                    pygame.draw.rect(surface, color, mirror_rect)
    
    # Adiciona contorno
    if add_outline:
        outline_color = (0, 0, 0)
        for y in range(height):
            for x in range(width):
                px = x * pixel_size
                py = y * pixel_size
                
                # Verifica se há pixel nesta posição
                has_pixel = False
                if mirror:
                    orig_x = x if x < len(mask[0]) else (width - x - 1)
                    has_pixel = mask[y][orig_x] > 0
                else:
                    has_pixel = mask[y][x] > 0
                
                if has_pixel:
                    # Verifica vizinhos para adicionar contorno
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if mirror:
                                orig_nx = nx if nx < len(mask[0]) else (width - nx - 1)
                                neighbor_empty = mask[ny][orig_nx] == 0
                            else:
                                neighbor_empty = mask[ny][nx] == 0
                            
                            if neighbor_empty:
                                # Desenha linha de contorno
                                if dx != 0:  # Vertical
                                    line_x = px if dx < 0 else px + pixel_size - 1
                                    pygame.draw.line(
                                        surface,
                                        outline_color,
                                        (line_x, py),
                                        (line_x, py + pixel_size - 1)
                                    )
                                else:  # Horizontal
                                    line_y = py if dy < 0 else py + pixel_size - 1
                                    pygame.draw.line(
                                        surface,
                                        outline_color,
                                        (px, line_y),
                                        (px + pixel_size - 1, line_y)
                                    )
    
    return surface


# Máscaras para diferentes tipos de sprites

# Player/Personagem humanóide
PLAYER_MASK = [
    [0, 0, 2, 2, 0],  # Cabeça
    [0, 0, 3, 3, 0],
    [0, 1, 2, 2, 0],  # Corpo
    [0, 1, 2, 2, 0],
    [0, 1, 2, 2, 0],
    [0, 1, 2, 2, 0],
    [0, 1, 2, 2, 0],
    [0, 0, 1, 1, 0],  # Pernas
    [0, 0, 1, 1, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 2, 2, 0],  # Pés
]

# Inimigo tipo robô
ENEMY_ROBOT_MASK = [
    [0, 1, 1, 1, 0],  # Antena
    [0, 0, 2, 0, 0],
    [0, 2, 3, 3, 0],  # Cabeça
    [0, 2, 4, 3, 0],
    [1, 2, 2, 2, 1],  # Corpo
    [1, 2, 3, 3, 1],
    [1, 2, 2, 2, 1],
    [0, 1, 2, 2, 0],  # Pernas
    [0, 1, 1, 1, 0],
]

# Inimigo tipo alien
ENEMY_ALIEN_MASK = [
    [0, 0, 1, 1, 0],  # Antenas
    [0, 1, 0, 0, 1],
    [0, 2, 3, 3, 0],  # Cabeça grande
    [1, 2, 4, 4, 1],
    [1, 2, 3, 3, 1],
    [0, 2, 2, 2, 0],  # Corpo pequeno
    [0, 1, 2, 2, 0],
    [0, 1, 1, 1, 0],
]

# Nave espacial
SPACESHIP_MASK = [
    [0, 0, 0, 1, 0],  # Ponta
    [0, 0, 1, 2, 0],
    [0, 1, 2, 3, 0],
    [1, 2, 3, 3, 1],  # Corpo
    [1, 2, 3, 3, 1],
    [0, 2, 3, 3, 0],
    [0, 1, 2, 2, 0],  # Motor
    [0, 0, 1, 1, 0],
    [0, 0, 2, 2, 0],  # Chama
]

# Cristal/Gema
CRYSTAL_MASK = [
    [0, 0, 1, 0, 0],  # Ponta
    [0, 1, 2, 1, 0],
    [0, 2, 3, 2, 0],
    [1, 2, 4, 2, 1],  # Centro brilhante
    [0, 2, 3, 2, 0],
    [0, 1, 2, 1, 0],
    [0, 0, 1, 0, 0],  # Base
]

# Coração/Power-up
HEART_MASK = [
    [0, 1, 0, 1, 0],
    [1, 2, 1, 2, 1],
    [1, 3, 3, 3, 1],
    [0, 2, 3, 2, 0],
    [0, 1, 2, 1, 0],
    [0, 0, 1, 0, 0],
]


def generate_variations(
    mask: List[List[int]],
    name: str,
    count: int = 3,
    pixel_size: int = 4
) -> None:
    """Gera múltiplas variações de um sprite.
    
    Args:
        mask: Máscara do sprite
        name: Nome base do arquivo
        count: Número de variações
        pixel_size: Tamanho do pixel
    """
    for i in range(count):
        # Gera paleta de cor aleatória
        hue = random.random()
        palette = generate_color_palette(hue, variations=4)
        
        # Gera sprite
        sprite = generate_sprite_from_mask(
            mask,
            pixel_size=pixel_size,
            mirror=True,
            color_palette=palette,
            add_outline=True
        )
        
        # Salva
        filename = f"{name}_var{i+1}.png"
        pygame.image.save(sprite, str(SPRITES_DIR / filename))
        print(f"  ✓ {filename} ({sprite.get_width()}x{sprite.get_height()})")


# Gera sprites procedurais
print("🎨 Gerando sprites procedurais...")

# Player com diferentes cores
print("\n🧍 Player variations:")
player_palettes = [
    generate_color_palette(0.55, 4),  # Azul (Sonic)
    generate_color_palette(0.0, 4),   # Vermelho
    generate_color_palette(0.33, 4),  # Verde
]

for i, palette in enumerate(player_palettes):
    sprite = generate_sprite_from_mask(
        PLAYER_MASK,
        pixel_size=4,
        mirror=True,
        color_palette=palette,
        add_outline=True
    )
    filename = f"player_procedural_{i+1}.png"
    pygame.image.save(sprite, str(SPRITES_DIR / filename))
    print(f"  ✓ {filename} ({sprite.get_width()}x{sprite.get_height()})")

# Inimigos
print("\n👾 Enemy variations:")
generate_variations(ENEMY_ROBOT_MASK, "enemy_robot", count=3, pixel_size=4)
generate_variations(ENEMY_ALIEN_MASK, "enemy_alien", count=3, pixel_size=4)

# Naves espaciais
print("\n🚀 Spaceship variations:")
generate_variations(SPACESHIP_MASK, "spaceship", count=4, pixel_size=3)

# Cristais/Gemas
print("\n💎 Crystal variations:")
generate_variations(CRYSTAL_MASK, "crystal", count=4, pixel_size=3)

# Corações
print("\n❤️  Heart variations:")
generate_variations(HEART_MASK, "heart", count=3, pixel_size=3)

print(f"\n✅ Sprites procedurais criados com sucesso em: {SPRITES_DIR}")
print(f"\n📊 Total de sprites gerados: {len(list(SPRITES_DIR.glob('*.png')))}")
print("\n💡 Dica: Cada execução gera sprites únicos com cores aleatórias!")
print("   Execute novamente para criar novas variações.")

pygame.quit()
