from dataclasses import dataclass, field

from src.game.skill import Skill


@dataclass
class Weapon:
    id: int
    type: str
    name: str
    required_level: int
    min_attack: int
    max_attack: int
    sprite: str
    skills: list[Skill] = field(default_factory=lambda: [])
