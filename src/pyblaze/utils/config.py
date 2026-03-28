"""Sistema de configuração com suporte a variáveis de ambiente."""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """Gerencia configurações do jogo a partir de variáveis de ambiente."""

    def __init__(self) -> None:
        """Inicializa o sistema de configuração."""
        self._load_env()

    def _load_env(self) -> None:
        """Carrega arquivo .env se existir."""
        env_file = Path(".env")
        if env_file.exists():
            try:
                with open(env_file, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            key, _, value = line.partition("=")
                            key = key.strip()
                            value = value.strip()
                            if key and value:
                                os.environ[key] = value
                logger.info("Loaded configuration from .env")
            except OSError as e:
                logger.warning("Failed to load .env file: %s", e)

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Obtém valor booleano de variável de ambiente.

        Args:
            key: Nome da variável de ambiente.
            default: Valor padrão se não existir.

        Returns:
            Valor booleano da variável.
        """
        value = os.environ.get(key, str(default)).lower()
        return value in ("true", "1", "yes", "on")

    def get_int(self, key: str, default: int = 0) -> int:
        """Obtém valor inteiro de variável de ambiente.

        Args:
            key: Nome da variável de ambiente.
            default: Valor padrão se não existir.

        Returns:
            Valor inteiro da variável.
        """
        try:
            return int(os.environ.get(key, str(default)))
        except ValueError:
            logger.warning("Invalid int value for %s, using default: %d", key, default)
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        """Obtém valor float de variável de ambiente.

        Args:
            key: Nome da variável de ambiente.
            default: Valor padrão se não existir.

        Returns:
            Valor float da variável.
        """
        try:
            return float(os.environ.get(key, str(default)))
        except ValueError:
            logger.warning(
                "Invalid float value for %s, using default: %.2f", key, default
            )
            return default

    def get_str(self, key: str, default: str = "") -> str:
        """Obtém valor string de variável de ambiente.

        Args:
            key: Nome da variável de ambiente.
            default: Valor padrão se não existir.

        Returns:
            Valor string da variável.
        """
        return os.environ.get(key, default)

    def get_path(self, key: str, default: str = "") -> Path:
        """Obtém caminho de variável de ambiente com expansão de ~.

        Args:
            key: Nome da variável de ambiente.
            default: Valor padrão se não existir.

        Returns:
            Path expandido da variável.
        """
        value = self.get_str(key, default)
        return Path(value).expanduser() if value else Path(default).expanduser()

    @property
    def debug(self) -> bool:
        """Retorna se está em modo debug."""
        return self.get_bool("PYBLAZE_DEBUG", False)

    @property
    def log_level(self) -> str:
        """Retorna o nível de log configurado."""
        return self.get_str("PYBLAZE_LOG_LEVEL", "INFO")

    @property
    def save_dir(self) -> Path:
        """Retorna o diretório de saves."""
        return self.get_path("PYBLAZE_SAVE_DIR", "~/.pyblaze")

    @property
    def screen_width(self) -> int:
        """Retorna largura da tela."""
        return self.get_int("PYBLAZE_SCREEN_WIDTH", 1280)

    @property
    def screen_height(self) -> int:
        """Retorna altura da tela."""
        return self.get_int("PYBLAZE_SCREEN_HEIGHT", 720)

    @property
    def fps(self) -> int:
        """Retorna FPS alvo."""
        return self.get_int("PYBLAZE_FPS", 60)

    @property
    def fullscreen(self) -> bool:
        """Retorna se deve usar tela cheia."""
        return self.get_bool("PYBLAZE_FULLSCREEN", False)

    @property
    def vsync(self) -> bool:
        """Retorna se VSync está ativado."""
        return self.get_bool("PYBLAZE_VSYNC", True)

    @property
    def volume_master(self) -> float:
        """Retorna volume master."""
        return self.get_float("PYBLAZE_VOLUME_MASTER", 0.8)

    @property
    def volume_music(self) -> float:
        """Retorna volume da música."""
        return self.get_float("PYBLAZE_VOLUME_MUSIC", 0.6)

    @property
    def volume_sfx(self) -> float:
        """Retorna volume dos efeitos sonoros."""
        return self.get_float("PYBLAZE_VOLUME_SFX", 0.8)

    @property
    def enable_profiling(self) -> bool:
        """Retorna se profiling está ativado."""
        return self.get_bool("PYBLAZE_ENABLE_PROFILING", False)

    @property
    def show_fps(self) -> bool:
        """Retorna se deve mostrar FPS na tela."""
        return self.get_bool("PYBLAZE_SHOW_FPS", False)

    @property
    def enable_analytics(self) -> bool:
        """Retorna se analytics está ativado."""
        return self.get_bool("PYBLAZE_ENABLE_ANALYTICS", True)

    @property
    def analytics_dir(self) -> Path:
        """Retorna diretório de analytics."""
        return self.get_path("PYBLAZE_ANALYTICS_DIR", "~/.pyblaze/analytics")


# Singleton global
_config_instance: Config | None = None


def get_config() -> Config:
    """Obtém a instância singleton do Config.

    Returns:
        Instância do Config.
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
