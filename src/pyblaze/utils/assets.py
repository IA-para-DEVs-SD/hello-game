"""Gerenciador de assets (sprites, sons, etc)."""

import logging
from pathlib import Path
from typing import Final

import pygame

logger = logging.getLogger(__name__)

# Diretório de assets
ASSETS_DIR: Final = Path(__file__).parent.parent.parent.parent / "assets"
SPRITES_DIR: Final = ASSETS_DIR / "sprites"


class AssetManager:
    """Gerencia carregamento e cache de assets do jogo."""

    def __init__(self) -> None:
        """Inicializa o gerenciador de assets."""
        self.sprites: dict[str, pygame.Surface] = {}
        self.spritesheets: dict[str, list[pygame.Surface]] = {}
        self._load_sprites()

    def _load_sprites(self) -> None:
        """Carrega todos os sprites do jogo."""
        if not SPRITES_DIR.exists():
            logger.warning("Sprites directory not found: %s", SPRITES_DIR)
            logger.info("Using fallback colored rectangles")
            return

        try:
            # Player spritesheet (4 frames de 40x50)
            # Tenta carregar versão procedural primeiro
            player_sheet_path = SPRITES_DIR / "player_procedural.png"
            if not player_sheet_path.exists():
                player_sheet_path = SPRITES_DIR / "player.png"

            if player_sheet_path.exists():
                if "procedural" in str(player_sheet_path):
                    # Sprite procedural único - replica para 4 frames
                    sprite = pygame.image.load(str(player_sheet_path)).convert_alpha()
                    self.spritesheets["player"] = [sprite] * 4
                    logger.info("Loaded player procedural sprite")
                else:
                    # Spritesheet normal
                    sheet = pygame.image.load(str(player_sheet_path)).convert_alpha()
                    self.spritesheets["player"] = [
                        self._get_sprite_from_sheet(sheet, i * 40, 0, 40, 50)
                        for i in range(4)
                    ]
                    logger.info("Loaded player spritesheet (4 frames)")
            else:
                logger.warning("Player sprite not found")

            # Enemy - tenta procedural primeiro
            enemy_path = SPRITES_DIR / "enemy_procedural.png"
            if not enemy_path.exists():
                enemy_path = SPRITES_DIR / "enemy.png"

            if enemy_path.exists():
                self.sprites["enemy"] = pygame.image.load(
                    str(enemy_path)
                ).convert_alpha()
                sprite_type = (
                    "procedural" if "procedural" in str(enemy_path) else "standard"
                )
                logger.info(f"Loaded enemy sprite ({sprite_type})")

            # Ring - tenta procedural primeiro
            ring_path = SPRITES_DIR / "ring_procedural.png"
            if not ring_path.exists():
                ring_path = SPRITES_DIR / "ring.png"

            if ring_path.exists():
                self.sprites["ring"] = pygame.image.load(str(ring_path)).convert_alpha()
                sprite_type = (
                    "procedural" if "procedural" in str(ring_path) else "standard"
                )
                logger.info(f"Loaded ring sprite ({sprite_type})")

            # Checkpoint
            checkpoint_path = SPRITES_DIR / "checkpoint.png"
            if checkpoint_path.exists():
                self.sprites["checkpoint"] = pygame.image.load(
                    str(checkpoint_path)
                ).convert_alpha()
                logger.info("Loaded checkpoint sprite")

            # Checkpoint active
            checkpoint_active_path = SPRITES_DIR / "checkpoint_active.png"
            if checkpoint_active_path.exists():
                self.sprites["checkpoint_active"] = pygame.image.load(
                    str(checkpoint_active_path)
                ).convert_alpha()
                logger.info("Loaded checkpoint_active sprite")

            # Platform tile
            platform_path = SPRITES_DIR / "platform_tile.png"
            if platform_path.exists():
                self.sprites["platform"] = pygame.image.load(
                    str(platform_path)
                ).convert_alpha()
                logger.info("Loaded platform tile sprite")

        except pygame.error as e:
            logger.error("Error loading sprites: %s", e)
            logger.info("Using fallback colored rectangles")

    def _get_sprite_from_sheet(
        self, sheet: pygame.Surface, x: int, y: int, width: int, height: int
    ) -> pygame.Surface:
        """Extrai um sprite de uma spritesheet.

        Args:
            sheet: Spritesheet completa.
            x: Posição X do sprite.
            y: Posição Y do sprite.
            width: Largura do sprite.
            height: Altura do sprite.

        Returns:
            Superfície com o sprite extraído.
        """
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(sheet, (0, 0), (x, y, width, height))
        return sprite

    def get_player_sprite(self, frame: int = 0) -> pygame.Surface | None:
        """Retorna sprite do player.

        Args:
            frame: Frame da animação (0-3).

        Returns:
            Sprite do player ou None se não carregado.
        """
        if "player" in self.spritesheets:
            return self.spritesheets["player"][frame % 4]
        return None

    def get_enemy_sprite(self) -> pygame.Surface | None:
        """Retorna sprite do inimigo."""
        return self.sprites.get("enemy")

    def get_ring_sprite(self) -> pygame.Surface | None:
        """Retorna sprite do anel."""
        return self.sprites.get("ring")

    def get_checkpoint_sprite(self, active: bool = False) -> pygame.Surface | None:
        """Retorna sprite do checkpoint.

        Args:
            active: Se True, retorna sprite ativo. Se False, inativo.

        Returns:
            Sprite do checkpoint ou None se não carregado.
        """
        key = "checkpoint_active" if active else "checkpoint"
        return self.sprites.get(key)

    def get_platform_sprite(self) -> pygame.Surface | None:
        """Retorna sprite da plataforma."""
        return self.sprites.get("platform")

    def has_sprites(self) -> bool:
        """Verifica se há sprites carregados.

        Returns:
            True se há sprites, False caso contrário.
        """
        return bool(self.sprites or self.spritesheets)


# Instância global (singleton)
_asset_manager: AssetManager | None = None


def get_asset_manager() -> AssetManager:
    """Retorna a instância global do AssetManager.

    Returns:
        Instância do AssetManager.
    """
    global _asset_manager
    if _asset_manager is None:
        _asset_manager = AssetManager()
    return _asset_manager
