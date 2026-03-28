"""Sistema de save/load para persistir progresso do jogador."""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SaveSystem:
    """Gerencia salvamento e carregamento de progresso."""

    def __init__(self, save_dir: Path | None = None) -> None:
        """Inicializa o sistema de save.

        Args:
            save_dir: Diretório para salvar arquivos. Se None, usa ~/.pyblaze/
        """
        if save_dir is None:
            self.save_dir = Path.home() / ".pyblaze"
        else:
            self.save_dir = Path(save_dir)

        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.save_file = self.save_dir / "save.json"
        logger.info("SaveSystem initialized at %s", self.save_dir)

    def save_game(self, player_data: dict[str, Any]) -> bool:
        """Salva o progresso do jogador.

        Args:
            player_data: Dicionário com dados do jogador
                - lives: int
                - rings: int
                - checkpoint_x: float
                - checkpoint_y: float
                - level: str
                - time_played: float

        Returns:
            True se salvou com sucesso, False caso contrário.
        """
        try:
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(player_data, f, indent=2)
            logger.info("Game saved successfully: %s", self.save_file)
            return True
        except (OSError, TypeError, ValueError) as e:
            logger.error("Failed to save game: %s", e)
            return False

    def load_game(self) -> dict[str, Any] | None:
        """Carrega o progresso salvo.

        Returns:
            Dicionário com dados do jogador ou None se não houver save.
        """
        if not self.save_file.exists():
            logger.info("No save file found at %s", self.save_file)
            return None

        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info("Game loaded successfully from %s", self.save_file)
            return data
        except (OSError, json.JSONDecodeError) as e:
            logger.error("Failed to load game: %s", e)
            return None

    def delete_save(self) -> bool:
        """Deleta o arquivo de save.

        Returns:
            True se deletou com sucesso, False caso contrário.
        """
        try:
            if self.save_file.exists():
                self.save_file.unlink()
                logger.info("Save file deleted: %s", self.save_file)
                return True
            return False
        except OSError as e:
            logger.error("Failed to delete save file: %s", e)
            return False

    def has_save(self) -> bool:
        """Verifica se existe um save.

        Returns:
            True se existe um save, False caso contrário.
        """
        return self.save_file.exists()

    def get_save_info(self) -> dict[str, Any] | None:
        """Obtém informações sobre o save sem carregar completamente.

        Returns:
            Dicionário com metadados do save ou None se não existir.
        """
        if not self.has_save():
            return None

        try:
            stat = self.save_file.stat()
            return {
                "exists": True,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "path": str(self.save_file),
            }
        except OSError as e:
            logger.error("Failed to get save info: %s", e)
            return None


# Singleton global para fácil acesso
_save_system_instance: SaveSystem | None = None


def get_save_system(save_dir: Path | None = None) -> SaveSystem:
    """Obtém a instância singleton do SaveSystem.

    Args:
        save_dir: Diretório para salvar arquivos (apenas na primeira chamada).

    Returns:
        Instância do SaveSystem.
    """
    global _save_system_instance
    if _save_system_instance is None:
        _save_system_instance = SaveSystem(save_dir)
    return _save_system_instance
