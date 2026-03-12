"""Testes unitários para anéis."""

from pyblaze.entities.ring import Ring


class TestRing:
    """Testes do anel coletável."""

    def test_collect_marks_ring_as_collected(self, mock_ring: Ring) -> None:
        """Testa se collect() marca anel como coletado."""
        assert mock_ring.collected is False
        mock_ring.collect()
        assert mock_ring.collected is True

    def test_fly_out_sets_flying_state(self, mock_ring: Ring) -> None:
        """Testa se fly_out() ativa estado de voo."""
        assert mock_ring.flying is False
        mock_ring.fly_out(direction=1.0)
        assert mock_ring.flying is True
        assert mock_ring.vx != 0.0
        assert mock_ring.vy < 0

    def test_flying_stops_after_timer(self, mock_ring: Ring) -> None:
        """Testa se voo para após timer expirar."""
        mock_ring.fly_out(direction=1.0)
        # Simula tempo maior que RING_FLY_DURATION
        for _ in range(200):
            mock_ring.update(16)
        assert mock_ring.flying is False
