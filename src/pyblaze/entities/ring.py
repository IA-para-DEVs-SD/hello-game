"""Anel coletável com animação de voo ao tomar dano."""

import logging
import math

import pygame

from pyblaze.entities.base_entity import BaseEntity
from pyblaze.settings import (
    COLOR_RING,
    GRAVITY,
    RING_FLY_DURATION,
    RING_FLY_VX,
    RING_FLY_VY,
    RING_SIZE,
)
from pyblaze.utils.assets import get_asset_manager

logger = logging.getLogger(__name__)


class Ring(BaseEntity):
    """Item coletável (anel/orb)."""

    def __init__(self, x: float, y: float) -> None:
        """Inicializa o anel.

        Args:
            x: Posição X inicial.
            y: Posição Y inicial.
        """
        super().__init__(x, y, RING_SIZE, RING_SIZE)
        self.collected = False
        self.flying = False
        self.vx = 0.0
        self.vy = 0.0
        self.fly_timer = 0
        self.rotation = 0.0
        self.asset_manager = get_asset_manager()

    def fly_out(self, direction: float = 1.0) -> None:
        """Inicia animação de voo ao jogador perder anéis.

        Args:
            direction: Direção do voo (1.0 = direita, -1.0 = esquerda).
        """
        self.flying = True
        self.vx = RING_FLY_VX * direction
        self.vy = RING_FLY_VY
        self.fly_timer = RING_FLY_DURATION
        self.collected = False
        logger.debug("Ring flying out in direction %.1f", direction)

    def collect(self) -> None:
        """Marca o anel como coletado."""
        self.collected = True
        logger.debug("Ring collected at (%.1f, %.1f)", self.x, self.y)

    def update(self, dt: int) -> None:
        """Atualiza o estado do anel.

        Args:
            dt: Delta time em milissegundos.
        """
        if self.collected:
            return

        if self.flying:
            # Aplica física durante o voo
            self.vy += GRAVITY
            self.x += self.vx
            self.y += self.vy

            self.fly_timer -= 1
            if self.fly_timer <= 0:
                self.flying = False
                self.vx = 0.0
                self.vy = 0.0

        # Animação de rotação
        self.rotation += 5.0
        if self.rotation >= 360:
            self.rotation = 0

    def draw(self, surface: pygame.Surface, camera_x: float = 0.0) -> None:
        """Renderiza o anel.

        Args:
            surface: Superfície do pygame onde renderizar.
            camera_x: Offset da câmera no eixo X.
        """
        if self.collected:
            return

        rect = self.rect.copy()
        rect.x -= int(camera_x)

        # Tenta usar sprite, senão usa círculo colorido
        sprite = self.asset_manager.get_ring_sprite()

        if sprite:
            # Rotaciona sprite
            rotated_sprite = pygame.transform.rotate(sprite, self.rotation)
            sprite_rect = rotated_sprite.get_rect(center=rect.center)
            surface.blit(rotated_sprite, sprite_rect)
        else:
            # Fallback: círculo pulsante
            pulse = abs(math.sin(self.rotation * 0.1)) * 3
            radius = int(RING_SIZE // 2 + pulse)

            pygame.draw.circle(
                surface, COLOR_RING, (rect.centerx, rect.centery), radius
            )
            pygame.draw.circle(
                surface, (200, 180, 0), (rect.centerx, rect.centery), radius, 2
            )
