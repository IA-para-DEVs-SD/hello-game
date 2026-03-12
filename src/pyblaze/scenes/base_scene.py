"""Classe base abstrata para todas as cenas."""

from abc import ABC, abstractmethod

import pygame


class BaseScene(ABC):
    """Classe base para todas as cenas do jogo."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Inicializa a cena.

        Args:
            screen: Superfície principal do pygame.
        """
        self.screen = screen
        self.next_scene: BaseScene | None = self

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Processa eventos da cena.

        Args:
            event: Evento do pygame.
        """
        pass

    @abstractmethod
    def update(self, dt: int) -> None:
        """Atualiza a lógica da cena.

        Args:
            dt: Delta time em milissegundos.
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """Renderiza a cena."""
        pass

    def switch_to(self, scene: "BaseScene | None") -> None:
        """Troca para outra cena.

        Args:
            scene: Nova cena (None encerra o jogo).
        """
        self.next_scene = scene
