import pygame
from pygame.font import Font

from src.game.character import Character


class GameContext:
    player_index: int = 1000
    character_defs: dict = {}
    characters: dict[int, Character] = {}
    sprites: dict[str, pygame.Surface] = {}
    fonts: dict[int, Font] = {}
    running: bool = False
    delta_time: float = 0.0
    surface: pygame.Surface = None
    internal_surface: pygame.Surface = None