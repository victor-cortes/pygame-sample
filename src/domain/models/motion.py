from enum import Enum


class Motion(Enum):
    IDLE = 'idle'
    MOVING = 'moving'
    ATTACKING_BOW = 'attacking_bow'
    DYING = 'dying'
    DEAD = 'dead'
