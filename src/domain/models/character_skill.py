from types import SimpleNamespace
from typing import cast

from models.skill import Skill


class SkillProjectileWhenCollides:
    damage_multiplier: 1
    fixed_damage: 0


class SkillProjectile:
    projectile: int
    projectile_max_distance: float
    when_collides: dict


class CharacterSkill:
    script_line = 0
    skill_clock = 0
    delay_mode = False
    delay_clock = 0
    finished = False

    def __init__(self, character, skill: Skill):
        self.character = character
        self.skill = skill

    def tick(self, context):
        self.skill_clock += context.delta_time
        self.execute_script(context)

    def execute_script(self, context):
        try:
            function = list(self.skill.script.keys())[self.script_line]
            self.exec_function(function, self.skill.script[function], context)
        except IndexError:
            self.finish_skill()

    def exec_function(self, function, param, context):
        try:
            self.__getattribute__(function)(param, context)
        except AttributeError:
            pass

    def spawn_projectile(self, param, context):
        from models.game_context import GameContext
        item = SimpleNamespace(**param)
        projectile = cast(GameContext, context).projectiles[item.projectile]

        self.character.spawn_projectile(projectile)
        self.script_line += 1

    def delay(self, param, context):
        if not self.delay_mode:
            self.delay_mode = True

        self.delay_clock += context.delta_time
        if self.delay_clock >= param / 1000:
            self.delay_mode = False
            self.delay_clock = 0
            self.script_line += 1

    def finish_skill(self):
        self.finished = True
