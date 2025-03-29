import setup
import tools
from Component import collider
from Data import constant as c
import pygame as pg
from Component import mario
from Component import brick
from Component import Enemy

class LoadScreen(tools._State):
    def __init__(self):
        tools._State.__init__(self)


    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.game_info = self.persist

        self.next = self.set_next_state()
        info_state = self.set_overhead_info_state()

        self.overhead_info = info.OverheadInfo(self.game_info, info_state)

    def set_next_state(self):
        return c.LEVEL1

    def set_overhead_info_state(self):
        return c.LOAD_SCREEN

    def update(self, surface, keys, current_time):
        if current_time - self.start_time < 2400:
            surface.fill(c.BLACK_COLOR)
            self.overhead_info.draw(surface)


