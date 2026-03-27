"""Gerador de sprites básicos para PyBlaze.

Este script cria sprites visuais simples usando pygame para substituir
os retângulos coloridos do jogo.
"""

import pygame
from pathlib import Path

# Inicializa pygame
pygame.init()

# Diretório de saída
ASSETS_DIR = Path(__file__).parent.parent / "assets"
SPRITES_DIR = ASSETS_DIR / "sprites"
SPRITES_DIR.mkdir(parents=True, exist_ok=True)

print(f"📁 Criando sprites em: {SPRITES_DIR}")


def create_player_sprite(width: int = 40, height: int = 50) -> pygame.Surface:
    """Cria sprite do personagem principal (estilo Sonic)."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Corpo azul
    pygame.draw.ellipse(surface, (0, 120, 255), (5, 15, 30, 25))
    
    # Cabeça
    pygame.draw.circle(surface, (0, 120, 255), (20, 15), 12)
    
    # Olhos brancos
    pygame.draw.ellipse(surface, (255, 255, 255), (12, 10, 10, 8))
    pygame.draw.ellipse(surface, (255, 255, 255), (22, 10, 10, 8))
    
    # Pupilas
    pygame.draw.circle(surface, (0, 0, 0), (16, 13), 3)
    pygame.draw.circle(surface, (0, 0, 0), (26, 13), 3)
    
    # Pernas
    pygame.draw.rect(surface, (0, 100, 200), (10, 35, 8, 12))
    pygame.draw.rect(surface, (0, 100, 200), (22, 35, 8, 12))
    
    # Sapatos vermelhos
    pygame.draw.ellipse(surface, (255, 50, 50), (8, 42, 12, 8))
    pygame.draw.ellipse(surface, (255, 50, 50), (20, 42, 12, 8))
    
    return surface


def create_enemy_sprite(width: int = 40, height: int = 40) -> pygame.Surface:
    """Cria sprite do inimigo."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Corpo vermelho escuro
    pygame.draw.ellipse(surface, (180, 40, 40), (5, 10, 30, 25))
    
    # Olhos amarelos malvados
    pygame.draw.circle(surface, (255, 255, 0), (13, 18), 5)
    pygame.draw.circle(surface, (255, 255, 0), (27, 18), 5)
    
    # Pupilas vermelhas
    pygame.draw.circle(surface, (255, 0, 0), (13, 18), 2)
    pygame.draw.circle(surface, (255, 0, 0), (27, 18), 2)
    
    # Espinhos
    points = [(10, 10), (15, 5), (20, 10)]
    pygame.draw.polygon(surface, (150, 30, 30), points)
    points = [(20, 10), (25, 5), (30, 10)]
    pygame.draw.polygon(surface, (150, 30, 30), points)
    
    return surface


def create_ring_sprite(size: int = 20) -> pygame.Surface:
    """Cria sprite do anel/moeda."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Anel dourado externo
    pygame.draw.circle(surface, (255, 215, 0), (size // 2, size // 2), size // 2)
    
    # Buraco interno (transparente)
    pygame.draw.circle(surface, (0, 0, 0, 0), (size // 2, size // 2), size // 4)
    
    # Brilho
    pygame.draw.circle(surface, (255, 255, 150), (size // 2 - 3, size // 2 - 3), 3)
    
    return surface


def create_checkpoint_sprite(width: int = 50, height: int = 80) -> pygame.Surface:
    """Cria sprite do checkpoint (poste)."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Poste cinza
    pygame.draw.rect(surface, (100, 100, 100), (22, 10, 6, 70))
    
    # Bandeira azul (inativa)
    points = [(28, 15), (45, 20), (28, 25)]
    pygame.draw.polygon(surface, (100, 150, 255), points)
    
    # Base
    pygame.draw.rect(surface, (80, 80, 80), (15, 75, 20, 5))
    
    return surface


