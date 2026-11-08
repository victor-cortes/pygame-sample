import pygame
from pygame import Rect, Surface

from src.domain.models.character import Character
from src.domain.models.game_context import GameContext
from src.domain.service.sprite_service import SpriteSet
from src.view.health_bar_view import HealthBarView
from src.view.view import View


class CharacterView(View):
    health_bar: HealthBarView
    animation_var: float = 0
    position: tuple[float, float]
    tile_position: Rect
    sprite_set: SpriteSet
    sprite: Surface

    def __init__(self, character: Character):
        super().__init__()
        self.character = character
        self.health_bar = HealthBarView(character)

    def draw(self, ctx: GameContext) -> None:
        self.health_bar.draw(ctx)

        ctx.surface.blit(
            self.sprite,
            self.position,
            self.tile_position
        )
        char_collision = Rect(
            self.character.collision_box.x + self.character.position.x,
            self.character.collision_box.y + self.character.position.y,
            self.character.collision_box.w,
            self.character.collision_box.h
        )

        pygame.draw.rect(
            ctx.surface,
            (255, 0, 0),
            char_collision
            , 1
        )

        for projectile in self.character.character_projectiles:
            ctx.surface.blit(
                projectile.projectile.sprite,
                projectile.position, (
                    projectile.projectile.start_x * projectile.projectile.width,
                    projectile.projectile.y, projectile.projectile.width, projectile.projectile.height)
            )

            rect = Rect(
                projectile.projectile.collision_box['x'] + projectile.position.x,
                projectile.projectile.collision_box['y'] + projectile.position.y,
                projectile.projectile.collision_box['w'],
                projectile.projectile.collision_box['h']
            )
            pygame.draw.rect(
                ctx.surface,
                (255, 0, 0),
                rect
                , 1
            )
