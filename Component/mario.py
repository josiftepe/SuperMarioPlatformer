import pygame as pg

import tools
from Data import constant as c
import setup


class Mario(pg.sprite.Sprite):
    def __init__(self):
        self.left_big_normal_frames = None
        self.sprite_sheet = setup.graphics
        self.setup_timers()
        self.state = c.WALK
        # self.image =

    def setup_timer(self):
        self.walking_timer = 0
        self.invincible_animation_timer = 0
        self.invincible_start_timer = 0
        self.death_timer = 0

    def state_setup(self):
        self.facing_right = True
        self.allow_jump = True
        self.dead = False
        self.invincible = False
        self.big = False
        self.allow_fireball = False

    def setup_forces(self):
        self.x_vel = 0
        self.y_vel = 0
        self.max_x_vel = c.MAX_WALKING_SPEED
        self.max_y_vel = c.MAX_Y_VEL
        self.x_accelaration = c.WALK_ACCELERATION
        self.jump_vel = c.JUMP_VELOCITY
        self.gravity = c.GRAVITY

    def setup_counters(self):
        self.frame_index = 0
        self.invincible_index = 0

    def load_images_from_sprite_sheet(self):
        self.right_frames = []
        self.left_frames = []

        self.left_small_normal_frames = []
        self.right_small_normal_frames = []
        self.left_big_normal_frames = []
        self.right_big_normal_frames = []

        self.left_fire_frames = []
        self.right_fire_frames = []


        self.left_small_normal_frames(self.get_image())

        #TODO --> write cords for mario spritesheet

        for frame in self.right_small_normal_frames:
            new_image = pg.transform.flip(frame, True, True)
            self.left_small_normal_frames.append(new_image)

        for frame in self.right_big_normal_frames:
            new_image = pg.transform.flip(frame, True, True)
            self.left_big_normal_frames.append(new_image)

        for frame in self.right_frames:
            new_image = pg.transform.flip(frame, True, True)
            self.right_frames.append(new_image)

        for frame in self.right_fire_frames:
            new_image = pg.transform.flip(frame, True, True)
            self.left_fire_frames.append(new_image)


        self.normal_small_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.normal_big_frames = [self.right_big_normal_frames, self.left_big_normal_frames]
        self.fire_frames = [self.right_fire_frames, self.left_fire_frames]

        self.all_images = [
            self.left_small_normal_frames,
            self.right_small_normal_frames,
            self.left_big_normal_frames,
            self.right_big_normal_frames,
            self.left_fire_frames,
            self.right_fire_frames,
        ]

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height])
        rect = image.get_rect()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        image.set_colorkey(c.BLACK_COLOR)
        image = pg.transform.scale(image, (int(rect.width * c.SIZE_MULTIPLIER), int(rect.height * c.SIZE_MULTIPLIER)))

        return image

    def handle_state(self, keys, fire_group):
        if self.state == c.STAND:
            self.standing(keys, fire_group)
        elif self.state == c.WALK:
            self.walking(keys, fire_group)
        elif self.state == c.JUMP:
            self.jump(keys, fire_group)
        elif self.state == c.FALL:
            self.fall(keys, fire_group)
        elif self.state == c.SMALL_TO_BIG:
            self.change_to_big(keys, fire_group)
        elif self.state == c.BIG_TO_SMALL:
            self.chage_to_small(keys, fire_group)


    def standing(self, keys, fire_group):
        self.check_to_allow_jump(keys)
        self.check_to_allow_fireball(keys)

        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0

        if keys[tools.keybindings['action']]:
            if self.fire and self.allow_fireball:
                self.shoot_fireball(fire_group)

        if keys[tools.keybindings['down']]:
            self.crouching = True

        if keys[tools.keybindings['left']]:
            self.facing_right = False
            self.get_out_of_crouch()
            self.state = c.WALK
        elif keys[tools.keybindings['right']]:
            self.facing_right = True
            self.get_out_of_crouch()
            self.state = c.WALK
        elif keys[tools.keybindings['jump']]:
            if self.allow_jump:
                self.state = c.JUMP
                self.y_vel = c.JUMP_VELOCITY
            else:
                self.state = c.STAND

    def get_out_of_crouch(self):
        bottom = self.rect.bottom
        left = self.rect.x

        if self.facing_right:
            self.image = self.right_frames[0]
        else:
            self.image = self.left_frames[0]

        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = left
        self.crouching = False

    def check_to_allow_jump(self, keys):
        if not keys[tools.keybindings['jump']]:
            self.allow_jump = True


    def check_to_allow_fireball(self, keys):
        if not keys[tools.keybindings['action']]:
            self.allow_fireball = True


    def shoot_fireball(self, powerup_group):
        self.fireball_count = self.count_number_of_fireballs(powerup_group)

        if self.current_time - self.last_fireball_time > 200:
            if self.fireball_count < 2:
                self.allow_fireball = True
                powerup_group.add(powerups.Fireball(self.rect.right, self.rect.y, self.facing_right))
            self.last_fireball_time = self.current_time

            self.frame_index = 1 # TODO

            if self.facing_right:
                self.image = self.right_frames[self.frame_index]
            else:
                self.image = self.left_frames[self.frame_index]


    def count_number_of_fireballs(self, powerup_group):
        fireball_list = []

        for powerup in powerup_group:
            if powerup.name == c.FIREBALL:
                fireball_list.append(powerup)
        return len(fireball_list)

    def walking(self, keys, fire_group):
        self.check_to_allow_jump(keys)
        self.check_to_allow_fireball(keys)

        if self.frame_index == 0:
            self.frame_index += 1
            self.walking_timer = self.current_time

        else:
            if (self.current_time - self.walking_timer) > self.calculate_animation_speed():
                if self.frame_index < 3: # TODO check for the frames
                    self.frame_index += 1
                else:
                    self.frame_index = 1
                self.walking_timer = self.current_time

            if keys[tools.keybindings['action']]:
                self.max_x_vel = c.MAX_RUN_SPEED
                self.x_accelaration = c.RUN_ACCELARATION

                if self.fire and self.allow_fireball:
                    self.shoot_fireball(fire_group)
            else:
                self.max_x_vel = c.MAX_WALKING_SPEED
                self.x_accelaration = c.WALK_ACCELERATION

            if keys[tools.keybindings['jump']]:
                if self.allow_jump:
                    if self.big:
                        self.state = c.JUMP

                    if self.x_vel > 4.5 or self.x_vel < -4.5:
                        self.y_vel = c.JUMP_VELOCITY - 5
                    else:
                        self.y_vel = c.JUMP_VELOCITY

            if keys[tools.keybindings['left']]:
                self.get_out_of_crouch()
                self.facing_right = False

                if self.x_vel > 0:
                    self.frame_index = 5
                    self.x_accelaration = c.SMALL_TURNARAOUND
                else:
                    self.x_accelaration = c.WALK_ACCELERATION

                if self.x_vel > (self.max_x_vel * -1):
                    self.x_val -= self.x_accelaration

                    if self.x_vel > -0.5:
                        self.x_vel = -0.5
                elif self.x_vel > (self.max_x_vel * -1):
                    self.x_vel += self.x_accelaration
            if keys[tools.keybindings['right']]:
                self.get_out_of_crouch()
                self.facing_right = True

                if self.x_vel < 0:
                    self.frame_index = 5 # TODO check frame index
                    self.x_accelaration = c.SMALL_TURNARAOUND
                else:
                    self.x_accelaration = c.WALK_ACCELERATION

                if self.x_vel < self.max_x_vel:
                    self.x_vel += self.x_accelaration

                    if self.x_vel < 0.5:
                        self.x_vel = 0.5

                elif self.x_vel > self.max_x_vel:
                    self.x_vel -= self.x_accelaration

            else:
                if self.facingla_right:
                    if self.x_vel > 0:
                        self.x_vel -= self.x_accelaration
                    else:
                        self.x_vel = 0
                        self.state = c.STAND

                else:
                    if self.x_vel < 0:
                        self.x_vel += self.x_accelaration
                    else:
                        self.x_vel = 0
                        self.state = c.STAND

    def calculate_animation_speed(self):
        if self.x_vel == 0:
            animation_speed = 130
        elif self.x_vel > 0:
            animation_speed = 130 - (self.x_vel * 10)
        else:
            animation_speed = 130 - (self.x_vel * 10 * (-1))

        return animation_speed


    def jumping(self, keys, fire_group):
        self.allow_jump = False
        self.frame_index = 4
        self.gravity = c.GRAVITY

        self.y_vel += self.gravity
        self.check_to_allow_fireball(keys)

        if self.y_vel >= 0 and self.y_vel < self.max_y_vel:
            self.state = c.FALL
            self.gravity = c.GRAVITY

        if keys[tools.keybindings['left']]:
            if self.x_vel > (self.max_x_vel * -1):
                self.x_vel -= self.x_accelaration

        if keys[tools.keybindings['right']]:
            if self.x_vel < self.max_x_vel:
                self.x_vel += self.x_accelaration

        if not keys[tools.keybindings['jump']]:
            self.gravity = c.GRAVITY
            self.state = c.FALL

        if keys[tools.keybindings['action']]:
            if self.allow_fireball and self.fire:
                self.shoot_fireball(fire_group)

    def falling(self, keys, fire_group):
        self.check_to_allow_fireball(keys)

        if self.y_vel < c.MAX_Y_VEL:
            self.y_vel += self.gravity

        if keys[tools.keybindings['left']]:
            if self.x_vel > (self.max_x_vel * -1):
                self.x_vel -= self.x_accelaration

        if keys[tools.keybindings['right']]:
            if self.x_vel < self.max_x_vel:
                self.x_vel += self.x_accelaration

        if keys[tools.keybindings['action']]:
            if self.fire and self.allow_fireball:
                self.shoot_fireball(fire_group)


    def jumping_to_death(self):
        if self.death_timer == 0:
            self.death_timer = self.current_time

        elif (self.current_time - self.death_timer) > 500:
            self.rect.y += self.y_vel
            self.y_vel += self.gravity

