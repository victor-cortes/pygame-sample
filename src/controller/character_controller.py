from pygame import Rect
from pygame.math import Vector2

from models.character import Character
from models.character_skill import CharacterSkill
from models.character_state import CharacterState
from models.game_context import GameContext
from models.motion import Motion
from models.skill import Skill
from service.sprite_service import SpriteDef
from src.controller.skill_controller import SkillController
from src.view.character_view import CharacterView


class CharacterController:
    character: Character
    character_view: CharacterView
    cached_motion: str = Motion.IDLE.value
    motion: str = Motion.IDLE.value
    skill_motion: str = None
    animation_var: float = 0
    skill_controller: SkillController = None

    def __init__(self, character: Character, sprite_def: SpriteDef) -> None:
        self.character = character
        self.sprite_def = sprite_def
        self.character_view = CharacterView(character)
        self.character.on['die'].add_listener(lambda x: self.on_die())
        self.character.on['skill_started'].add_listener(lambda x: self.on_skill_stated(x))
        self.character.on['skill_ended'].add_listener(lambda x: self.on_skill_stated(x))

    def render(self, ctx: GameContext):
        sprite_set = self.sprite_def.sprite_sheet.sets[self.motion]

        self.animation_var += ctx.delta_time * sprite_set.speed
        end = sprite_set.end_x

        try:
            direction_index = sprite_set.dirs.index(self.character.direction.value)
        except ValueError:
            direction_index = 0

        if sprite_set.repeat:
            index = round(self.animation_var) % end if end != 0 else 0
        else:
            index = min(round(self.animation_var) if end != 0 else 0, sprite_set.end_x)

        if self.character.state == CharacterState.USING_SKILL and self.skill_controller is not None:
            self.skill_controller.render(ctx)

        self.character_view.sprite = self.sprite_def.sprite

        self.character_view.position = (self.character.position.x - sprite_set.x_offset,
                                        self.character.position.y - sprite_set.y_offset)
        self.character_view.tile_position = Rect((sprite_set.start_x + index) * sprite_set.width,
                                                 sprite_set.y + direction_index * sprite_set.height,
                                                 sprite_set.width, sprite_set.height)
        self.character_view.draw(ctx)

        # if self.motion != self.cached_motion:
        #     self.animation_var = 0
        #     self.cached_motion = self.motion
        #
        # sprite_set: SpriteSet = self.sprite_def.sprite_sheet.sets[self.motion.value]
        # self.animation_var += ctx.delta_time * (
        #     sprite_set.speed if self.motion != Motion.ATTACKING_BOW else sprite_set.speed * self.character.attack_speed)
        # try:
        #     dir_index = sprite_set.dirs.index(self.character.direction.value)
        # except ValueError:
        #     dir_index = 0
        # end = sprite_set.end_x
        #
        # if sprite_set.repeat:
        #     index = round(self.animation_var) % end if end != 0 else 0
        # else:
        #     index = min(round(self.animation_var) if end != 0 else 0, sprite_set.end_x)
        #
        # self.character_view.position = (self.character.position.x - sprite_set.x_offset,
        #                                 self.character.position.y - sprite_set.y_offset)
        # self.character_view.tile_position = Rect((sprite_set.start_x + index) * sprite_set.width,
        #                                          sprite_set.y + dir_index * sprite_set.height,
        #                                          sprite_set.width, sprite_set.height)
        # self.character_view.draw(ctx)

    def use_skill(self, skill: Skill):
        self.character.use_skill(skill)

    def stop(self):
        if self.character.stop():
            self.set_motion(Motion.IDLE.value)

    def set_motion(self, new_motion: str):
        if new_motion != self.cached_motion:
            self.motion = new_motion
            self.cached_motion = new_motion
            self.animation_var = 0

    def move(self, vector: Vector2):
        if (not self.character.is_dead()
                and not self.character.is_using_skill()
                and self.character.move(vector)):
            self.set_motion(Motion.MOVING.value)

    def take_damage(self, damage: int):
        self.character.take_damage(damage)

    def on_die(self):
        self.set_motion(Motion.DYING.value)

    def on_skill_stated(self, skill: CharacterSkill):
        self.skill_controller = SkillController(skill, self)
