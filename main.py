import pygame
from pygame.locals import *
from sys import exit
from random import randint


pygame.init()

largura, altura = 900, 600
janela = pygame.display.set_mode((largura, altura))
try:
    pygame.display.set_icon(pygame.image.load('Imagens/flappy_bird_icon.png').convert_alpha())
except:
    pass
pygame.display.set_caption('Flappy Bird')
relogio = pygame.time.Clock()
sprite_background = pygame.image.load('Imagens/flappy_bird_backdrop.png')
sprite_group_principal = pygame.sprite.Group()
sprite_group_obstaculos = pygame.sprite.Group()
velocidade = 3


class Bird(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagens = []
        for n in range(4):
            img = pygame.image.load('Imagens/flappy_bird.png')
            img = img.subsurface((n * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (64, 64))
            self.imagens.append(img)
        self.idx = 0
        self.image = self.imagens[self.idx]
        self.mask = pygame.mask.from_surface(self.image) # Gambiarra, mais ou menos
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
    
    def update(self) -> None:
        self.idx += 0.5
        if self.idx >= len(self.imagens):
            self.idx = 0
        self.image = self.imagens[int(self.idx)]


class Chao(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Imagens/flappy_bird_chao.png'), (308, 112))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 500
    
    def update(self) -> None:
        if self.rect.topright[0] <= 0:
            self.rect.x = largura
        self.rect.x -= velocidade


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Imagens/flappy_bird_obstaculo.png').convert_alpha(), (52, 668))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) # Gambiarra, mais ou menos
        self.rect.x = x_pos
        self.rect.y = randint(-156, 0)
    
    def update(self) -> None:
        if self.rect.topright[0] <= 0:
            self.rect.x = largura
            self.rect.y = randint(-156, 0)
        self.rect.x -= velocidade


for n in range(4):
    sprite_group_obstaculos.add(Obstaculo(n * (largura // 4) + 500))

for n in range(6):
    sprite_group_obstaculos.add(Chao(n * (largura // 3)))

bird = Bird()
sprite_group_principal.add(bird)

while True:
    relogio.tick(30)
    janela.fill((0, 0, 0))
    janela.blit(sprite_background, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    sprite_group_obstaculos.draw(janela)
    sprite_group_principal.draw(janela)

    sprite_group_principal.update()
    sprite_group_obstaculos.update()
    pygame.display.flip()
