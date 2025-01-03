import pygame, os
from lib.constantes import *
from sys import exit
from random import randint, randrange
from math import ceil


pygame.init()

janela = pygame.display.set_mode((LARGURA, ALTURA))
try:
    pygame.display.set_icon(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird_icon.png')).convert_alpha())
except:
    pass
pygame.display.set_caption('Flappy Bird')
relogio = pygame.time.Clock()

som_score = pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'point.wav'))
som_score.set_volume(0.25)
som_death = pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'hit.wav'))
som_death.set_volume(0.25)
som_game_over = pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'death_sound.wav'))
som_jump = pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'jump.wav'))
som_jump.set_volume(0.25)

sprite_group_background = pygame.sprite.Group()
sprite_group_principal = pygame.sprite.Group()
sprite_group_obstaculos = []

velocidade = 5
gravidade = 0
inicio = False
pontos = 0
permissao = [True] * 5


def draw_text(msg: str, font: str, tam: int, pos: tuple[int, int],  color: tuple[int, int, int] = (0, 0, 0), shadow: None | tuple[int, int, tuple] = None) -> None:
    font = pygame.font.SysFont(font, tam)
    if shadow:
        msg_formatada = font.render(msg, True, shadow[2])
        janela.blit(msg_formatada, msg_formatada.get_rect(center=(pos[0] + shadow[0], pos[1] + shadow[1])))
    msg_formatada = font.render(msg, True, color)
    janela.blit(msg_formatada, msg_formatada.get_rect(center=pos))


class SpriteSheet:
    def __init__(self, sprite_sheet: str, size: tuple):
        sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        width = sprite_sheet.get_width()
        height = sprite_sheet.get_height()
        self.sprites = []
        for l in range(0, height, size[1]):
            for c in range(0, width, size[0]):
                self.sprites.append(sprite_sheet.subsurface(c, l, *size))
    
    def get_sprites(self) -> list:
        return self.sprites


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites_config()
        self.image_idx = 0
        self.angulo = 0
        self.x_pos, self.y_pos = LARGURA / 4, 220
        self.exibicao_config()
        self.velocidade = 0
        self.pulo = False
    
    def update(self) -> None:
        self.animar()
        self.gravidade()
        if self.pulo:
            self.velocidade = -15
        self.exibicao_config()
        self.pulo = False
    
    def rotacionar(self) -> None:
        if inicio:
            self.angulo = (-self.velocidade + 18) * 3
            if self.angulo > 15:
                self.angulo = 15
            if self.angulo < -45:
                self.angulo = -45
        self.image = pygame.transform.rotate(self.sprites[int(self.image_idx)], self.angulo)
    
    def exibicao_config(self) -> None:
        self.image = self.sprites[int(self.image_idx)]
        self.rotacionar()
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rect_colision = pygame.Rect(self.x_pos - 16, self.y_pos - 14, 34, 27)
    
    def gravidade(self) -> None:
        self.velocidade += gravidade
        self.y_pos += self.velocidade
    
    def sprites_config(self) -> None:
        numero = randrange(0, 16, 4)
        sprite_sheet = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird.png'), (64, 64))
        self.sprites = sprite_sheet.get_sprites()[numero:numero + 4]
    
    def animar(self) -> None:
        self.image_idx += 0.5
        if self.image_idx >= len(self.sprites):
            self.image_idx = 0
    
    def pular(self) -> None:
        self.pulo = True


