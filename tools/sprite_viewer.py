"""Visualizador de sprites - Mostra todos os sprites criados.

Use as setas para navegar entre os sprites.
ESC para sair.
"""

import pygame
from pathlib import Path
import sys

pygame.init()

# Configurações
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (40, 40, 50)
TEXT_COLOR = (255, 255, 255)
GRID_COLOR = (80, 80, 90)

# Diretórios de sprites
ASSETS_DIR = Path(__file__).parent.parent / "assets" / "sprites"

# Carrega todos os sprites
sprite_files = []
for sprite_dir in [ASSETS_DIR, ASSETS_DIR / "procedural"]:
    if sprite_dir.exists():
        sprite_files.extend(list(sprite_dir.glob("*.png")))

sprite_files.sort()

if not sprite_files:
    print("❌ Nenhum sprite encontrado!")
    sys.exit(1)

print(f"📁 Encontrados {len(sprite_files)} sprites")

# Carrega sprites
sprites = []
for file in sprite_files:
    try:
        img = pygame.image.load(str(file))
        sprites.append({
            "name": file.name,
            "path": str(file.relative_to(ASSETS_DIR.parent)),
            "image": img,
            "size": img.get_size()
        })
    except Exception as e:
        print(f"⚠️  Erro ao carregar {file.name}: {e}")

if not sprites:
    print("❌ Nenhum sprite carregado com sucesso!")
    sys.exit(1)

# Cria janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyBlaze Sprite Viewer")
clock = pygame.time.Clock()

# Fonte
font = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 18)

# Estado
current_index = 0
scale = 4.0
show_grid = True

def draw_grid(surface: pygame.Surface, sprite_rect: pygame.Rect, pixel_size: int):
    """Desenha grade de pixels."""
    for x in range(sprite_rect.left, sprite_rect.right, pixel_size):
        pygame.draw.line(surface, GRID_COLOR, (x, sprite_rect.top), (x, sprite_rect.bottom))
    for y in range(sprite_rect.top, sprite_rect.bottom, pixel_size):
        pygame.draw.line(surface, GRID_COLOR, (sprite_rect.left, y), (sprite_rect.right, y))

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                current_index = (current_index + 1) % len(sprites)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                current_index = (current_index - 1) % len(sprites)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                scale = min(scale + 1, 16)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                scale = max(scale - 1, 1)
            elif event.key == pygame.K_g:
                show_grid = not show_grid
            elif event.key == pygame.K_SPACE:
                # Próximo diretório
                current_dir = Path(sprites[current_index]["path"]).parent
                for i in range(len(sprites)):
                    next_idx = (current_index + i + 1) % len(sprites)
                    next_dir = Path(sprites[next_idx]["path"]).parent
                    if next_dir != current_dir:
                        current_index = next_idx
                        break
    
    # Limpa tela
    screen.fill(BG_COLOR)
    
    # Sprite atual
    sprite = sprites[current_index]
    
    # Escala sprite
    scaled_img = pygame.transform.scale(
        sprite["image"],
        (int(sprite["size"][0] * scale), int(sprite["size"][1] * scale))
    )
    
    # Centraliza sprite
    sprite_rect = scaled_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    # Desenha fundo xadrez (para ver transparência)
    checker_size = 16
    for y in range(sprite_rect.top, sprite_rect.bottom, checker_size):
        for x in range(sprite_rect.left, sprite_rect.right, checker_size):
            if ((x - sprite_rect.left) // checker_size + (y - sprite_rect.top) // checker_size) % 2:
                pygame.draw.rect(screen, (60, 60, 70), (x, y, checker_size, checker_size))
    
    # Desenha sprite
    screen.blit(scaled_img, sprite_rect)
    
    # Desenha grade
    if show_grid and scale >= 4:
        draw_grid(screen, sprite_rect, int(scale))
    
    # Informações
    info_y = 20
    
    # Nome
    name_text = font.render(sprite["name"], True, TEXT_COLOR)
    screen.blit(name_text, (20, info_y))
    info_y += 30
    
    # Caminho
    path_text = font_small.render(sprite["path"], True, (180, 180, 180))
    screen.blit(path_text, (20, info_y))
    info_y += 25
    
    # Tamanho
    size_text = font_small.render(
        f"Size: {sprite['size'][0]}x{sprite['size'][1]} | Scale: {scale:.0f}x",
        True,
        (180, 180, 180)
    )
    screen.blit(size_text, (20, info_y))
    info_y += 25
    
    # Contador
    counter_text = font_small.render(
        f"Sprite {current_index + 1} / {len(sprites)}",
        True,
        (180, 180, 180)
    )
    screen.blit(counter_text, (20, info_y))
    
    # Controles (canto inferior)
    controls = [
        "← → : Navigate sprites",
        "↑ ↓ : Zoom in/out",
        "G : Toggle grid",
        "SPACE : Next folder",
        "ESC : Exit"
    ]
    
    control_y = SCREEN_HEIGHT - 20 - (len(controls) * 20)
    for control in controls:
        control_text = font_small.render(control, True, (150, 150, 150))
        screen.blit(control_text, (20, control_y))
        control_y += 20
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("👋 Sprite Viewer fechado")
