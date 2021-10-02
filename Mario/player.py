import math
import random
import pygame as pg
import settings as s

class Player():
    def __init__(self, pos, surface):
        self.big = False
        self.fire = False
        self.small = True
        self.pos = pos
        self.index = 0
        self.surface = surface
        self.status = ['run', 'idle', 'jump', 'cround']
        self.transform(self.pos)
        self.speed = 2
        self.cround = False
        self.vel_y = s.vel_y
        self.accer = s.acerlerate
        self.time = 0
        self.direction = 1
        self.alive = True
        self.flip = False
        self.jump = False
        self.in_air = False
        self.move_left = False
        self.move_right = False
        self.trans = False
        self.trans_small = False
        self.fire_trans = False
        self.firing = False
        self.temp = 0
        self.delay_time = 30
        self.incredible = False
        self.get_pole = False
        self.tamp = 0
        self.game_over = False

    def status_manager(self):
        if self.status == 'run':
            self.index += 0.1
            if self.index >= 3:
                self.index = 0
        elif self.status == 'idle':
            self.index = 6
        elif self.status == 'cround':
            self.index = 5
        elif self.status == 'death':
            self.index = 5
        elif self.status == 'jump':
            self.index = 4
        elif self.status == 'big_trans':
            self.index = random.choice((6,15))
        elif self.status == 'fire_trans':
            self.index = random.choice((6,19))
        elif self.status == 'fire_trans_2':
            self.index = random.choice((random.choice((6,19)), random.choice((15,20))))
        elif self.status == 'small_trans':
            self.index = random.choice((6,13))
        elif self.status == 'firing':
            if self.move_left or self.move_right:
                self.temp += 0.1
                self.index = 16+ self.temp
            else:
                self.index = 16
            if self.temp >= 3:
                self.index = 16
                self.temp = 0
        elif self.status == 'pole':
            self.temp += 0.1
            self.index = 7+ self.temp
            if self.index >= 9:
                self.temp = 0
                self.index = 7

    def animated(self):
        self.image = self.image_list[int(self.index)]
        if self.big or self.fire:
            self.image = pg.transform.scale(self.image, (int(16 * 2.1), int(31 * 2.1)))
        else:
            self.image = pg.transform.scale(self.image, (35, 35))

    def check_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.index = int(self.index)
        return self.status, self.index

    def move(self):
        keys = pg.key.get_pressed()
        dx, dy = 0, 0
        if keys[pg.K_LEFT] and not self.cround:
            self.direction = -1
            self.move_left = True
            self.flip = True
        elif keys[pg.K_RIGHT] and not self.cround:
            self.direction = 1
            self.move_right = True
            self.flip = False
        else:
            self.move_right = False
            self.move_left = False
            self.cround = False
            self.check_status('idle')
        if self.move_right or self.move_left:
            dx = self.speed * self.direction
            self.time += 0.2
            self.check_status('run')
        else:
            self.time -= 0.1

        # accer and velocity

        if self.time > 1.5:
            self.time = 1.5
        elif self.time <= 0:
            self.time = 0

        if keys[pg.K_DOWN] and (self.big or self.fire):
            dx = 0
            self.cround = True
            self.check_status('cround')

        #jumping
        if keys[pg.K_a]:
            self.jump = True
        else:
            self.jump = False
        if self.jump and self.in_air == False:
            s.load_music('sound/small_jump.ogg', 0, False)
            if self.big or self.fire:
                self.vel_y = -17
            else:
                self.vel_y = -14
            self.in_air = True
        if self.in_air:
            self.check_status('jump')

        self.vel_y += s.gravity
        dy += self.vel_y
        self.rect.centerx += dx + self.accer * self.time * self.direction
        self.rect.centery += dy

        #fire and delay time:
        if self.fire and keys[pg.K_s]:
            self.check_status('firing')
            if self.delay_time <= 0:
                s.load_music('sound/fireball.ogg', 0, False)
                self.delay_time = 30
                self.firing = True
            else:
                self.firing = False
        if self.delay_time > 0:

            self.delay_time -= 1

    def finish(self):
        self.rect.centery += self.tamp
        if self.get_pole:
            self.check_status('pole')
            self.tamp = 4
            if self.rect.bottom >=500:
                self.rect.centery = 500
        else:
            self.tamp = 0

    def get_value(self):
        if math.sin(pg.time.get_ticks()) > 0: return 255
        else: return 0

    def draw(self):
        alpha = self.get_value()
        if self.incredible:
            self.image.set_alpha(alpha)
        self.surface.blit(pg.transform.flip(self.image, self.flip, False), self.rect)

    def update(self):
        self.draw()
        self.animated()
        self.status_manager()
        self.finish()
        if (not self.trans) and (not self.fire_trans) and(not self.trans_small) and self.alive and not self.get_pole\
                and not self.game_over:
            self.move()
        if self.rect.bottom > 630:
            self.alive = False
            self.vel_y = 0
            self.rect.bottom = 620
        if not self.alive:
            self.game_over = True

    def transform(self, pos):
        if self.big:
            self.image_list = s.cut_graphic('graphic/mario_bros.png', 80, 0, 16, 31, 0, 496)
            self.image = self.image_list[int(self.index)]
            self.image = pg.transform.scale(self.image, (int(16 * 2.1), int(31 * 2.1)))
        elif self.fire:
            self.image_list = s.cut_graphic('graphic/mario_bros.png', 80, 48, 16, 31, 0, 496 - 48)\
                              + s.cut_graphic('graphic/mario_bros.png', 80+ 16*6, 0, 16, 31, 16*12, 496) \
                              + s.cut_graphic('graphic/mario_bros.png', 320, 0, 16, 31, 48, 496)
            self.image = self.image_list[int(self.index)]
            self.image = pg.transform.scale(self.image, (int(16 * 2.1), int(31 * 2.1)))
        elif self.small:
            self.image_list = s.cut_graphic('graphic/mario_bros.png', 80, 32, 16, 16, 82, 479)\
                              + s.cut_graphic('graphic/mario_bros.png', 320, 0, 16, 31, 48, 496)
            self.image = self.image_list[int(self.index)]
            self.image = pg.transform.scale(self.image, (35, 35))

        self.rect = self.image.get_rect(center=pos)


