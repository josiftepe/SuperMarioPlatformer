import pygame as pg
from .. import setup
from Data import constant as c


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y, score_group):
        self.sprite_sheet = setup.gfx['item_object'] # TODO change name
        self.frames = []
        self.frame_index = 0

        self.animation_timer = 0
        self.state = c.SPIN
        self.setup_frames()

        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y - 5

        self.gravity = 1
        self.y_vel = -15

        self.initial_height = self.rect.bottom - 5
        self.score_group = score_group


    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK_COLOR)

        image = pg.transform.scale(image, int(rect.width * c.SIZE_MULTIPLIER), int(rect.height * c.SIZE_MULTIPLIER))

        return image

    def setup_frames(self):
        self.frames.append(self.get_image()) # TODO Set indexes for goomba


    def update(self, game_info, viewport):
        self.current_time = game_info[c.CURRENT_TIME]
        self.viewport = viewport

        if self.state == c.SPIN:
            self.spinning()

    def spinning(self):
        self.image = self.frames[self.frame_index]
        self.rect.y += self.y_vel
        self.y_vel += self.gravity

        if self.current_time - self.animation_timer > 50:
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 0

        self.animation_timer = self.current_time

        if self.rect.bottom > self.initial_height:
            self.kill()
            self.score_group.append() # TODO add coin


