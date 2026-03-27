"""Checkpoint de respawn ativável."""

import logging

import pygame

from pyblaze.entities.base_entity import BaseEntity
from pyblaze.settings import (
    CHECKPOINT_HEIGHT,
    CHECKPOINT_WIDTH,
    COLOR_CHECKPOINT,
    COLOR_CHECKPOINT_ACTIVE,
)
from pyblaze.utils.assets import get_asset_manager

logger = logging.getLogger(__name__)


class Checkpoint(BaseEntity):
    """Ponto de respawn ativável pelo jogador."""

    def __init__(self, x: float, y: float) -> None:
        """Inicializa o checkpoint.

        Args:
            x: Posição X do checkpoint.
            y: Posição Y do checkpoint.
        """
        super().__init__(x, y, CHECKPOINT_WIDTH, CHECKPOINT_HEIGHT)
        self.activated = False
        self.spawn_x = x + CHECKPOINT_WIDTH // 2
        self.spawn_y = y + CHECKPOINT_HEIGHT
        self.asset_manager = get_asset_manager()

    def activate(self) -> None:
        """Ativa o checkpoint."""
        if not self.activated:
            self.activated = True
            logger.info("Checkpoint activated at (%.1f, %.1f)", self.x, self.y)

    def update(self, dt: int) -> None:
        """Atualiza o checkpoint.

        Args:
            dt: Delta time em milissegundos.
        """
        pass

    def draw(self, surface: pygame.Surface, camera_x: float = 0.0) -> None:
        """Renderiza o checkpoint.

        Args:
            surface: Superfície do pygame onde renderizar.
            camera_x: Offset da câmera no eixo X.
        """
        rect = self.rect.copy()
        rect.x -= int(camera_x)

        # Tenta usar sprite, senão usa retângulo colorido
        sprite = self.asset_manager.get_checkpoint_sprite(self.activated)

        if sprite:
            sprite_rect = sprite.get_rect(center=rect.center)
            surface.blit(sprite, sprite_rect)
        else:
            # Fallback: retângulo colorido com bandeira
            color = COLOR_CHECKPOINT_ACTIVE if self.activated else COLOR_CHECKPOINT

            # Desenha poste
            pygame.draw.rect(surface, color, rect)

            # Desenha bandeira
            flag_points = [
                (rect.right, rect.top),
                (rect.right + 30, rect.top + 15),
                (rect.right, rect.top + 30),
            ]
            pygame.draw.polygon(surface, color, flag_points)

            # Borda
            pygame.draw.rect(surface, (255, 255, 255), rect, 2)