def create_checkpoint_active_sprite(width: int = 50, height: int = 80) -> pygame.Surface:
    """Cria sprite do checkpoint ativo."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Poste cinza
    pygame.draw.rect(surface, (100, 100, 100), (22, 10, 6, 70))
    
    # Bandeira verde (ativa)
    points = [(28, 15), (45, 20), (28, 25)]
    pygame.draw.polygon(surface, (0, 255, 100), points)
    
    # Base
    pygame.draw.rect(surface, (80, 80, 80), (15, 75, 20, 5))
    
    # Efeito de brilho
    pygame.draw.circle(surface, (150, 255, 150, 100), (35, 20), 15)
    
    return surface


def create_platform_tile(size: int = 32) -> pygame.Surface:
    """Cria tile de plataforma."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Base marrom
    pygame.draw.rect(surface, (139, 90, 43), (0, 0, size, size))
    
    # Grama verde no topo
    pygame.draw.rect(surface, (34, 139, 34), (0, 0, size, 8))
    
    # Textura de terra
    for i in range(0, size, 8):
        for j in range(8, size, 8):
            if (i + j) % 16 == 0:
                pygame.draw.rect(surface, (120, 80, 40), (i, j, 4, 4))
    
    # Borda
    pygame.draw.rect(surface, (100, 70, 30), (0, 0, size, size), 1)
    
    return surface


def create_player_spritesheet() -> pygame.Surface:
    """Cria spritesheet do player com animações."""
    # 4 frames de animação x 40x50 pixels
    sheet_width = 40 * 4
    sheet_height = 50
    sheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
    
    # Frame 1: Idle
    sprite = create_player_sprite()
    sheet.blit(sprite, (0, 0))
    
    # Frame 2: Running 1
    sprite = create_player_sprite()
    # Inclina um pouco para frente
    pygame.draw.line(sprite, (0, 120, 255), (15, 40), (12, 48), 3)
    sheet.blit(sprite, (40, 0))
    
    # Frame 3: Running 2
    sprite = create_player_sprite()
    pygame.draw.line(sprite, (0, 120, 255), (25, 40), (28, 48), 3)
    sheet.blit(sprite, (80, 0))
    
    # Frame 4: Jumping
    sprite = create_player_sprite()
    # Forma de bola (spin)
    pygame.draw.circle(sprite, (0, 120, 255), (20, 25), 15)
    sheet.blit(sprite, (120, 0))
    
    return sheet


# Gera todos os sprites
print("🎨 Gerando sprites...")

# Player
player_sheet = create_player_spritesheet()
pygame.image.save(player_sheet, str(SPRITES_DIR / "player.png"))
print("  ✓ player.png (spritesheet 160x50)")

# Enemy
enemy = create_enemy_sprite()
pygame.image.save(enemy, str(SPRITES_DIR / "enemy.png"))
print("  ✓ enemy.png (40x40)")

# Ring
ring = create_ring_sprite()
pygame.image.save(ring, str(SPRITES_DIR / "ring.png"))
print("  ✓ ring.png (20x20)")

# Checkpoints
checkpoint = create_checkpoint_sprite()
pygame.image.save(checkpoint, str(SPRITES_DIR / "checkpoint.png"))
print("  ✓ checkpoint.png (50x80)")

checkpoint_active = create_checkpoint_active_sprite()
pygame.image.save(checkpoint_active, str(SPRITES_DIR / "checkpoint_active.png"))
print("  ✓ checkpoint_active.png (50x80)")

# Platform tile
platform = create_platform_tile()
pygame.image.save(platform, str(SPRITES_DIR / "platform_tile.png"))
print("  ✓ platform_tile.png (32x32)")

print(f"\n✅ Sprites criados com sucesso em: {SPRITES_DIR}")
print("\n📝 Próximos passos:")
print("  1. Execute: python tools/generate_sprites.py")
print("  2. Integre os sprites nas entidades do jogo")
print("  3. Ajuste as cores e detalhes conforme necessário")

pygame.quit()
