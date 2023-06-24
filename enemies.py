import pygame
from debug import debug

from settings import *
from misc_functions import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, type = '1'):
        super().__init__()
        self.pos = pos
        
        self.frames = import_folder('graphics/enemy_0'+type)
        self.frame_index = 0
        self.animation_speed = .05
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft = self.pos)
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))
        
    def update(self):
        self.animate()