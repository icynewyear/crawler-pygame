import pygame
from settings import *
from misc_functions import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = pos)
        self.image.fill(TILE_COLOR)
        
class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface

class AnimatedTile(Tile):
    def __init__(self, pos, size, frames):
        super().__init__(pos, size)
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = .05
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))
    
    def update(self):
        super().update()
        self.animate()
        
class Waterfall(AnimatedTile):
    def __init__(self, pos, size, type = 'middle', inverted = False):
        path = 'graphics/terrain/waterfall/'+ type
        frames = import_folder(path)
        
        if inverted:
            new_surf_list = []
            for frame in frames:
                new_frame = pygame.transform.flip(frame, False, True)
                new_surf_list.append(new_frame)
            frames = new_surf_list
                
        super().__init__(pos, size, frames)

class Door(StaticTile):
    def __init__(self, pos, state = 'closed'):
        print(state)
        image = pygame.image.load('graphics/door/'+ state + '.png').convert_alpha()
        
        surface = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    
        super().__init__(pos, TILE_SIZE, surface)