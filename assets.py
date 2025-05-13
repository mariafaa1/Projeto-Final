import pygame

def carregar_recursos():
    recursos = {}

    # Imagens
    recursos['jogador1'] = pygame.image.load('assets/player1.png').convert_alpha()
    recursos['jogador2'] = pygame.image.load('assets/player2.png').convert_alpha()
    recursos['bala'] = pygame.image.load('assets/bullet.png').convert_alpha()
    recursos['coracao'] = pygame.image.load('assets/coracao.png').convert_alpha()  # <-- ESTA LINHA É ESSENCIAL

    # Sons
    recursos['som_tiro'] = pygame.mixer.Sound('assets/MA_Designed_ModifiedGunBlasts_2.wav')

    # Fonte
    recursos['fonte_padrao'] = pygame.font.SysFont('arial', 30)

    return recursos
