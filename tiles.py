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
        """Animate the tile sprite"""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))
    
    def update(self):
        """Update the tile sprite"""
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

    def bleed(self):
        """Tints the waterfall red"""
        new_surf_list = []
        for frame in self.frames:
            new_frame = tint_icon(frame, RED)
            new_surf_list.append(new_frame)
        self.frames = new_surf_list
    
    def freeze(self):
        """Freezes the waterfall. Stops animation and tints the image"""
        self.frozen = True
        self.animation_speed = 0
        new_frame = tint_icon(self.frames[0], LIGHT_BLUE)
        self.image = pygame.transform.scale(new_frame, (TILE_SIZE, TILE_SIZE))
    
    def animate(self):
        """Animate the tile sprite"""
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
        """Opens the door if the player has a key"""
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
        """Opens the chest and adds the contents to the player's inventory"""
        if self.state == 'closed':
            self.image = pygame.image.load('graphics/chest/open.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            player.add_inventory(self.contents)
            self.state = 'open'
            
class PullChain(StaticTile):
    def __init__(self, pos, state = 'down'):
        self.state = state
        self.prep_images()
        
        super().__init__(pos, TILE_SIZE, self.image)
        
    def prep_images(self):
        """loads and scales the images for the pull chain"""
        if self.state == 'down':
            #combies base and tip image
            #loads
            base = pygame.image.load('graphics/chain/base.png').convert_alpha()
            tip = pygame.image.load('graphics/chain/tip.png').convert_alpha()
            #resizes
            base = pygame.transform.scale(base, (TILE_SIZE, TILE_SIZE))
            tip = pygame.transform.scale(tip, (TILE_SIZE, TILE_SIZE))
            #combines
            image = pygame.Surface((TILE_SIZE, TILE_SIZE*2))
            image.blit(base, (0,0))
            image.blit(tip, (0, TILE_SIZE))
            
            self.image = image
            
        if self.state == 'up':
            tip = pygame.image.load('graphics/chain/tip.png').convert_alpha()
            tip = pygame.transform.scale(tip, (TILE_SIZE, TILE_SIZE))
            self.image = tip
            
    def interact(self, player):
        """Pulls the chain up or down"""
        if self.state == 'down':
            self.state = 'up'
            self.prep_images()
        else:
            self.state = 'down'
            self.prep_images()
    
    def tint(self, color):
        """Tints the chain"""
        self.image = tint_icon(self.image, color)
    
class Button(StaticTile):
    def __init__(self, pos, state = 'off'):
        self.state = state
        self.image = pygame.image.load('graphics/button/'+ state + '.png').convert_alpha()
        self.surface = self.image
       # self.surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        super().__init__(pos, TILE_SIZE, self.surface)
        
    def interact(self, player):
        """Toggles the button state"""
        if self.state == 'off':
            self.state = 'on'
        else:
            self.state = 'off'    
        self.image = pygame.image.load('graphics/button/' + self.state + 'png').convert_alpha()
      #  self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))         
            
class Spike(StaticTile):
    def __init__(self, pos, type):
        terrain_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
        self.image = pygame.transform.flip(terrain_list[type], False, True)
        self.surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        super().__init__(pos, TILE_SIZE, self.surface)
    
    def bleed(self):
        """Tints the spike red"""
        self.image = tint_icon(self.image, RED)
        self.surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        
class SpikeTrap(StaticTile):
    def __init__(self, pos, pointing = 'down', extended = False):
        self.type = 'trap'
        self.pointing = pointing
        self.extended = extended
        self.prep_images()
        
        if extended:
            self.image = self.extended_img
            self.damaging =True
        else:
            self.image = self.retracted_img
            self.damaging = False
             
        super().__init__(pos, TILE_SIZE, self.image)
        
    def prep_images(self):
        """loads and scales the images for the spike trap"""
        retracted = pygame.image.load('graphics/traps/retracted.png').convert_alpha()
        extended = pygame.image.load('graphics/traps/extended.png').convert_alpha()
        
        if self.pointing == 'down':
            retracted = pygame.transform.flip(retracted, False, True)
        elif self.pointing == 'up':
            extended = pygame.transform.flip(extended, False, True)
        
        self.retracted_img = pygame.transform.scale(retracted, (TILE_SIZE, TILE_SIZE))
        self.extended_img = pygame.transform.scale(extended, (TILE_SIZE, TILE_SIZE))
        
    def step(self): 
        """alternates between extended and retracted"""
        if self.extended:
            self.image = self.retracted_img
            self.extended = False
            self.damaging = False
        else:
            self.image = self.extended_img
            self.extended = True
            self.damaging = True
            
    def bleed(self):
        """Tints the spike trap red"""
        self.image = tint_icon(self.image, RED)
            
class ItemIcon(StaticTile):
    def __init__(self, pos, item):
        self.item = item
        self.image = pygame.image.load(item[1]).convert_alpha()
        self.surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        super().__init__(pos, TILE_SIZE, self.surface)
    