import pygame
import random
from config import LARGURA, ALTURA, VELOCIDADE_JOGADOR

# Definindo a largura e altura dos blocos
TAMANHO_BLOCO = 32  # Tamanho de cada bloco (parede ou chão)

# Classe que representa a parede
class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/parede.png').convert_alpha()  # Imagem da parede
        self.rect = self.image.get_rect(topleft=(x, y))  # Posiciona a parede

# Função para gerar o mapa
def gerar_mapa():
    mapa = pygame.sprite.Group()  # Grupo de todos os sprites do mapa (paredes e chão)

    # Geração das paredes em torno do mapa
    for x in range(0, LARGURA, TAMANHO_BLOCO):
        for y in range(0, ALTURA, TAMANHO_BLOCO):
            # Adicionando as paredes no contorno
            if x == 0 or x == LARGURA - TAMANHO_BLOCO or y == 0 or y == ALTURA - TAMANHO_BLOCO:
                parede = Parede(x, y)
                mapa.add(parede)

    # Geração de paredes internas aleatórias
    for _ in range(50):  # Gera 50 paredes aleatórias no mapa
        x = random.randint(1, (LARGURA // TAMANHO_BLOCO) - 1) * TAMANHO_BLOCO
        y = random.randint(1, (ALTURA // TAMANHO_BLOCO) - 1) * TAMANHO_BLOCO
        parede = Parede(x, y)
        mapa.add(parede)

    return mapa
