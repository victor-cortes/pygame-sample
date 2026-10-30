import pygame
from pygame import Rect

from src.domain.models.game_context import GameContext
from src.domain.models.character import Character
from src.view.view import View

HP_BAR_WIDTH = 50
HP_BAR_HEIGHT = 7


class HealthBarView(View):
    cached_hp: float
    stored_hp = None
    timer = 0
    damages = []

    def __init__(self, character: Character):
        super().__init__()
        self.character = character
        self.cached_hp = character.hp

    def draw(self, ctx: GameContext) -> None:
        bar_rect: Rect = pygame.Rect((32 - HP_BAR_WIDTH / 2, -8) + self.character.position,
                                     (HP_BAR_WIDTH, HP_BAR_HEIGHT))
        pygame.draw.rect(ctx.surface, (175, 160, 160), bar_rect)
        pygame.draw.rect(ctx.surface, (200, 50, 50),
                         (bar_rect.topleft, (HP_BAR_WIDTH * self.cached_hp / self.character.max_hp, HP_BAR_HEIGHT)))
        pygame.draw.rect(ctx.surface, (50, 50, 200), (bar_rect.topleft, (HP_BAR_WIDTH * self.character.hp / self.character.max_hp, HP_BAR_HEIGHT)))
        pygame.draw.rect(ctx.surface, (100, 100, 200),
                         ((bar_rect.x, bar_rect.y + 1), (HP_BAR_WIDTH * self.character.hp / self.character.max_hp, 2)))

        if self.character.hp < self.cached_hp:
            if self.stored_hp is None:
                self.stored_hp = self.character.hp

            if self.stored_hp == self.character.hp:
                self.timer += ctx.delta_time
            else:
                self.timer = 0
                self.stored_hp = self.character.hp

            if self.timer >= 0.45:
                self.cached_hp -= ctx.delta_time * 1600
        else:
            self.cached_hp = self.character.hp
            self.stored_hp = None
            self.timer = 0

        pygame.draw.rect(ctx.surface, (250, 250, 250), bar_rect, 1)

        # print(bar_rect)
        # level_surface: pygame.Surface = ctx.fonts['font_level'].render(f"{self.character.level}", True, (255, 255, 255))
        # pygame.draw.circle(self.surface, (0, 0, 255) if not self.character.is_dead() else (100, 100, 100),
        #                    self.character.position + (6, -4), 8)
        # centered = Rect(self.character.position + (-1, -11), (14, 14))
        # self.surface.blit(level_surface, (centered.x + centered.w / 2 - level_surface.get_width() / 2, centered.y + centered.h / 2 - level_surface.get_height() / 2))
        # pygame.draw.rect(self.surface, (255, 0, 0) if not self.character.is_dead() else (100, 100, 100),
        #                  ((self.character.position) + (12, -6), (50, 6)), 3)
        # pygame.draw.rect(self.surface, (0, 0, 255), ((self.character.position) + (12, -6),
        #                                              (50 * self.character.hp / self.character.max_hp, 6)), 3)

    def spawn_damage(self, dmg):
        print(dmg)
        pass
