"""Configuração de fixtures compartilhadas para testes."""

import os

import pygame
import pytest


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Inicializa pygame em modo headless para testes."""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


@pytest.fixture
def mock_player():
    """Cria um player em posição padrão para testes."""
    from pyblaze.entities.player import Player

    return Player(x=100, y=400)


@pytest.fixture
def mock_platform_rect():
    """Cria um retângulo de plataforma padrão."""
    return pygame.Rect(0, 500, 800, 32)


@pytest.fixture
def mock_enemy():
    """Cria um inimigo para testes."""
    from pyblaze.entities.enemy import Enemy

    return Enemy(x=200, y=400)


@pytest.fixture
def mock_ring():
    """Cria um anel para testes."""
    from pyblaze.entities.ring import Ring

    return Ring(x=150, y=450)


@pytest.fixture
def mock_pygame_surface():
    """Cria uma superfície pygame para testes de renderização."""
    return pygame.Surface((800, 600))
