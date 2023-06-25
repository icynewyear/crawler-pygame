import pygame
from settings import *
from misc_functions import *
from debug import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        #pos and movement
        self.pos = pos
        self.facing = 'right'
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1
        self.gravity = .6
        
        #combat
        self.max_health = 3
        self.current_health = self.max_health
        
        #image and animation
        self.frames = import_folder('graphics/player/walk')
        self.frame_index = 0
        self.animation_speed = .05
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft = self.pos)

        #collisio
        self.last_direction = None
        self.on_ladder = False
        
        # player status
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
        #invetory
        self.inventory = []
        self.inventory_test()

    def inventory_test(self):
        item = pygame.image.load('graphics/unsorted/sword_a.png').convert_alpha()
        self.add_inventory('sword', item)
        item = pygame.image.load('graphics/unsorted/shield_a.png').convert_alpha()
        self.add_inventory('shield', item)
        item = pygame.image.load('graphics/unsorted/boots_a.png').convert_alpha()
        self.add_inventory('boots', item)
        item = pygame.image.load('graphics/unsorted/orb_a.png').convert_alpha()
        self.add_inventory('orb', item)
        item = pygame.image.load('graphics/unsorted/key_a.png').convert_alpha()
        self.add_inventory('key', item)
        
        self.current_health = 1

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
            self.direction = pygame.math.Vector2(-1, 0)
            self.facing = 'left'
            step = True
        elif keys[pygame.K_RIGHT]:
            self.direction = pygame.math.Vector2(1, 0)
            self.facing = 'right'
            step = True
        else:
            self.direction.x = 0
            
        if keys[pygame.K_UP] and self.on_ladder:
            self.rect.y -= self.speed/2
            self.pos = self.rect.topleft
            step = True
        elif keys[pygame.K_DOWN] and self.on_ladder:
            self.rect.y += self.speed/2
            self.pos = self.rect.topleft
            step = True
            
        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.jump()
        return step
                    
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
                
    def do_movement(self):
        self.rect.x += self.direction.x * self.speed
        self.pos = self.rect.topleft
        
    def do_movement_step(self):
        self.do_gravity()
        self.rect.y += self.direction.y
        self.rect.x += self.direction.x * self.speed
        self.pos = self.rect.topleft
        
    def jump(self):
        self.direction.y = -12
        self.on_ground = False
    
    def do_gravity(self):
        if not self.on_ladder:
            self.direction.y += self.gravity
            
    def do_gravity_old(self):
        if not self.on_ladder:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y
            self.pos = self.rect.topleft
    
    def add_inventory(self, name, image):
        self.inventory.append((name, image))
    
    def update(self):
        
        self.get_input()
        self.do_movement_step()
        #self.do_gravity()
        self.animate()
        self.show_hitboxes()