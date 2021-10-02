import math
import random
import warnings

import pygame as pg
import win32ts
from settings import *
import os

class BG():
    def __init__(self, pos, surface):
        self.image = pg.image.load('graphic/bg_1.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (s.width, s.height))
        self.rect = self.image.get_rect(topleft = pos)
        self.display_surface = surface

    def draw(self):
        self.display_surface.blit(self.image, self.rect)

class Water():
    def __init__(self, y, surface):
        self.image_list = []
        self.index = 0
        self.display = surface
        self.pos = []
        number_list = len(os.listdir('graphic/decoration/water'))
        for number in range(number_list):
            image = pg.image.load(f'graphic/decoration/water/{number}.png').convert_alpha()
            self.image_list.append(image)
        self.image = self.image_list[self.index]
        for i in range(int(s.width/192) +1):
            x = 192 * i
            self.pos.append((x,y))

    def animated(self):
        self.index += 0.1
        if self.index >= len(self.image_list):
            self.index = 0
        self.image = self.image_list[int(self.index)]

    def draw(self):
        for pos in self.pos:
            self.display.blit(self.image, pos)

    def update(self):
        self.animated()
        self.draw()

class Tile_screen():
    def __init__(self, pos, surface, create_level):
        self.display = surface
        self.image = just_graphic('graphic/title_screen.png', 1, 59,175,83, 80,170).convert_alpha()
        self.image = pg.transform.scale(self.image, (400, 200))
        #self.image = self.image_list[0]
        self.rect = self.image.get_rect(center = (pos[0], pos[1] -100))
        self.bg = pg.image.load('graphic/bg.PNG').convert_alpha()
        self.bg = pg.transform.scale(self.bg, (s.width, s.height))
        self.bg_rect = self.bg.get_rect(center = pos)
        self.char = just_graphic('graphic/mario_bros.png', 176, 32, 16, 16,193,479).convert_alpha()
        self.char = pg.transform.scale2x(self.char)
        self.char_rect = self.char.get_rect(center = (220, 525))
        self.font = pg.font.SysFont('comisans', 40, True)
        self.text = 'Press Enter to Begin'
        self.text_dis = self.font.render(f'{self.text}', False, WHITE)
        self.tex_rect = self.text_dis.get_rect(center = (pos[0], pos[1] + 75))
        self.create_level = create_level
        self.circle = Screen_fade((220, 525), self.display, 850, -1, 20)
        self.screen_fade = False
        self.screen_out = Screen_out((0,0), 7, self.display)

    def get_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            self.screen_fade = True

    def get_value(self):
        value = random.randint(0,20)
        if value == 10 or value == 5: return 255
        else: return 150

    def draw(self):
        self.get_input()
        self.display.blit(self.bg, self.bg_rect)
        self.display.blit(self.image, self.rect)
        self.display.blit(self.char, self.char_rect)
        self.text_dis.set_alpha(self.get_value())
        self.display.blit(self.text_dis, self.tex_rect)
        self.screen_out.update()
        if self.screen_fade:
            if self.circle.dra():
                self.create_level()

class Screen_fade(pg.sprite.Sprite):
    def __init__(self, pos, surface, start, direction, step):
        super().__init__()
        self.display = surface
        self.start = start
        self.pos = pos
        self.direction = direction
        self.temp = []
        self.index = 0
        self.delay_time = pg.time.get_ticks()
        self.step = step
        for i in range(40):
            circle = start + i* 20 * self.direction
            self.temp.append(circle)
        self.image = pg.Surface((s.width, s.height), flags= pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (0,0))

    def dra(self):
        self.index += 0.4
        if self.index >= len(self.temp):
            self.index = len(self.temp) - 1
            #return True
        self.rad= self.temp[int(self.index)]

        #for i in range(int(self.index)):
        #    pg.draw.circle(self.image, (0, 0, 0), (self.pos), self.start + i* 20 * self.direction, 20)
        #    self.display.blit(self.image, (0, 0))

        for i in range(int(self.index)):
            pg.draw.circle(self.display, (0, 0, 0), (self.pos), self.start + i* self.step * self.direction, self.step)

        #pg.draw.circle(self.display, (0, 0, 0),(self.pos), self.rad, 20)
        if int(self.index) == 2:
            self.delay_time = pg.time.get_ticks()
        if self.index == len(self.temp) - 1  and pg.time.get_ticks() - self.delay_time > 2500:
            return True

class Screen_out():
    def __init__(self, pos, speed, surface):
        self.display = surface
        self.speed = speed
        self.rect_A = pg.Rect(pos[0], pos[1], s.width, s.height/2)
        self.rect_B = pg.Rect(pos[0], s.height/2, s.width, s.height/2)

    def draw(self):
        pg.draw.rect(self.display, (0, 0, 0), self.rect_A)
        pg.draw.rect(self.display, (0, 0, 0), self.rect_B)

    def update(self):
        self.rect_A.centery -= self.speed
        self.rect_B.centery += self.speed
        self.draw()
        if self.rect_A.centery == - s.height:
            self.kill()


