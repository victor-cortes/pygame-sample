from pygame import Vector2

from models.character_state import CharacterState
from models.direction import Direction
from models.game_context import GameContext

DEFAULT_MOVE_PIXELS = 64


class PhysicsService:
    def tick(self, ctx: GameContext):
        for character in ctx.characters.values():
            match character.state:
                case CharacterState.MOVING:
                    if not character.is_dead():
                        character.position += character.move_vec * character.move_speed * ctx.delta_time * DEFAULT_MOVE_PIXELS

            if character.activated_skill:
                character.activated_skill.tick(ctx)
                if character.activated_skill.finished:
                    character.finish_skill()

            i = 0
            while i < len(character.character_projectiles):
                projectile = character.character_projectiles[i]
                if projectile.distance < projectile.param['projectile_max_distance']:
                    (x, y) = projectile.position
                    speed = projectile.param['projectile_speed']
                    delta_s = ctx.delta_time * speed
                    projectile.distance += delta_s
                    match projectile.direction.value:
                        case Direction.UP.value:
                            y -= delta_s
                        case Direction.DOWN.value:
                            y += delta_s
                        case Direction.LEFT.value:
                            x -= delta_s
                        case Direction.RIGHT.value:
                            x += delta_s
                    projectile.position = Vector2(x, y)
                    i += 1
                else:
                    character.character_projectiles.remove(projectile)


