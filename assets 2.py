import pygame
import os

def carregar_animacoes():
    animacoes = {
        'parado': [],
        'andando': [],
        'ataque_leve': [],
        'ataque_pesado': [],
        'ataque_arco': [],
        'dano': [],
        'morrer': [],
    }

    for i in range(6):
        imagem = pygame.image.load(os.path.join('assets', 'soldado_parado', f'soldado_parado{i}.png')).convert_alpha()
        animacoes['parado'].append(imagem)

    for i in range(8):
        imagem = pygame.image.load(os.path.join('assets', 'soldado_andando', f'soldado_andando{i}.png')).convert_alpha()
        animacoes['andando'].append(imagem)

    for i in range(6):  # ATAQUE LEVE (6 frames)
        imagem = pygame.image.load(os.path.join('assets', 'ataque_leve', f'ataque_leve{i}.png')).convert_alpha()
        animacoes['ataque_leve'].append(imagem)

    for i in range(6):  # ATAQUE PESADO (6 frames)
        imagem = pygame.image.load(os.path.join('assets', 'ataque_pesado', f'ataque_pesado{i}.png')).convert_alpha()
        animacoes['ataque_pesado'].append(imagem)

    for i in range(9):  # ATAQUE ARCO (9 frames)
        imagem = pygame.image.load(os.path.join('assets', 'ataque_arco', f'ataque_arco{i}.png')).convert_alpha()
        animacoes['ataque_arco'].append(imagem)

    for i in range(4):  # DANO (4 frames)
        imagem = pygame.image.load(os.path.join('assets', 'dano_soldado', f'dano{i+1}.png')).convert_alpha()
        animacoes['dano'].append(imagem)

    for i in range(4):  # MORTE (4 frames)
        imagem = pygame.image.load(os.path.join('assets', 'morrer_soldado', f'morrer{i}.png')).convert_alpha()
        animacoes['morrer'].append(imagem)

    return animacoes