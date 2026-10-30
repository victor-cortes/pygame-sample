from abc import ABC, abstractmethod

import pygame

from src.domain.models.game_context import GameContext


class View(ABC):
    def __init__(self):
        self.pos = (0, 0)

    @abstractmethod
    def draw(self, ctx: GameContext) -> None:
        pass
