from dataclasses import dataclass

from src.game.projectile import Projectile


@dataclass
class Skill:
    id: int
    name: str
    weapon_type: int
    attack_type: int
    damage_multiplier: float
    fixed_damage: float
    projectile: Projectile | None = None
    slash: None = None
