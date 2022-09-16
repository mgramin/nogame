from hkb_diamondsquare import DiamondSquare
from enum import Enum

import random


class TextureType(Enum):
    EARTH = 'earth'
    WATER = 'water'

class Texture():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type


textures = {
    "grass_left_top_corner":        Texture(0,1, 'earth'),
    "grass_left_border":            Texture(0,2, 'earth'),
    "grass_left_bottom_corner":     Texture(0,3, 'earth'),
    "grass_top_border":             Texture(1,1, 'earth'),
    "grass":                        Texture(1,2, 'earth'),
    "grass_bottom_border":          Texture(1,3, 'earth'),
    "grass_right_top_corner":       Texture(2,1, 'earth'),
    "grass_right_border":           Texture(2,2, 'earth'),
    "grass_right_bottom_corner":    Texture(2,3, 'earth'),
    "grass_with_flowers":           Texture(1,6, 'earth'),
    "water":                        Texture(19,4, 'water'),
    "water_top_border":             Texture(17,16, 'water')
}


class Tile():
    def __init__(self, x, y, height, texture):
        self.x = x
        self.y = y
        self.height = height
        self.texture = texture
        # self.current = map[i][j]
        # self.left = ""
        # self.right = ""
        # self.top = ""
        # self.bottom = ""
        # self.top_right = ""
        # self.top_left = ""
        # self.bottom_right = ""
        # self.bottom_left = ""


def generate_earth_and_water(func):

    def inner(*args, **kwargs):
        origin = func(*args, **kwargs)
        for i in range(len(origin)):
            for j in range(len(origin[i])):
                tile = origin[i][j]
                if origin[i][j].height > 4:
                    tile.texture = textures['grass']
                else:
                    tile.texture = textures['water']
        return origin
                
    return inner


def generate_flowers(func):
    def inner(*args, **kwargs):
        origin = func(*args, **kwargs)

        for i in range(len(origin)):
            for j in range(len(origin[i])):
                if origin[i][j].texture.type == 'earth':
                    v = bool(random.getrandbits(1))
                    if v == True:
                        origin[i][j].texture = textures['grass_with_flowers']
        return origin
                
    return inner



def generate_coasts(func):

    def inner(*args, **kwargs):
        origin = func(*args, **kwargs)

        for i in range(len(origin)):
            for j in range(len(origin[i])):
                if origin[i][j].texture.type == "water" and origin[i][j-1].texture.type == 'earth':
                    origin[i][j].texture = textures["water_top_border"]

                
                if origin[i][j].texture.type == "earth" and origin[i-1][j].texture.type == "water":
                    origin[i][j].texture = textures["grass_left_border"]

                if origin[i][j].texture.type == "earth" and i+1<len(origin) and origin[i+1][j].texture.type == "water":
                    origin[i][j].texture = textures["grass_right_border"]

                if origin[i][j].texture.type == "earth" and origin[i][j-1].texture.type == "water":
                    origin[i][j].texture = textures["grass_top_border"]

        return origin

    return inner


@generate_coasts
@generate_flowers
@generate_earth_and_water
def generate_world():
    height_map = DiamondSquare.diamond_square(shape=(200, 200), min_height=0, max_height=10, roughness=0.2)
    new_map = []
    for i in range(len(height_map)):
        new_map.append([])
        for j in range(len(height_map[i])):
            new_map[i].append(Tile(i, j, height_map[i][j], None))
    return new_map
