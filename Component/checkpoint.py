from Data import constant as c
import pygame as pg

class Checkpoint(pg.sprite.Sprite):
    def __init__(self, x, name, y = 0, width = 10, height = 600):
        super(Checkpoint, self).__init__()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.image.fill(c.BLACK_COLOR)
        self.rect.x = x
        self.rect.y = y
        self.name = name


