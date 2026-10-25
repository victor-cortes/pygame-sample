from pathlib import Path

import pygame
import yaml

from src.game.character import Character
from src.game.projectile import Projectile
from src.game.skill import Skill
from src.game.weapon import Weapon
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
    def load_character(cls, folder: Path, weapons: dict[int, Weapon]):
        chars = {}
        for file in folder.rglob("*.yaml"):
            with open(file) as stream:
                file = yaml.safe_load(stream)
                new_character = Character().__dict__ | file
                character = Character(**new_character)
                try:
                    character.weapon = weapons[new_character['weapon']]
                except KeyError:
                    character.weapon = None
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
    def load_weapons(cls, folder: Path, skills: dict[int, Skill]):
        weapons = {}
        for file in folder.rglob("weapons*.yaml"):
            with open(file) as stream:
                file = yaml.safe_load(stream)
                for key, value in file.items():
                    weapon = Weapon(**value)
                    weapon.skills = [skills[skill] for skill in value['skills']]
                    weapons[key] = weapon

        return weapons

    @classmethod
    def load_skills(cls, folder: Path, projectiles: dict[int, Projectile]):
        skills = {}
        for file in folder.rglob("skills*.yaml"):
            with open(file) as stream:
                file = yaml.safe_load(stream)
                for key, value in file.items():
                    skill = Skill(**value)
                    skill.projectile = projectiles[int(key)]
                    skills[key] = skill


        return skills

    @classmethod
    def load_projectiles(cls, folder: Path):
        projectiles = {}
        for file in folder.rglob("projectiles*.yaml"):
            with open(file) as stream:
                file = yaml.safe_load(stream)
                for key, value in file.items():
                    projectiles[key] = Projectile(**value)

        return projectiles

    @classmethod
    def load_resources(cls):
        sprites = ResourceLoader.load_sprites(Path("assets/sprites"))
        fonts = ResourceLoader.load_fonts(Path("assets/fonts"))
        character_defs = ResourceLoader.load_character_defs(Path("data/character_defs"), sprites)
        projectiles = ResourceLoader.load_projectiles(Path("data/skills"))
        skills = ResourceLoader.load_skills(Path("data/skills"), projectiles)
        weapons = ResourceLoader.load_weapons(Path("data/equipments"), skills)
        characters = ResourceLoader.load_character(Path("data/characters"), weapons)

        return fonts, character_defs, characters, sprites
