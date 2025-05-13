import pygame

def carregar_recursos():
    recursos = {}

    # Imagens dos jogadores e projéteis
    recursos['jogador1'] = pygame.image.load('assets/player1.png').convert_alpha()
    recursos['jogador2'] = pygame.image.load('assets/player2.png').convert_alpha()
    recursos['bala1'] = pygame.transform.scale(pygame.image.load('assets/bala1.png'), (15, 15))
    recursos['bala2'] = pygame.transform.scale(pygame.image.load('assets/bala2.png'), (15, 15))

    # Granada e explosão
    recursos['granada'] = pygame.transform.scale(pygame.image.load('assets/granada.png'), (30, 30))
    recursos['explosao'] = pygame.transform.scale(pygame.image.load('assets/explosao.png'), (60, 60))

    # Coração
    coracao = pygame.image.load('assets/coracao.png').convert_alpha()
    recursos['coracao'] = pygame.transform.scale(coracao, (30, 16))

    # Som
    recursos['som_tiro'] = pygame.mixer.Sound('assets/MA_Designed_ModifiedGunBlasts_2.wav')

    # Fonte
    recursos['fonte_padrao'] = pygame.font.SysFont('arial', 26)

    return recursos
