import pygame
import os

def carregar_animacoes():
    animacoes = {
        'parado': [],
        'andando': [],
        'andando_invertido': []
    }

    for i in range(6):
        img = pygame.image.load(os.path.join('assets', 'soldado_parado', f'soldado_parado{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (40, 40))
        animacoes['parado'].append(img)

    for i in range(7):
        img = pygame.image.load(os.path.join('assets', 'soldado_andando', f'soldado_andando{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (40, 40))
        animacoes['andando'].append(img)
        animacoes['andando_invertido'].append(pygame.transform.flip(img, True, False))

    return animacoes
