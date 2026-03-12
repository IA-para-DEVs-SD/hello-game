"""Testes unitários para o sistema de física."""

import pygame
import pytest

from pyblaze.entities.player import Player
from pyblaze.settings import GRAVITY, MAX_FALL_SPEED
from pyblaze.systems.physics import PhysicsSystem


class TestGravity:
    """Testes de aplicação de gravidade."""

    def test_apply_gravity_increases_vy(self, mock_player: Player) -> None:
        """Testa se gravidade aumenta velocidade vertical."""
        system = PhysicsSystem()
        mock_player.vy = 0.0
        system.apply_gravity(mock_player)
        assert mock_player.vy == pytest.approx(GRAVITY)

    def test_gravity_capped_at_max_fall_speed(self, mock_player: Player) -> None:
        """Testa se velocidade de queda é limitada."""
        system = PhysicsSystem()
        mock_player.vy = MAX_FALL_SPEED
        system.apply_gravity(mock_player)
        assert mock_player.vy == MAX_FALL_SPEED

    def test_gravity_does_not_exceed_max(self, mock_player: Player) -> None:
        """Testa se gravidade não excede máximo mesmo após múltiplas aplicações."""
        system = PhysicsSystem()
        mock_player.vy = 0.0
        for _ in range(100):
            system.apply_gravity(mock_player)
        assert mock_player.vy <= MAX_FALL_SPEED


class TestCollision:
    """Testes de detecção e resolução de colisões."""

    def test_player_lands_on_platform(
        self, mock_player: Player, mock_platform_rect: pygame.Rect
    ) -> None:
        """Testa se jogador aterrissa em plataforma."""
        system = PhysicsSystem()
        mock_player.y = 470.0
        mock_player.vy = 8.0
        system.resolve_collision(mock_player, [mock_platform_rect])
        assert mock_player.on_ground is True

    def test_player_does_not_fall_through_platform(
        self, mock_player: Player, mock_platform_rect: pygame.Rect
    ) -> None:
        """Testa se jogador não atravessa plataforma."""
        system = PhysicsSystem()
        mock_player.y = 470.0
        mock_player.vy = 8.0
        system.resolve_collision(mock_player, [mock_platform_rect])
        assert mock_player.rect.bottom <= mock_platform_rect.top + 1

    def test_check_collision_detects_overlap(self) -> None:
        """Testa se detecção de colisão funciona."""
        system = PhysicsSystem()
        rect1 = pygame.Rect(100, 100, 50, 50)
        rect2 = pygame.Rect(120, 120, 50, 50)
        assert system.check_collision(rect1, rect2) is True

    def test_check_collision_no_overlap(self) -> None:
        """Testa se não detecta colisão quando não há overlap."""
        system = PhysicsSystem()
        rect1 = pygame.Rect(100, 100, 50, 50)
        rect2 = pygame.Rect(200, 200, 50, 50)
        assert system.check_collision(rect1, rect2) is False
