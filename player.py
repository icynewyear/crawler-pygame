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
        self.speed = TILE_SIZE
        self.gravity = .6
        self.movement_lockout = Timer(250)
        self.interact_lockout = Timer(250)
        
        #combat
        self.max_health = 3
        self.current_health = self.max_health
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
        self.walkable_tiles = {'W', 'L', 'B'}
        self.vertical_collidable_tiles = {'W', 'B'}
        
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
        
        #death animaion
        self.angle = 0
        self.dy = -15
        self.death_animation_over = False
        
    def test(self):
        """test function for debugging"""
        print(self.check_grid('down', 'W'))
        self.print_grid()
        
    def print_grid(self):
        """prints the rows and cols of the grid to the console in a formatted way for debugging"""
        print(len(self.grid))
        for x in self.grid:
            print(x)  
               
    def show_hitboxes(self):
        """draws the hitboxes of the player for debugging"""
        screen = pygame.display.get_surface()
        if DEBUG:
            pygame.draw.rect(screen, NEON_GREEN, self.rect, 3)
            pygame.draw.circle(screen, LIGHT_BLUE, self.pos, 5)  
            pygame.draw.circle(screen, ORANGE, (self.rect.right, self.rect.centery), 5)
            
    def get_hitbox_from_image(self, surf):
        """gets the hitbox from an image. Unused"""
        image_mask = pygame.mask.from_surface(surf)
        rect_list = image_mask.get_bounding_rects()
        return rect_list[0].unionall(rect_list)
            
    def check_item_in_inventory(self, item):
        """takes a string of the item name and returns true if the item is in the inventory"""
        for i in self.inventory:
            if i[0] == item:
                return True
        return False
    
    def add_inventory(self, item):
        """takes a tuple of (name, imagepath) adds the item to the inventory"""
        name = item[0]
        image = pygame.image.load(item[1]).convert_alpha()
        self.inventory.append((name, image))
    
    def remove_inventory(self, item):
        """takes a string of the item name and removes it from inventory"""
        for i in self.inventory:
            if i[0] == item:
                self.inventory.remove(i)
    
    def animate(self):
        """animates the player based on the direction and if they are on a ladder"""
        
        #sets correct animation folder
        if self.on_ladder:
            self.frames = import_folder('graphics/player/climb')
        else:
            self.frames = import_folder('graphics/player/walk')
        self.frame_index += self.animation_speed
        
        #loops the animation
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        #scales image
        image = pygame.transform.scale(self.frames[int(self.frame_index)], (TILE_SIZE, TILE_SIZE))

        #sets the image based on the direction
        if self.facing == 'right':
            self.image = image
        else:
            #flips the image if facing left
            self.image = pygame.transform.flip(image, True, False)
    
    def get_input(self):
        """checks for input and controls movement"""
        keys = pygame.key.get_pressed()
        step = False
        
        #left and right
        if keys[pygame.K_LEFT]:
            if not self.check_grid('left', 'W'):
                self.update_grid_pos('left')
                self.rect.x -= self.speed
                self.facing = 'left'
                step = True
        elif keys[pygame.K_RIGHT]:
            if not self.check_grid('right', 'W'):
                self.update_grid_pos('right')
                self.rect.x += self.speed
                self.facing = 'right'
                step = True
            
        #ladder          
        if keys[pygame.K_UP] and self.check_grid('self', 'L') and not self.check_grid('up', 'W') and self.check_grid('up', 'L') != 'OOB':
            self.update_grid_pos('up')
            self.rect.y -= self.speed 
            step = True
        elif keys[pygame.K_DOWN] and self.check_grid('down','L') != 'OOB' and (self.check_grid('down', 'L') or (self.check_grid('self', 'L') and not self.check_grid('down', 'VC'))):
            self.update_grid_pos('down')
            self.rect.y += self.speed
            step = True
            
        #interactables
        if keys[pygame.K_e] and self.interact_lockout.active == False:
            self.check_for_interaction()
            self.interact_lockout.start()
            step = False
        #if movement has been made move the player and start the movement lockout
        if step: 
            self.pos = self.rect.topleft
            self.movement_lockout.start()
        return step
    
    def check_grid(self, direction, check):
        #returns true if the grid contains the check in the direction
        #if check = LC checks for all non ladder vertical collidables
        #if check = VC checks for all vertical collidables
        #retuns true if the grid contains the check in the direction
    
        #set for convience    
        orb = self.check_item_in_inventory('orb')
        boots = self.check_item_in_inventory('boots')
        
        #sets check_x and check_y based on direction
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
        elif direction == 'self':   
            check_x = self.grid_pos[0]
            check_y = self.grid_pos[1]
        
        #checks if the check is out of bounds
        if check_y < 0 or check_y > TILE_HEIGHT - 1 or check_x < 0 or check_x > TILE_WIDTH - 1:
           return 'OOB'
       
        gridcheck = self.grid[check_y][check_x]
        
        #checks Vertical Collidables
        if check == 'VC' or check == 'LC':
            if check == 'VC':
                walkable = self.walkable_tiles
            if check == 'LC':
                walkable = self.vertical_collidable_tiles
            
            if orb:
                walkable.add('w')
                walkable.add('F')
            if boots:
                walkable.add('S')
                  
            for i in walkable:
                if i in gridcheck:
                    return True
            return False
        
        #orb/ladder checks
        if orb and check == 'L':
            if 'F' in gridcheck:
                return True
            
        if check in gridcheck:
            return True
        else:
            return False
    
    def update_grid_pos(self, direction, amount_of_tiles = 1):
       """updates the grid position of the player based on the direction and amount of tiles"""
       if direction == 'up':
            dest_x = self.grid_pos[0]
            dest_y = self.grid_pos[1] - amount_of_tiles
       elif direction == 'down':
            dest_x = self.grid_pos[0] 
            dest_y = self.grid_pos[1] + amount_of_tiles
       elif direction == 'left':
            dest_x = self.grid_pos[0] - amount_of_tiles
            dest_y = self.grid_pos[1]
       elif direction == 'right':
            dest_x = self.grid_pos[0] + amount_of_tiles
            dest_y = self.grid_pos[1]  
       #moves player in grid and updates playe grid_pos
       self.grid[self.grid_pos[1]][self.grid_pos[0]].remove('P')
       self.grid[dest_y][dest_x].append('P')
       self.grid_pos = (dest_x, dest_y)
             
    def check_collisions(self, rect, return_sprite = False):
        """checks if the player is colliding with any sprites in the collision_sprites list"""
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(rect):
                if return_sprite: return sprite
                return True
        return False   
    
    def check_spike_collion(self):
        """checks if the player is colliding with any spikes and kills the player if they are"""
        if self.check_grid('self', 'S'):
            self.die()
    
    def do_gravity(self):
        """applies gravity to the player"""
        test = self.check_grid('down', 'VC')
        if test == 'OOB':
            return False
        if not test:
            self.update_grid_pos('down')
            self.rect.y = self.grid_pos[1] * TILE_SIZE
            self.pos = self.grid_pos[0] * TILE_SIZE, self.grid_pos[1] * TILE_SIZE
                 
    def die(self):
        """kills the player"""
        self.is_dead = True
        self.collision_sprites = []
    
    def death_animation(self, start = True):
        """animates the player when they die"""
        self.rect.y += self.dy
        self.dy += 1
        
        #rotate the player
        #I want to revist this and make it look better
        self.angle += 15
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        
        #check if the player is off the screen. if so  set death_animation_over to true
        if self.rect.top > SCREEN_HEIGHT:
            self.death_animation_over = True
           
    def step(self):
        """if not dead and not in a movement lockout, gets input from the player. retuns true if the player moved"""
        if self.movement_lockout.active or self.is_dead:
            return False
        return self.get_input()
                
    def update(self):
        """core update method for the player"""
        #advance lockout timers
        self.movement_lockout.update()
        self.interact_lockout.update()
        
        if not self.is_dead:
            self.do_gravity()
            self.check_spike_collion()
        if self.is_dead and not self.death_animation_over:
            self.death_animation()
        self.animate()
        if DEBUG: self.show_hitboxes()