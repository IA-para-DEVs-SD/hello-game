"""Personagem principal com state machine completa."""

import logging
from enum import Enum, auto

import pygame

from pyblaze.entities.base_entity import BaseEntity
from pyblaze.settings import (
    ACCELERATION,
    COLOR_PLAYER,
    COLOR_PLAYER_HURT,
    FRICTION,
    INVINCIBILITY_FRAMES,
    JUMP_FORCE,
    JUMP_FORCE_SHORT,
    PLAYER_HEIGHT,
    PLAYER_LIVES,
    PLAYER_SPEED,
    PLAYER_SPRINT_SPEED,
    PLAYER_WIDTH,
    SPRINT_THRESHOLD_FRAMES,
)

logger = logging.getLogger(__name__)


class PlayerState(Enum):
    """Estados possíveis do personagem."""

    IDLE = auto()
    RUNNING = auto()
    SPRINTING = auto()
    JUMPING = auto()
    FALLING = auto()
    SPIN_ATTACK = auto()
    HURT = auto()
    INVINCIBLE = auto()
    DEAD = auto()


class Player(BaseEntity):
    """Personagem principal com mecânicas de movimento e combate."""

    def __init__(self, x: float, y: float) -> None:
        """Inicializa o personagem.

        Args:
            x: Posição X inicial.
            y: Posição Y inicial.
        """
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.lives = PLAYER_LIVES
        self.rings = 0
        self.state = PlayerState.IDLE
        self.facing_right = True
        self.sprint_timer = 0
        self.invincibility_timer = 0
        self.last_checkpoint_x = x
        self.last_checkpoint_y = y

    def move(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Processa input de movimento.

        Args:
            keys: Estado do teclado do pygame.
        """
        if self.state in (PlayerState.HURT, PlayerState.DEAD):
            return

        # Movimento horizontal
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx -= ACCELERATION
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx += ACCELERATION
            self.facing_right = True
            moving = True

        # Limita velocidade máxima
        if self.state == PlayerState.SPRINTING:
            max_speed = PLAYER_SPRINT_SPEED
        else:
            max_speed = PLAYER_SPEED

        self.vx = max(-max_speed, min(max_speed, self.vx))

        # Atualiza sprint timer
        if moving and abs(self.vx) > PLAYER_SPEED * 0.9:
            self.sprint_timer += 1
            if (
                self.sprint_timer >= SPRINT_THRESHOLD_FRAMES
                and self.state in (PlayerState.RUNNING, PlayerState.IDLE)
            ):
                self.state = PlayerState.SPRINTING
        else:
            self.sprint_timer = 0
            if self.state == PlayerState.SPRINTING:
                self.state = PlayerState.RUNNING

        # Atualiza estado de movimento
        if self.on_ground:
            if abs(self.vx) > 0.5:
                if self.state == PlayerState.IDLE:
                    self.state = PlayerState.RUNNING
            else:
                if self.state in (PlayerState.RUNNING, PlayerState.SPRINTING):
                    self.state = PlayerState.IDLE

    def jump(self, long_jump: bool = False) -> None:
        """Executa pulo.

        Args:
            long_jump: Se True, pulo longo. Se False, pulo curto.
        """
        if self.on_ground and self.state not in (PlayerState.HURT, PlayerState.DEAD):
            self.vy = JUMP_FORCE if long_jump else JUMP_FORCE_SHORT
            self.state = PlayerState.JUMPING
            self.on_ground = False
            logger.debug("Player jumped: long=%s", long_jump)

    def spin_attack(self) -> None:
        """Ativa spin attack no ar."""
        if (
            not self.on_ground
            and self.state != PlayerState.SPIN_ATTACK
            and self.state not in (PlayerState.HURT, PlayerState.DEAD)
        ):
            self.state = PlayerState.SPIN_ATTACK
            logger.debug("Player spin attack activated")

    def take_damage(self) -> None:
        """Processa dano recebido."""
        if (
            self.invincibility_timer > 0
            or self.state == PlayerState.DEAD
            or self.state == PlayerState.HURT
        ):
            return

        if self.rings > 0:
            logger.info("Player lost %d rings", self.rings)
            self.rings = 0
            self.state = PlayerState.INVINCIBLE
            self.invincibility_timer = INVINCIBILITY_FRAMES
        else:
            self.lives -= 1
            logger.info("Player lost 1 life. Lives remaining: %d", self.lives)
            if self.lives <= 0:
                self.state = PlayerState.DEAD
                logger.info("Player died")
            else:
                self.state = PlayerState.HURT
                self.respawn()

    def collect_ring(self) -> None:
        """Coleta um anel."""
        self.rings += 1
        logger.debug("Ring collected. Total: %d", self.rings)

    def set_checkpoint(self, x: float, y: float) -> None:
        """Define novo checkpoint de respawn.

        Args:
            x: Posição X do checkpoint.
            y: Posição Y do checkpoint.
        """
        self.last_checkpoint_x = x
        self.last_checkpoint_y = y
        logger.info("Checkpoint set at (%.1f, %.1f)", x, y)

    def respawn(self) -> None:
        """Reaparece no último checkpoint."""
        self.x = self.last_checkpoint_x
        self.y = self.last_checkpoint_y
        self.vx = 0.0
        self.vy = 0.0
        self.invincibility_timer = INVINCIBILITY_FRAMES
        self.state = PlayerState.INVINCIBLE
        logger.info("Player respawned at checkpoint")

    @property
    def is_dead(self) -> bool:
        """Retorna True se o personagem está morto."""
        return self.state == PlayerState.DEAD

    def update(self, dt: int) -> None:
        """Atualiza estado do personagem.

        Args:
            dt: Delta time em milissegundos.
        """
        # Aplica fricção
        self.vx *= FRICTION

        # Zera velocidade muito pequena
        if abs(self.vx) < 0.1:
            self.vx = 0.0

        # Atualiza posição
        self.x += self.vx
        self.y += self.vy

        # Atualiza timer de invencibilidade
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
            if (
                self.invincibility_timer == 0
                and self.state == PlayerState.INVINCIBLE
            ):
                self.state = PlayerState.IDLE

        # Transição de estados
        if not self.on_ground and self.vy > 0 and self.state not in (
            PlayerState.HURT,
            PlayerState.DEAD,
            PlayerState.SPIN_ATTACK,
        ):
            self.state = PlayerState.FALLING

    def draw(self, surface: pygame.Surface, camera_x: float = 0.0) -> None:
        """Renderiza o personagem.

        Args:
            surface: Superfície do pygame onde renderizar.
            camera_x: Offset da câmera no eixo X.
        """
        rect = self.rect.copy()
        rect.x -= int(camera_x)

        # Cor baseada no estado
        if self.invincibility_timer > 0 and self.invincibility_timer % 10 < 5:
            return  # Efeito de piscar durante invencibilidade

        color = (
            COLOR_PLAYER_HURT
            if self.state == PlayerState.HURT
            else COLOR_PLAYER
        )

        pygame.draw.rect(surface, color, rect)

        # Indicador de direção
        indicator_x = rect.right if self.facing_right else rect.left - 5
        pygame.draw.circle(surface, (255, 255, 0), (indicator_x, rect.centery), 3)
