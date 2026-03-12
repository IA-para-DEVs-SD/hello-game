"""Testes unitários para o personagem."""

from pyblaze.entities.player import Player, PlayerState
from pyblaze.settings import PLAYER_LIVES


class TestPlayerDamage:
    """Testes de sistema de dano do jogador."""

    def test_take_damage_with_rings_loses_rings_not_life(
        self, mock_player: Player
    ) -> None:
        """Testa se jogador com anéis perde anéis e não vidas."""
        mock_player.rings = 10
        initial_lives = mock_player.lives
        mock_player.take_damage()
        assert mock_player.rings == 0
        assert mock_player.lives == initial_lives

    def test_take_damage_without_rings_loses_life(
        self, mock_player: Player
    ) -> None:
        """Testa se jogador sem anéis perde vida."""
        mock_player.rings = 0
        mock_player.take_damage()
        assert mock_player.lives == PLAYER_LIVES - 1

    def test_player_dead_when_no_lives(self, mock_player: Player) -> None:
        """Testa se jogador morre quando vidas chegam a zero."""
        mock_player.lives = 1
        mock_player.rings = 0
        mock_player.take_damage()
        assert mock_player.is_dead is True
        assert mock_player.state == PlayerState.DEAD

    def test_invincibility_after_taking_damage_with_rings(
        self, mock_player: Player
    ) -> None:
        """Testa se jogador fica invencível após perder anéis."""
        mock_player.rings = 5
        mock_player.take_damage()
        assert mock_player.invincibility_timer > 0
        assert mock_player.state == PlayerState.INVINCIBLE


class TestPlayerMovement:
    """Testes de movimentação do jogador."""

    def test_collect_ring_increments_counter(self, mock_player: Player) -> None:
        """Testa se coleta de anel incrementa contador."""
        initial = mock_player.rings
        mock_player.collect_ring()
        assert mock_player.rings == initial + 1

    def test_jump_sets_negative_vy(self, mock_player: Player) -> None:
        """Testa se pulo define velocidade vertical negativa."""
        mock_player.on_ground = True
        mock_player.jump(long_jump=True)
        assert mock_player.vy < 0
        assert mock_player.state == PlayerState.JUMPING

    def test_cannot_jump_in_air(self, mock_player: Player) -> None:
        """Testa se jogador não pode pular no ar."""
        mock_player.on_ground = False
        initial_vy = mock_player.vy
        mock_player.jump(long_jump=True)
        assert mock_player.vy == initial_vy

    def test_respawn_sets_checkpoint_position(self, mock_player: Player) -> None:
        """Testa se respawn coloca jogador no checkpoint."""
        mock_player.set_checkpoint(500, 300)
        mock_player.x = 1000
        mock_player.y = 600
        mock_player.respawn()
        assert mock_player.x == 500
        assert mock_player.y == 300
