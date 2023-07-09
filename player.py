import pygame
from settings import *
from misc_functions import *
from debug import *
from timer import Timer
from gamedata import *
from items import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, check_for_interaction, grid, grid_pos):
        super().__init__()
        #pos and movement
        self.pos = pos
        self.facing = 'right'
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 64
        self.gravity = .6
        self.movement_lockout = Timer(250)
        
        #combat
        self.max_health = 3
        self.current_health = 3
        self.is_dead = False
        
        #image and animation
        self.frames = import_folder('graphics/player/walk')
        self.frame_index = 0
        self.animation_speed = .05
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft = self.pos)
        

        #collision and grid
        self.grid = grid
        self.grid_pos = grid_pos
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
        self.test()

    def test(self):
        print(self.check_grid('down', 'W'))
        self.print_grid()
       
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
        if self.on_ladder:
            self.frames = import_folder('graphics/player/climb')
        else:
            self.frames = import_folder('graphics/player/walk')
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
        if keys[pygame.K_UP] and self.on_ladder and not self.is_dead:
            self.rect.y -= self.speed 
            self.pos = self.rect.topleft
            step = True
        elif keys[pygame.K_DOWN] and self.on_ladder and not self.is_dead:
            self.rect.y += self.speed
            self.pos = self.rect.topleft
            step = True
        #interactables
        if keys[pygame.K_e]:
            self.check_for_interaction()
            step = False
        
        if step: 
            self.movement_lockout.start()
        return step
    
    def check_grid(self, direction, check):
        #returns true if the grid contains the check in the direction

        if direction == 'up':
            check_x = self.grid_pos[0]
            check_y = self.grid_pos[1] - 1
        elif direction == 'down':
            check_x = self.grid_pos[0] 
            check_y = self.grid_pos[1] + 1
        elif direction == 'left':
            check_x = self.grid_pos[0] - 1
            check_y = self.grid_pos[1]
        elif direction == 'right':
            check_x = self.grid_pos[0] + 1
            check_y = self.grid_pos[1]  
        print(self.grid[check_y][check_x])
        if check in self.grid[check_y][check_x]:
            return True
        else:
            return False
        
    def print_grid(self):
        #prints the rows and cols of the grid to the console in a formatted way
        #for debugging
        print(len(self.grid))
        for x in self.grid:
            print(x)
            
    def check_collisions(self, rect, return_sprite = False):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(rect):
                if return_sprite: return sprite
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
    
    def gravity_grid_test(self):
        test = self.check_grid('down', 'W')
        if not test:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y
            self.pos = self.rect.topleft
            
           
    def do_gravity(self):
        new_rect = self.rect.copy()
        new_rect.y += self.gravity
        collison_sprite = self.check_collisions(new_rect)
        if self.is_dead:
            self.on_ladder = False
        if not self.on_ladder:
            if collison_sprite != False and not self.is_dead:
                if self.direction.y > 0:
                    self.rect.bottom = collison_sprite.rect.top
                    self.on_ground = True
                    self.direction.y = 0
                elif self.direction.y < 0:
                    self.rect.top = collison_sprite.rect.bottom
                    self.direction.y = 0
            else:
                self.direction.y += self.gravity
                self.rect.y += self.direction.y
                self.pos = self.rect.topleft
                
        # if not self.on_ladder:
        #     self.direction.y += self.gravity
        #     self.rect.y += self.direction.y
        #     self.pos = self.rect.topleft
    
    def die(self):
        self.is_dead = True
        self.collision_sprites = []
        self.direction.y = -12
        self.current_health = 0
        
    def step(self):
        if self.movement_lockout.active or self.is_dead:
            return False
        return self.get_input()
                
    def update(self):
        self.movement_lockout.update()
        #self.do_gravity()
        self.gravity_grid_test()
        self.animate()
        if DEBUG: self.show_hitboxes()