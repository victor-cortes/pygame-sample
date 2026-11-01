from pygame import Rect

from src.domain.models.character import Character
from src.domain.models.game_context import GameContext
from src.domain.service.sprite_service import SpriteDef, SpriteSet
from src.view.health_bar_view import HealthBarView
from src.view.view import View


class CharacterView(View):
    health_bar: HealthBarView
    animation_var: float = 0
    position: tuple[float, float]
    tile_position: Rect

    def __init__(self, character: Character, sprite_def: SpriteDef):
        super().__init__()
        self.character = character
        self.health_bar = HealthBarView(character)
        self.sprite_def = sprite_def

    def draw(self, ctx: GameContext) -> None:
        self.health_bar.draw(ctx)

        ctx.surface.blit(self.sprite_def.sprite,
                          self.position,
                          self.tile_position)

        # pygame.draw.rect(self.surface, (255, 0, 0), Rect(self.character.collision_box.x + self.character.position.x, self.character.collision_box.y + self.character.position.y, self.character.collision_box.w, self.character.collision_box.h), 2)
