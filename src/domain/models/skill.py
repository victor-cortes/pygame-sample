from dataclasses import dataclass


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