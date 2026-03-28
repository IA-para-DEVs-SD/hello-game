"""Sistema de analytics local para rastrear métricas de gameplay."""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AnalyticsSystem:
    """Coleta e armazena métricas de gameplay localmente."""

    def __init__(self, analytics_dir: Path | None = None) -> None:
        """Inicializa o sistema de analytics.

        Args:
            analytics_dir: Diretório para armazenar analytics.
        """
        if analytics_dir is None:
            self.analytics_dir = Path.home() / ".pyblaze" / "analytics"
        else:
            self.analytics_dir = Path(analytics_dir)

        self.analytics_dir.mkdir(parents=True, exist_ok=True)
        self.session_start = time.time()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.events: list[dict[str, Any]] = []

        logger.info("AnalyticsSystem initialized at %s", self.analytics_dir)

    def track_event(
        self, event_name: str, properties: dict[str, Any] | None = None
    ) -> None:
        """Registra um evento de gameplay.

        Args:
            event_name: Nome do evento.
            properties: Propriedades adicionais do evento.
        """
        event = {
            "timestamp": time.time(),
            "session_id": self.session_id,
            "event": event_name,
            "properties": properties or {},
        }
        self.events.append(event)
        logger.debug("Event tracked: %s", event_name)

    def track_level_start(self, level_name: str) -> None:
        """Registra início de uma fase.

        Args:
            level_name: Nome da fase.
        """
        self.track_event("level_start", {"level": level_name})

    def track_level_complete(
        self, level_name: str, time_seconds: float, rings_collected: int
    ) -> None:
        """Registra conclusão de uma fase.

        Args:
            level_name: Nome da fase.
            time_seconds: Tempo para completar em segundos.
            rings_collected: Número de anéis coletados.
        """
        self.track_event(
            "level_complete",
            {
                "level": level_name,
                "time": time_seconds,
                "rings": rings_collected,
            },
        )

    def track_player_death(self, cause: str, position: tuple[float, float]) -> None:
        """Registra morte do jogador.

        Args:
            cause: Causa da morte (fall, enemy, etc).
            position: Posição (x, y) onde morreu.
        """
        self.track_event(
            "player_death", {"cause": cause, "x": position[0], "y": position[1]}
        )

    def track_checkpoint_reached(self, checkpoint_id: int) -> None:
        """Registra ativação de checkpoint.

        Args:
            checkpoint_id: ID do checkpoint.
        """
        self.track_event("checkpoint_reached", {"checkpoint": checkpoint_id})

    def track_enemy_defeated(self, enemy_type: str) -> None:
        """Registra derrota de inimigo.

        Args:
            enemy_type: Tipo do inimigo.
        """
        self.track_event("enemy_defeated", {"type": enemy_type})

    def get_session_duration(self) -> float:
        """Retorna duração da sessão em segundos.

        Returns:
            Duração da sessão.
        """
        return time.time() - self.session_start

    def get_summary(self) -> dict[str, Any]:
        """Retorna resumo da sessão.

        Returns:
            Dicionário com estatísticas da sessão.
        """
        event_counts: dict[str, int] = {}
        for event in self.events:
            name = event["event"]
            event_counts[name] = event_counts.get(name, 0) + 1

        return {
            "session_id": self.session_id,
            "duration_seconds": self.get_session_duration(),
            "total_events": len(self.events),
            "event_counts": event_counts,
        }

    def save_session(self) -> bool:
        """Salva a sessão atual em arquivo JSON.

        Returns:
            True se salvou com sucesso, False caso contrário.
        """
        try:
            filename = f"session_{self.session_id}.json"
            filepath = self.analytics_dir / filename

            data = {
                "summary": self.get_summary(),
                "events": self.events,
            }

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            logger.info("Analytics session saved to %s", filepath)
            return True
        except (OSError, TypeError) as e:
            logger.error("Failed to save analytics session: %s", e)
            return False


# Singleton global
_analytics_instance: AnalyticsSystem | None = None


def get_analytics() -> AnalyticsSystem:
    """Obtém a instância singleton do AnalyticsSystem.

    Returns:
        Instância do AnalyticsSystem.
    """
    global _analytics_instance
    if _analytics_instance is None:
        _analytics_instance = AnalyticsSystem()
    return _analytics_instance
