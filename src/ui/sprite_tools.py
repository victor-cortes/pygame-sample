from dataclasses import dataclass
from pathlib import Path

import pygame
import yaml


@dataclass
class SpriteSet:
    y: int
    x_offset: int
    y_offset: int
    width: int
    height: int
    start_x: int
    end_x: int
    speed: float
    repeat: bool
    dirs: list[str]

@dataclass
class SpriteSheet:
    name: str
    sheet: str
    sets: dict[str, SpriteSet]

    def __post_init__(self):
        if self.sets:
            self.sets = {
                key: SpriteSet(**value) if isinstance(value, dict) else value
                for key, value in self.sets.items()
            }


@dataclass()
class SpriteDef:
    sprite_sheet: SpriteSheet
    sprite: pygame.Surface

class SpriteTools:
    @staticmethod
    def load(path: Path, sprites: dict[str, pygame.Surface]) -> SpriteDef:
        with open(path) as stream:
            file = yaml.safe_load(stream)
            sprite_sheet: SpriteSheet = SpriteSheet(**(file['sprite_sheet']))
            return SpriteDef(
                sprite_sheet,
                sprites[sprite_sheet.sheet]
            )
