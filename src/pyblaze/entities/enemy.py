"""Inimigo patrulheiro com IA simples."""

import logging

import pygame

from pyblaze.entities.base_entity import BaseEntity
from pyblaze.settings import (
    COLOR_ENEMY,
    ENEMY_HEIGHT,
    ENEMY_PATROL_RANGE,
    ENEMY_PATROL_SPEED,
    ENEMY_WIDTH,
)
from pyblaze.utils.assets import get_asset_manager

logger = logging.getLogger(__name__)


class Enemy(BaseEntity):
    """Inimigo que patrulha horizontalmente em uma plataforma."""

    def __init__(self, x: float, y: float, patrol_range: int | None = None) -> None:
        """Inicializa o inimigo.

        Args:
            x: Posição X inicial (centro da patrulha).
            y: Posição Y inicial.
            patrol_range: Distância máxima de patrulha. Se None, usa padrão.
        """
        super().__init__(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.start_x = x
        self.patrol_range = patrol_range or ENEMY_PATROL_RANGE
        self.patrol_speed = ENEMY_PATROL_SPEED
        self.direction = 1.0  # 1 = direita, -1 = esquerda
        self.alive = True
        self.asset_manager = get_asset_manager()

    def die(self) -> None:
        """Marca o inimigo como morto."""
        self.alive = False
        logger.debug("Enemy destroyed at (%.1f, %.1f)", self.x, self.y)

    def update(self, dt: int) -> None:
        """Atualiza a patrulha do inimigo.

        Args:
            dt: Delta time em milissegundos.
        """
        if not self.alive:
            return

        # Move na direção atual
        self.x += self.patrol_speed * self.direction

        # Inverte direção ao atingir limite de patrulha
        distance_from_start = self.x - self.start_x
        if abs(distance_from_start) > self.patrol_range:
            self.direction *= -1
            # Corrige posição para não ultrapassar o limite
            if distance_from_start > 0:
                self.x = self.start_x + self.patrol_range
            else:
                self.x = self.start_x - self.patrol_range

    def draw(self, surface: pygame.Surface, camera_x: float = 0.0) -> None:
        """Renderiza o inimigo.

        Args:
            surface: Superfície do pygame onde renderizar.
            camera_x: Offset da câmera no eixo X.
        """
        if not self.alive:
            return

        rect = self.rect.copy()
        rect.x -= int(camera_x)

        # Tenta usar sprite, senão usa retângulo colorido
        sprite = self.asset_manager.get_enemy_sprite()

        if sprite:
            # Espelha sprite baseado na direção
            if self.direction < 0:
                sprite = pygame.transform.flip(sprite, True, False)

            sprite_rect = sprite.get_rect(center=rect.center)
            surface.blit(sprite, sprite_rect)
        else:
            # Fallback: retângulo colorido
            pygame.draw.rect(surface, COLOR_ENEMY, rect)

            # Indicador de direção (olhos)
            eye_offset = 5 if self.direction > 0 else -5
            pygame.draw.circle(
                surface,
                (255, 255, 255),
                (rect.centerx + eye_offset, rect.centery - 5),
                3,
            )
