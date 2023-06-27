import pygame
from settings import *
from misc_functions import import_folder, import_cut_graphics, tint_icon

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
        self.type = type
        self.frozen = False
        path = 'graphics/terrain/waterfall/'+ self.type
        frames = import_folder(path)
        
        if inverted:
            new_surf_list = []
            for frame in frames:
                new_frame = pygame.transform.flip(frame, False, True)
                new_surf_list.append(new_frame)
            frames = new_surf_list
                
        super().__init__(pos, size, frames)

    def freeze(self):
        self.frozen = True
        self.animation_speed = 0
        new_frame = tint_icon(self.frames[0], LIGHT_BLUE)
        self.image = pygame.transform.scale(new_frame, (TILE_SIZE, TILE_SIZE))
    
    def animate(self):
        if not self.frozen:
            super().animate()
        
class Coin(AnimatedTile):
    def __init__(self, pos):
        path = 'graphics/coin'
        frames = import_folder(path)
        super().__init__(pos, TILE_SIZE, frames)
        self.animation_speed = .1
                
class Door(StaticTile):
    def __init__(self, pos, state = 'closed'):
        self.state = state
        self.image = pygame.image.load('graphics/door/'+ state + '.png').convert_alpha()
        self.surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        super().__init__(pos, TILE_SIZE, self.surface)
        
    def interact(self, player):
        if player.check_item_in_inventory('key') and self.state == 'closed':
            self.image = pygame.image.load('graphics/door/open.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            self.state = 'open'
            player.remove_inventory('key')

class Chest(StaticTile):
    def __init__(self, pos, contents, state = 'closed'):
        #contents is ('name', image)
        self.contents = contents
        self.state = state
        self.image = pygame.image.load('graphics/chest/'+ state + '.png').convert_alpha()
        self.surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        super().__init__(pos, TILE_SIZE, self.surface)
    
    def interact(self, player):
        if self.state == 'closed':
            self.image = pygame.image.load('graphics/chest/open.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            player.add_inventory(self.contents)
            self.state = 'open'

class Spikke(StaticTile):
    def __init__(self, pos, type):
        terrain_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
        self.image = pygame.transform.flip(terrain_list[type], False, True)
        self.surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        super().__init__(pos, TILE_SIZE, self.surface)
    
    def bleed(self):
        self.image = tint_icon(self.image, RED)
        self.surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        
    
class ItemIcon(StaticTile):
    def __init__(self, pos, item):
        self.item = item
        self.image = pygame.image.load(item[1]).convert_alpha()
        self.surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        super().__init__(pos, TILE_SIZE, self.surface)
    