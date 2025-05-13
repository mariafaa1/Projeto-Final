import pygame

def carregar_recursos():
    recursos = {}

    recursos['jogador1'] = pygame.image.load('assets/player1.png').convert_alpha()
    recursos['jogador2'] = pygame.image.load('assets/player2.png').convert_alpha()
    recursos['bala1'] = pygame.transform.scale(pygame.image.load('assets/bala1.png'), (15, 15))
    recursos['bala2'] = pygame.transform.scale(pygame.image.load('assets/bala2.png'), (15, 15))
    recursos['granada'] = pygame.transform.scale(pygame.image.load('assets/granada.png'), (20, 20))
    recursos['explosao'] = pygame.transform.scale(pygame.image.load('assets/explosao.png'), (60, 60))
    recursos['coracao'] = pygame.transform.scale(pygame.image.load('assets/coracao.png'), (30, 16))

    recursos['som_tiro'] = pygame.mixer.Sound('assets/MA_Designed_ModifiedGunBlasts_2.wav')

    recursos['fonte_padrao'] = pygame.font.SysFont('arcadeclassic', 22)

    return recursos
