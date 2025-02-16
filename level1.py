import tools
from Data import constant as c

class Level(tools._State):
    def __init__(self):
        tools._State.__init__(self)


    def startup(self, current_time, persistance):
        self.game_info = persistance
        self.persist = self.game_info

        self.game_info[c.CURRENT_TIME] = current_time
        self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
        self.game_info[c.MARIO_DEAD] = False

        self.state = c.NOT_FROZEN
        self.flag_score = None
        self.death_timer = 0



