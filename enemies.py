import pygame
from debug import debug

from settings import *
from misc_functions import import_folder, tint_icon

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, check_enemy_constraints, add_to_enemy_sprites, type = '1'):
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
        self.screen = pygame.display.get_surface()
        
        self.type = type
        self.bleed = False
        
        self.whips = pygame.sprite.Group()
        self.add_to_enemy_sprites = add_to_enemy_sprites
        self.whiptest = True
        self.whip_stage = 0
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        frame = self.frames[int(self.frame_index)]
        if self.bleed: frame = tint_icon(frame, RED)
        self.image = pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE))
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
    
    def whip(self):
        if self.whip_stage == 0 or self.whip_stage == 2:
            for whip in self.whips:
                whip.kill()
            
            new_rect = self.rect.copy()
            
            if self.facing == 'right':
                new_rect.x += self.speed - 10
                
                top_rect = new_rect.copy()
                top_rect.x += 26
                top_rect.y -= self.speed - 16
            
            elif self.facing == 'left':
                new_rect.x -= self.speed - 10
    
                top_rect = new_rect.copy()
                top_rect.x -= 16
                top_rect.y -= self.speed - 24
                
            
            # top_rect = new_rect.copy()
            # top_rect.y -= self.speed - 24
            # top_rect.x -= 16
            
            whip = Whip(new_rect.topleft, self.facing)
            whip_top = Whip(top_rect.topleft, 'top', 'tip')
            
            self.whips.add(whip)
            self.add_to_enemy_sprites(whip)
            
            self.whips.add(whip_top)
            self.add_to_enemy_sprites(whip_top)

            self.whip_stage += 1
            
        elif self.whip_stage == 1:
            for whip in self.whips:
                whip.kill()
            
            new_rect = self.rect.copy()
            new_rect2 = self.rect.copy()
            if self.facing == 'right':
                new_rect.x += self.speed - 10
                new_rect2.x += self.speed*2 - 10
            elif self.facing == 'left':
                new_rect.x -= self.speed - 10
                new_rect2.x -= self.speed * 2 - 10
            whip = Whip(new_rect.topleft, self.facing)
            whip_tip = Whip(new_rect2.topleft, self.facing, type = 'tip', )
            
            self.whips.add(whip)
            self.whips.add(whip_tip)
            self.add_to_enemy_sprites(whip)
            self.add_to_enemy_sprites(whip_tip)
            self.whip_stage += 1
            
        if self.whip_stage == 3:
            for whip in self.whips:
                whip.kill()
            self.whip_stage = 0
    
    def bleed(self):
        self.bleed = True
                    
    def step(self):
        self.move()
        if self.type == '2':
            self.whip()
        
    def update(self):
        self.animate()
        self.whips.update()
        self.whips.draw(self.screen)

class Whip(pygame.sprite.Sprite):
    def __init__(self, orgin_pos, facing, type = 'base'):
        super().__init__()
        self.facing = facing
        self.prep_images(type)
        self.stage = 0
        self.set_image_facing()
        self.rect = self.image.get_rect(topleft = orgin_pos)
        
    def prep_images(self, type):
        #load
        if type == 'base':
            base = pygame.image.load('graphics/chain/base.png').convert_alpha()
            base = pygame.transform.rotate(base, 90)
            base = pygame.transform.scale(base, (TILE_SIZE, TILE_SIZE))
            self.image = base
        if type == 'tip':
            tip = pygame.image.load('graphics/chain/tip.png').convert_alpha()
            tip = pygame.transform.rotate(tip, 90)
            tip = pygame.transform.scale(tip, (TILE_SIZE, TILE_SIZE))
            self.image = tip

    def set_image_facing(self):
        if self.facing == 'right':
            img = pygame.transform.rotate(self.image, 0)
        elif self.facing == 'left':
            img = pygame.transform.rotate(self.image, 180)
        elif self.facing == 'top':
            img = pygame.transform.rotate(self.image, 90)
           
        image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        
        self.image = image
    
    def bleed(self):
        self.image = tint_icon(self.image, RED)

    def step(self):
        pass 