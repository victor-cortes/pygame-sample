from models.character import Character
from models.game_context import GameContext


class CharacterController:
    character: Character

    def __init__(self, character: Character) -> None:
        self.character = character

    def tick(self, context: GameContext):
        self.character.tick(context)