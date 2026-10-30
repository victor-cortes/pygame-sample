import pygame
from pygame.constants import K_1
from pygame.event import Event
from pygame.math import Vector2
from pygame.time import Clock

from models import character
from src.controller.character_controller import CharacterController
from src.domain.models.game_context import GameContext
from src.domain.service.resource_service import ResourceService
from src.view.game_view import GameView

clock = Clock()
FPS = 60
INTERNAL_WIDTH = 600
INTERNAL_HEIGHT = 480
SCALE_FACTOR = 2

SCREEN_WIDTH = INTERNAL_WIDTH * SCALE_FACTOR
SCREEN_HEIGHT = INTERNAL_HEIGHT * SCALE_FACTOR

PLAYER = 1000

SKILL_KEYMAPS = {
    K_1: 1000
}


def get_move_vector() -> Vector2:
    pressed_keys = pygame.key.get_pressed()
    vec = Vector2(0, 0)

    if pressed_keys[pygame.K_d]:
        vec.x += 1
    if pressed_keys[pygame.K_a]:
        vec.x -= 1
    if pressed_keys[pygame.K_w]:
        vec.y -= 1
    if pressed_keys[pygame.K_s]:
        vec.y += 1

    if vec.length() == 0:
        return Vector2(0, 0)
    return vec.normalize()


def get_used_skill() -> int | None:
    for key in SKILL_KEYMAPS:
        if pygame.key.get_pressed()[key]:
            return SKILL_KEYMAPS[key]

    return None


class GameController:
    game_view = GameView()
    context: GameContext
    character_controllers: dict[int, CharacterController]

    def init(self):
        pygame.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), depth=32)
        pygame.display.set_caption("Game")
        internal_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)

        self.context = GameContext()
        self.context.outer_surface = pygame.display.get_surface()
        self.context.surface = internal_surface
        self.load_resources()
        self.load_characters()

    def load_resources(self):
        (self.context.fonts,
         self.context.character_defs,
         self.context.characters,
         self.context.sprites,
         self.context.skills) = ResourceService.load_resources()

    def load_characters(self):
        self.character_controllers = {
            key: CharacterController(character, self.context.character_defs[character.sprite_sheet])
            for key, character in self.context.characters.items()
        }
        self.game_view.character_views = [c.character_view for c in self.character_controllers.values()]

    def teardown(self):
        pygame.quit()

    def handle_events(self):
        player = self.character_controllers[PLAYER]
        self.context.player = self.context.characters[PLAYER]
        move_input = get_move_vector()
        used_skill: int | None = get_used_skill()

        if used_skill is not None:
            player.use_skill(self.context.skills[used_skill])

        if move_input.x == 0 and move_input.y == 0:
            player.stop()
        else:
            player.move(get_move_vector())
        event: Event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.context.running = False

    def render(self):
        self.context.delta_time = clock.tick(FPS) / 1000
        self.context.surface.fill((150, 150, 150))

        self.game_view.draw(self.context)

        scaled_surface = pygame.transform.scale(self.context.surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.context.outer_surface.fill((0, 0, 0))
        self.context.outer_surface.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def start(self):
        self.init()
        self.context.running = True

        while self.context.running:
            self.handle_events()
            self.render()

        self.teardown()