class Nuvens(pygame.sprite.Sprite):
    def __init__(self, x_pos: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird_nuvens.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 275
    
    def update(self) -> None:
        if self.rect.right <= 0:
            self.rect.x = self.image.get_width() + self.rect.right
        self.rect.x -= ceil(velocidade / 5)


class Predios(pygame.sprite.Sprite):
    def __init__(self, x_pos: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird_predios.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 340
    
    def update(self) -> None:
        if self.rect.right <= 0:
            self.rect.x = self.image.get_width() + self.rect.right
        self.rect.x -= ceil(velocidade / 3)


class Arvores(pygame.sprite.Sprite):
    def __init__(self, x_pos: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird_arvores.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 403
    
    def update(self) -> None:
        if self.rect.right <= 0:
            self.rect.x = self.image.get_width() + self.rect.right
        self.rect.x -= ceil(velocidade / 2)


class Chao(pygame.sprite.Sprite):
    def __init__(self, x_pos: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird_chao.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 500
    
    def update(self) -> None:
        if self.rect.right <= 0:
            self.rect.x = self.image.get_width() + self.rect.right
        self.rect.x -= velocidade

class Obstaculo:
    def __init__(self, x_pos: int):
        self.x_pos = x_pos
        self.images = [
            pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird_obstaculo_superior.png')).convert_alpha(),
            pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird_obstaculo_inferior.png')).convert_alpha()                                           
        ]
        self.new_position()
    
    def new_position(self):
        y_pos = randint(-300, -100)
        self.rects = [
            self.images[0].get_rect(topleft=(self.x_pos, y_pos)),
            self.images[1].get_rect(topleft=(self.x_pos, y_pos + 528))
        ]
    
    def draw(self, screen: pygame.Surface):
        for idx, rect in enumerate(self.rects):
            screen.blit(self.images[idx], rect)
    
    def mover(self):
        for rect in self.rects:
            rect.x -= velocidade
        if rect.right <= 0:
            self.x_pos = LARGURA - rect.right + 173
            self.new_position()


for n in range(2):
    sprite_group_background.add(Nuvens(n * 900))

for n in range(2):
    sprite_group_background.add(Predios(n * 900))

for n in range(2):
    sprite_group_background.add(Arvores(n * 900))

for n in range(5):
    sprite_group_obstaculos.append(Obstaculo(n * 225 + LARGURA))

for n in range(2):
    sprite_group_principal.add(Chao(n * 910))

bird = Bird()
sprite_group_principal.add(bird)

while True:
    relogio.tick(FPS)
    janela.fill((0, 153, 204))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w] and not bird.pulo and velocidade:
            som_jump.play()
            inicio = True
            bird.pular()

    sprite_group_background.draw(janela)
    for obstaculo in sprite_group_obstaculos:
        obstaculo.draw(janela)
    sprite_group_principal.draw(janela)

    for idx, obstaculo in enumerate(sprite_group_obstaculos):
        if obstaculo.rects[0].centerx <= 225 and permissao[idx]:
            som_score.play()
            permissao[idx] = False
            pontos += 1
        elif obstaculo.rects[0].left >= LARGURA:
            permissao[idx] = True

    if inicio:
        gravidade = 1.5
        for obstaculo in sprite_group_obstaculos:
            obstaculo.mover()
        draw_text(str(pontos), '04b19', 60, (LARGURA // 2, 50), 'white', (4, 4, (48, 48, 64)))
    else:
        name = pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird_name.png')).convert_alpha(), (384, 88))
        janela.blit(name, name.get_rect(center=(LARGURA // 2, 100)))
        draw_text('Press SPACE, W or UP to start', '04b19', 40, (LARGURA // 2, 557), 'white', (5, 5, (48, 48, 64)))

    for obstaculo in sprite_group_obstaculos:
        for rect in obstaculo.rects:
            if bird.rect_colision.colliderect(rect.x - velocidade, rect.y - ceil(bird.velocidade), rect.width, rect.height) and velocidade != 0:
                som_death.play()
                velocidade = 0
                break
    
    for item in sprite_group_principal:
        if item is not bird:
            if bird.rect_colision.colliderect(item.rect.x, item.rect.y, item.rect.width, item.rect.height):
                som_game_over.play()
                game_over = pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'flappy_bird_game_over.png')).convert_alpha(), (564, 114))
                janela.blit(game_over, game_over.get_rect(center=(LARGURA // 2, ALTURA // 2)))
                fim = True
                while fim:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            fim = False

                    draw_text('R para reiniciar', '04b19', 40, (LARGURA // 2, 557), 'white', (5, 5, (48, 48, 64)))
                    pygame.display.flip()

                bird.y_pos = 220
                pontos = bird.angulo = bird.velocidade = gravidade = 0
                inicio = False
                velocidade = 5
                sprite_group_obstaculos.clear()
                for n in range(5):
                    sprite_group_obstaculos.append(Obstaculo(n * 225 + LARGURA))
                break

    sprite_group_background.update()
    sprite_group_principal.update()
    pygame.display.flip()
