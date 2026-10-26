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
    cooldown: float = 0
    projectile: Projectile | None = None
    projectile_max_distance: float = 0
    slash: None = None
