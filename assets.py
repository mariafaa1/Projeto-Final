import pygame
import os

def carregar_recursos():
    recursos = {}

    # Imagens dos jogadores
    recursos['jogador1'] = pygame.transform.scale(
        pygame.image.load(os.path.join('assets', 'player1.png')).convert_alpha(),
        (60, 60)
    )
    recursos['jogador2'] = pygame.transform.scale(
        pygame.image.load(os.path.join('assets', 'player2.png')).convert_alpha(),
        (60, 60)
    )

    # Imagens das balas (diferentes para cada jogador)
    recursos['bala1'] = pygame.transform.scale(
        pygame.image.load(os.path.join('assets', 'bala1.png')).convert_alpha(),
        (20, 8)
    )
    recursos['bala2'] = pygame.transform.scale(
        pygame.image.load(os.path.join('assets', 'bala2.png')).convert_alpha(),
        (20, 8)
    )

    # Imagem dos corações (vidas)
    coracao = pygame.image.load(os.path.join('assets', 'coracao.png')).convert_alpha()
    recursos['coracao'] = pygame.transform.scale(coracao, (30, 16))

    # Som do tiro
    recursos['som_tiro'] = pygame.mixer.Sound(os.path.join('assets', 'MA_Designed_ModifiedGunBlasts_2.wav'))

    # Fonte
    recursos['fonte_padrao'] = pygame.font.SysFont('arial', 30)

    return recursos
