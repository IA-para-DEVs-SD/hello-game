"""Gerenciamento de áudio e efeitos sonoros."""

import logging
from pathlib import Path

import pygame

logger = logging.getLogger(__name__)


class AudioManager:
    """Gerencia músicas e efeitos sonoros."""

    def __init__(self) -> None:
        """Inicializa o gerenciador de áudio."""
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        pygame.mixer.set_num_channels(16)
        logger.debug("AudioManager initialized")

    def load_music(self, filepath: str | Path) -> None:
        """Carrega e toca música de fundo.

        Args:
            filepath: Caminho para o arquivo de música.
        """
        try:
            pygame.mixer.music.load(str(filepath))
            pygame.mixer.music.set_volume(self.music_volume)
            logger.info("Music loaded: %s", filepath)
        except pygame.error as e:
            logger.warning("Failed to load music %s: %s", filepath, e)

    def play_music(self, loops: int = -1) -> None:
        """Toca a música carregada.

        Args:
            loops: Quantidade de loops (-1 para infinito).
        """
        try:
            pygame.mixer.music.play(loops)
            logger.debug("Music playing")
        except pygame.error as e:
            logger.warning("Failed to play music: %s", e)

    def stop_music(self) -> None:
        """Para a música."""
        pygame.mixer.music.stop()
        logger.debug("Music stopped")

    def load_sound(self, name: str, filepath: str | Path) -> None:
        """Carrega um efeito sonoro.

        Args:
            name: Nome identificador do som.
            filepath: Caminho para o arquivo de som.
        """
        try:
            sound = pygame.mixer.Sound(str(filepath))
            sound.set_volume(self.sfx_volume)
            self.sounds[name] = sound
            logger.debug("Sound loaded: %s -> %s", name, filepath)
        except pygame.error as e:
            logger.warning("Failed to load sound %s: %s", name, e)

    def play_sound(self, name: str) -> None:
        """Toca um efeito sonoro.

        Args:
            name: Nome do som a tocar.
        """
        if name in self.sounds:
            self.sounds[name].play()
        else:
            logger.warning("Sound not found: %s", name)

    def set_music_volume(self, volume: float) -> None:
        """Define volume da música.

        Args:
            volume: Volume entre 0.0 e 1.0.
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume: float) -> None:
        """Define volume dos efeitos sonoros.

        Args:
            volume: Volume entre 0.0 e 1.0.
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
