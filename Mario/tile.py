import pygame as pg
import settings as s
import player as p

class Tile(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pg.Surface((size, size))
        #self.rect = pg.Rect(pos[0],pos[1], size, size)
        self.image.fill(s.BLACK)
        self.rect = self.image.get_rect(center = pos)

    def update(self, schroll):
        self.rect.centerx += schroll

class Static_tile(Tile):
    def __init__(self, pos, size, i):
        super().__init__(pos, size)
        self.type = i
        self.image = s.cut_graphic('graphic/tile_set.png', 0, 0, 16, 16, 464, 432)[i]
        self.image = pg.transform.scale(self.image, (size, size)).convert_alpha()
        self.last_time = pg.time.get_ticks()
        self.bounce = False
        self.breakk = False
    def bounced(self):
        self.rect.centery -= 10
        self.bounce = True


class Animated_tile(Tile):
    def __init__(self, pos, size, path, off_set_x, off_set_y, xsize, ysize, off_set_wid, off_set_high):
        super().__init__(pos, size)
        self.image_list = s.cut_graphic(path, off_set_x, off_set_y, xsize, ysize, off_set_wid, off_set_high)
        self.index = 0
        self.image = self.image_list[self.index]
        self.image = pg.transform.scale(self.image, (int(xsize* 2.8), int(ysize* 2.8))).convert_alpha()
        self.bounce = False
        self.breakk = False
        self.x = xsize
        self.y = ysize

    def bounced(self):
        self.rect.centery -= 10
        self.bounce = True

    def animated(self):
        self.index += 0.1
        if self.index >= len(self.image_list):
            self.index = 0
        self.image = self.image_list[int(self.index)]
        self.image = pg.transform.scale(self.image, (int(self.x* 2.8), int(self.y* 2.8))).convert_alpha()


    def update(self, schroll):
        self.rect.centerx += schroll
        self.animated()

class Brick_break(Animated_tile):
    def __init__(self, pos, size):
        super().__init__(pos, size, 'graphic/item_objects.png', 64, 0,16, 16, 496, 288)
        self.image_list = s.impro_cut_graphic('graphic/item_objects.png', 64, 0, 16, 16, 496, 288)
        self.vel_y = 0
        self.brick = False

    def animated(self):
        self.index += 0.1
        if self.index >= len(self.image_list):
            self.index = len(self.image_list) - 1
        self.image = self.image_list[int(self.index)]
        self.image = pg.transform.scale(self.image, (45, 45)).convert_alpha()

    def update(self, schroll):
        dy = 0
        if self.brick:
            self.vel_y = -10
            self.brick = False
        self.vel_y += s.gravity
        dy += self.vel_y
        self.rect.centery += dy
        self.rect.centerx += schroll
        self.animated()
        if self.rect.top >= s.height:
            self.kill()

class Item_box(Animated_tile):
    def __init__(self, pos, size, kind):
        super().__init__(pos, size, 'graphic/item_objects.png', 0, 16*5, 16, 16, 512, 240)
        self.type = 'box'
        self.kind = kind

class Fire(Item_box):
    def __init__(self, pos, size):
        super().__init__(pos, size,'fire')
        self.image_list = s.cut_graphic('graphic/item_objects.png',0, 32, 16, 16, 512, 288)
        self.off_set = 0
        self.dy = self.rect.centery
    def update(self, schroll):
        self.off_set += 0.5
        if self.off_set >= 44:
            self.off_set = 44
        self.rect.centery = self.dy - self.off_set
        self.rect.centerx += schroll
        self.animated()

class Coin_box(Item_box):
    def __init__(self, pos, size):
        super().__init__(pos, size, 'coin')
        self.image_list = s.cut_graphic('graphic/item_objects.png', 0, 7*16, 16, 16, 512, 208)
        self.rect = self.image.get_rect(center = pos)

    def animated(self):
        self.index += 0.23
        if self.index >= len(self.image_list):
            self.index = 0
            self.kill()
        self.image = self.image_list[int(self.index)]
        self.image = pg.transform.scale(self.image, (35, 35)).convert_alpha()

    def update(self, schroll):
        self.rect.centery -= 4
        self.rect.centerx += schroll
        self.animated()

class Mush_room(Item_box):
    def __init__(self,pos, size):
        super().__init__(pos, size, 'mush')
        self.image_list = s.cut_graphic('graphic/item_objects.png', 0, 16, 16, 16, 528, 304)
        self.off_set = 0
        self.dy = self.rect.centery
        self.move_left = False
        self.move_right = False
        self.speed = 2
        self.direction = 1
        self.vel_y = 0
        self.fade = True
    def move(self):
        dx = 0
        if self.move_right:
            self.direction = 1
        elif self.move_left:
            self.direction *= -1
        else:
            self.move_right = False
            self.move_left = False
        self.vel_y += s.gravity
        dx = self.speed * self.direction
        self.rect.centerx += dx
        self.rect.centery += self.vel_y
    def update(self, schroll):
        if self.fade:
            self.off_set += 0.5
            if self.off_set >= 46:
                self.off_set = 46
                self.fade = False
            self.rect.centery = self.dy - self.off_set
        self.rect.centerx += schroll
        self.animated()
        if not  self.fade:
            self.move()

class Bullet(Animated_tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size, 'graphic/item_objects.png', 96, 143, 8, 8, 463, 175)
        self.image_list = s.cut_graphic('graphic/item_objects.png', 96, 143, 8, 8, 463, 175)
        self.rect = self.image.get_rect(center = pos)
        self.speed = 14
        self.direction = 1
        self.vel_y = 0
        self.dy = 0
        self.display_surface = surface
        self.flip = False
    def animated(self):
        self.index += 0.1
        if self.index >= len(self.image_list):
            self.index = 0
        self.image = self.image_list[int(self.index)]
        self.image = pg.transform.scale(self.image, ((4 * 3), (4 * 3))).convert_alpha()

    def trajactory(self):
        dy = 0
        self.vel_y += 0.4
        dx = self.speed * self.direction
        dy += self.vel_y
        self.rect.centerx += dx
        self.rect.centery += dy
        if self.direction > 0:
            self.flip = False
        else:
            self.flip = True

    def draw(self):
        self.display_surface.blit(pg.transform.flip(self.image, False, False), self.rect)

    def update(self, schroll):
        self.trajactory()
        self.draw()
        self.rect.centerx += schroll
        self.animated()
        if self.rect.centerx > s.width or self.rect.centerx < 0 or self.rect.centery > 630:
            self.kill()

class Boom(Animated_tile):
    def __init__(self, pos, size):
        super().__init__(pos, size, 'graphic/item_objects.png', 7*16, 143, 16, 16, 447, 143)
        self.image_list = s.impro_cut_graphic('graphic/item_objects.png', 7 * 16, 143, 16, 16, 447, 143)

    def animated(self):
        self.index += 0.3
        if self.index >= len(self.image_list):
            self.index = len(self.image_list) - 1
            self.kill()
        self.image = self.image_list[int(self.index)]
        self.image = pg.transform.scale(self.image, (25, 25)).convert_alpha()

    def update(self, schroll):
        self.rect.centerx += schroll
        self.animated()

