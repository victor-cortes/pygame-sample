from pygame import Rect
from pygame.math import Vector2

from models.character import Character
from models.game_context import GameContext
from models.motion import Motion
from models.skill import Skill
from service.sprite_service import SpriteDef, SpriteSet
from src.view.character_view import CharacterView


class CharacterController:
    character: Character
    character_view: CharacterView
    cached_motion: Motion = Motion.IDLE
    motion: Motion = Motion.IDLE
    animation_var: float = 0

    def __init__(self, character: Character, sprite_def: SpriteDef) -> None:
        self.character = character
        self.sprite_def = sprite_def
        self.character_view = CharacterView(character, sprite_def)
        self.character.on['die'].add_listener(lambda x: self.on_die())

    def render(self, ctx: GameContext):
        if self.motion != self.cached_motion:
            self.animation_var = 0
            self.cached_motion = self.motion

        sprite_set: SpriteSet = self.sprite_def.sprite_sheet.sets[self.motion.value]
        self.animation_var += ctx.delta_time * (
            sprite_set.speed if self.motion != Motion.ATTACKING_BOW else sprite_set.speed * self.character.attack_speed)
        try:
            dir_index = sprite_set.dirs.index(self.character.direction.value)
        except ValueError:
            dir_index = 0
        end = sprite_set.end_x

        if sprite_set.repeat:
            index = round(self.animation_var) % end if end != 0 else 0
        else:
            index = min(round(self.animation_var) if end != 0 else 0, sprite_set.end_x)

        self.character_view.position = (self.character.position.x - sprite_set.x_offset, self.character.position.y - sprite_set.y_offset)
        self.character_view.tile_position = Rect((sprite_set.start_x + index) * sprite_set.width, sprite_set.y + dir_index * sprite_set.height,
             sprite_set.width, sprite_set.height)
        self.character_view.draw(ctx)
        self.character.tick(ctx.delta_time)


    def use_skill(self, skill: Skill):
        self.character.use_skill(skill)

    def stop(self):
        if self.character.stop():
            self.motion = Motion.IDLE

    def move(self, vector: Vector2):
        if not self.character.is_dead() and not self.character.is_using_skill() and self.character.move(vector):
            self.motion = Motion.MOVING

    def take_damage(self, damage: int):
        self.character.take_damage(damage)

    def on_die(self):
        self.motion = Motion.DYING
