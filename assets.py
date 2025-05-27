import pygame
import os

def carregar_animacoes():
    animacoes = {
        'parado': [],
        'andando': [],
        'ataque_leve': [],
        'ataque_pesado': [],
        'ataque_arco': []  # Adicionando animação de ataque à distância
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

    for i in range(6):
        imagem = pygame.image.load(os.path.join('assets', 'ataque_pesado', f'ataque_pesado{i}.png')).convert_alpha()
        animacoes['ataque_pesado'].append(imagem)

    # Carregando animação de ataque à distância
    for i in range(9):  # 9 frames para ataque arco
        imagem = pygame.image.load(os.path.join('assets', 'ataque_arco', f'ataque_arco{i}.png')).convert_alpha()
        animacoes['ataque_arco'].append(imagem)

    return animacoes
