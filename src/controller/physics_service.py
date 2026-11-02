from models.character_state import CharacterState
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
                character.activated_skill.tick(ctx.delta_time)
                if character.activated_skill.finished:
                    character.finish_skill()
