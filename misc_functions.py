import pygame
from os import walk
from csv import reader
from settings import *


def import_folder(path):
    surface_list = []
    for _,__,files in walk(path):
        for image in files:
            full_path = path + '/' + image
            frame_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(frame_surf)
    return surface_list

def import_folder_dict(path):
    surface_dict = {}
    for _,__,files in walk(path):
        for image in files:
            full_path = path + '/' + image
            frame_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = frame_surf
    return surface_dict

def import_csv_layout(path):
    terrain_map = []
    with open(path) as csvfile:
        level = reader(csvfile, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILESET_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILESET_SIZE)
    
    tiles = []
    
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILESET_SIZE
            y = row * TILESET_SIZE
            new_surface = pygame.Surface((TILESET_SIZE, TILESET_SIZE), flags = pygame.SRCALPHA)
            new_surface.blit(surface, (0,0), pygame.Rect(x,y,TILESET_SIZE,TILESET_SIZE))
            tiles.append(new_surface)

    return tiles

def tint_icon(icon, tint_color):
    for x in range(icon.get_width()):
        for y in range(icon.get_height()):
            color = icon.get_at((x,y))
            
            new_color = (
                min(color[0] * tint_color[0] // 255, 255),
                min(color[1] * tint_color[1] // 255, 255),
                min(color[2] * tint_color[2] // 255, 255),
                color[3]
            )
            icon.set_at((x,y), new_color)
    return icon
