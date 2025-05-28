import pygame
import random
from config import LARGURA, ALTURA, VELOCIDADE_JOGADOR

# Define o tamanho dos blocos (tanto para parede quanto para chão)
TAMANHO_BLOCO = 32

# Classe que representa uma parede do mapa
class Parede(pygame.sprite.Sprite):
    """
    Sprite que representa um bloco de parede no mapa.
    """
    def __init__(self, x, y):
        super().__init__()
        # Carrega a imagem da parede
        self.image = pygame.image.load('assets/parede.png').convert_alpha()
        # Define a posição inicial da parede no mapa
        self.rect = self.image.get_rect(topleft=(x, y))

# Função responsável por gerar o layout do mapa (paredes externas e internas)
def gerar_mapa():
    """
    Cria e retorna um grupo de sprites representando o mapa.
    Inclui as paredes nas bordas e algumas paredes aleatórias no interior.
    """
    mapa = pygame.sprite.Group()  # Grupo que conterá todos os blocos do mapa

    # Cria as paredes das bordas (contorno)
    for x in range(0, LARGURA, TAMANHO_BLOCO):
        for y in range(0, ALTURA, TAMANHO_BLOCO):
            # Condição para adicionar a parede apenas nas bordas
            if x == 0 or x == LARGURA - TAMANHO_BLOCO or y == 0 or y == ALTURA - TAMANHO_BLOCO:
                parede = Parede(x, y)
                mapa.add(parede)

    # Gera 50 paredes internas em posições aleatórias
    for _ in range(50):
        x = random.randint(1, (LARGURA // TAMANHO_BLOCO) - 1) * TAMANHO_BLOCO
        y = random.randint(1, (ALTURA // TAMANHO_BLOCO) - 1) * TAMANHO_BLOCO
        parede = Parede(x, y)
        mapa.add(parede)

    return mapa  # Retorna o grupo de sprites contendo todas as paredes
