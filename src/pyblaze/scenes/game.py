"""Cena principal do jogo com fase completa."""

import logging

import pygame

from pyblaze.entities.checkpoint import Checkpoint
from pyblaze.entities.enemy import Enemy
from pyblaze.entities.player import Player
from pyblaze.entities.ring import Ring
from pyblaze.scenes.base_scene import BaseScene
from pyblaze.settings import (
    COLOR_BG,
    COLOR_PLATFORM,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from pyblaze.systems.camera import Camera
from pyblaze.systems.hud import HUD
from pyblaze.systems.physics import PhysicsSystem

logger = logging.getLogger(__name__)


class GameScene(BaseScene):
    """Cena principal com gameplay completo."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Inicializa a cena do jogo.

        Args:
            screen: Superfície principal do pygame.
        """
        super().__init__(screen)

        # Sistemas
        self.physics = PhysicsSystem()
        self.camera = Camera(map_width=6000)
        self.hud = HUD()

        # Timer
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0.0

        # Jogador - spawn em cima da primeira plataforma (y=500, player_height=50, margin=5)
        self.player = Player(100, 445)

        # Fase hardcoded com 4 zonas
        self.platforms = self._create_platforms()
        self.rings = self._create_rings()
        self.enemies = self._create_enemies()
        self.checkpoints = self._create_checkpoints()
        # Goal em cima da última plataforma (5450, 360, 500, 40)
        # Goal: largura=80, altura=120, posicionado em cima da plataforma
        # Goal.bottom deve estar em platform.top = 360
        # Então goal.y = 360 - 120 = 240
        self.goal_rect = pygame.Rect(5800, 240, 80, 120)

        # Estado
        self.game_over = False
        self.victory = False
        self.victory_time = 0.0

        # Input
        self.jump_pressed = False

        logger.info("GameScene initialized with full level")

    def _create_platforms(self) -> list[pygame.Rect]:
        """Cria plataformas da fase."""
        platforms = []

        # Zona 1: Plataformas baixas (início)
        platforms.append(pygame.Rect(0, 500, 800, 40))
        platforms.append(pygame.Rect(900, 480, 300, 40))
        platforms.append(pygame.Rect(1250, 460, 250, 40))

        # Zona 2: Rampa de aceleração e corredor
        for i in range(10):
            platforms.append(pygame.Rect(1550 + i * 60, 440 - i * 10, 60, 40))
        platforms.append(pygame.Rect(2200, 330, 1200, 40))

        # Zona 3: Plataformas aéreas (com abismo)
        platforms.append(pygame.Rect(3500, 450, 200, 40))
        platforms.append(pygame.Rect(3800, 380, 150, 40))
        platforms.append(pygame.Rect(4050, 320, 150, 40))
        platforms.append(pygame.Rect(4300, 380, 150, 40))
        platforms.append(pygame.Rect(4550, 450, 200, 40))

        # Zona 4: Sprint final
        platforms.append(pygame.Rect(4800, 470, 300, 40))
        for i in range(5):
            platforms.append(pygame.Rect(5150 + i * 50, 450 - i * 15, 50, 40))
        platforms.append(pygame.Rect(5450, 360, 500, 40))

        logger.debug("Created %d platforms", len(platforms))
        return platforms

    def _create_rings(self) -> list[Ring]:
        """Cria anéis distribuídos pela fase."""
        rings = []

        # Zona 1: 5 anéis
        for i in range(5):
            rings.append(Ring(200 + i * 100, 440))

        # Zona 2: 10 anéis no corredor
        for i in range(10):
            rings.append(Ring(2300 + i * 100, 260))

        # Zona 3: 8 anéis nas plataformas aéreas
        rings.append(Ring(3550, 380))
        rings.append(Ring(3850, 310))
        rings.append(Ring(4100, 250))
        rings.append(Ring(4350, 310))
        rings.append(Ring(4600, 380))
        rings.append(Ring(3900, 250))
        rings.append(Ring(4200, 200))
        rings.append(Ring(4400, 250))

        # Zona 4: 5 anéis finais
        for i in range(5):
            rings.append(Ring(5200 + i * 80, 390 - i * 15))

        logger.debug("Created %d rings", len(rings))
        return rings

    def _create_enemies(self) -> list[Enemy]:
        """Cria inimigos patrulheiros."""
        enemies = []

        # Zona 1: 1 inimigo
        enemies.append(Enemy(1000, 430, patrol_range=120))

        # Zona 2: 2 inimigos no corredor
        enemies.append(Enemy(2500, 280, patrol_range=200))
        enemies.append(Enemy(3000, 280, patrol_range=150))

        # Zona 3: 1 inimigo nas plataformas
        enemies.append(Enemy(4100, 270, patrol_range=100))

        # Zona 4: 2 inimigos finais
        enemies.append(Enemy(4900, 420, patrol_range=120))
        enemies.append(Enemy(5500, 310, patrol_range=150))

        logger.debug("Created %d enemies", len(enemies))
        return enemies

    def _create_checkpoints(self) -> list[Checkpoint]:
        """Cria checkpoints com spawn points corretos."""
        checkpoints = []

        # Checkpoint 0 - Início (automático)
        # Plataforma: Rect(0, 500, 800, 40) => top=500
        # Player height=50, então spawn y = 500-50-5 = 445 (margem de segurança)
        checkpoints.append(Checkpoint(50, 420))
        checkpoints[0].activate()
        checkpoints[0].spawn_x = 100.0
        checkpoints[0].spawn_y = 445.0
        self.player.set_checkpoint(100, 445)

        # Checkpoint 1 - Após rampa
        # Plataforma: Rect(2200, 330, 1200, 40) => top=330
        # Spawn y = 330-50-5 = 275
        checkpoints.append(Checkpoint(2150, 250))
        checkpoints[1].spawn_x = 2250.0
        checkpoints[1].spawn_y = 275.0

        # Checkpoint 2 - Após plataformas aéreas
        # Plataforma: Rect(4550, 450, 200, 40) => top=450
        # Spawn y = 450-50-5 = 395
        checkpoints.append(Checkpoint(4500, 370))
        checkpoints[2].spawn_x = 4600.0
        checkpoints[2].spawn_y = 395.0

        # Checkpoint 3 - Antes da meta
        # Plataforma: Rect(5450, 360, 500, 40) => top=360
        # Spawn y = 360-50-5 = 305
        checkpoints.append(Checkpoint(5400, 280))
        checkpoints[3].spawn_x = 5500.0
        checkpoints[3].spawn_y = 305.0

        logger.debug("Created %d checkpoints", len(checkpoints))
        return checkpoints

    def handle_event(self, event: pygame.event.Event) -> None:
        """Processa eventos.

        Args:
            event: Evento do pygame.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.game_over or self.victory:
                    self._restart_game()
                else:
                    self.jump_pressed = True
            elif event.key == pygame.K_LSHIFT:
                self.player.spin_attack()
            elif event.key == pygame.K_ESCAPE:
                from pyblaze.scenes.menu import MenuScene

                self.switch_to(MenuScene(self.screen))

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.jump_pressed = False

    def update(self, dt: int) -> None:
        """Atualiza o jogo.

        Args:
            dt: Delta time em milissegundos.
        """
        if self.game_over or self.victory:
            return

        # Atualiza timer
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0

        # Input do jogador
        keys = pygame.key.get_pressed()
        self.player.move(keys)

        if self.jump_pressed:
            self.player.jump(long_jump=True)
        elif keys[pygame.K_SPACE]:
            pass  # Já processado no handle_event

        # Física (desabilita gravidade durante cooldown de respawn)
        if self.player.respawn_cooldown == 0:
            self.physics.apply_gravity(self.player)
        self.player.update(dt)
        self.physics.resolve_collision(self.player, self.platforms)

        # Verifica morte por queda (apenas se não estiver em cooldown de respawn)
        if self.player.y > SCREEN_HEIGHT + 100 and self.player.respawn_cooldown == 0:
            logger.warning("Player fell off the map")
            self.player.take_damage()
            if self.player.is_dead:
                self.game_over = True
                self.victory_time = self.elapsed_time

        # Atualiza inimigos
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(dt)

                # Colisão com inimigo
                if self.physics.check_collision(self.player.rect, enemy.rect):
                    if self.physics.check_collision_from_above(self.player, enemy):
                        enemy.die()
                        self.player.vy = -8
                        logger.info("Enemy destroyed by player")
                    else:
                        self.player.take_damage()
                        if self.player.is_dead:
                            self.game_over = True
                            self.victory_time = self.elapsed_time

        # Atualiza e coleta anéis
        for ring in self.rings:
            if not ring.collected:
                ring.update(dt)
                if self.physics.check_collision(self.player.rect, ring.rect):
                    ring.collect()
                    self.player.collect_ring()

        # Atualiza checkpoints
        for checkpoint in self.checkpoints:
            if not checkpoint.activated and self.physics.check_collision(
                self.player.rect, checkpoint.rect
            ):
                checkpoint.activate()
                self.player.set_checkpoint(checkpoint.spawn_x, checkpoint.spawn_y)

        # Verifica vitória
        if self.physics.check_collision(self.player.rect, self.goal_rect):
            self.victory = True
            self.victory_time = self.elapsed_time
            logger.info("Player reached goal! Time: %.2fs", self.victory_time)

        # Câmera
        self.camera.follow(self.player.x)

    def draw(self) -> None:
        """Renderiza o jogo."""
        self.screen.fill(COLOR_BG)

        # Plataformas
        for platform in self.platforms:
            rect = self.camera.apply(platform)
            pygame.draw.rect(self.screen, COLOR_PLATFORM, rect)
            pygame.draw.rect(self.screen, (80, 50, 20), rect, 2)

        # Meta
        goal_rect = self.camera.apply(self.goal_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), goal_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), goal_rect, 3)

        # Checkpoints
        for checkpoint in self.checkpoints:
            checkpoint.draw(self.screen, self.camera.x)

        # Anéis
        for ring in self.rings:
            ring.draw(self.screen, self.camera.x)

        # Inimigos
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera.x)

        # Jogador
        self.player.draw(self.screen, self.camera.x)

        # HUD
        self.hud.render(
            self.screen, self.player.rings, self.player.lives, self.elapsed_time
        )

        # Game Over / Victory
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            self.hud.render_game_over(self.screen, False, self.victory_time)

        if self.victory:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 50, 0))
            self.screen.blit(overlay, (0, 0))
            self.hud.render_game_over(self.screen, True, self.victory_time)

    def _restart_game(self) -> None:
        """Reinicia o jogo."""
        from pyblaze.scenes.game import GameScene

        self.switch_to(GameScene(self.screen))
        logger.info("Game restarted")
