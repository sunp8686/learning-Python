import random

import pygame as pg
import settings as s

class Enemies(pg.sprite.Sprite):
    def __init__(self, pos, size, surface, kind):
        super().__init__()
        self.alive = True
        self.direction = 1
        self.speed = 1.0
        self.size = size
        self.state = ['move', 'death']
        self.image_list = s.cut_graphic('graphic/enemies.png', 0, 16, 16, 16, 760, 96)
        self.index = 0
        self.image = self.image_list[self.index]
        self.image = pg.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(center = (pos[0], pos[1] -10))
        self.kind = kind
        self.display_surface = surface
        self.move_left = True
        self.move_right = False
        self.vel_y = 0
        self.flip = False
        self.flip_y = False
        self.alive_1 = True
        self.kick = False
        self.temp = 0

    def state_manager(self):

        if self.kind == 'mosh':
            if self.state == 'move':
                self.index += 0.1
                if self.index >= 2:
                    self.index = 0
            elif self.state == 'death':
                self.index = 2
        elif self.kind == 'duck':
            if self.state == 'move':
                self.index += 0.1
                if self.index >= 2:
                    self.index = 0
            elif self.state == 'death':
                self.index = 4
        elif self.kind == 'duck_death':
            if self.state == 'station':
                self.index = 4
            elif self.state == 'move':
                self.index = 5
        elif self.kind == 'fly_duck':
            if self.state == 'move':
                self.index += 0.1
                if self.index >= 2:
                    self.index = 0
            elif self.state == 'fly':
                self.temp += 0.1
                self.index = 2 + self.temp
                if self.index >= 4:
                    self.temp = 0
                    self.index = 2
            elif self.state == 'death':
                self.index = 4
        elif self.kind == 'monkey':
            if self.state == 'move':
                self.index += 0.1
                if self.index >= 2:
                    self.index = 0
            elif self.state == 'death':
                self.index = 1
            elif self.state == 'attack':
                self.temp += 0.1
                self.index = 2+ self.temp
                if self.temp >= 2:
                    self.temp = 0
                    self.index = 2

        self.image = self.image_list[int(self.index)]
        self.image = pg.transform.scale(self.image, (self.size, self.size))

    def check_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.index = int(self.index)
            return  self.state, self.index

    def ai_move(self):
        dx, dy = 0, 0
        dx = self.speed * self.direction
        if self.move_left:
            self.direction = -1
        elif self.move_right:
            self.direction = 1
        else:
            self.move_left = False
            self.move_right = False

        if self.move_right or self.move_left:
            self.check_state('move')

        self.vel_y += s.gravity

        self.rect.centery += self.vel_y
        self.rect.centerx += dx

    def draw(self):
        self.display_surface.blit(pg.transform.flip(self.image, self.flip, self.flip_y), self.rect)

    def update(self, schroll):
        self.rect.centerx += schroll
        self.draw()
        self.state_manager()
        if self.alive_1:
            self.ai_move()

        #pg.draw.rect(self.display_surface, (0,0,0), self.rect, 1)
        if self.rect.top > 630:
            self.kill()

class Mosh(Enemies):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size, surface, 'mosh')

class Duck(Enemies):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size, surface, 'duck')
        self.image_list = s.cut_graphic('graphic/enemies.png',95,8,16,24, 616,94)

class Duck_death(Enemies):
    def __init__(self,pos, size, surface):
        super().__init__(pos, size, surface, 'duck_death')
        self.image_list = s.cut_graphic('graphic/enemies.png',96,8,16,24, 616,94)
        self.move_left = False
        self.move_right = False
        self.move = False
    def ai_move(self):
        dx, dy = 0, 0
        if self.move_left:
            self.direction = -1
        elif self.move_right:
            self.direction = 1
        elif not self.move:
            self.move_left = False
            self.move_right = False

        if (self.move_right or self.move_left) and self.move:
            dx = 7 * self.direction
            self.check_state('move')
        if not self.move:
            self.check_state('station')

        self.vel_y += s.gravity
        self.rect.centery += self.vel_y
        self.rect.centerx += dx

    def update(self, schroll):
        self.rect.centerx += schroll
        self.draw()
        self.state_manager()
        self.ai_move()
        #pg.draw.rect(self.display_surface, (0,0,0), self.rect, 1)
        if self.rect.top > 630:
            self.kill()

