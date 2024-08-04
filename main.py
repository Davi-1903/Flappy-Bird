import pygame, os
from pygame.locals import *
from sys import exit
from random import randint
from math import ceil


pygame.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'Imagens')
diretorio_sons = os.path.join(diretorio_principal, 'Sons')

largura, altura = 900, 600
janela = pygame.display.set_mode((largura, altura))
try:
    pygame.display.set_icon(pygame.image.load(os.path.join(diretorio_imagens, 'flappy_bird_icon.png')).convert_alpha())
except:
    pass
pygame.display.set_caption('Flappy Bird')
relogio = pygame.time.Clock()

font_pontos = pygame.font.SysFont('04b19', 60)
font_game_over_principal = pygame.font.SysFont('04b19', 120)
font_game_over_secundaria = pygame.font.SysFont('04b19', 40)

som_score = pygame.mixer.Sound(os.path.join(diretorio_sons, 'point.wav'))
som_score.set_volume(0.25)
som_death = pygame.mixer.Sound(os.path.join(diretorio_sons, 'hit.wav'))
som_death.set_volume(0.25)
som_game_over = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav'))
som_jump = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump.wav'))
som_jump.set_volume(0.25)

sprite_group_background = pygame.sprite.Group()
sprite_group_principal = pygame.sprite.Group()
sprite_group_obstaculos = pygame.sprite.Group()

with open(os.path.join(diretorio_principal, 'recorde.txt'), 'r') as arquivo:
    recorde = int(arquivo.read())
velocidade = 5
gravidade = 0
inicio = False
pontos = 0


class Bird(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        bird_n = randint(0, 2)
        self.imagens = []
        for n in range(4):
            img = pygame.image.load(os.path.join(diretorio_imagens, 'flappy_bird.png'))
            img = pygame.transform.scale(img.subsurface((n * 32, bird_n * 32), (32, 32)), (64, 64))
            self.imagens.append(img)
        self.idx = 0
        self.image = self.imagens[self.idx]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.angulo = 0
        self.velocidade = 0
        self.rect.x = 150
        self.rect.y = 220
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
        
        self.image = pygame.transform.rotate(self.imagens[int(self.idx)], self.angulo)
        if inicio:
            self.angulo = (-self.velocidade + 18) * 3
            if self.angulo > 15:
                self.angulo = 15
            if self.angulo < -45:
                self.angulo = -45
        
        self.pulo = False
    
    def pular(self) -> None:
        self.pulo = True


class Nuvens(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(diretorio_imagens, 'flappy_bird_nuvens.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 275
    
    def update(self) -> None:
        if self.rect.right <= 0:
            self.rect.x = self.image.get_width() + self.rect.right
        self.rect.x -= ceil(velocidade / 5)


class Predios(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(diretorio_imagens, 'flappy_bird_predios.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 340
    
    def update(self) -> None:
        if self.rect.right <= 0:
            self.rect.x = self.image.get_width() + self.rect.right
        self.rect.x -= ceil(velocidade / 3)


class Arvores(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(diretorio_imagens, 'flappy_bird_arvores.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 403
    
    def update(self) -> None:
        if self.rect.right <= 0:
            self.rect.x = self.image.get_width() + self.rect.right
        self.rect.x -= ceil(velocidade / 2)


class Chao(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(diretorio_imagens, 'flappy_bird_chao.png')).convert()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 500
    
    def update(self) -> None:
        if self.rect.right <= 0:
            self.rect.x = self.image.get_width() + self.rect.right
        self.rect.x -= velocidade


class ObstaculoUp(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(diretorio_imagens, 'flappy_bird_obstaculo_superior.png')).convert_alpha(), (52, 400))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x_pos
        self.rect.y = randint(-330, -100)
        self.colidir = True
    
    def update(self) -> None:
        global pontos

        if self.rect.center[0] - 150 in range(0, 27) and self.colidir:
            som_score.play()
            self.colidir = False
            pontos += 1

        if self.rect.topright[0] <= 0:
            self.colidir = True
            self.rect.x = largura + 173
            self.rect.y = randint(-330, -100)
        self.rect.x -= velocidade


class ObstaculoDown(pygame.sprite.Sprite):
    def __init__(self, objeto) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(diretorio_imagens, 'flappy_bird_obstaculo_inferior.png')).convert_alpha(), (52, 400))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.objeto = objeto
        self.update()
    
    def update(self) -> None:
        self.rect.x = self.objeto.rect.x
        self.rect.y = self.objeto.rect.bottom + 128


for n in range(2):
    sprite_group_background.add(Nuvens(n * 900))

for n in range(2):
    sprite_group_background.add(Predios(n * 900))

for n in range(2):
    sprite_group_background.add(Arvores(n * 900))

for n in range(5):
    obstaculo = ObstaculoUp(n * 225 + largura)
    sprite_group_obstaculos.add(obstaculo)
    sprite_group_obstaculos.add(ObstaculoDown(obstaculo))

for n in range(2):
    sprite_group_principal.add(Chao(n * 910))

bird = Bird()
sprite_group_principal.add(bird)

while True:
    relogio.tick(30)
    janela.fill((0, 153, 204))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN and event.key == K_SPACE and not bird.pulo and velocidade:
            som_jump.play()
            inicio = True
            bird.pular()
    
    sprite_group_background.draw(janela)
    sprite_group_obstaculos.draw(janela)
    sprite_group_principal.draw(janela)

    if pygame.sprite.spritecollide(bird, sprite_group_obstaculos, False, pygame.sprite.collide_mask) and velocidade != 0:
        som_death.play()
        velocidade = 0
    
    sprite_group_background.update()
    sprite_group_principal.update()

    if inicio:
        gravidade = 1.5
        sprite_group_obstaculos.update()
    
    if bird.rect.bottom - 20 > 500:
        som_game_over.play()
        fim = True
        while fim:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN and event.key == K_r:
                    fim = False
            
            msg_1 = font_game_over_principal.render('Game over', True, (48, 48, 64))
            msg_rect_1 = msg_1.get_rect(center=(largura // 2, altura // 2))
            msg_2 = font_game_over_secundaria.render('R para reiniciar', True, (48, 48, 64))
            msg_rect_2 = msg_2.get_rect(center=(largura // 2, altura - 200))
            janela.blit(msg_1, msg_rect_1)
            janela.blit(msg_2, msg_rect_2)
            janela.blit(font_pontos.render(f'{pontos:0>3} {recorde:0>3}', True, (255, 255, 255)), (10, 10))
            pygame.display.update()

        bird.rect.y = 220
        pontos = bird.angulo = bird.velocidade = gravidade = 0
        inicio = False
        velocidade = 5
        sprite_group_obstaculos.empty()
        for n in range(5):
            obstaculo = ObstaculoUp(n * 225 + largura)
            sprite_group_obstaculos.add(obstaculo)
            sprite_group_obstaculos.add(ObstaculoDown(obstaculo))

    if pontos > recorde:
        recorde = pontos
        with open(os.path.join(diretorio_principal, 'recorde.txt'), 'w') as arquivo:
            arquivo.write(str(recorde))
    
    janela.blit(font_pontos.render(f'{pontos:0>3} {recorde:0>3}', True, (255, 255, 255)), (10, 10))
    pygame.display.flip()
