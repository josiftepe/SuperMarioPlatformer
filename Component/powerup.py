import pygame as pg
from .. import setup
from Data import constant as c


class Powerup(pg.sprite.Sprite):
    def __init__(self , x, y):
        super(Powerup, self).__init__()

    def setup_powerup(self, x, y, name, setup_frames):
        self.sprite_sheet = setup.graphics['item_objects']
        self.frames = []
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.state = c.REVEAL
        self.y_vel = 1
        self.x_vel = 0
        self.box_height = y

        self.name = name

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK_COLOR)

        image = pg.transform.scale(image, int(rect.width * c.SIZE_MULTIPLIER), int(rect.height * c.SIZE_MULTIPLIER))

        return image

    def revealing(self, *args):
        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.y_vel = 0
            self.state = c.SLIDE

    def sliding(self):
        if self.direction == c.RIGHT:
            self.x_vel = 3
        else:
            self.x_vel = -3



class Mushroom(Powerup):
    def __init__(self, x, y, name='mushroom'):
        super(Mushroom, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)

    def setup_frames(self):
        self.frames.append(self.get_image()) # TODO set mushroom frames


    def handle_state(self):
        if self.state == c.REVEAL:
            self.revealing()
        elif self.state == c.SLIDE:
            self.sliding()



