import pygame

def carregar_recursos():
    recursos = {}

    # === IMAGENS DOS JOGADORES ===
    recursos['jogador1'] = pygame.transform.scale(
        pygame.image.load('assets/player1.png').convert_alpha(), (50, 50)
    )
    recursos['jogador2'] = pygame.transform.scale(
        pygame.image.load('assets/player2.png').convert_alpha(), (50, 50)
    )

    # === PROJÉTEIS (BALAS) DE CADA JOGADOR ===
    recursos['bala1'] = pygame.transform.scale(
        pygame.image.load('assets/bala1.png').convert_alpha(), (15, 15)
    )
    recursos['bala2'] = pygame.transform.scale(
        pygame.image.load('assets/bala2.png').convert_alpha(), (15, 15)
    )

    # === CORAÇÃO (VIDAS) ===
    coracao_img = pygame.image.load('assets/coracao.png').convert_alpha()
    recursos['coracao'] = pygame.transform.scale(coracao_img, (30, 16))

    # === SOM ===
    recursos['som_tiro'] = pygame.mixer.Sound('assets/MA_Designed_ModifiedGunBlasts_2.wav')

    # === FONTE PADRÃO ===
    recursos['fonte_padrao'] = pygame.font.SysFont('arial', 30)

    return recursos
