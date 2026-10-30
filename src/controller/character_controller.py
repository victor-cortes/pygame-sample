from pygame.math import Vector2

from models.character import Character
from models.game_context import GameContext
from models.skill import Skill
from service.sprite_service import SpriteDef
from src.view.character_view import CharacterView


class CharacterController:
    character: Character
    character_view: CharacterView

    def __init__(self, character: Character, sprite_def: SpriteDef) -> None:
        self.character = character
        self.character_view = CharacterView(character, sprite_def)

    def render(self, ctx: GameContext):
        self.character_view.draw(ctx)

    def use_skill(self, skill: Skill):
        self.character.use_skill(skill)

    def stop(self):
        self.character.stop()

    def move(self, vector: Vector2):
        self.character.move(vector)