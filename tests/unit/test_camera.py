"""Testes unitários para o sistema de câmera."""

import pygame

from pyblaze.systems.camera import Camera


class TestCamera:
    """Testes do sistema de câmera."""

    def test_camera_follows_player_position(self) -> None:
        """Testa se câmera segue posição do jogador."""
        camera = Camera()
        initial_x = camera.x
        camera.follow(target_x=500.0)
        assert camera.x > initial_x

    def test_camera_does_not_go_negative(self) -> None:
        """Testa se câmera não vai para posição negativa."""
        camera = Camera()
        camera.follow(target_x=0.0)
        assert camera.x >= 0

    def test_camera_does_not_exceed_map_bounds(self) -> None:
        """Testa se câmera não excede limites do mapa."""
        camera = Camera(map_width=2000)
        camera.follow(target_x=10000.0)
        assert camera.x <= camera.max_x

    def test_apply_returns_offset_rect(self) -> None:
        """Testa se aplicação de câmera retorna rect com offset."""
        camera = Camera()
        camera.x = 100.0
        original = pygame.Rect(200, 300, 32, 32)
        result = camera.apply(original)
        assert result.x == 100  # 200 - 100
        assert result.y == 300
        assert result.width == 32
        assert result.height == 32

    def test_reset_sets_camera_to_zero(self) -> None:
        """Testa se reset coloca câmera na posição inicial."""
        camera = Camera()
        camera.x = 500.0
        camera.reset()
        assert camera.x == 0.0
