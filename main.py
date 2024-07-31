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
velocidade = 4
gravidade = 1.5


class Bird(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagens = []
        for n in range(4):
            img = pygame.image.load('Imagens/flappy_bird.png')
            img = pygame.transform.scale(img.subsurface((n * 32, 0), (32, 32)), (64, 64))
            self.imagens.append(img)
        self.idx = 0
        self.image = self.imagens[self.idx]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade = 0
        self.rect.x = 150
        self.rect.y = 219
        self.pulo = False
    
    def update(self) -> None:
        self.idx += 0.5
        if self.idx >= len(self.imagens):
            self.idx = 0
        
        self.velocidade += gravidade
        self.rect.y += self.velocidade
        if self.pulo:
            self.rect.y -= 15
            self.velocidade = -15
        
        angulo = (-self.velocidade + 18) * 3
        if angulo > 15:
            angulo = 15
        if angulo < -45:
            angulo = -45
        
        self.image = pygame.transform.rotate(self.imagens[int(self.idx)], angulo)
        self.pulo = False
    
    def pular(self) -> None:
        self.pulo = True


class Chao(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Imagens/flappy_bird_chao.png'), (900, 112))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x_pos
        self.rect.y = 500
    
    def update(self) -> None:
        if self.rect.topright[0] < 0:
            self.rect.x = largura - 4 # Ajuste fino...
        self.rect.x -= velocidade


class ObstaculoUp(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Imagens/flappy_bird_obstaculo_superior.png').convert_alpha(), (52, 400))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x_pos
        self.rect.y = randint(-330, -100)
    
    def update(self) -> None:
        if self.rect.topright[0] <= 0:
            self.rect.x = largura + 173
            self.rect.y = randint(-330, -100)
        self.rect.x -= velocidade


class ObstaculoDown(pygame.sprite.Sprite):
    def __init__(self, objeto) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('Imagens/flappy_bird_obstaculo_inferior.png').convert_alpha(), (52, 400))
        self.rect = self.image.get_rect()
        self.objeto = objeto
        self.x_pos = objeto.rect.x
        self.y_pos = objeto.rect.bottom + 128
    
    def update(self) -> None:
        self.rect.x = self.objeto.rect.x
        self.rect.y = self.objeto.rect.bottom + 128


for n in range(5):
    obstaculo = ObstaculoUp(n * 225 + 500)
    sprite_group_obstaculos.add(obstaculo)
    sprite_group_obstaculos.add(ObstaculoDown(obstaculo))

for n in range(2):
    sprite_group_obstaculos.add(Chao(n * 900))

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
        if event.type == KEYDOWN and event.key == K_SPACE:
            bird.pular()
    
    sprite_group_obstaculos.draw(janela)
    sprite_group_principal.draw(janela)

    if pygame.sprite.spritecollide(bird, sprite_group_obstaculos, False, pygame.sprite.collide_mask):
        print('Colidiu!')

    sprite_group_principal.update()
    sprite_group_obstaculos.update()
    
    pygame.display.flip()
