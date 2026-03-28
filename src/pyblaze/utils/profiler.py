"""Sistema de profiling e performance monitoring."""

import cProfile
import logging
import pstats
import time
from collections import deque
from collections.abc import Callable
from io import StringIO
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor de performance em tempo real."""

    def __init__(self, window_size: int = 60) -> None:
        """Inicializa o monitor de performance.

        Args:
            window_size: Tamanho da janela para médias móveis (frames).
        """
        self.window_size = window_size
        self.frame_times: deque[float] = deque(maxlen=window_size)
        self.update_times: deque[float] = deque(maxlen=window_size)
        self.render_times: deque[float] = deque(maxlen=window_size)
        self.last_frame_time = time.perf_counter()

    def start_frame(self) -> None:
        """Marca o início de um frame."""
        self.last_frame_time = time.perf_counter()

    def end_frame(self) -> float:
        """Marca o fim de um frame e retorna o tempo decorrido.

        Returns:
            Tempo do frame em segundos.
        """
        frame_time = time.perf_counter() - self.last_frame_time
        self.frame_times.append(frame_time)
        return frame_time

    def record_update_time(self, elapsed: float) -> None:
        """Registra tempo de update.

        Args:
            elapsed: Tempo decorrido em segundos.
        """
        self.update_times.append(elapsed)

    def record_render_time(self, elapsed: float) -> None:
        """Registra tempo de renderização.

        Args:
            elapsed: Tempo decorrido em segundos.
        """
        self.render_times.append(elapsed)

    @property
    def avg_fps(self) -> float:
        """Retorna FPS médio."""
        if not self.frame_times:
            return 0.0
        avg_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_time if avg_time > 0 else 0.0

    @property
    def current_fps(self) -> float:
        """Retorna FPS atual."""
        if not self.frame_times:
            return 0.0
        last_time = self.frame_times[-1]
        return 1.0 / last_time if last_time > 0 else 0.0

    @property
    def avg_update_time_ms(self) -> float:
        """Retorna tempo médio de update em ms."""
        if not self.update_times:
            return 0.0
        return (sum(self.update_times) / len(self.update_times)) * 1000

    @property
    def avg_render_time_ms(self) -> float:
        """Retorna tempo médio de render em ms."""
        if not self.render_times:
            return 0.0
        return (sum(self.render_times) / len(self.render_times)) * 1000

    def get_stats(self) -> dict[str, float]:
        """Retorna estatísticas completas.

        Returns:
            Dicionário com estatísticas de performance.
        """
        return {
            "fps_current": self.current_fps,
            "fps_avg": self.avg_fps,
            "update_ms": self.avg_update_time_ms,
            "render_ms": self.avg_render_time_ms,
            "frame_ms": (
                sum(self.frame_times) / len(self.frame_times) * 1000
                if self.frame_times
                else 0.0
            ),
        }


class GameProfiler:
    """Profiler para análise detalhada de performance."""

    def __init__(self) -> None:
        """Inicializa o profiler."""
        self.profiler = cProfile.Profile()
        self.is_profiling = False

    def start(self) -> None:
        """Inicia o profiling."""
        if not self.is_profiling:
            self.profiler.enable()
            self.is_profiling = True
            logger.info("Profiling started")

    def stop(self) -> None:
        """Para o profiling."""
        if self.is_profiling:
            self.profiler.disable()
            self.is_profiling = False
            logger.info("Profiling stopped")

    def save_stats(self, output_path: Path | str) -> None:
        """Salva estatísticas em arquivo.

        Args:
            output_path: Caminho para salvar as estatísticas.
        """
        if not self.is_profiling:
            self.profiler.dump_stats(str(output_path))
            logger.info("Profiling stats saved to %s", output_path)

    def print_stats(self, sort_by: str = "cumulative", limit: int = 20) -> None:
        """Imprime estatísticas no console.

        Args:
            sort_by: Critério de ordenação (cumulative, time, calls, etc).
            limit: Número de linhas a exibir.
        """
        if not self.is_profiling:
            stream = StringIO()
            stats = pstats.Stats(self.profiler, stream=stream)
            stats.sort_stats(sort_by)
            stats.print_stats(limit)
            logger.info("Profiling stats:\n%s", stream.getvalue())

    def profile_function(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator para profilear uma função.

        Args:
            func: Função a ser profileada.

        Returns:
            Função decorada.
        """

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.start()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                self.stop()

        return wrapper
