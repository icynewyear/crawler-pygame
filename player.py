import pygame
from settings import *
from misc_functions import *
from debug import *
from timer import Timer
from gamedata import *
from items import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, check_for_interaction):
        super().__init__()
        #pos and movement
        self.pos = pos
        self.facing = 'right'
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 64
        self.gravity = .6
        self.movement_lockout = Timer(300)
        
        #combat
        self.max_health = 3
        self.current_health = 3
        
        #image and animation
        self.frames = import_folder('graphics/player/walk')
        self.frame_index = 0
        self.animation_speed = .05
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft = self.pos)

        #collisio
        self.last_direction = None
        self.on_ladder = False
        self.collision_sprites = None
        
        # player status
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
        #invetory
        self.check_for_interaction = check_for_interaction
        self.coins = 0
        self.lives = 3
        self.inventory = []
        self.inventory_test()

    def inventory_test(self):
        #self.add_inventory(SWORD)
        pass
       

    def check_item_in_inventory(self, item):
        for i in self.inventory:
            if i[0] == item:
                return True
        return False
    
    def add_inventory(self, item):
        #takes a tuple of (name, imagepath)
        name = item[0]
        image = pygame.image.load(item[1]).convert_alpha()
        self.inventory.append((name, image))
    
    def remove_inventory(self, item):
        for i in self.inventory:
            if i[0] == item:
                self.inventory.remove(i)
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        if self.facing == 'right':
            self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))
        else:
            self.image = pygame.transform.flip(pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE)), True, False)
   
    def get_input(self):
        keys = pygame.key.get_pressed()
        step = False
        
        #left and right
        if keys[pygame.K_LEFT]:
            new_rect = self.rect.copy()
            new_rect.x -= self.speed
            if not self.check_collisions(new_rect):
                self.rect.x -= self.speed
                self.facing = 'left'
                step = True
        elif keys[pygame.K_RIGHT]:
            new_rect = self.rect.copy()
            new_rect.x += self.speed
            if not self.check_collisions(new_rect):
                self.rect.x += self.speed
                self.facing = 'right'
                step = True
        if step: self.pos = self.rect.topleft
            
        #ladder  
        if keys[pygame.K_UP] and self.on_ladder:
            self.rect.y -= self.speed
            self.pos = self.rect.topleft
            step = True
        elif keys[pygame.K_DOWN] and self.on_ladder:
            self.rect.y += self.speed
            self.pos = self.rect.topleft
            step = True
        #interactables
        if keys[pygame.K_e]:
            self.check_for_interaction()
            step = False
            
        #jump (Neeeds rework)    
        if keys[pygame.K_SPACE] and self.check_item_in_inventory('boots'):
            if self.on_ground:
                self.jump()  
        if step: 
            self.movement_lockout.start()
        return step
    
    def check_collisions(self, rect):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(rect):
                return True
        return False   
                
    def get_hitbox_from_image(self, surf):
        image_mask = pygame.mask.from_surface(surf)
        rect_list = image_mask.get_bounding_rects()
        return rect_list[0].unionall(rect_list)
     
    def show_hitboxes(self):
        screen = pygame.display.get_surface()
        if DEBUG:
            pygame.draw.rect(screen, NEON_GREEN, self.rect, 3)
            pygame.draw.circle(screen, LIGHT_BLUE, self.pos, 5)  
            pygame.draw.circle(screen, ORANGE, (self.rect.right, self.rect.centery), 5)
        
    def jump(self):
        self.direction.y = -12
        self.on_ground = False
            
    def do_gravity(self):
        if not self.on_ladder:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y
            self.pos = self.rect.topleft
            
    def step(self):
        if self.movement_lockout.active:
            return False
        return self.get_input()
                
    def update(self):
        self.movement_lockout.update()
        self.do_gravity()
        self.animate()
        self.show_hitboxes()