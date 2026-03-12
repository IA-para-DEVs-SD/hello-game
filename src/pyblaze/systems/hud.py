"""Sistema de HUD (Head-Up Display)."""

import logging

import pygame

from pyblaze.settings import COLOR_HUD_TEXT, SCREEN_WIDTH

logger = logging.getLogger(__name__)


class HUD:
    """Renderiza informações do jogo na tela."""

    def __init__(self) -> None:
        """Inicializa o HUD."""
        try:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        except Exception as e:
            logger.error("Failed to load fonts: %s", e)
            raise

    def render(
        self,
        surface: pygame.Surface,
        rings: int,
        lives: int,
        time_seconds: float,
    ) -> None:
        """Renderiza o HUD na tela.

        Args:
            surface: Superfície do pygame onde renderizar.
            rings: Quantidade de anéis do jogador.
            lives: Vidas restantes do jogador.
            time_seconds: Tempo decorrido em segundos.
        """
        # Renderiza contador de anéis
        rings_text = self.font.render(f"Rings: {rings}", True, COLOR_HUD_TEXT)
        surface.blit(rings_text, (20, 20))

        # Renderiza vidas
        lives_text = self.font.render(f"Lives: {lives}", True, COLOR_HUD_TEXT)
        surface.blit(lives_text, (20, 60))

        # Renderiza timer
        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)
        time_text = self.font.render(
            f"Time: {minutes:02d}:{seconds:02d}", True, COLOR_HUD_TEXT
        )
        time_rect = time_text.get_rect()
        time_rect.topright = (SCREEN_WIDTH - 20, 20)
        surface.blit(time_text, time_rect)

    def render_game_over(
        self, surface: pygame.Surface, victory: bool, final_time: float
    ) -> None:
        """Renderiza tela de game over ou vitória.

        Args:
            surface: Superfície do pygame onde renderizar.
            victory: True se é vitória, False se é game over.
            final_time: Tempo final em segundos.
        """
        title = "VICTORY!" if victory else "GAME OVER"
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render(title, True, COLOR_HUD_TEXT)
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_WIDTH // 4)
        )
        surface.blit(title_text, title_rect)

        # Tempo final
        minutes = int(final_time // 60)
        seconds = int(final_time % 60)
        time_text = self.font.render(
            f"Time: {minutes:02d}:{seconds:02d}", True, COLOR_HUD_TEXT
        )
        time_rect = time_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_WIDTH // 3)
        )
        surface.blit(time_text, time_rect)

        # Instruções
        instruction = "Press SPACE to restart" if not victory else "Press SPACE to menu"
        inst_text = self.small_font.render(instruction, True, COLOR_HUD_TEXT)
        inst_rect = inst_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_WIDTH // 2)
        )
        surface.blit(inst_text, inst_rect)
