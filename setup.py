import pygame as pg

import tools
from Data import constant as c

ORIGINAL_TITLE = c.ORIGINAL_CAPTION
pg.init()
pg.event.set_allowed((pg.KEYDOWN, pg.KEYUP, pg.QUIT))
pg.display.set_caption(ORIGINAL_TITLE)

SCREEN = pg.display.set_mode(c.SCREEN_SIZE)

graphics = tools.load_all_graphics('Assets')