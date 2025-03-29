import setup
import tools
from Component import collider
from Data import constant as c
import pygame as pg
from Component import brick
from Component import Enemy
from Component import mario
class Level(tools._State):
    def __init__(self):
        tools._State.__init__(self)


    def startup(self, current_time, persistance):
        self.game_info = persistance
        self.persist = self.game_info

        self.game_info[c.CURRENT_TIME] = current_time
        self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
        self.game_info[c.MARIO_DEAD] = False

        self.state = c.NOT_FROZEN
        self.flag_score = None


        self.death_timer = 0

        self.setup_background()
        self.setup_ground()
        self.setup_pipes()
        self.setup_steps()
        self.setup_bricks()

        self.setup_enemies()
        self.setup_mario()

        self.setup_spritegroups()
        self.moving_score_list = []

    def setup_background(self):
        self.background  = setup.graphics['level_1']
        self.back_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background, int(self.back_rect.width * c.BACKGROUND_MULTIPLIER), int(self.back_rect.height * c.BACKGROUND_MULTIPLIER))
        self.back_rect = self.background.get_rect()
        width = self.back_rect.width
        height = self.back_rect.height

        self.level = pg.Surface((width, height)).convert(self.background)
        self.level_rect = self.level.get_rect()
        self.viewport = setup.SCREEN.get_rect(bottom = self.level_rect.bottom)

        self.viewport.x = self.game_info[c.CAMERA_START_X]

    def setup_ground(self):
        ground_rect1 = collider.Collider(0, c.GROUND_HEIGHT, 2500, 60)
        ground_rect2 = collider.Collider(3000, c.GROUND_HEIGHT, 600, 60)

        ground_rect3 = collider.Collider(3800, c.GROUND_HEIGHT, 2500, 60)
        ground_rect4 = collider.Collider(6000, c.GROUND_HEIGHT, 2300, 60)
        self.ground_group = pg.sprite.Group(ground_rect1, ground_rect2, ground_rect3, ground_rect4)

    def setup_pipes(self):
        pipe1 = collider.Collider(1200, 450, 80, 80)
        pipe2 = collider.Collider(1200, 450, 80, 80)
        pipe3 = collider.Collider(1200, 450, 80, 80)
        pipe4 = collider.Collider(1200, 450, 80, 80)
        pipe5 = collider.Collider(1200, 450, 80, 80)
        pipe6 = collider.Collider(1200, 450, 80, 80)
        #TODO setup pipes coordinates
        self.pipe_group = pg.sprite.Group(pipe1, pipe2, pipe3, pipe4, pipe5, pipe6)


    def setup_steps(self):
        step1 = collider.Collider(100, 100, 70, 20)
        # TODO define the rest of the steps

        self.steps_group = pg.sprite.Group(step1)

    def setup_bricks(self):
        self.coin_group = pg.sprite.Group()
        self.powerup_group = pg.sprite.Group()

        brick1 = brick.Brick(100, 100)
        #TODO setup bricks, coins and powerups
        self.brick_group = pg.sprite.Group(brick1) # TODO ...

    def setup_enemies(self):
        goomba0 = Enemy.Goomba()
        goomba1 = Enemy.Goomba(190)
        goomba2 = Enemy.Goomba(190)

        enemy_group1 = pg.sprite.Group(goomba0, goomba1, goomba2)

        self.enemy_group = pg.sprite.Group(enemy_group1)




    def setup_mario(self):
        self.mario = mario.Mario()
        self.mario.rect.x = self.viewport.x + 110
        self.mario.rect.bottom = c.GROUND_HEIGHT

    def setup_spritegroups(self):
        self.sprite_about_to_die_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()

        self.ground_step_pipe_group = pg.sprite.Group(self.ground_group, self.pipe_group, self.steps_group)
        self.mario_and_enemy_group = pg.sprite.Sprite(self.mario, self.enemy_group)

    def update(self, surface, keys, current_time):
        self.game_info[c.CURRENT_TIME] = self.current_time
        self.handle_state(keys)
        self.blit_everything(surface)

    def handle_state(self, keys):
        if self.state == c.FROZEN:
            self.update_during_transition_state(keys)
        elif self.state == c.NOT_FROZEN:
            self.update_all_sprite(keys)

    def update_all_sprite(self, keys):
        self.mario.update(keys, self.game_info, self.powerup_group)

        if self.flag_score:
            self.flag_score.update(None, self.game_info)

            self.enemy_group.update(self.game_info)
            self.brick_group.update()
            self.coin_group.update(self.game_info)

            self.update_viewport()
            self.check_for_mario_death()

    def adjust_sprite_positions(self):
        self.adjust_mario_position()
        self.adjust_enemy_position()
        self.adjust_powerup_position()

    def adjust_mario_position(self):
        self.last_x_position = self.mario.rect.right
        self.mario.rect.x += self.mario.x_vel
        self.check_mario_x_collisions()

        if self.mario_in_transition_state == False:
            self.mario.rect.y += self.mario.x_vel

            self.check_mario_y_collisions()

        if self.mario.rect.x < (self.viewport.x + 5):
            self.mario.rect.x = self.viewport.x + 5

    def update_viewport(self):
        third = self.viewport.x + (self.viewport.w // 3)
        mario_center = self.mario.rect.centerx
        mario_right = self.mario.rect.right

        if self.mario.x_vel > 0 and mario_center >= third:
            multiply = 1
            if mario_right < self.viewport.centerx:
                multiply = 0.5

            new = self.viewport.x + multiply * self.mario.x_vel

            maximum = self.level_rect.w - self.viewport.w
            self.viewport.x = min(maximum, new)

    def blit_everything(self, surface):
        self.level.blit(self.background, self.viewport, self.viewport)

        if self.flag_score:
            self.flag_score.draw(self.level)
            self.powerup_group.draw(self.level)
            self.mario_and_enemy_group.draw(self.level)
            self.coin_group.draw(self.level)
            self.brick_group.draw(self.level)

            surface.blit(self.level, (0, 0), self.viewport)

            for score in self.moving_score_list:
                score.draw(surface)

    def update_during_transition_state(self, keys):
        self.mario.update(keys, self.game_info, self.powerup_group)

        if self.flag_score:
            self.flag_score.update(None, self.game_info)

        self.coin_group.update(self.game_info)
        self.check_flag()
        self.check_for_mario_death()



















