import pygame as pg
from .. import setup

from Data import constant as c

class Digit(pg.sprite.Sprite):
    def __init__(self, image):
        super(Digit, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()

class Score():
    def __init__(self, x, y, score, flag_pole=False):
        self.x = x
        self.y = y

        if flag_pole:
            self.y_vel = -4
        else:
            self.y_vel = -3

        self.sprite_sheet = setup.graphics['item_objects']
        self.create_image_dict()

        self.score_string = str(score)

        self.create_digit_list()
        self.flag_pole_score = flag_pole

    def create_image_dict(self):
        self.image_dict = {}
        image0 = self.get_image() # TODO: take the coordinates
        image1 = self.get_image()
        image2 = self.get_image()
        image3 = self.get_image()
        image4 = self.get_image()
        image5 = self.get_image()
        image6 = self.get_image()
        image7 = self.get_image()
        image8 = self.get_image()
        image9 = self.get_image()

        self.image_dict['0'] = image0
        self.image_dict['1'] = image1
        self.image_dict['2'] = image2
        self.image_dict['3'] = image3
        self.image_dict['4'] = image4
        self.image_dict['5'] = image5
        self.image_dict['6'] = image6
        self.image_dict['7'] = image7
        self.image_dict['8'] = image8
        self.image_dict['9'] = image9

    def create_digit_list(self):
        self.digit_list = []
        self.digit_group = pg.sprite.Group()

        for digit in self.score_string:
            self.digit_list.append(Digit(self.image_dict[digit]))

        self.set_rects_for_images()

    def set_rects_for_images(self):
        for i, digit in enumerate(self.digit_list):
            digit.rect = digit.image.get_rect()
            digit.rect.x = self.x + (i * 10)
            digit.rect.y = self.y


    def update(self, score_list, level_info):
        for number  in self.digit_list:
            number.rect.y += self.y_vel

        if score_list:
            self.check_to_delete_floating_scores(score_list, level_info)

        if self.flag_pole_score:
            if self.digit_list[0].rect.y <= 100:
                self.y_vel = 0

    def draw(self, screen):
        for digit in self.digit_list:
            screen.blit(digit.image, digit.rect)

    def check_to_delete_floating_scores(self, score_list, level_info):
        for i, score in enumerate(score_list):
            if int(score.score_string) == 999:
                if score.y - score.digit_list[0].rect.y > 130:
                    score_list.pop(i)

                else:
                    if score.y - score.digit_list[0].rect.y > 80:
                        score_list.pop(i)
    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK_COLOR)

        image = pg.transform.scale(image, int(rect.width * c.SIZE_MULTIPLIER), int(rect.height * c.SIZE_MULTIPLIER))

        return image


