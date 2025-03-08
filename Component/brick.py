import pygame as pg
from .. import setup

from Data import constant as c

from . import coin

class Brick(pg.sprite.Sprite):
    def __init__(self, x, y, contents=None, powerup_group=None, name='brick'):
        pg.sprite.Sprite.__init__(self)
        self.sprite_sheet = setup.graphics['tile_set']
        self.frames = []
        self.frame_index = 0
        self.setup_frames()
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)
        self.rest_height = y
        self.bumped_up = False
        self.state = c.RESTING
        self.y_vel = 0
        self.gravity = 1.2
        self.name = name
        self.contents = contents
        self.group = powerup_group
        self.powerup_in_box = True

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK_COLOR)

        image = pg.transform.scale(image, int(rect.width * c.SIZE_MULTIPLIER), int(rect.height * c.SIZE_MULTIPLIER))

        return image

    def setup_frames(self):
        self.frames.append(self.get_image()) # TODO setup brick indexes

    def set_contents(self):
        if self.contents == '6coins':
            self.coin_total = 6
        else:
            self.coin_total = 0


    def update(self):
        self.handle_state()


    def handle_state(self):
        if self.state == c.RESTING:
            self.resting()
        elif self.state == c.BUMPED:
            self.bumped()
        elif self.state == c.OPENED:
            self.opened()

    def resting(self):
        if self.contents == '6coins':
            if self.coin_total == 0:
                self.state = c.OPENED

    def bumped(self):
        self.rect.y += self.y_vel
        self.y_vel += self.gravity

        if self.rect.y >= (self.rest_height + 5):
            self.rect.y = self.rest_height
            if self.contents == 'star':
                self.state = c.OPENED
            if self.contents == '6coins':
                if self.coin_total == 0:
                    self.state = c.OPENED
                else:
                    self.state = c.RESTING
        else:
            self.state = c.RESTING

    def opened(self):
        self.frame_index = 1
        self.image = self.frames[self.frame_index]

        if self.contents == 'star' and self.powerup_in_box:
            self.group.add(powerup.Star(self.rect.centerx, self.rest_height))
            self.powerup_in_box = False
