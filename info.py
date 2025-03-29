import setup
import tools
from Component import collider
from Data import constant as c
import pygame as pg
from Component import mario
from Component import brick
from Component import Enemy


class Character(pg.sprite.Sprite):
    def __init__(self, image):
        super(Character, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()


class OverheadInfo(object):
    def __init__(self, game_info, state):
        self.sprite_sheet = setup.graphics['text_images']
        self.coin_total = game_info[c.COIN_TOTAL]
        self.time = 400

        self.current_time = 0
        self.total_lives = game_info[c.TOP_SCORE]
        self.state = state
        self.game_info = game_info
        self.create_image_dict()
        self.create_info_label()
        self.create_load_screen_labels()
        self.create_countdown_clock()
        self.create_coin_counter()
        self.create_mario_image()

    def create_image_dict(self):
        self.image_dict = {}
        image_list = []

        image_list.append(self.get_image()) # TODO get position from the sprite sheet
        # TODO

        character_string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        for character, image in zip(character_string, image_list):
            self.image_dict[character] = image

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height])
        rect = image.get_rect()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        image.set_colorkey(c.BLACK_COLOR)
        image = pg.transform.scale(image, (int(rect.width * c.SIZE_MULTIPLIER), int(rect.height * c.SIZE_MULTIPLIER)))

        return image

    def create_score_group(self):
        self.score_images = []
        self.create_label(self.score_images, '000000', 50, 50)


    def create_info_label(self):
        self.mario_label = []
        self.world_label = []
        self.time_label = []
        self.stage_label = []

        self.create_label(self.mario_label, "MARIO", 50, 30)
        self.create_label(self.world_label, "WORLD", 400, 30)
        self.create_label(self.time_label, 'TIME', 600, 30)
        self.create_label(self.stage_label, '1-1', 480, 30)


        self.label_list [
            self.mario_label,
            self.world_label,
            self.time_label,
            self.stage_label
        ]

    def create_label(self, label_list, string, x, y):
        for letter in string:
            label_list.append(Character(self.image_dict[letter]))

    def create_load_screen_labels(self):
        world_label = []
        number_label = []
        self.create_label(world_label, 'WORLD', 250, 200)
        self.create_label(number_label, '1-1', 400, 200)

        self.center_labels = [world_label, number_label]

    def create_countdown_clock(self):
        self.count_down_images = []
        self.create_label(self.count_down_images, str(self.time), 650, 50)

    def create_coin_counter(self):
        self.coin_count_images = []
        self.create_label(self.count_down_images, '00', 300, 55)



    def create_mario_image(self):
        self.life_times_image = self.get_image() # TODO life times
        self.life_times_rect = self.life_times_image.get_rect(center = (370, 290))
        self.life_total_label = []
        self.create_label(self.life_total_label, str(self.total_lives), 480, 250)

        self.sprite_sheet = setup.graphics['mario_lives']
        self.mario_image = self.get_image() # TODO
        self.mario_rect = self.mario_image.get_rect(center = (300, 290))

