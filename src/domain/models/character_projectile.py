from pygame import Vector2

from models.direction import Direction
from models.projectile import Projectile


class CharacterProjectile:

    def __init__(self, projectile: Projectile, position: Vector2, direction: Direction):
        self.projectile = projectile
        self.position = position
        self.direction = direction
