from models.game_context import GameContext
from src.view.view import View


class GameView(View):
    def __init__(self):
        super().__init__()

    def draw(self, ctx: GameContext) -> None:
        pass
