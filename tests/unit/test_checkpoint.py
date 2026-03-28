"""Testes para o sistema de checkpoints."""

import pygame

from pyblaze.entities.checkpoint import Checkpoint
from pyblaze.settings import CHECKPOINT_HEIGHT, CHECKPOINT_WIDTH


class TestCheckpoint:
    """Testes para a classe Checkpoint."""

    def test_checkpoint_initialization(self) -> None:
        """Testa inicialização do checkpoint."""
        checkpoint = Checkpoint(100.0, 200.0)

        assert checkpoint.x == 100.0
        assert checkpoint.y == 200.0
        assert checkpoint.width == CHECKPOINT_WIDTH
        assert checkpoint.height == CHECKPOINT_HEIGHT
        assert checkpoint.activated is False

    def test_checkpoint_spawn_position_calculated(self) -> None:
        """Testa cálculo da posição de spawn."""
        checkpoint = Checkpoint(100.0, 200.0)

        expected_spawn_x = 100.0 + CHECKPOINT_WIDTH // 2
        expected_spawn_y = 200.0 + CHECKPOINT_HEIGHT

        assert checkpoint.spawn_x == expected_spawn_x
        assert checkpoint.spawn_y == expected_spawn_y

    def test_activate_changes_state(self) -> None:
        """Testa que activate() muda o estado do checkpoint."""
        checkpoint = Checkpoint(100.0, 200.0)

        assert checkpoint.activated is False
        checkpoint.activate()
        assert checkpoint.activated is True

    def test_activate_is_idempotent(self) -> None:
        """Testa que ativar múltiplas vezes não causa problemas."""
        checkpoint = Checkpoint(100.0, 200.0)

        checkpoint.activate()
        assert checkpoint.activated is True

        # Ativa novamente
        checkpoint.activate()
        assert checkpoint.activated is True

    def test_update_does_not_crash(self) -> None:
        """Testa que update() executa sem erros."""
        checkpoint = Checkpoint(100.0, 200.0)

        # update() não faz nada, mas não deve crashar
        checkpoint.update(16)
        checkpoint.update(1000)

        assert True  # Se chegou aqui, não crashou

    def test_checkpoint_rect_position(self) -> None:
        """Testa que o rect está na posição correta."""
        checkpoint = Checkpoint(150.0, 250.0)

        assert checkpoint.rect.x == 150
        assert checkpoint.rect.y == 250
        assert checkpoint.rect.width == CHECKPOINT_WIDTH
        assert checkpoint.rect.height == CHECKPOINT_HEIGHT

    def test_checkpoint_collision_detection(self) -> None:
        """Testa detecção de colisão com checkpoint."""
        checkpoint = Checkpoint(100.0, 100.0)

        # Cria um rect que colide
        player_rect = pygame.Rect(105, 105, 32, 32)
        assert checkpoint.rect.colliderect(player_rect)

        # Cria um rect que não colide
        far_rect = pygame.Rect(500, 500, 32, 32)
        assert not checkpoint.rect.colliderect(far_rect)

    def test_multiple_checkpoints_independent(self) -> None:
        """Testa que múltiplos checkpoints são independentes."""
        checkpoint1 = Checkpoint(100.0, 100.0)
        checkpoint2 = Checkpoint(200.0, 100.0)

        checkpoint1.activate()

        assert checkpoint1.activated is True
        assert checkpoint2.activated is False

    def test_draw_does_not_crash_inactive(
        self, mock_pygame_surface: pygame.Surface
    ) -> None:
        """Testa que draw() não crasha com checkpoint inativo."""
        checkpoint = Checkpoint(100.0, 100.0)

        # Não deve crashar
        checkpoint.draw(mock_pygame_surface, camera_x=0.0)
        checkpoint.draw(mock_pygame_surface, camera_x=50.0)

        assert True

    def test_draw_does_not_crash_active(
        self, mock_pygame_surface: pygame.Surface
    ) -> None:
        """Testa que draw() não crasha com checkpoint ativo."""
        checkpoint = Checkpoint(100.0, 100.0)
        checkpoint.activate()

        # Não deve crashar
        checkpoint.draw(mock_pygame_surface, camera_x=0.0)
        checkpoint.draw(mock_pygame_surface, camera_x=100.0)

        assert True

    def test_checkpoint_spawn_position_offset(self) -> None:
        """Testa que spawn position está acima do checkpoint."""
        checkpoint = Checkpoint(0.0, 0.0)

        # Spawn X deve estar no centro do checkpoint
        assert checkpoint.spawn_x == CHECKPOINT_WIDTH // 2

        # Spawn Y deve estar abaixo do checkpoint (para player spawnar em cima)
        assert checkpoint.spawn_y == CHECKPOINT_HEIGHT
