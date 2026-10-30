from dataclasses import dataclass
from typing import cast


@dataclass
class Skill:
    id: int
    name: str
    weapon_type: int
    skill_type: str
    damage_multiplier: float
    fixed_damage: float
    cast_time: float
    cooldown: float
    script: dict

    script_index = 0
    character = None

    is_active = False

    def start_skill(self, character):
        self.is_active = True
        self.character = character
        print(self.script)

    def tick(self, delta_time: float):
        cur_func = list(self.script.keys())[self.script_index]
        getattr(self, cur_func)(self.script[cur_func], delta_time)

    @dataclass()
    class AnimateParams:
        anim: str
        overrides: dict

    def async_animate(self, val, delta_time):
        from models.character import Character

        params =  Skill.AnimateParams(**val)
        cast(Character, self.character).motion = Motion(params.anim)
        self.script_index += 1

    def delay(self, val, delta_time):
        pass

    def spawn_projectile(self):
        pass
