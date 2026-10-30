from models.game_context import GameContext
from src.view.character_view import CharacterView
from src.view.hud_view import HUDView
from src.view.view import View


class GameView(View):
    hud: HUDView = None
    character_views: list[CharacterView] = []

    def __init__(self):
        super().__init__()
        self.hud = HUDView()

    def draw(self, ctx: GameContext) -> None:
        self.hud.draw(ctx)
        for c in sorted(self.character_views, key=lambda p: p.character.position.y):
            c.draw(ctx)