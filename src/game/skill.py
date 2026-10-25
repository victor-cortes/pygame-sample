from dataclasses import dataclass

import pygame

from src.game.character import Direction


@dataclass
class ProjectileDirectionDef:
    sprite: str
    start_x: int
    end_x: int
    width: int
    height: int
    speed: float
    spawn_x: int
    spawn_y: int
    collision_box: pygame.Rect


@dataclass
class Skill:
    id: int
    name: str
    weapon_type: int
    attack_type: int
    damage_multiplier: float
    fixed_damage: float
    projectile: dict[Direction, ProjectileDirectionDef]

    def __post_init__(self):
        if self.projectile:
            self.projectile = {
                key: ProjectileDirectionDef(**value) if isinstance(value, dict) else value
                for key, value in self.projectile.items()
            }
