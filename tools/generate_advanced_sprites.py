"""Gerador de sprites avançados com efeitos visuais.

Este script cria sprites mais elaborados com gradientes, sombras e brilhos.
"""

import pygame
import math
from pathlib import Path

pygame.init()

ASSETS_DIR = Path(__file__).parent.parent / "assets"
SPRITES_DIR = ASSETS_DIR / "sprites"
SPRITES_DIR.mkdir(parents=True, exist_ok=True)

print(f"📁 Criando sprites avançados em: {SPRITES_DIR}")


def create_gradient_circle(
    size: int, color1: tuple, color2: tuple
) -> pygame.Surface:
    """Cria círculo com gradiente radial."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    for radius in range(center, 0, -1):
        ratio = radius / center
        r = int(color1[0] * ratio + color2[0] * (1 - ratio))
        g = int(color1[1] * ratio + color2[1] * (1 - ratio))
        b = int(color1[2] * ratio + color2[2] * (1 - ratio))
        pygame.draw.circle(surface, (r, g, b), (center, center), radius)
    
    return surface


def create_player_advanced(width: int = 40, height: int = 50) -> pygame.Surface:
    """Cria sprite do player com sombras e brilhos."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Sombra no chão
    shadow = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 80), (8, 45, 24, 6))
    surface.blit(shadow, (0, 0))
    
    # Corpo com gradiente
    body_gradient = create_gradient_circle(30, (0, 150, 255), (0, 80, 200))
    surface.blit(body_gradient, (5, 15))
    
    # Cabeça com gradiente
    head_gradient = create_gradient_circle(24, (0, 150, 255), (0, 100, 220))
    surface.blit(head_gradient, (8, 3))
    
    # Olhos com brilho
    # Olho esquerdo
    pygame.draw.ellipse(surface, (255, 255, 255), (12, 10, 10, 8))
    pygame.draw.circle(surface, (0, 0, 0), (16, 13), 3)
    pygame.draw.circle(surface, (255, 255, 255), (17, 12), 1)  # Brilho
    
    # Olho direito
    pygame.draw.ellipse(surface, (255, 255, 255), (22, 10, 10, 8))
    pygame.draw.circle(surface, (0, 0, 0), (26, 13), 3)
    pygame.draw.circle(surface, (255, 255, 255), (27, 12), 1)  # Brilho
    
    # Pernas com volume
    pygame.draw.ellipse(surface, (0, 100, 200), (10, 35, 8, 14))
    pygame.draw.ellipse(surface, (0, 120, 220), (10, 35, 6, 10))  # Highlight
    
    pygame.draw.ellipse(surface, (0, 100, 200), (22, 35, 8, 14))
    pygame.draw.ellipse(surface, (0, 120, 220), (22, 35, 6, 10))  # Highlight
    
    # Sapatos com brilho
    pygame.draw.ellipse(surface, (255, 50, 50), (8, 42, 12, 8))
    pygame.draw.ellipse(surface, (255, 100, 100), (9, 43, 6, 4))  # Brilho
    
    pygame.draw.ellipse(surface, (255, 50, 50), (20, 42, 12, 8))
    pygame.draw.ellipse(surface, (255, 100, 100), (21, 43, 6, 4))  # Brilho
    
    return surface


