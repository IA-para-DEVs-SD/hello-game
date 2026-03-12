"""Sistema de física com gravidade e swept AABB collision."""

import logging
from typing import Any

import pygame

from pyblaze.entities.base_entity import BaseEntity
from pyblaze.settings import GRAVITY, MAX_FALL_SPEED

logger = logging.getLogger(__name__)


class PhysicsSystem:
    """Sistema responsável por física e colisões."""

    def __init__(self) -> None:
        """Inicializa o sistema de física."""
        self.gravity = GRAVITY
        self.max_fall_speed = MAX_FALL_SPEED

    def apply_gravity(self, entity: Any) -> None:
        """Aplica gravidade a uma entidade.

        Args:
            entity: Entidade que terá gravidade aplicada.
        """
        if not hasattr(entity, "vy"):
            return

        entity.vy += self.gravity
        if entity.vy > self.max_fall_speed:
            entity.vy = self.max_fall_speed

    def resolve_collision(
        self, entity: Any, platforms: list[pygame.Rect]
    ) -> None:
        """Resolve colisões com plataformas usando AABB.

        Args:
            entity: Entidade que será testada para colisão.
            platforms: Lista de retângulos de plataformas.
        """
        if not hasattr(entity, "vy") or not hasattr(entity, "on_ground"):
            return

        entity_rect = entity.rect
        entity.on_ground = False

        for platform in platforms:
            if entity_rect.colliderect(platform):
                # Colisão vertical (topo ou base)
                if entity.vy > 0:
                    entity.y = platform.top - entity.height
                    entity.vy = 0.0
                    entity.on_ground = True
                elif entity.vy < 0:
                    entity.y = platform.bottom
                    entity.vy = 0.0

                # Colisão horizontal
                if hasattr(entity, "vx"):
                    if entity.vx > 0 and entity_rect.right > platform.left:
                        entity.x = platform.left - entity.width
                    elif entity.vx < 0 and entity_rect.left < platform.right:
                        entity.x = platform.right

    def check_collision(
        self, rect1: pygame.Rect, rect2: pygame.Rect
    ) -> bool:
        """Verifica se dois retângulos colidem.

        Args:
            rect1: Primeiro retângulo.
            rect2: Segundo retângulo.

        Returns:
            True se há colisão, False caso contrário.
        """
        return rect1.colliderect(rect2)

    def check_collision_from_above(
        self, entity: Any, target: BaseEntity, tolerance: int = 10
    ) -> bool:
        """Verifica se entidade está colidindo vindo de cima.

        Args:
            entity: Entidade que está atacando.
            target: Entidade alvo.
            tolerance: Margem de tolerância em pixels.

        Returns:
            True se colisão veio de cima, False caso contrário.
        """
        if not hasattr(entity, "vy"):
            return False

        entity_rect = entity.rect
        target_rect = target.rect

        if not entity_rect.colliderect(target_rect):
            return False

        # Verifica se está caindo e se base da entidade está acima do topo do alvo
        return bool(
            entity.vy > 0
            and entity_rect.bottom <= target_rect.top + tolerance
        )
