import pygame
from settings import *
from ui import UI
from player import Player
from tiles import *
from enemies import Enemy
from misc_functions import *
from gamedata import levels

from debug import debug

class Level:
    def __init__(self, screen):
        self.screen = screen
        
        
        #player
        self.player_layout = import_csv_layout(levels[0]['player'])
        self.player_sprites = self.create_tile_group(self.player_layout, 'player')
        #ui
        self.ui = UI(self.player_sprites.sprites()[0])
        
        #levels
        self.current_level = 0
        self.level_data = levels[self.current_level]
        
        #tiles
        self.terrain_layout = import_csv_layout(self.level_data['terrain'])
        self.terrain_tiles = self.create_tile_group(self.terrain_layout, 'terrain')
        
        #ladders
        
        self.ladder_layout = import_csv_layout(self.level_data['ladders'])
        self.ladder_tiles = self.create_tile_group(self.ladder_layout, 'ladders')
        
        #bridges
        self.bridge_layout = import_csv_layout(self.level_data['bridges'])
        self.bridge_tiles = self.create_tile_group(self.bridge_layout, 'bridges')
        
        #waterfalls
        self.waterfall_layout = import_csv_layout(self.level_data['waterfalls'])
        self.waterfall_tiles = self.create_tile_group(self.waterfall_layout, 'waterfalls')
        
        #doors
        self.door_layout = import_csv_layout(self.level_data['doors'])
        self.door_tiles = self.create_tile_group(self.door_layout, 'doors')
        
        #chests
        self.chest_layout = import_csv_layout(self.level_data['chests'])
        self.chest_tiles = self.create_tile_group(self.chest_layout, 'chests')
        
        #items
        self.item_layout = import_csv_layout(self.level_data['items'])
        self.item_tiles = self.create_tile_group(self.item_layout, 'items')
        
        #enemeies
        self.enemies_layout = import_csv_layout(self.level_data['enemies'])
        self.enemies = self.create_tile_group(self.enemies_layout, 'enemies')
        
        #collisons
        self.collision_sprites = self.terrain_tiles.sprites()
        
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == '0':
                    sprite = Player((x,y))
                    self.player.add(sprite)
    
    def create_tile_group(self, layout, tile_type):
        group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    
                    if tile_type in ['terrain', 'ladders', 'bridges']:
                        terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(col)]
                        tile = StaticTile((x,y), TILE_SIZE, pygame.transform.scale(tile_surface, (TILE_SIZE, TILE_SIZE)))
                        
                    if tile_type == 'player':
                        tile = Player((x,y))
                        self.player = tile
                        
                    if tile_type == 'waterfalls':
                        if col == '4':
                            tile = Waterfall((x,y), TILE_SIZE, 'top')
                        elif col == '5':
                            tile = Waterfall((x,y), TILE_SIZE, 'top', True)
                        elif col == '9':
                            tile = Waterfall((x,y), TILE_SIZE, 'middle')
                        elif col == '10':
                            tile = Waterfall((x,y), TILE_SIZE, 'middle', True)
                        elif col == '15':
                            tile = Waterfall((x,y), TILE_SIZE, 'bottom')
                        elif col == '16':
                            tile = Waterfall((x,y), TILE_SIZE, 'bottom', True)
                        elif col == '21':
                            tile = Waterfall((x,y), TILE_SIZE, 'water')
                        elif col == '22':
                            tile = Waterfall((x,y), TILE_SIZE, 'water', True)
                     
                    if tile_type == 'enemies':
                        tile = Enemy((x,y), col)  
                    
                    if tile_type == 'doors':
                        if col == '2': state = 'open' 
                        else: state = 'closed'
                        tile = Door((x,y), state)
                        
                    if tile_type == 'chests':
                        if col == '2': state = 'open' 
                        else: state = 'closed'
                        tile = Chest((x,y), state)
                    
                    if tile_type == 'items':
                        if col == '1':
                            tile = Coin((x,y))
                        
                      
                    group.add(tile)
        return group
    
    def horizontal_movement_collision(self):
        player = self.player
        player.rect.x += player.direction.x * player.speed
        
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.pos = player.rect.topleft
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.pos = player.rect.topleft
                player.direction.x = 0
    
    def vertical_movement_collision(self):
        player = self.player
        debug(player.inventory[0][0], (80,80))
       # if not player.on_ladder: player.do_gravity()
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.pos = player.rect.topleft
                    player.direction.y = 0               
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.pos = player.rect.topleft
                    player.direction.y = 0
                    player.on_ground = True
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def ladder_collision(self):
        player = self.player
        for sprite in self.ladder_tiles:
            if sprite.rect.colliderect(player.rect):
                player.on_ladder = True
                return True
            else:
                player.on_ladder = False
            
    def run(self, dt):
        self.screen.fill(BG_COLOR)
       
        #terrain
        self.terrain_tiles.update()
        self.terrain_tiles.draw(self.screen)
        
        #ladders
        self.ladder_tiles.update()
        self.ladder_tiles.draw(self.screen)
        
        #bridges
        self.bridge_tiles.update()
        self.bridge_tiles.draw(self.screen)
        
        #waterfalls
        self.waterfall_tiles.update()
        self.waterfall_tiles.draw(self.screen)
        
        #doors
        self.door_tiles.update()
        self.door_tiles.draw(self.screen)
        
        #chests
        self.chest_tiles.update()
        self.chest_tiles.draw(self.screen)
        
        #items
        self.item_tiles.update()
        self.item_tiles.draw(self.screen)
        
        #enemies
        self.enemies.update()
        self.enemies.draw(self.screen)
        
        #Player
        
        
        self.ladder_collision()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        
        self.player_sprites.update() 
        self.player_sprites.draw(self.screen)
        
        self.ui.run()