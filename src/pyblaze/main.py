"""Entry point do jogo PyBlaze."""

import logging
import sys

import pygame

from pyblaze.scenes.menu import MenuScene
from pyblaze.settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Função principal do jogo."""
    logger.info("Initializing PyBlaze")

    # Inicializa pygame
    pygame.init()
    pygame.mixer.init()

    # Cria janela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    logger.info("Game window created: %dx%d", SCREEN_WIDTH, SCREEN_HEIGHT)

    # Cena inicial
    current_scene: MenuScene | None = MenuScene(screen)

    # Game loop principal
    running = True
    while running and current_scene is not None:
        dt = clock.tick(FPS)

        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quit event received")
                running = False
            else:
                current_scene.handle_event(event)

        # Atualiza e renderiza
        current_scene.update(dt)
        current_scene.draw()
        pygame.display.flip()

        # Troca de cena
        current_scene = current_scene.next_scene  # type: ignore[assignment]

    # Finaliza
    pygame.quit()
    logger.info("PyBlaze terminated")
    sys.exit()


if __name__ == "__main__":
    main()
