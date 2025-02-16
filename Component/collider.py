from Data import constant as c
import pygame as pg

class Collider(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, name = 'collider'):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.state = None
