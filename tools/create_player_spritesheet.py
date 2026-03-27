"""Cria spritesheet do player avançado com 4 frames de animação."""

import pygame
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from generate_advanced_sprites import create_player_advanced

pygame.init()

ASSETS_DIR = Path(__file__).parent.parent / "assets" / "sprites"

print("🎨 Criando spritesheet do player avançado...")

# Cria 4 frames
frames = []

# Frame 0: Idle (parado)
frame0 = create_player_advanced()
frames.append(frame0)

# Frame 1: Running 1 (perna esquerda à frente)
frame1 = create_player_advanced()
# Adiciona movimento nas pernas
pygame.draw.line(frame1, (0, 100, 200), (15, 40), (12, 48), 3)
frames.append(frame1)

# Frame 2: Running 2 (perna direita à frente)
frame2 = create_player_advanced()
pygame.draw.line(frame2, (0, 100, 200), (25, 40), (28, 48), 3)
frames.append(frame2)

# Frame 3: Jumping/Spin (bola)
frame3 = pygame.Surface((40, 50), pygame.SRCALPHA)
# Forma de bola com gradiente
center_x, center_y = 20, 25
for radius in range(15, 0, -1):
    ratio = radius / 15
    r = int(0 * ratio + 0 * (1 - ratio))
    g = int(150 * ratio + 80 * (1 - ratio))
    b = int(255 * ratio + 200 * (1 - ratio))
    pygame.draw.circle(frame3, (r, g, b), (center_x, center_y), radius)
# Linhas de spin
pygame.draw.arc(frame3, (255, 255, 255), (10, 15, 20, 20), 0, 3.14, 2)
frames.append(frame3)

# Cria spritesheet (160x50)
sheet = pygame.Surface((160, 50), pygame.SRCALPHA)
for i, frame in enumerate(frames):
    sheet.blit(frame, (i * 40, 0))

# Salva
output_path = ASSETS_DIR / "player.png"
pygame.image.save(sheet, str(output_path))

print(f"✅ Spritesheet criada: {output_path}")
print(f"   Dimensões: 160x50 (4 frames de 40x50)")

pygame.quit()
