from abc import ABC, abstractmethod

import pygame

from src.game.game_context import GameContext


class Object(ABC):
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.pos = (0, 0)

    @abstractmethod
    def draw(self, ctx: GameContext) -> None:
        pass
