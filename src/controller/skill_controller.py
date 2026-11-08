from models.character_skill import CharacterSkill
from models.game_context import GameContext


class SkillController:
    def __init__(self, skill: CharacterSkill, character_controller):
        self.skill = skill
        self.character_controller = character_controller

    def render(self, ctx: GameContext):
        self.execute_script(ctx.delta_time)

    def execute_script(self, delta_time):
        try:
            line = self.skill.skill.script[self.skill.script_line]
            function = list(line.keys())[0]
            params = list(line.values())[0]
            self.exec_function(function, params, delta_time)
        except IndexError:
            self.skill.finish_skill()

    def exec_function(self, function, param, delta_time):
        try:
            self.__getattribute__(function)(param, delta_time)
        except AttributeError:
            pass

    def set_motion(self, param, delta_time):
        self.character_controller.set_motion(param)
        self.skill.script_line += 1
