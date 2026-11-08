from pygame import Vector2

from models.direction import Direction
from models.projectile import ProjectileDirectionDef
from models.skill import Skill


class CharacterProjectile:
    distance: float = 0

    def __init__(self, projectile: ProjectileDirectionDef, position: Vector2, direction: Direction, skill: Skill, param: dict):
        self.projectile = projectile
        self.position = position
        self.direction = direction
        self.skill = skill
        self.param = param
