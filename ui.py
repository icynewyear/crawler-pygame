import pygame
from debug import debug

from settings import *

class UI:
    def __init__(self, player):
        self.player = player
        self.screen = pygame.display.get_surface()
            
    def display_inventory(self):
        for index, item in enumerate(self.player.inventory):
            display_item = pygame.transform.scale(item[1], (64, 64))
            self.screen.blit(display_item, (20 + index * 64, 640))
    
    def display_health(self):
        for index in range(self.player.max_health):
            heart = pygame.image.load('graphics/unsorted/heart_a.png').convert_alpha()
            print(index, self.player.current_health)
            if index < self.player.current_health:
                heart = self.tint_icon(heart, RED)
            display_health = pygame.transform.scale(heart, (64, 64))
            self.screen.blit(display_health, (748 + index * 64, 640))
    
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
        self.display_health()