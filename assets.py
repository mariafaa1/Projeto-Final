import pygame

def load_assets():
    assets = {}

    # Imagens
    assets['player1'] = pygame.image.load('assets/player1.png').convert_alpha()
    assets['player2'] = pygame.image.load('assets/player2.png').convert_alpha()
    assets['bullet'] = pygame.image.load('assets/bullet.png').convert_alpha()

    # Sons
    assets['som_tiro'] = pygame.mixer.Sound('assets/MA_Designed_ModifiedGunBlasts_2.wav')

    # Fonte
    assets['fonte_padrao'] = pygame.font.SysFont('arial', 30)

    return assets