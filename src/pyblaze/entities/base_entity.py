"""Entidade base com posição, tamanho e rect de colisão."""

import pygame


class BaseEntity:
    """Classe base para todas as entidades do jogo."""

    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        """Inicializa a entidade com posição e dimensões.

        Args:
            x: Posição X inicial.
            y: Posição Y inicial.
            width: Largura da entidade.
            height: Altura da entidade.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def rect(self) -> pygame.Rect:
        """Retorna o retângulo de colisão da entidade."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt: int) -> None:
        """Atualiza a entidade.

        Args:
            dt: Delta time em milissegundos.
        """
        pass

    def draw(self, surface: pygame.Surface, camera_x: float = 0.0) -> None:
        """Renderiza a entidade na superfície.

        Args:
            surface: Superfície do pygame onde renderizar.
            camera_x: Offset da câmera no eixo X.
        """
        pass
