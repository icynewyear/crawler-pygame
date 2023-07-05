import pygame
from settings import *
from ui import UI
from player import Player
from tiles import *
from enemies import Enemy
from misc_functions import *
from gamedata import levels
from items import *

from debug import debug

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.gameover = False
        
        
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
        
        #spikes
        self.spike_layout = import_csv_layout(self.level_data['spikes'])
        self.spike_tiles = self.create_tile_group(self.spike_layout, 'spikes')
        
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
        
        #coins
        self.coin_layout = import_csv_layout(self.level_data['coins'])
        self.coin_tiles = self.create_tile_group(self.coin_layout, 'coins')
        
        #items
        self.item_layout = import_csv_layout(self.level_data['items'])
        self.item_tiles = self.create_tile_group(self.item_layout, 'items')
        
        #enemeies
        self.enemies_layout = import_csv_layout(self.level_data['enemies'])
        self.enemies = self.create_tile_group(self.enemies_layout, 'enemies')
        
        #enemy constraints
        self.constraint_layout = import_csv_layout(self.level_data['constraints'])
        self.constraints = self.create_tile_group(self.constraint_layout, 'constraints')
        
        #traps
        self.trap_layout = import_csv_layout(self.level_data['traps'])
        self.traps = self.create_tile_group(self.trap_layout, 'traps')
        
        #collisons
        self.collision_sprites = self.terrain_tiles.sprites() + self.bridge_tiles.sprites()
        self.player.collision_sprites = self.collision_sprites
        
    def add_to_enemy_sprites(self, sprite):
        self.enemies.add(sprite)
        
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
                    
                    if tile_type == 'spikes':
                        tile = Spike((x,y), int(col))
                        
                    if tile_type == 'player':
                        tile = Player((x,y),self.check_for_interaction)
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
                        tile = Enemy((x,y), self.check_enemy_constraints, self.add_to_enemy_sprites, col)  
                    
                    if tile_type == 'doors':
                        if col == '2': state = 'open' 
                        else: state = 'closed'
                        tile = Door((x,y), state)
                        
                    if tile_type == 'chests':
                        if col == '1':
                            contents = SWORD
                        if col == '2':
                            contents = SHIELD
                        if col == '3':
                            contents = BOOTS
                        if col == '4':
                            contents = ORB
                        if col == '5':
                            contents = KEY
                        tile = Chest((x,y), contents)
                    
                    if tile_type == 'coins':
                        if col == '1':
                            tile = Coin((x,y))
                            
                    if tile_type == 'items':
                        if col == '1':
                            tile = ItemIcon((x,y), SWORD)
                        if col == '2':
                            tile = ItemIcon((x,y), SHIELD)
                        if col == '3':
                            tile = ItemIcon((x,y), BOOTS)
                        if col == '4':
                            tile = ItemIcon((x,y), ORB)
                        if col == '5':
                            tile = ItemIcon((x,y), KEY)
                    
                    if tile_type == 'constraints':
                        if col == '1':
                            tile = Tile((x,y), TILE_SIZE)
                     
                    if tile_type == 'traps':
                        if col == '1':
                            tile = SpikeTrap((x,y)) 
                        if col == '2':
                            tile = SpikeTrap((x,y), 'up')
                      
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
        boots = player.check_item_in_inventory('boots')
        
        if boots: self.collision_sprites += self.spike_tiles.sprites()
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
        waterfall_check = self.waterfall_tiles.sprites()
        #contains tiles that are not of type 'water'
        waterfall_ladder_check = [tile for tile in waterfall_check if tile.type != 'water']
        orb = player.check_item_in_inventory('orb')
        for sprite in self.ladder_tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                player.on_ladder = True
                return True
            else:
                player.on_ladder = False
        if orb:
            for sprite in waterfall_check:
                if sprite.rect.colliderect(player.rect):
                    sprite.freeze()
                    
                    player.on_ladder = True
                    return True
                else:
                    player.on_ladder = False    
    
    def check_for_interaction(self):
        player = self.player
        interactables = self.door_tiles.sprites() + self.chest_tiles.sprites()
        for sprite in self.door_tiles:
            if sprite.rect.colliderect(player.rect):
                sprite.interact(player)
        for sprite in self.chest_tiles:
            if sprite.rect.colliderect(player.rect):
                sprite.interact(player)
    
    def check_enemy_constraints(self, rect):
        for sprite in self.constraints:
            if sprite.rect.colliderect(rect):
                return True
        return False
     
    def check_coin_collision(self):
        player = self.player
        for sprite in self.coin_tiles:
            if sprite.rect.colliderect(player.rect):
                sprite.kill()
                player.coins += 1
    
    def check_item_collision(self):
        player = self.player
        for sprite in self.item_tiles:
            if sprite.rect.colliderect(player.rect):
                sprite.kill()
                player.add_inventory(sprite.item)   
    
    def check_spike_collison(self):
        player = self.player
        for sprite in self.spike_tiles:
            if sprite.rect.colliderect(player.rect):
                if not self.gameover:
                    player.die()
                    self.collision_sprites = []
                    sprite.bleed()
                    self.gameover = True
    
    def check_trap_colllison(self):
        player = self.player
        damaging_traps = [trap for trap in self.traps if trap.damaging]
        for sprite in damaging_traps:
            if sprite.rect.colliderect(player.rect):
                if not self.gameover:
                    player.die()
                    self.collision_sprites = []
                    sprite.bleed()
                    self.gameover = True
                
    def check_water_collisons(self):
        player = self.player
        orb = player.check_item_in_inventory('orb')
        if not orb:
            for sprite in self.waterfall_tiles:
                if sprite.type == 'water' or sprite.type == 'bottom':
                    if sprite.rect.colliderect(player.rect):
                        if not self.gameover:
                            player.die()
                            self.collision_sprites = []
                            sprite.bleed()
                            self.gameover = True
                
    def check_enemey_collsion(self):
        player = self.player
        sword = player.check_item_in_inventory('sword')
        shield = player.check_item_in_inventory('shield')
        for sprite in self.enemies:
            if sprite.rect.colliderect(player.rect):
                if sword:
                    if shield and player.facing != sprite.facing:
                        sprite.kill()
                    else:
                        player.current_health -= 1
                        sprite.kill()
                else:
                    player.current_health -= 1
    
                if player.current_health <= 0:
                    sprite.bleed()
                    player.die()
                    
                    self.collision_sprites = []
                    self.gameover = True 

    def run(self, dt):
        self.screen.fill(BG_COLOR)
        
        
        #terrain
        self.terrain_tiles.update()
        self.terrain_tiles.draw(self.screen)
        
        #spikes
        self.spike_tiles.update()
        self.spike_tiles.draw(self.screen)
        
        #ladders
        self.ladder_tiles.update()
        self.ladder_tiles.draw(self.screen)
        
        
        #bridges
        self.bridge_tiles.update()
        self.bridge_tiles.draw(self.screen)
        
        #waterfalls
        self.waterfall_tiles.update()
        self.waterfall_tiles.draw(self.screen)
        
        #traps
        self.traps.update()
        self.traps.draw(self.screen)
        
        #doors
        self.door_tiles.update()
        self.door_tiles.draw(self.screen)
        
        #chests
        self.chest_tiles.update()
        self.chest_tiles.draw(self.screen)
        
        #coins
        self.coin_tiles.update()
        self.coin_tiles.draw(self.screen)
        
        #items
        self.item_tiles.update()
        self.item_tiles.draw(self.screen)
    
        #Player Collisions
    
        self.ladder_collision()
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
        
    
        #collisions
        if not self.player.is_dead:
            self.check_coin_collision()
            self.check_item_collision()
            self.check_spike_collison()
            self.check_trap_colllison()
            self.check_water_collisons()
    
        #player movement check 
        if self.player.step() and not self.gameover:
            #anything that is turn based goes here
            for enemy in self.enemies:
                enemy.step()
                self.check_enemey_collsion()
            for trap in self.traps:
                trap.step()
                
        
        #enemies animation and draw
        self.enemies.update()
        self.enemies.draw(self.screen)
        
        #player animation and draw       
        self.player_sprites.update() 
        self.player_sprites.draw(self.screen)
        
        self.ui.run()
        if self.gameover:
            self.ui.display_game_over()