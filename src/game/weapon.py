from dataclasses import dataclass


@dataclass
class Weapon:
    id: int
    type: str
    name: str
    required_level: int
    min_attack: int
    max_attack: int
