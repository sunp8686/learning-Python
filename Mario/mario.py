import pygame as pg
import settings as s
from Level import *
from Decoration import *

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((s.width, s.height))

class Game():
    def __init__(self):
        self.title = Tile_screen((s.width/2, s.height/2), screen, self.create_level)
        self.game_state = 'title'

    def create_level(self):
        self.game_state = 'level'
        self.level = Level(screen, self.create_title)

    def create_title(self):
        self.game_state = 'title'
        self.title = Tile_screen((s.width / 2, s.height / 2), screen, self.create_level)

    def run(self):
        if self.game_state == 'title':
            self.title.draw()
        else:
            self.level.run()

game = Game()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    screen.fill(s.WHITE)
    game.run()
    pg.display.flip()
    clock.tick(s.fps)

