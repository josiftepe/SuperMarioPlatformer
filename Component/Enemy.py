import ctypes

import pygame as pg
from .. import setup
from .. import tools as c
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__()

    def setup_enemy(self, x, y, direction, name, setup_frames):
        self.sprite_sheet = setup.graphics("enemy")
        self.frames = []
        self.frame_index = 0
        self.animate_timer = 0
        self.gravity = 1.5
        self.state = c.WALK

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.bottom = y
