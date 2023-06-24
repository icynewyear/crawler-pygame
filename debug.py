import pygame

#intitialize pygame
pygame.init()

#display given string on screen
def debug(output, pos=(0,0)):
    screen = pygame.display.get_surface()
    #set up font
    font = pygame.font.SysFont('Arial', 20)
    #render text
    text = font.render(str(output), True, (255, 255, 255))   
    #display text
    screen.blit(text, pos)