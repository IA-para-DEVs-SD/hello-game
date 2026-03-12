"""Constantes globais do jogo PyBlaze."""

from typing import Final

# Janela
SCREEN_WIDTH: Final = 1280
SCREEN_HEIGHT: Final = 720
FPS: Final = 60
TITLE: Final = "PyBlaze"

# Física
GRAVITY: Final = 0.6
MAX_FALL_SPEED: Final = 20.0
PLAYER_SPEED: Final = 5.0
PLAYER_SPRINT_SPEED: Final = 12.0
JUMP_FORCE: Final = -14.0
JUMP_FORCE_SHORT: Final = -10.0

# Jogador
PLAYER_WIDTH: Final = 40
PLAYER_HEIGHT: Final = 50
PLAYER_LIVES: Final = 3
INVINCIBILITY_FRAMES: Final = 120
SPRINT_THRESHOLD_FRAMES: Final = 60
ACCELERATION: Final = 0.3
FRICTION: Final = 0.85

# Inimigo
ENEMY_WIDTH: Final = 40
ENEMY_HEIGHT: Final = 40
ENEMY_PATROL_SPEED: Final = 2.0
ENEMY_PATROL_RANGE: Final = 150

# Ring/Anel
RING_SIZE: Final = 20
RING_FLY_VX: Final = 4.0
RING_FLY_VY: Final = -8.0
RING_FLY_DURATION: Final = 180

# Checkpoint
CHECKPOINT_WIDTH: Final = 50
CHECKPOINT_HEIGHT: Final = 80

# Câmera
CAMERA_LERP: Final = 0.1
CAMERA_OFFSET_X: Final = SCREEN_WIDTH // 3

# Cores (fallback sem sprites)
COLOR_BG: Final = (30, 120, 200)
COLOR_PLAYER: Final = (0, 180, 80)
COLOR_PLAYER_HURT: Final = (255, 100, 100)
COLOR_ENEMY: Final = (200, 50, 50)
COLOR_RING: Final = (255, 215, 0)
COLOR_PLATFORM: Final = (100, 70, 40)
COLOR_CHECKPOINT: Final = (50, 200, 255)
COLOR_CHECKPOINT_ACTIVE: Final = (0, 255, 100)
COLOR_HUD_TEXT: Final = (255, 255, 255)
COLOR_MENU_TEXT: Final = (255, 255, 255)
COLOR_MENU_BG: Final = (20, 20, 40)
