import os

import pygame as pg

keybindings = {
    'left': pg.K_LEFT,
    'right': pg.K_RIGHT,
    'down': pg.K_DOWN,
    'action': pg.K_s,
    'jump': pg.K_UP,
}

class Control():
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.caption = caption
        self.fps = 60
        self.show_fps = False
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self):
        self.current_time = pg.time.get_ticks()

        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def flip_state(self):
        previous_state = self.state_name
        self.state_name = self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous_state

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

            self.state.get_event(event)



    def toggle_show_fps(self, key):
        if key == pg.K_z:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)

    def main(self):
        # game loop for super mario game
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)

            if self.show_fps:
                fps = self.clock.get_fps()
                fps_string = "{} - {:2f}".format(self.caption, fps)
                pg.display.set_caption(fps_string)

class _State():
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def startup(self, current_time, persistance):
        self.persist = persistance
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, screen, keys, current_time):
        pass


def load_all_graphics(directory_name, color_key = (255, 0, 255), accepting = ('.jpg', 'png', '.jpeg')):
    graphics = []

    for picture in os.listdir(directory_name):
        name, ext = os.path.splitext(picture)
        if ext.lower() in accepting:
            image = pg.image.load(os.path.join(directory_name, picture))
            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert()
                image.set_colorkey(color_key)
            graphics.append(picture)

    return graphics







