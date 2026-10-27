import pygame
from pygame.constants import K_0

from src.domain.models.game_context import GameContext
from src.view.view import View


class HUDView(View):
    def draw(self, ctx: GameContext) -> None:
        for i, idx in enumerate(ctx.player.weapon.skills):
            shortcut = ctx.fonts['hud'].render(f"{i + 1}", False, (50, 50, 255) if pygame.key.get_pressed()[K_0 + i + 1] else (255, 255, 255))
            pygame.draw.rect(self.surface, (50, 50, 255) if pygame.key.get_pressed()[K_0 + i + 1] else (255, 255, 255), (16 + 40 * i, self.surface.get_height() - 48, 32, 32), 1, 4)
            self.surface.blit(shortcut, (20 + 40 * i, self.surface.get_height() - 44))
