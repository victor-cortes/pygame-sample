from dataclasses import dataclass, field

from pygame import Rect
from pygame.math import Vector2

from models.character_projectile import CharacterProjectile
from models.character_skill import CharacterSkill
from models.character_state import CharacterState
from models.projectile import Projectile, ProjectileDirectionDef
from models.skill import Skill
from service.event_dispatcher import EventDispatcher
from src.domain.models.direction import Direction
from src.domain.models.weapon import Weapon


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
    state: CharacterState = CharacterState.IDLE
    activated_skill: CharacterSkill | None = None
    character_projectiles: list[CharacterProjectile] = field(default_factory=lambda: [])

    position: Vector2 = field(default_factory=Vector2)
    move_vec: Vector2 = field(default_factory=Vector2)

    collision_box: Rect = field(default_factory=lambda x=16, y=12, w=30, h=40: Rect(x, y, w, h))

    on: dict[str, EventDispatcher] = field(default_factory=lambda: {
        'die': EventDispatcher(),
        'skill_started': EventDispatcher(),
        'skill_ended': EventDispatcher()
    })

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

    def heal(self, ammount: int):
        if not self.is_dead():
            self.hp = min(self.max_hp, self.hp + ammount)

    def take_damage(self, ammount: int):
        if not self.is_dead():
            dmg = round(ammount * (1 - self.damage_reduction))
            self.hp = max(0, self.hp - dmg)

            if self.hp <= 0:
                self.state = CharacterState.DEAD
                self.on['die'].trigger_event()
            return dmg
        return 0

    def move(self, vector: Vector2):
        if self.is_using_skill() or self.is_dead():
            return False

        self.state = CharacterState.MOVING

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
        return True

    def stop(self):
        if self.state == CharacterState.MOVING and not self.is_dead():
            self.state = CharacterState.IDLE
            self.move_vec = Vector2(0, 0)
            return True
        return False

    def is_using_skill(self):
        return (self.weapon
                and self.activated_skill is not None
                and not self.is_dead())

    def is_dead(self):
        return self.hp <= 0 or self.state == CharacterState.DEAD

    def use_skill(self, skill: Skill):
        if not self.is_using_skill() and self.weapon and skill in self.weapon.skills:
            self.state = CharacterState.USING_SKILL
            self.activated_skill = CharacterSkill(self, skill)
            self.on['skill_started'].trigger_event(self.activated_skill)

    def spawn_projectile(self, projectile: Projectile):
        dirdef: ProjectileDirectionDef = projectile.dirs[self.direction.value]
        vector = Vector2(self.position + (dirdef.spawn_x, dirdef.spawn_y))
        print(vector)
        self.character_projectiles.append(CharacterProjectile(projectile, vector, self.direction))

    def finish_skill(self):
        activated = self.activated_skill
        self.activated_skill.finished = False
        self.activated_skill = None
        self.state = CharacterState.IDLE
        self.on['skill_ended'].trigger_event(activated)
