"""Tela de game over e vitória."""

import logging

import pygame

from pyblaze.scenes.base_scene import BaseScene
from pyblaze.settings import COLOR_MENU_BG, SCREEN_HEIGHT, SCREEN_WIDTH

logger = logging.getLogger(__name__)


class GameOverScene(BaseScene):
    """Cena de game over ou vitória."""

    def __init__(
        self, screen: pygame.Surface, victory: bool, final_time: float
    ) -> None:
        """Inicializa a cena de game over.

        Args:
            screen: Superfície principal do pygame.
            victory: True se é vitória, False se é game over.
            final_time: Tempo final em segundos.
        """
        super().__init__(screen)
        self.victory = victory
        self.final_time = final_time
        self.title_font = pygame.font.Font(None, 72)
        self.text_font = pygame.font.Font(None, 48)
        logger.info("GameOverScene: victory=%s, time=%.2fs", victory, final_time)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Processa eventos.

        Args:
            event: Evento do pygame.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                from pyblaze.scenes.game import GameScene

                self.switch_to(GameScene(self.screen))
                logger.info("Restarting game")
            elif event.key == pygame.K_ESCAPE:
                from pyblaze.scenes.menu import MenuScene

                self.switch_to(MenuScene(self.screen))
                logger.info("Returning to menu")

    def update(self, dt: int) -> None:
        """Atualiza a cena.

        Args:
            dt: Delta time em milissegundos.
        """
        pass

    def draw(self) -> None:
        """Renderiza a cena."""
        self.screen.fill(COLOR_MENU_BG)

        # Título
        title = "VICTORY!" if self.victory else "GAME OVER"
        color = (0, 255, 0) if self.victory else (255, 50, 50)
        title_text = self.title_font.render(title, True, color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        # Tempo
        minutes = int(self.final_time // 60)
        seconds = int(self.final_time % 60)
        time_text = self.text_font.render(
            f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255)
        )
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(time_text, time_rect)

        # Instruções
        inst_font = pygame.font.Font(None, 32)
        restart_text = inst_font.render(
            "SPACE to restart | ESC for menu", True, (200, 200, 200)
        )
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        )
        self.screen.blit(restart_text, restart_rect)