class Fly_duck(Enemies):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size, surface, 'fly_duck')
        self.image_list = s.cut_graphic('graphic/enemies.png',96,8,16,24, 616,94)
        self.fly = True
        self.jump = True
        self.move_left = True
        self.move_right = False
        self.turn_to_duck = False
    def ai_move(self):
        dx, dy = 0, 0
        if self.move_left:
            self.direction = -1
        elif self.move_right:
            self.direction = 1
        elif not self.move:
            self.move_left = False
            self.move_right = False
        if self.fly:# and self.jump:
            self.vel_y = - 10
            self.fly = False
        if (self.move_right or self.move_left):
            dx = self.speed * self.direction
            if self.fly or self.jump:
                self.check_state('fly')
            else:
                self.check_state('move')

        self.vel_y += s.gravity
        self.rect.centery += self.vel_y
        self.rect.centerx += dx

    def update(self, schroll):
        self.rect.centerx += schroll
        self.draw()
        self.state_manager()
        self.ai_move()
        #pg.draw.rect(self.display_surface, (0, 0, 0), self.rect, 1)
        if self.rect.top > 630:
            self.kill()

class Monkey(Enemies):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size, surface, 'monkey')
        self.health = 100
        self.count = 0
        self.attack = False
        self.attack_delay = 40
        self.vision_rect = pg.Rect(0, 0,150,25)
        self.image_list = s.cut_graphic('graphic/enemies.png',320,8,16,25,423,95)
        self.hammer_group = pg.sprite.Group()

    def ai_move(self):
        dx, dy = 0, 0

        dx = self.speed * self.direction
        if self.move_left:
            self.direction = - 1
            self.vision_rect = pg.Rect(self.rect.centerx + 350 * self.direction, self.rect.top, 350, 40)
            self.flip = False
        elif self.move_right:
            self.direction = 1
            self.vision_rect = pg.Rect(self.rect.centerx, self.rect.top, 250, 40)
            self.flip = True
        #else:
        #    self.move_left = False
        #    self.move_right = False

        if self.move_right or self.move_left:
            self.check_state('move')
        if self.attack and self.attack_delay <=0:
            self.vel_y = - 5
            self.check_state('attack')
            self.attack_delay = 40
            hammer = Hammer(self.rect.center, 30)
            hammer.vel_y = - 5
            hammer.direction = self.direction
            self.hammer_group.add(hammer)

        if self.attack_delay > 0:
            self.attack_delay -= 1

        self.vel_y += s.gravity

        self.rect.centery += self.vel_y
        self.rect.centerx += dx

        #pg.draw.rect(self.display_surface, (255, 0, 0), self.vision_rect,1)

    def reverse(self):
        self.count += 1
        if self.count >= 200:
            self.direction *= -1
            if self.move_left:
                self.move_right = True
                self.move_left = False
            else:
                self.move_right = False
                self.move_left = True
            self.count = 0

    def check_death(self):
        if self.health <=0:
            self.alive = False

    def update(self, schroll):
        self.check_death()
        self.rect.centerx += schroll
        self.reverse()
        self.draw()
        self.state_manager()
        if self.alive_1:
            self.ai_move()
        self.hammer_group.draw(self.display_surface)
        self.hammer_group.update(schroll)

class Hammer(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.size = size
        self.image_list = s.cut_graphic('graphic/enemies.png',384,0,15,17,392,96)
        self.index = 0
        self.image = self.image_list[self.index].convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (size, size))
        self.rect = self.image.get_rect(center = pos)
        self.speed = 5
        self.vel_y = 0
        self.direction = 1

    def animated(self):
        self.index += 0.1
        if self.index >= len(self.image_list):
            self.index = 0
        self.image = self.image_list[int(self.index)].convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (self.size, self.size))

    def update(self, schroll):
        self.animated()
        dy =0
        dx= self.speed* self.direction
        self.rect.centerx += dx
        self.rect.centerx += schroll
        self.vel_y += 0.2
        dy += self.vel_y
        self.rect.centery += dy





