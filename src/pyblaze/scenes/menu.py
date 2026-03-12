"""Tela de menu principal."""

import logging

import pygame

from pyblaze.scenes.base_scene import BaseScene
from pyblaze.settings import (
    COLOR_MENU_BG,
    COLOR_MENU_TEXT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

logger = logging.getLogger(__name__)


class MenuScene(BaseScene):
    """Cena do menu principal."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Inicializa o menu.

        Args:
            screen: Superfície principal do pygame.
        """
        super().__init__(screen)
        self.title_font = pygame.font.Font(None, 84)
        self.option_font = pygame.font.Font(None, 48)
        self.selected_option = 0
        self.options = ["START GAME", "QUIT"]
        logger.debug("MenuScene initialized")

    def handle_event(self, event: pygame.event.Event) -> None:
        """Processa eventos do menu.

        Args:
            event: Evento do pygame.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = (self.selected_option - 1) % len(self.options)
                logger.debug("Menu option: %d", self.selected_option)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = (self.selected_option + 1) % len(self.options)
                logger.debug("Menu option: %d", self.selected_option)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.selected_option == 0:
                    # Lazy import para evitar circular import
                    from pyblaze.scenes.game import GameScene
                    self.switch_to(GameScene(self.screen))
                    logger.info("Starting game")
                elif self.selected_option == 1:
                    self.switch_to(None)
                    logger.info("Quitting game")

    def update(self, dt: int) -> None:
        """Atualiza o menu.

        Args:
            dt: Delta time em milissegundos.
        """
        pass

    def draw(self) -> None:
        """Renderiza o menu."""
        self.screen.fill(COLOR_MENU_BG)

        # Título
        title = self.title_font.render("PYBLAZE", True, COLOR_MENU_TEXT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)

        # Opções
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else COLOR_MENU_TEXT
            text = self.option_font.render(option, True, color)
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60)
            )
            self.screen.blit(text, text_rect)

        # Instruções
        inst_font = pygame.font.Font(None, 24)
        instructions = "Use ARROW KEYS or W/S to navigate, ENTER/SPACE to select"
        inst_text = inst_font.render(instructions, True, (150, 150, 150))
        inst_rect = inst_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        )
        self.screen.blit(inst_text, inst_rect)
