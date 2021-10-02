import pygame as pg
import csv
from tile import *
level_map = ['                     ',
            'xxxxx              xxx',
            'xxxxxx           xxxxx',
            '                      ',
            '              xx      ',
            '                      ',
            '      xxxxxxxxx       ',
            '   xxxxxxxxxxxxxx     ',
            '                      ',
            'xxx               xxx ',
            'xxx               xxx ',
            '                      ',
            '                       ',
            '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
            '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000']
#tile
TILE_SIZE = 45
width, height = 850, 630
#character
gravity = 0.75
speed = 3
vel_y = 0
acerlerate = 2
max_speed = 20
#image
number_of_row = 20
number_of_cell = 13
fps = 60
#color:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def cut_graphic(path, off_set_x, off_set_y, x_size, y_size, off_set_width, off_set_high):
    image_list = []
    image= pg.image.load(path).convert_alpha()
    size_width = x_size
    size_high = y_size
    image_width = image.get_width()- off_set_width - off_set_x
    image_high = image.get_height()- off_set_high - off_set_y
    number_x = int(image_width/size_width)
    number_y = int(image_high/size_high)
    for row in range(number_y):
        for cell in range(number_x):
            y = row * size_high + off_set_y
            x = cell * size_width + off_set_x
            new_surf = pg.Surface((x_size, y_size), flags= pg.SRCALPHA)
            new_surf.blit(image, (0, 0), pg.Rect(x, y, x_size, y_size))
            image_list.append(new_surf)
        return image_list

def import_csv():
    with open('graphic/level/map.csv', newline= '') as file:
        data = csv.reader(file, delimiter= ',')
        for row_index, row in enumerate(data):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == '0':
                    tile = Static_tile((x, y), TILE_SIZE, 0)
                elif cell == '1':
                    tile = Static_tile((x,y), TILE_SIZE, 1)

def impro_cut_graphic(path, off_set_x, off_set_y, x_size, y_size, off_set_width, off_set_high):
    image_list = []
    image= pg.image.load(path).convert_alpha()
    size_width = x_size
    size_high = y_size
    image_width = image.get_width()- off_set_width - off_set_x
    image_high = image.get_height()- off_set_high - off_set_y
    number_x = int(image_width/size_width)
    number_y = int(image_high/size_high)

    for cell in range(number_x):
        for row in range(number_y):
            y = row * size_high + off_set_y
            x = cell * size_width + off_set_x
            new_surf = pg.Surface((x_size, y_size), flags= pg.SRCALPHA)
            new_surf.blit(image, (0, 0), pg.Rect(x, y, x_size, y_size))
            image_list.append(new_surf)
        return image_list

def just_graphic(path, off_set_x, off_set_y, x_size, y_size, off_set_width, off_set_high):
    image_list = []
    image = pg.image.load(path).convert_alpha()
    size_width = x_size
    size_high = y_size
    image_width = image.get_width() - off_set_width - off_set_x
    image_high = image.get_height() - off_set_high - off_set_y
    new_surf = pg.Surface((x_size, y_size), flags=pg.SRCALPHA)
    new_surf.blit(image, (0, 0), pg.Rect(off_set_x, off_set_y, x_size, y_size))
    return new_surf

def load_music(path,loop, start):
    if start:
        pg.mixer.stop()
    audio = pg.mixer.Sound(path)
    audio.play(loop)


