from pathlib import Path

import pygame
import yaml

from src.game.character import Character
from src.ui.sprite_tools import SpriteTools


class ResourceLoader:
    @classmethod
    def load_character_defs(cls, folder: Path, sprites: dict[str, pygame.Surface]):
        resources = {}
        for file in folder.rglob("*.yaml"):
            sprite = SpriteTools.load(file, sprites)
            resources[f"{sprite.sprite_sheet.name}"] = sprite

        return resources

    @classmethod
    def load_character(cls, folder: Path):
        chars = {}
        for file in folder.rglob("*.yaml"):
            with open(file) as stream:
                file = yaml.safe_load(stream)
                character = Character()
                character_from_file = Character(**file)
                for key, value in character_from_file.__dict__.items():
                    character.__setattr__(key, value)
                character.calculate_status()
                chars[character.id] = character

        return chars

    @classmethod
    def load_fonts(cls, folder: Path):
        return {'font_level': pygame.font.Font(f"{folder}/numerals.ttf", 12)}

    @classmethod
    def load_sprites(cls, folder: Path):
        sprites = {}
        for file in folder.rglob("*.png"):
            with open(file) as stream:
                sprite = pygame.image.load(stream).convert_alpha()
                sprites[file.name] = sprite
        return sprites


    @classmethod
    def load_resources(cls):
        sprites = ResourceLoader.load_sprites(Path("assets/sprites"))
        fonts = ResourceLoader.load_fonts(Path("assets/fonts"))
        character_defs = ResourceLoader.load_character_defs(Path("assets/sprite_sheets"), sprites)
        characters = ResourceLoader.load_character(Path("assets/characters"))
        return fonts, character_defs, characters, sprites
