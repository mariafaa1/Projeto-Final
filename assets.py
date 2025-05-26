import pygame
import os

def carregar_animacoes():
    animacoes = {
        'parado': [],
        'andando': [],
        'ataque_leve': []
    }

    for i in range(6):
        imagem = pygame.image.load(os.path.join('assets', 'soldado_parado', f'soldado_parado{i}.png')).convert_alpha()
        animacoes['parado'].append(imagem)

    for i in range(7):
        imagem = pygame.image.load(os.path.join('assets', 'soldado_andando', f'soldado_andando{i}.png')).convert_alpha()
        animacoes['andando'].append(imagem)

    for i in range(6):
        imagem = pygame.image.load(os.path.join('assets', 'ataque_leve', f'ataque_leve{i}.png')).convert_alpha()
        animacoes['ataque_leve'].append(imagem)

    return animacoes
