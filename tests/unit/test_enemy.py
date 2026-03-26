"""Testes unitários para inimigos."""

from pyblaze.entities.enemy import Enemy


class TestEnemy:
    """Testes do inimigo patrulheiro."""

    def test_enemy_patrols_within_range(self, mock_enemy: Enemy) -> None:
        """Testa se inimigo patrulha dentro do alcance definido."""
        for _ in range(200):
            mock_enemy.update(16)
        distance = abs(mock_enemy.x - mock_enemy.start_x)
        assert distance <= mock_enemy.patrol_range

    def test_enemy_changes_direction_at_patrol_limit(self, mock_enemy: Enemy) -> None:
        """Testa se inimigo inverte direção no limite de patrulha."""
        initial_direction = mock_enemy.direction
        # Move até atingir limite
        for _ in range(150):
            mock_enemy.update(16)
        assert mock_enemy.direction != initial_direction

    def test_die_marks_enemy_as_not_alive(self, mock_enemy: Enemy) -> None:
        """Testa se die() marca inimigo como morto."""
        assert mock_enemy.alive is True
        mock_enemy.die()
        assert mock_enemy.alive is False
