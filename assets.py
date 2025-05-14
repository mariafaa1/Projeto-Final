import pygame

def carregar_recursos():
    recursos = {}

    recursos['jogador1'] = pygame.transform.scale(pygame.image.load('assets/player1.png'), (50, 50)).convert_alpha()
    recursos['jogador2'] = pygame.transform.scale(pygame.image.load('assets/player2.png'), (50, 50)).convert_alpha()
    recursos['bala1'] = pygame.transform.scale(pygame.image.load('assets/bala1.png'), (15, 15)).convert_alpha()
    recursos['bala2'] = pygame.transform.scale(pygame.image.load('assets/bala2.png'), (15, 15)).convert_alpha()
    recursos['granada'] = pygame.transform.scale(pygame.image.load('assets/granada.png'), (40, 40)).convert_alpha()
    recursos['explosao'] = pygame.transform.scale(pygame.image.load('assets/explosao.png'), (50, 50)).convert_alpha()
    recursos['fundo'] = pygame.transform.scale(pygame.image.load('assets/mapa1.png'), (1000, 600)).convert()
    
    coracao = pygame.image.load('assets/coracao.png').convert_alpha()
    recursos['coracao'] = pygame.transform.scale(coracao, (30, 16))
    recursos['som_tiro'] = pygame.mixer.Sound('assets/MA_Designed_ModifiedGunBlasts_2.wav')
    recursos['fonte_padrao'] = pygame.font.SysFont('arcadeclassic', 22)

    return recursos
