import os


LARGURA, ALTURA = 900, 600
FPS = 30

DIRETORIO_PRINCIPAL = os.path.dirname(__file__).replace('\\', '/')
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_PRINCIPAL, 'Imagens').replace('\\', '/')
DIRETORIO_SONS = os.path.join(DIRETORIO_PRINCIPAL, 'Sons').replace('\\', '/')
