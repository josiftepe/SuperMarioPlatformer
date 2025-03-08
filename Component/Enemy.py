import ctypes

import pygame as pg
from .. import setup
from Data import constant as c
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
        self.current_time = pg.time.Clock()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.bottom = y

        self.set_velocity()

    def set_velocity(self):
        if self.direction == c.LEFT:
            self.x_vel = -2
        else:
            self.x_vel = 2
        self.y_vel = 0

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK_COLOR)

        image = pg.transform.scale(image, int(rect.widht * c.SIZE_MULTIPLIER), int(rect.height * c.SIZE_MULTIPLIER))

        return image

    def handle_state(self):
        if self.state == c.WALK:
            self.walking()
        elif self.state == c.FALL:
            self.falling()
        elif self.state == c.JUMPED_ON:
            self.jumped_on()
        elif self.state == c.SHELL_SLIDE:
            self.shell_slidign()
        elif self.state == c.DEATH_JUMP:
            self.death_jumping()

    def walking(self):
        if (self.current_time - self.animate_timer) > 125:
            if self.frame_index == 0:
                self.frame_index += 1
            elif self.frame_index == 1:
                self.frame_index = 0
            self.animate_timer = self.current_time

    def falling(self):
        if self.y_vel < 10:
            self.y_vel += self.gravity


    def death_jumping(self):
        self.rect.y += self.y_vel
        self.rect.x += self.x_vel

        self.y_vel += self.gravity

        if self.rect.y > 600:
            self.kill()

    def start_death_jump(self, direction):
        self.y_vel = -8

        if direction == c.RIGHT:
            self.x_vel = 2
        else:
            self.x_vel = -2

        self.gravity = 0.5
        self.frame_index = 3 # TODO change frame index
        self.image = self.frames[self.frame_index]

        self.state = c.DEATH_JUMP

    def animation(self):
        self.image = self.frames[self.frame_index]

    def update(self, game_info, *args):
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()
        self.animation()


class Goomba(Enemy):
    def __init__(self, y = c.GROUND_HEIGHT, x = 0, direction = c.LEFT, name = 'goomba'):
        Enemy.__init__(self)
        self.setup_enemy(x, y, direction, self.setup_frames)

    def setup_frames(self):
        self.frames.append(self.get_image()) # TODO set the indexes

        self.frames.append(pg.transform.flip(self.frames[1], False, True))


    def jumped_on(self):
        self.frame_index = 2 # TODO set frame index
        if self.current_time - self.death_timer > 500:
            self.kill()






