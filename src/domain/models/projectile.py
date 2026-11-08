from dataclasses import dataclass

import pygame

from models.direction import Direction


@dataclass
class ProjectileDirectionDef:
    sprite: str
    y: int
    start_x: int
    end_x: int
    width: int
    height: int
    speed: float
    spawn_x: int
    spawn_y: int
    collision_box: pygame.Rect


@dataclass
class Projectile:
    id: int
    dirs: dict[Direction, ProjectileDirectionDef]

    def __post_init__(self):
        if self.dirs:
            self.dirs = {
                key: ProjectileDirectionDef(**value) if isinstance(value, dict) else value
                for key, value in self.dirs.items()
            }
