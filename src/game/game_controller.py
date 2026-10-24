import random
import pygame

from pygame.event import Event
from pygame.math import Vector2
from pygame.time import Clock

from src.game.character import Motion
from src.game.game_context import GameContext
from src.ui.character_object import CharacterObject
from src.ui.resource_loader import ResourceLoader

clock = Clock()
FPS = 60
INTERNAL_WIDTH = 800
INTERNAL_HEIGHT = 600
SCALE_FACTOR = 2

SCREEN_WIDTH = INTERNAL_WIDTH * SCALE_FACTOR
SCREEN_HEIGHT = INTERNAL_HEIGHT * SCALE_FACTOR


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


class GameController:
    context: GameContext = None
    character_objects: dict[int, CharacterObject] = {}

    def init(self):
        pygame.init()
        self.context = GameContext()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), depth=32)
        pygame.display.set_caption("Game")
        internal_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        self.context.surface = pygame.display.get_surface()
        self.context.internal_surface = internal_surface
        self.context.fonts, self.context.character_defs, self.context.characters, self.context.sprites = ResourceLoader.load_resources()
        for character in self.context.characters.values():
            self.character_objects[character.id] = CharacterObject(internal_surface, character,
                                                                   self.context.character_defs[character.sprite_sheet])

    def teardown(self):
        pygame.quit()

    def handle_events(self):
        player = self.character_objects[self.context.player_index]
        move_input = get_move_vector()
        if move_input.x == 0 and move_input.y == 0:
            player.stop()
        else:
            player.move(get_move_vector())

        event: Event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.context.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.attack()
                self.mock_damage(player)
            if event.key == pygame.K_ESCAPE:
                self.character_objects[1001].character.hp = self.character_objects[1001].character.max_hp
                self.character_objects[1001].character.motion = Motion.IDLE
                player.character.hp = player.character.max_hp
                player.character.motion = Motion.IDLE

    def mock_damage(self, player: CharacterObject):
        variance = 1 + ((random.random() * 10) - 5) / 100
        damage = player.character.attack * variance
        if random.random() < player.character.crit_strike:
            damage *= 3
        self.character_objects[1001].character.take_damage(round(damage))

    def render(self):
        self.context.delta_time = clock.tick(FPS) / 1000
        self.context.internal_surface.fill((150, 150, 150))
        for c in sorted(self.character_objects.values(), key=lambda c: c.character.position.y):
            c.draw(self.context)
        scaled_surface = pygame.transform.scale(self.context.internal_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.context.surface.fill((0, 0, 0))
        self.context.surface.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def start(self):
        self.init()
        self.context.running = True

        while self.context.running:
            self.handle_events()
            self.render()

        self.teardown()
