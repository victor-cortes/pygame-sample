import random

from models.game_context import GameContext
from src.controller.character_controller import CharacterController
from src.view.hud_view import HUDView
from src.view.view import View


class GameView(View):
    hud: HUDView = None
    character_controllers: dict[int, CharacterController]

    def __init__(self):
        super().__init__()
        self.hud = HUDView()

        self.a_max = 5

        randoms = [random.random() for i in range(self.a_max)]
        results = []
        cursor = 0
        for i in randoms:
            cursor = (1 - cursor) * i + cursor
            results.append(cursor)

        self.a = results
        print(results)

    clock = 0
    index = 0

    def draw(self, ctx: GameContext) -> None:
        self.hud.draw(ctx)
        self.clock += ctx.delta_time

        for c in sorted(self.character_controllers.values(), key=lambda controller: controller.character.position.y):
            c.render(ctx)

        if self.index < len(self.a) and self.clock > self.a[self.index]:
            self.index += 1
            ctx.player.take_damage(50)

        if self.clock > self.a_max:
            self.clock = 0
            self.index = 0

        # for c in sorted(self.character_views, key=lambda p: p.character.position.y):
        #     c.draw(ctx)
