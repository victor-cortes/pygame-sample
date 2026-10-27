import pygame
from pygame.font import Font

from src.domain.models.character import Character
from src.domain.models.skill import Skill


class GameContext:
    player: Character = None
    character_defs: dict = {}
    characters: dict[int, Character] = {}
    skills: dict[int, Skill] = {}
    sprites: dict[str, pygame.Surface] = {}
    fonts: dict[str, Font] = {}
    running: bool = False
    delta_time: float = 0.0
    surface: pygame.Surface = None
    internal_surface: pygame.Surface = None