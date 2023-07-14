import pygame
from settings import DEBUG

#intitialize pygame
pygame.init()

#display given string on screen
def debug(output, pos=(80,80)):
    screen = pygame.display.get_surface()
    #set up font
    font = pygame.font.SysFont('Arial', 20)
    #render text
    text = font.render(str(output), True, (255, 255, 255))   
    #display text
    if DEBUG:
        screen.blit(text, pos)