"""Sistema de câmera com lerp horizontal."""

import logging

import pygame

from pyblaze.settings import CAMERA_LERP, CAMERA_OFFSET_X, SCREEN_WIDTH

logger = logging.getLogger(__name__)


class Camera:
    """Câmera que acompanha o jogador com suavização."""

    def __init__(self, map_width: int = 5000) -> None:
        """Inicializa a câmera.

        Args:
            map_width: Largura total do mapa.
        """
        self.x = 0.0
        self.lerp_speed = CAMERA_LERP
        self.offset_x = CAMERA_OFFSET_X
        self.map_width = map_width
        self.max_x = max(0, map_width - SCREEN_WIDTH)

    def follow(self, target_x: float) -> None:
        """Atualiza posição da câmera para seguir o alvo.

        Args:
            target_x: Posição X do alvo.
        """
        # Calcula posição desejada (mantém o alvo um pouco à esquerda da tela)
        target_camera_x = target_x - self.offset_x

        # Aplica lerp para suavização
        self.x += (target_camera_x - self.x) * self.lerp_speed

        # Limita câmera aos bounds do mapa
        self.x = max(0, min(self.x, self.max_x))

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        """Aplica offset da câmera a um retângulo.

        Args:
            rect: Retângulo original.

        Returns:
            Novo retângulo com offset da câmera aplicado.
        """
        return pygame.Rect(
            rect.x - int(self.x), rect.y, rect.width, rect.height
        )

    def reset(self) -> None:
        """Reseta a câmera para posição inicial."""
        self.x = 0.0
        logger.debug("Camera reset to position 0")
