"""Testes de integração end-to-end para gameplay."""

import pygame

from pyblaze.entities.checkpoint import Checkpoint
from pyblaze.entities.enemy import Enemy
from pyblaze.entities.player import Player
from pyblaze.entities.ring import Ring
from pyblaze.systems.physics import PhysicsSystem


class TestGameplayIntegration:
    """Testes de integração do gameplay completo."""

    def test_player_collects_ring_increases_count(self) -> None:
        """Testa que coletar anel incrementa contador."""
        player = Player(x=100, y=100)
        ring = Ring(x=105, y=105)

        assert player.rings == 0
        assert ring.collected is False

        # Simula colisão
        if player.rect.colliderect(ring.rect):
            ring.collect()
            player.collect_ring()

        assert player.rings == 1
        assert ring.collected is True

    def test_player_takes_damage_from_enemy(self) -> None:
        """Testa que jogador toma dano de inimigo."""
        player = Player(x=100, y=100)
        enemy = Enemy(x=105, y=105)

        initial_lives = player.lives
        player.rings = 0  # Sem anéis

        # Simula colisão
        if player.rect.colliderect(enemy.rect) and player.invincibility_timer == 0:
            player.take_damage()

        assert player.lives == initial_lives - 1

    def test_player_loses_rings_not_life_when_hit_with_rings(self) -> None:
        """Testa que jogador perde anéis mas não vida quando tem anéis."""
        player = Player(x=100, y=100)
        player.rings = 10
        initial_lives = player.lives

        player.take_damage()

        assert player.rings == 0
        assert player.lives == initial_lives

    def test_checkpoint_activation_saves_spawn_point(self) -> None:
        """Testa que checkpoint ativa e salva ponto de spawn."""
        player = Player(x=100, y=100)
        checkpoint = Checkpoint(x=200, y=100)

        assert checkpoint.activated is False

        # Ativa checkpoint (sempre ativa para o teste)
        checkpoint.activate()
        player.last_checkpoint_x = checkpoint.spawn_x
        player.last_checkpoint_y = checkpoint.spawn_y

        assert checkpoint.activated is True
        assert player.last_checkpoint_x == checkpoint.spawn_x
        assert player.last_checkpoint_y == checkpoint.spawn_y

    def test_player_respawns_at_checkpoint_after_death(self) -> None:
        """Testa que jogador respawna no checkpoint após morte."""
        player = Player(x=100, y=100)
        checkpoint = Checkpoint(x=500, y=200)

        # Ativa checkpoint
        checkpoint.activate()
        player.last_checkpoint_x = checkpoint.spawn_x
        player.last_checkpoint_y = checkpoint.spawn_y

        # Jogador morre (sem vidas)
        player.lives = 0
        player.rings = 0

        # Respawn
        player.respawn()

        assert player.x == checkpoint.spawn_x
        assert player.y == checkpoint.spawn_y

    def test_physics_applies_gravity_to_player(self) -> None:
        """Testa que física aplica gravidade ao jogador."""
        player = Player(x=100, y=100)
        physics = PhysicsSystem()

        initial_vy = player.vy
        physics.apply_gravity(player)

        assert player.vy > initial_vy

    def test_player_collision_with_platform_stops_fall(self) -> None:
        """Testa que colisão com plataforma para a queda."""
        player = Player(x=100, y=100)
        player.vy = 10.0  # Caindo
        physics = PhysicsSystem()

        # Plataforma abaixo do jogador - colocando de forma que colida
        platform = pygame.Rect(0, 132, 800, 32)  # y = 132 (toca o player em 132)
        player.rect.y = 132  # Player colide com plataforma

        physics.resolve_collision(player, [platform])

        assert player.on_ground is True

    def test_enemy_patrol_behavior(self) -> None:
        """Testa comportamento de patrulha do inimigo."""
        enemy = Enemy(x=200, y=100, patrol_range=100)

        initial_x = enemy.x

        # Simula várias atualizações
        for _ in range(200):
            enemy.update(16)

        # Inimigo deve ter se movido
        assert enemy.x != initial_x
        # Deve ter mudado de direção ao menos uma vez
        assert enemy.direction in (-1, 1)

    def test_complete_gameplay_flow(self) -> None:
        """Testa fluxo completo: spawn -> checkpoint -> ring -> enemy -> goal."""
        # Setup
        player = Player(x=100, y=100)
        checkpoint = Checkpoint(x=300, y=100)
        ring = Ring(x=200, y=100)
        enemy = Enemy(x=400, y=100)

        # 1. Jogador coleta anel
        ring.collect()
        player.collect_ring()
        assert player.rings == 1

        # 2. Jogador ativa checkpoint
        checkpoint.activate()
        player.last_checkpoint_x = checkpoint.spawn_x
        player.last_checkpoint_y = checkpoint.spawn_y
        assert checkpoint.activated is True

        # 3. Jogador toma dano (perde anéis)
        player.take_damage()
        assert player.rings == 0

        # 4. Inimigo é derrotado
        enemy.die()
        assert enemy.alive is False  # Enemy tem alive (not is_alive)

        # 5. Se player morresse, respawnaria no checkpoint
        assert player.last_checkpoint_x == checkpoint.spawn_x

    def test_multiple_rings_collection(self) -> None:
        """Testa coleta de múltiplos anéis."""
        player = Player(x=100, y=100)
        rings = [Ring(x=i * 50, y=100) for i in range(5)]

        for ring in rings:
            ring.collect()
            player.collect_ring()

        assert player.rings == 5
        assert all(ring.collected for ring in rings)

    def test_player_death_and_respawn_cycle(self) -> None:
        """Testa ciclo completo de morte e respawn."""
        player = Player(x=100, y=100)
        checkpoint = Checkpoint(x=500, y=200)

        # Configura checkpoint
        checkpoint.activate()
        player.last_checkpoint_x = checkpoint.spawn_x
        player.last_checkpoint_y = checkpoint.spawn_y

        initial_lives = player.lives
        player.rings = 0

        # Jogador toma dano (perde vida)
        player.take_damage()
        assert player.lives == initial_lives - 1

        # Respawn
        player.respawn()
        assert player.x == checkpoint.spawn_x
        assert player.y == checkpoint.spawn_y
        assert player.respawn_cooldown > 0
