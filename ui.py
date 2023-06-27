import pygame
from debug import debug

from settings import *

class UI:
    def __init__(self, player):
        self.player = player
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font('graphics/ARCADECLASSIC.ttf', 64)
            
    def display_inventory(self):
        for index, item in enumerate(self.player.inventory):
            display_item = pygame.transform.scale(item[1], (64, 64))
            self.screen.blit(display_item, (20 + index * 64, 640))
    
    def display_health(self):
        for index in range(self.player.max_health):
            print(index)
            print(self.player.current_health)
            heart = pygame.image.load('graphics/unsorted/heart_a.png').convert_alpha()
            #if COLOR:
            if index  < self.player.current_health:
                heart = self.tint_icon(heart, RED)
            # if not COLOR:
            #     if index > self.player.current_health:
            #         heart = self.tint_icon(heart, GREY)
            heart = pygame.transform.scale(heart, (TILE_SIZE, TILE_SIZE))
            self.screen.blit(heart, (748 + index * 64, 640))
    
    def display_lives(self):
        #icon
        player_icon = pygame.image.load('graphics/player/walk/00.png').convert_alpha()
        player_icon = pygame.transform.scale(player_icon, (TILE_SIZE, TILE_SIZE))
        if COLOR:
            player_icon = self.tint_icon(player_icon, PURPLE)
        self.screen.blit(player_icon, (602, 640))
        
        #lives count
        lives = str(self.player.lives)
        if self.player.lives < 10:
            lives = '0' + lives
        surf = self.font.render(lives, True, WHITE)
        self.screen.blit(surf, (662,640))
    
    def display_coins(self):
        #icon
        coin_img = pygame.image.load('graphics/coin/00.png').convert_alpha()
        if COLOR:
            coin_img = self.tint_icon(coin_img, YELLOW)
        coin_img = pygame.transform.scale(coin_img, (TILE_SIZE, TILE_SIZE))
        self.screen.blit(coin_img, (455, 640))
       
        #coin count 
        coins = str(self.player.coins)
        if self.player.coins < 10:
            coins = '0' + coins
        surf = self.font.render(coins, True, WHITE)
        self.screen.blit(surf, (515,640))
    
    def tint_icon(self, icon, tint_color):
        for x in range(icon.get_width()):
            for y in range(icon.get_height()):
                color = icon.get_at((x,y))
                
                new_color = (
                    min(color[0] * tint_color[0] // 255, 255),
                    min(color[1] * tint_color[1] // 255, 255),
                    min(color[2] * tint_color[2] // 255, 255),
                    color[3]
                )
                icon.set_at((x,y), new_color)
        return icon
        
    def run(self):
        self.display_inventory()
        self.display_coins()
        self.display_lives()
        self.display_health()