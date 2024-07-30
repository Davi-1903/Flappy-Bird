import pygame
from pygame.locals import *
from sys import exit


pygame.init()

largura, altura = 900, 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_icon(pygame.image.load('Imagens/flappy_bird_icon.png').convert_alpha())
pygame.display.set_caption('Flappy Bird')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    pygame.display.flip()
