"""Utilitário para carregar e fatiar spritesheets."""

import logging
from pathlib import Path

import pygame

logger = logging.getLogger(__name__)


class SpriteSheet:
    """Gerencia carregamento e fatiamento de spritesheets."""

    def __init__(self, filepath: str | Path) -> None:
        """Carrega uma spritesheet.

        Args:
            filepath: Caminho para o arquivo de imagem.

        Raises:
            FileNotFoundError: Se o arquivo não existe.
        """
        try:
            self.sheet = pygame.image.load(str(filepath)).convert_alpha()
            logger.debug("Spritesheet loaded: %s", filepath)
        except pygame.error as e:
            logger.error("Failed to load spritesheet %s: %s", filepath, e)
            raise FileNotFoundError(f"Spritesheet not found: {filepath}") from e

    def get_sprite(
        self, x: int, y: int, width: int, height: int
    ) -> pygame.Surface:
        """Extrai um sprite da spritesheet.

        Args:
            x: Posição X do sprite na sheet.
            y: Posição Y do sprite na sheet.
            width: Largura do sprite.
            height: Altura do sprite.

        Returns:
            Superfície contendo o sprite extraído.
        """
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite

    def get_sprites_row(
        self, y: int, sprite_width: int, sprite_height: int, count: int
    ) -> list[pygame.Surface]:
        """Extrai uma linha de sprites da spritesheet.

        Args:
            y: Posição Y da linha.
            sprite_width: Largura de cada sprite.
            sprite_height: Altura de cada sprite.
            count: Quantidade de sprites a extrair.

        Returns:
            Lista de superfícies contendo os sprites.
        """
        sprites = []
        for i in range(count):
            sprite = self.get_sprite(i * sprite_width, y, sprite_width, sprite_height)
            sprites.append(sprite)
        return sprites
