import pygame
from debug import debug

from settings import *
from misc_functions import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, check_enemy_constraints, type = '1'):
        super().__init__()
        #movement
        self.pos = pos
        self.facing = 'left'
        self.speed = 64
        self.check_enemey_constraints = check_enemy_constraints
        
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
        if self.facing == 'right':
            self.image = pygame.transform.flip(self.image, True, False)
     
    def move(self):
        test_rect = self.rect.copy()
        if self.facing =='right':
            test_rect.x += self.speed
        elif self.facing == 'left':
            test_rect.x -= self.speed
            
        if not self.check_enemey_constraints(test_rect):
            self.rect = test_rect
            self.pos = test_rect.topleft
        else:
            if self.facing == 'right':
                self.facing = 'left'
            elif self.facing == 'left':
                self.facing = 'right'
    
    def step(self):
        self.move()
    
    def update(self):
        self.animate()
