import pygame as pg
import settings as s
from tile import *
from player import *
from enemy import *
from Decoration import *
import csv

class Level():
    def __init__(self, surface, create_title):
        self.display_surface = surface
        self.create_title = create_title
        self.bg = BG((0,0), self.display_surface)
        self.water = Water(600, self.display_surface)
        self.schroll = 0
        self.con = 0
        self.screen_out = Screen_out((0,0), 6, self.display_surface)
        self.import_csv()

        self.brick = pg.sprite.Group()
        self.empty_box = pg.sprite.Group()
        self.fire_group = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        self.mushroom = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()
        self.boom_group = pg.sprite.Group()
        self.duck_death = pg.sprite.Group()
        self.hammer_group = pg.sprite.Group()

        self.player = Player((300, 170), self.display_surface)
        self.player_dambox = pg.Rect(0, 0, 30, 20)

        self.screen_fade = Screen_fade((self.player.rect.center), self.display_surface, 850, -1, 20)
        self.sum = 0
        self.last_time = pg.time.get_ticks()
        self.current_time = pg.time.get_ticks()
        self.fire_trans_time = pg.time.get_ticks()
        self.get_time = pg.time.get_ticks()
        self.small_trans_time = pg.time.get_ticks()
        self.incredible_time = pg.time.get_ticks()
        self.duck_time = pg.time.get_ticks()
        self.finish_time = pg.time.get_ticks()
        self.finish = False
        self.game_over = False

        self.pole = pg.Rect(8300,150,5,400)
        self.flag = s.just_graphic('graphic/item_objects.png',129,0,15,16,432,319).convert_alpha()
        self.flag = pg.transform.scale(self.flag,(40,40))
        self.flag_rect = self.flag.get_rect(topleft = (8300,150))
        self.flag_brick = s.just_graphic('graphic/tile_set.png',0,16,16,16,511,416).convert_alpha()
        self.flag_brick = pg.transform.scale(self.flag_brick, (45,45))
        self.flag_brick_rect = self.flag_brick.get_rect(center= (8300,540))
        self.brick_bounce = False
        s.load_music('music/main_theme.ogg', -1, True)

    def set_tile(self, layout):
        self.tile_group = pg.sprite.Group()
        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                y = row_index * s.TILE_SIZE
                x = cell_index * s.TILE_SIZE
                if cell == 'x':
                    tile = Static_tile((x, y), s.TILE_SIZE, 1)
                    self.tile_group.add(tile)
                elif cell == '0':
                    tile = Static_tile((x, y), s.TILE_SIZE, 0)
                    self.tile_group.add(tile)

    def import_csv(self):
        self.tile_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        with open('graphic/level/map.csv', newline='') as file:
            data = csv.reader(file, delimiter=',')
            for row_index, row in enumerate(data):
                for col_index, cell in enumerate(row):
                    x = col_index * s.TILE_SIZE
                    y = row_index * s.TILE_SIZE
                    if cell == '0':# terrain
                        tile = Static_tile((x, y), s.TILE_SIZE, 0)
                        self.tile_group.add(tile)
                    elif cell == '1':# brick
                        tile = Static_tile((x, y), s.TILE_SIZE, 1)
                        self.tile_group.add(tile)
                    elif cell == '2':# Item_box
                        tile = Item_box((x,y), s.TILE_SIZE, 'mush')
                        self.tile_group.add(tile)
                    elif cell == '3':
                        tile = Item_box((x,y), s.TILE_SIZE, 'coin')
                        self.tile_group.add(tile)
                    elif cell == '4':
                        tile = Item_box((x,y), s.TILE_SIZE, 'fire')
                        self.tile_group.add(tile)
                    elif cell == '16':
                        mosh = Mosh((x,y), 40, self.display_surface)
                        self.enemy_group.add(mosh)
                    elif cell == '17':
                        duck = Duck((x,y), 40, self.display_surface)
                        self.enemy_group.add(duck)
                    elif cell == '18':
                        fly_duck = Fly_duck((x,y), 40, self.display_surface)
                        self.enemy_group.add(fly_duck)
                    elif cell == '19':
                        monkey = Monkey((x,y), 50, self.display_surface)
                        self.enemy_group.add(monkey)

    def check_game_state(self):
        if not self.player.alive:
            s.load_music('music/death.wav', 0, True)
            self.screen_fade = Screen_fade(self.player.rect.center, self.display_surface, 1000, -1, 24)
            self.game_over = True
            self.player.alive = True
        if self.game_over:
            self.player.check_status('death')
            if self.screen_fade.dra():
                self.create_title()

    def check_colli(self):
        for tile in self.tile_group:
            if tile.rect.colliderect(self.player.rect):
                if tile.rect.top < self.player.rect.centery < tile.rect.bottom:
                    self.player.time = 0
                    self.player.speed = 0
                    if self.player.move_left and self.player.rect.centerx > tile.rect.right:
                        self.player.rect.left = tile.rect.right + 10
                    elif self.player.move_right and self.player.rect.centerx < tile.rect.left:
                        self.player.rect.right = tile.rect.left - 10
                    elif tile.rect.left < self.player.rect.centerx < tile.rect.right:
                        self.player.rect.bottom = tile.rect.top

                else:
                    if self.player.vel_y < 0:
                        self.player.rect.top = tile.rect.bottom
                        self.player.vel_y = 0
                        if tile.type == 1: # bricks
                            if not self.player.big:
                                tile.bounced()
                            else:
                                tile.breakk = True
                                tile.kill()
                                s.load_music('sound/brick_smash.ogg', 0, False)
                                brick_break = Brick_break(tile.rect.center, s.TILE_SIZE)
                                self.brick.add(brick_break)
                                brick_break.brick = True
                            self.last_time = pg.time.get_ticks()
                        elif tile.type == 'box': # Itemboxes
                            tile.kill()
                            empty_box = Static_tile(tile.rect.center, s.TILE_SIZE, 3)
                            self.tile_group.add(empty_box) # become empty box afer colli
                            if tile.kind == 'fire': #fire flower
                                fire = Fire(tile.rect.center, s.TILE_SIZE)
                                self.fire_group.add(fire)
                            elif tile.kind == 'coin': #coin box
                                coin = Coin_box(tile.rect.center, s.TILE_SIZE)
                                self.coin_group.add(coin)
                                s.load_music('sound/coin.ogg',0,False)
                            elif tile.kind == 'mush': #mushroom
                                mushroom = Mush_room(tile.rect.center, s.TILE_SIZE)#, self.display_surface)
                                self.mushroom.add(mushroom)

                    elif self.player.vel_y > 0:
                        self.player.rect.bottom = tile.rect.top
                        self.player.vel_y = 0
                        self.player.in_air = False
            #brick bounce back
            if tile.bounce and (pg.time.get_ticks() - self.last_time) > 100:
                s.load_music('sound/bump.ogg',0,False)
                tile.rect.centery += 10
                tile.bounce = False

    def check_mushroom_colli(self):
        for mushroom in self.mushroom:
            #mushroom collide with tile
            for tile in self.tile_group:
                if tile.rect.colliderect(mushroom.rect):
                    if tile.rect.top < mushroom.rect.centery < tile.rect.bottom:
                        mushroom.direction *= -1
                    else:
                        if mushroom.direction != 0 and tile.bounce:
                            mushroom.direction *= -1
                        if mushroom.vel_y > 0:
                            mushroom.rect.bottom = tile.rect.top
                            mushroom.vel_y = 0
            #mushroom colli player
            if mushroom.rect.colliderect(self.player.rect):
                self.current_time = pg.time.get_ticks()
                mushroom.kill()
                if not self.player.fire: #fire can not be big
                    self.player.big = True
                    self.player.small = False
                    self.player.check_status('idle')
                    self.player.transform(self.player.rect.center)
                    self.player.trans = True
        #player transforming:
        if self.player.trans:
            s.load_music('sound/powerup.ogg',0,False)
            self.player.check_status('big_trans')
            if pg.time.get_ticks() - self.current_time > 700:
                self.player.trans = False
                self.current_time = pg.time.get_ticks()

    def check_can_fire(self):
        for fire in self.fire_group:
            if fire.rect.colliderect(self.player.rect):
                self.player.fire = True
                self.player.big = False
                self.player.fire_trans = True
                self.fire_trans_time = pg.time.get_ticks()
                self.player.transform(self.player.rect.center)
                fire.kill()

        if self.player.fire_trans:
            self.player.check_status('idle')
            s.load_music('sound/powerup.ogg',0,False)
            if self.player.small:
                self.player.check_status('fire_trans_2')
                self.player.small = False
            else:
                self.player.check_status('fire_trans')
            if pg.time.get_ticks() - self.fire_trans_time > 700:
                self.player.fire_trans = False
                self.fire_trans_time = pg.time.get_ticks()
        #create bullet
        if self.player.fire and self.player.firing:
            bullet = Bullet((self.player.rect.centerx + 20, self.player.rect.centery -20), s.TILE_SIZE, self.display_surface)
            bullet.direction = self.player.direction
            self.bullet_group.add(bullet)

        for bullet in self.bullet_group:
            for tile in self.tile_group:
                if bullet.rect.colliderect(tile.rect):
                    if tile.rect.top < bullet.rect.centery < tile.rect.bottom:
                        s.load_music('sound/kick.ogg', 0, False)
                        boom = Boom((bullet.rect.center), 16)
                        self.boom_group.add(boom)
                        bullet.kill()
                    else:
                        if bullet.vel_y > 0:
                            bullet.rect.bottom = tile.rect.top
                            bullet.vel_y *= - 0.7

                        else:
                            bullet.rect.top = tile.rect.bottom
                            bullet.vel_y *= -1

    def enemy_colli(self):
        self.player_dambox = pg.Rect(self.player.rect.bottomleft[0], self.player.rect.bottomleft[1], 40, 30)
        #pg.draw.rect(self.display_surface, (0, 0, 0), self.player_dambox, 1)
        for enemy in self.enemy_group:
            for tile in self.tile_group:
                #if enemy.alive:
                    if tile.rect.colliderect(enemy.rect) and enemy.alive:
                        if tile.rect.top < enemy.rect.centery < tile.rect.bottom:
                            enemy.direction *= -1
                            if enemy.move_left:
                                enemy.rect.left = tile.rect.right + 10
                                enemy.move_left = False
                                enemy.move_right = True
                                enemy.flip = True
                            elif enemy.move_right:
                                enemy.rect.right = tile.rect.left - 10
                                enemy.move_left = True
                                enemy.move_right = False
                                enemy.flip = False
                        else:
                            if enemy.vel_y > 0:
                                enemy.vel_y = 0
                                enemy.rect.bottom = tile.rect.top
                                if enemy.kind == 'fly_duck':# and enemy.jump:
                                    enemy.fly = True
                        if tile.bounce or tile.breakk:
                            enemy.rect.centery += 5
                            enemy.alive = False
                            enemy.flip_y = True
            #dam enemy
            if enemy.alive:
                if self.player_dambox.colliderect(enemy.rect) and enemy.alive_1:
                    self.player.vel_y = -3
                    s.load_music('sound/stomp.ogg', 0, False)
                    if enemy.kind == 'fly_duck':
                        enemy.fly = False
                        enemy.jump = False
                        enemy.turn_to_duck = True
                        self.duck_time = pg.time.get_ticks()
                    else:
                        enemy.alive_1 = False
                        enemy.check_state('death')
                        self.get_time = pg.time.get_ticks()

                # player colli enemy and transfer small
                #if enemy.alive:
                if self.player.rect.colliderect(enemy.rect) and enemy.alive_1:
                    self.check_death('0')
                    if not self.player.incredible and not self.player.trans_small and enemy.alive_1 \
                             and not self.player_dambox.colliderect(enemy.rect) and self.player.small\
                            and not self.game_over:
                        self.player.alive = False

            #fly duck become duck:
            if enemy.kind == 'fly_duck' and enemy.turn_to_duck:
                #if enemy.turn_to_duck:
                    if pg.time.get_ticks() - self.duck_time > 400:
                        enemy.kill()
                        duck = Duck((enemy.rect.center), 40, self.display_surface)
                        self.enemy_group.add(duck)
                        #self.current_time = pg.time.get_ticks()
                        enemy.turn_to_duck = False

            # bullet hit enemy
            for bullet in self.bullet_group:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.kill()
                    s.load_music('sound/kick.ogg',0,False)
                    boom = Boom((bullet.rect.center), 16)
                    self.boom_group.add(boom)
                    if enemy.kind == 'monkey':
                        enemy.health -= 15

                    else:
                        enemy.alive = False
                        enemy.flip_y = True

            if not enemy.alive_1:
                #not duck then be killed
                if enemy.kind != 'duck':
                    if pg.time.get_ticks() - self.get_time > 500:
                        enemy.kill()
                #duck will be kick
                else: #self.player.rect.colliderect(enemy.rect):
                    #enemy.kick = True
                    enemy.kill()
                    duck_d = Duck_death(enemy.rect.center, 40, self.display_surface)
                    self.duck_death.add(duck_d)

            #if enemy.kick:
            #    if enemy.alive:
            #        s.load_music('sound/kick.ogg',0,False)
            #        enemy.kill()
            #        duck_d = Duck_death(enemy.rect.center, 40, self.display_surface)
            #        self.duck_death.add(duck_d)
            #    elif not enemy.alive and not enemy.alive_1:
            #        enemy.ai_move()

            if enemy.kind == 'monkey':
                if enemy.vision_rect.colliderect(self.player.rect):
                    enemy.attack = True
                    enemy.move_left = False
                    enemy.move_right = False
                else:
                    enemy.attack = False
                for hammer in enemy.hammer_group:
                    if hammer.rect.colliderect(self.player.rect):
                        self.check_death('1')

        if self.player.trans_small:
            self.player.check_status('small_trans')
            if pg.time.get_ticks() - self.current_time > 500:
                self.player.trans_small = False
                self.player.incredible = True
                self.incredible_time = pg.time.get_ticks()
        if self.player.incredible:
            if pg.time.get_ticks() - self.incredible_time > 1500:
                self.player.incredible = False

    def duck_death_coli(self):
        for duck in self.duck_death:
            for tile in self.tile_group:
                #if duck.alive:
                    if duck.rect.colliderect(tile.rect) and duck.alive:
                        if tile.rect.top < duck.rect.centery < tile.rect.bottom:
                            duck.direction *= -1
                            if duck.move_left:
                                duck.rect.left = tile.rect.right + 10
                                duck.move_left = False
                                duck.move_right = True
                                duck.flip = True
                            elif duck.move_right:
                                duck.rect.right = tile.rect.left - 10
                                duck.move_left = True
                                duck.move_right = False
                                duck.flip = False
                        else:
                            if duck.vel_y > 0:
                                duck.vel_y = 0
                                duck.rect.bottom = tile.rect.top

            if self.player_dambox.colliderect(duck.rect):
                duck.move = False
                self.player.vel_y = -2

            if self.player.rect.colliderect(duck.rect):
                duck.move = True
                s.load_music('sound/kick.ogg',0,False)
                #if self.player.vel_y > 0:
                #    self.player.rect.bottom = duck.rect.top
                if self.player.direction > 0 and self.player.move_right:
                    duck.move_right = True
                    duck.move_left = False
                elif self.player.direction <0 and self.player.move_left:
                    duck.move_left = True
                    duck.move_right = False

            for bullet in self.bullet_group:
                if bullet.rect.colliderect(duck.rect):
                    bullet.kill()
                    duck.alive = False
                    duck.flip_y = True
                    boom = Boom((bullet.rect.center), 16)
                    self.boom_group.add(boom)

            for enemy in self.enemy_group:
                if duck.rect.colliderect(enemy.rect) and duck.move:
                    enemy.alive = False
                    enemy.flip_y = True


    def bg_schroll(self):
        if self.player.move_right and self.player.rect.centerx >= 550 and not self.game_over:
            self.schroll = - 5
            self.player.speed = 0
            self.player.time = 0
        elif self.player.move_left and self.player.rect.centerx <= 250 and not self.game_over:
            self.schroll =  5
            self.player.speed = 0
            self.player.time = 0
        else:
            self.player.speed = 2
            self.schroll = 0

    def check_death(self, status):
        #trans small
        self.current_time = pg.time.get_ticks()
        if self.player.big or self.player.fire:
            self.player.trans_small = True
            self.player.big = False
            self.player.fire = False
            self.player.small = True
            self.player.check_status('idle')
            self.player.transform(self.player.rect.center)

        # player death condition
        elif not self.player.incredible and not self.player.trans_small and status == '1':
            self.player.alive = False
            self.screen_fade = Screen_fade((self.player.rect.center), self.display_surface, 850, -1)

    def update_rect(self, new_pos):
        if self.player.rect.center != new_pos:
            self.player.rect.center = new_pos
            return self.player.rect.center

    def draw_line(self):
        pg.draw.rect(self.display_surface, (255,255,200), self.pole)
        self.display_surface.blit(self.flag, self.flag_rect)
        self.display_surface.blit(self.flag_brick, self.flag_brick_rect)
        self.flag_brick_rect.centerx += self.schroll
        self.pole.centerx += self.schroll
        self.flag_rect.centerx += self.schroll
        self.flag_rect.centery += self.con

    def check_finish(self):
        if self.player.rect.colliderect(self.pole) and self.flag_rect.centery <= 180:
            s.load_music('music/flagpole.wav', 0, True)
            self.player.get_pole = True
        if self.player.get_pole:
            self.con = 5
            self.schroll = 0
            if self.flag_rect.centery >= 490:
                self.player.get_pole = False
                self.finish_time = pg.time.get_ticks()
                self.finish = True
                #self.create_title()
        else:
            self.con = 0
        if self.finish and pg.time.get_ticks() - self.finish_time >= 700:
            self.create_title()

    def run(self):
        self.check_finish()
        self.bg.draw()
        self.brick.draw(self.display_surface)
        self.brick.update(self.schroll)

        self.empty_box.draw(self.display_surface)
        self.empty_box.update(self.schroll)

        self.fire_group.draw(self.display_surface)
        self.fire_group.update(self.schroll)

        self.coin_group.draw(self.display_surface)
        self.coin_group.update(self.schroll)

        self.mushroom.draw(self.display_surface)

        self.mushroom.update(self.schroll)
        #pg.draw.rect(self.display_surface, (0,0,0), mushroom.rect, 1)

        self.tile_group.draw(self.display_surface)
        self.tile_group.update(self.schroll)

        self.check_mushroom_colli()
        self.check_can_fire()

        for enemy in self.enemy_group:
            enemy.update(self.schroll)

        for bullet in self.bullet_group:
            bullet.update(self.schroll)

        self.duck_death.draw(self.display_surface)
        self.duck_death.update(self.schroll)
        self.duck_death_coli()

        self.boom_group.draw(self.display_surface)
        self.boom_group.update(self.schroll)

        self.water.update()
        self.check_colli()
        self.enemy_colli()

        self.draw_line()
        self.player.update()

        self.check_game_state()
        self.screen_out.update()

        self.bg_schroll()