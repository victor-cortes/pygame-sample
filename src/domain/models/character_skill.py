from types import SimpleNamespace

from models.skill import Skill


class CharacterSkill:
    script_line = 0
    skill_clock = 0
    delay_mode = False
    delay_clock = 0
    finished = False

    def __init__(self, character, skill: Skill):
        self.character = character
        self.skill = skill

    def tick(self, delta_time):
        self.skill_clock += delta_time
        self.execute_script(delta_time)

    def execute_script(self, delta_time):
        try:
            function = list(self.skill.script.keys())[self.script_line]
            self.exec_function(function, self.skill.script[function], delta_time)
        except IndexError:
            self.finish_skill()

    def exec_function(self, function, param, delta_time):
        try:
            self.__getattribute__(function)(param, delta_time)
        except AttributeError:
            pass

    def spawn_projectile(self, param, delta_time):
        item = SimpleNamespace(**param)
        self.character.spawn_projectile(item)
        self.script_line += 1

    def delay(self, param, delta_time):
        if not self.delay_mode:
            self.delay_mode = True

        self.delay_clock += delta_time
        if self.delay_clock >= param / 1000:
            self.delay_mode = False
            self.delay_clock = 0
            self.script_line += 1

    def finish_skill(self):
        self.finished = True
