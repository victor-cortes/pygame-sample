from pygame import Surface, Rect, Vector2

from src.domain.models.game_context import GameContext
from src.controller.skill_controller import SkillController
from src.domain.core.sprite_tools import SpriteDef, SpriteSet
from src.domain.models.character import Character, Motion
from src.domain.models.skill import Skill
from src.view.health_bar_view import HealthBarView
from src.view.view import View


class CharacterView(View):
    health_bar: HealthBarView
    animation_var: float = 0
    cached_motion: Motion = Motion.IDLE

    def __init__(self, character: Character, sprite_def: SpriteDef):
        super().__init__()
        self.character = character
        self.health_bar = HealthBarView(character)
        self.sprite_def = sprite_def

    def move(self, vector: Vector2):
        self.character.move(vector)

    def stop(self):
        self.character.stop()

    def use_skill(self, skill: Skill):
        self.character.use_skill(skill)
        SkillController.use_skill(self.character, skill)

    def draw(self, ctx: GameContext) -> None:
        self.health_bar.draw(ctx)

        if self.character.motion != self.cached_motion:
            self.animation_var = 0
            self.cached_motion = self.character.motion

        motion: SpriteSet = self.sprite_def.sprite_sheet.sets[self.character.motion.value]
        self.animation_var += ctx.delta_time * (motion.speed if self.character.motion != Motion.ATTACKING_BOW else motion.speed * self.character.attack_speed)
        try:
            dir_index = motion.dirs.index(self.character.direction.value)
        except ValueError:
            dir_index = 0
        end = motion.end_x

        if motion.repeat:
            index = round(self.animation_var) % end if end != 0 else 0
        else:
            index = min(round(self.animation_var) if end != 0 else 0, motion.end_x)

        ctx.surface.blit(self.sprite_def.sprite,
                          (self.character.position.x - motion.x_offset, self.character.position.y - motion.y_offset),
                          Rect((motion.start_x + index) * motion.width, motion.y + dir_index * motion.height,
                               motion.width, motion.height))

        # pygame.draw.rect(self.surface, (255, 0, 0), Rect(self.character.collision_box.x + self.character.position.x, self.character.collision_box.y + self.character.position.y, self.character.collision_box.w, self.character.collision_box.h), 2)
        self.character.tick(ctx.delta_time)
