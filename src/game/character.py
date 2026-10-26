from dataclasses import dataclass, field
from enum import Enum

from pygame import Rect
from pygame.math import Vector2

from src.game.direction import Direction
from src.game.weapon import Weapon

DEFAULT_MOVE_PIXELS = 64

class Motion(Enum):
    IDLE = 'idle'
    MOVING = 'moving'
    ATTACKING_BOW = 'attacking_bow'
    DYING = 'dying'
    DEAD = 'dead'


@dataclass
class Character:
    id: int = 0
    name: str = ""
    sprite_sheet: str = ""

    level: int = 0
    knowledge: int = 0
    vitality: int = 0
    strength: int = 0
    dextery: int = 0
    armor: int = 0
    weapon: Weapon | None = None
    hp: int = 0

    move_speed: int = 1.3
    attack_speed: int = 1.3

    max_hp: int = 0
    attack_multiplier = 1
    min_attack: int = 0
    max_attack: int = 0
    defense: int = 0
    damage_reduction: float = 0.0
    crit_strike: float = 0.0

    direction: Direction = Direction.DOWN
    motion: Motion = Motion.IDLE

    position: Vector2 = field(default_factory=Vector2)
    move_vec: Vector2 = field(default_factory=Vector2)

    collision_box: Rect = field(default_factory=lambda x=16, y=12, w=30, h=40: Rect(x, y, w, h))
    attack_timer: float = 0

    def __post_init__(self):
        if isinstance(self.position, dict):
            self.position = Vector2(**self.position)

        elif isinstance(self.position, (list, tuple)):
            self.position = Vector2(*self.position)

        if isinstance(self.collision_box, dict):
            self.collision_box = Rect(self.collision_box['x'], self.collision_box['y'], self.collision_box['w'],
                                      self.collision_box['h'])

        elif isinstance(self.collision_box, (list, tuple)):
            self.collision_box = Rect(*self.collision_box)

    def set_move(self, direction: Direction):
        self.direction = direction
        self.motion = Motion.MOVING

    def calculate_status(self):
        self.max_hp = self.vitality * 10 + self.level * 100
        self.hp = self.max_hp
        self.attack_multiplier = 1 + self.strength * 0.005 + self.dextery * 0.015
        self.min_attack = round(self.weapon.min_attack * self.attack_multiplier if self.weapon is not None else 0)
        self.max_attack = round(self.weapon.max_attack * self.attack_multiplier if self.weapon is not None else 0)
        self.defense = self.armor
        self.damage_reduction = self.defense / (self.defense + 100.0)
        self.crit_strike = 0.01 + self.dextery * 0.003

    def get_used_points(self):
        return self.knowledge + self.strength + self.dextery + self.vitality

    def get_available_points(self):
        return self.level * 10 - self.get_used_points()

    def is_dead(self):
        return self.hp == 0

    def heal(self, ammount: int):
        if not self.is_dead():
            self.hp = min(self.max_hp, self.hp + ammount)

    def take_damage(self, ammount: int):
        if not self.is_dead():
            dmg = round(ammount * (1 - self.damage_reduction))
            self.hp = max(0, self.hp - dmg)

            if self.hp <= 0:
                self.motion = Motion.DYING
            return dmg
        return 0

    def move(self, vector: Vector2) -> Motion:
        if self.motion == Motion.DYING or self.motion == Motion.ATTACKING_BOW or self.is_dead():
            return self.motion

        if abs(vector.x) > abs(vector.y):
            if vector.x > 0:
                self.direction = Direction.RIGHT
            else:
                self.direction = Direction.LEFT
        elif vector.x != 0 or vector.y != 0:
            if vector.y > 0:
                self.direction = Direction.DOWN
            else:
                self.direction = Direction.UP
        self.move_vec = vector
        self.motion = Motion.MOVING
        return self.motion

    def stop(self) -> Motion:
        if self.motion == Motion.MOVING:
            self.motion = Motion.IDLE
            self.move_vec = Vector2(0, 0)
        return self.motion

    def make_attack(self) -> Motion:
        return self.motion

    def tick(self, dt: float):
        match self.motion:
            case Motion.MOVING:
                if not self.is_dead():
                    self.position += self.move_vec * self.move_speed * dt * DEFAULT_MOVE_PIXELS
            case Motion.ATTACKING_BOW:
                if not self.is_dead():
                    self.attack_timer += dt
                    if self.attack_timer > 1 / self.attack_speed:
                        self.motion = Motion.IDLE
                        self.attack_timer = 0

    def use_skill(self, skill):
        if self.weapon and skill in self.weapon.skills:
            pass