def create_enemy_advanced(width: int = 40, height: int = 40) -> pygame.Surface:
    """Cria sprite do inimigo com efeitos."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Sombra
    shadow = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 100), (8, 32, 24, 6))
    surface.blit(shadow, (0, 0))
    
    # Corpo com gradiente vermelho
    body_gradient = create_gradient_circle(30, (220, 50, 50), (150, 20, 20))
    surface.blit(body_gradient, (5, 10))
    
    # Olhos amarelos brilhantes
    # Olho esquerdo
    pygame.draw.circle(surface, (255, 255, 0), (13, 18), 6)
    pygame.draw.circle(surface, (255, 255, 100), (13, 18), 4)
    pygame.draw.circle(surface, (255, 0, 0), (13, 18), 2)
    pygame.draw.circle(surface, (255, 255, 255), (14, 17), 1)  # Brilho
    
    # Olho direito
    pygame.draw.circle(surface, (255, 255, 0), (27, 18), 6)
    pygame.draw.circle(surface, (255, 255, 100), (27, 18), 4)
    pygame.draw.circle(surface, (255, 0, 0), (27, 18), 2)
    pygame.draw.circle(surface, (255, 255, 255), (28, 17), 1)  # Brilho
    
    # Espinhos com volume
    points = [(10, 10), (15, 3), (20, 10)]
    pygame.draw.polygon(surface, (180, 30, 30), points)
    pygame.draw.polygon(surface, (220, 50, 50), [(11, 10), (15, 5), (19, 10)])
    
    points = [(20, 10), (25, 3), (30, 10)]
    pygame.draw.polygon(surface, (180, 30, 30), points)
    pygame.draw.polygon(surface, (220, 50, 50), [(21, 10), (25, 5), (29, 10)])
    
    return surface


def create_ring_animated(size: int = 20, frame: int = 0) -> pygame.Surface:
    """Cria frame de animação do anel."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Rotação baseada no frame
    angle = frame * 15  # 15 graus por frame
    
    # Anel com efeito 3D
    for i in range(3):
        offset = i * 2
        alpha = 255 - (i * 50)
        color = (255 - offset * 10, 215 - offset * 10, 0, alpha)
        pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2 - i)
    
    # Buraco interno
    pygame.draw.circle(surface, (0, 0, 0, 0), (size // 2, size // 2), size // 4)
    
    # Brilho animado
    brilho_x = size // 2 + int(math.cos(math.radians(angle)) * 3)
    brilho_y = size // 2 + int(math.sin(math.radians(angle)) * 3)
    pygame.draw.circle(surface, (255, 255, 200, 200), (brilho_x, brilho_y), 3)
    
    return surface


def create_checkpoint_advanced(
    width: int = 50, height: int = 80, active: bool = False
) -> pygame.Surface:
    """Cria checkpoint com efeitos visuais."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Sombra da base
    pygame.draw.ellipse(surface, (0, 0, 0, 100), (12, 78, 26, 4))
    
    # Poste com volume
    pygame.draw.rect(surface, (80, 80, 80), (22, 10, 6, 70))
    pygame.draw.rect(surface, (120, 120, 120), (22, 10, 2, 70))  # Highlight
    pygame.draw.rect(surface, (50, 50, 50), (26, 10, 2, 70))  # Sombra
    
    # Bandeira com gradiente
    if active:
        color1 = (0, 255, 100)
        color2 = (0, 200, 80)
        glow_color = (150, 255, 150, 100)
    else:
        color1 = (100, 150, 255)
        color2 = (80, 120, 200)
        glow_color = None
    
    # Bandeira principal
    points = [(28, 15), (45, 20), (28, 25)]
    pygame.draw.polygon(surface, color2, points)
    
    # Highlight da bandeira
    points_highlight = [(28, 15), (40, 18), (28, 21)]
    pygame.draw.polygon(surface, color1, points_highlight)
    
    # Efeito de brilho se ativo
    if glow_color:
        glow = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(glow, glow_color, (35, 20), 20)
        surface.blit(glow, (0, 0))
    
    # Base com volume
    pygame.draw.rect(surface, (60, 60, 60), (15, 75, 20, 5))
    pygame.draw.rect(surface, (100, 100, 100), (15, 75, 20, 2))  # Highlight
    
    return surface


def create_platform_advanced(size: int = 32) -> pygame.Surface:
    """Cria tile de plataforma com textura detalhada."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Base de terra com gradiente
    for y in range(8, size):
        ratio = (y - 8) / (size - 8)
        r = int(139 * (1 - ratio * 0.3))
        g = int(90 * (1 - ratio * 0.3))
        b = int(43 * (1 - ratio * 0.3))
        pygame.draw.line(surface, (r, g, b), (0, y), (size, y))
    
    # Grama com variação
    for x in range(0, size, 4):
        height = 6 + (x % 3)
        pygame.draw.rect(surface, (34, 139, 34), (x, 0, 4, height))
        pygame.draw.rect(surface, (50, 180, 50), (x, 0, 2, height - 2))
    
    # Pedrinhas de textura
    import random
    random.seed(42)  # Seed fixo para consistência
    for _ in range(8):
        x = random.randint(2, size - 3)
        y = random.randint(10, size - 3)
        stone_color = (random.randint(100, 130), random.randint(70, 90), random.randint(30, 50))
        pygame.draw.circle(surface, stone_color, (x, y), 2)
    
    # Borda sutil
    pygame.draw.rect(surface, (100, 70, 30), (0, 0, size, size), 1)
    
    return surface


# Gera sprites avançados
print("🎨 Gerando sprites avançados...")

# Player avançado
player_advanced = create_player_advanced()
pygame.image.save(player_advanced, str(SPRITES_DIR / "player_advanced.png"))
print("  ✓ player_advanced.png (40x50)")

# Enemy avançado
enemy_advanced = create_enemy_advanced()
pygame.image.save(enemy_advanced, str(SPRITES_DIR / "enemy_advanced.png"))
print("  ✓ enemy_advanced.png (40x40)")

# Ring animado (8 frames)
ring_sheet = pygame.Surface((20 * 8, 20), pygame.SRCALPHA)
for i in range(8):
    frame = create_ring_animated(20, i)
    ring_sheet.blit(frame, (i * 20, 0))
pygame.image.save(ring_sheet, str(SPRITES_DIR / "ring_animated.png"))
print("  ✓ ring_animated.png (160x20, 8 frames)")

# Checkpoint avançado
checkpoint_adv = create_checkpoint_advanced(active=False)
pygame.image.save(checkpoint_adv, str(SPRITES_DIR / "checkpoint_advanced.png"))
print("  ✓ checkpoint_advanced.png (50x80)")

checkpoint_adv_active = create_checkpoint_advanced(active=True)
pygame.image.save(checkpoint_adv_active, str(SPRITES_DIR / "checkpoint_advanced_active.png"))
print("  ✓ checkpoint_advanced_active.png (50x80)")

# Platform avançada
platform_adv = create_platform_advanced()
pygame.image.save(platform_adv, str(SPRITES_DIR / "platform_advanced.png"))
print("  ✓ platform_advanced.png (32x32)")

print(f"\n✅ Sprites avançados criados com sucesso!")
print("\n📝 Para usar os sprites avançados:")
print("  1. Renomeie os arquivos removendo '_advanced' do nome")
print("  2. Ou modifique o AssetManager para carregar as versões avançadas")
print("\nExemplo:")
print("  mv player_advanced.png player.png")

pygame.quit()
