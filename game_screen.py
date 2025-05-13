import pygame
from sprites import Jogador, Bala
from config import FPS, LARGURA, ALTURA, CINZA_ESCURO

def tela_jogo(janela, recursos):
    relogio = pygame.time.Clock()
    executando = True

    todos_sprites = pygame.sprite.Group()
    balas = pygame.sprite.Group()

    # Teclas dos jogadores
    controles1 = {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d, 'atirar': pygame.K_SPACE}
    controles2 = {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT, 'atirar': pygame.K_RSHIFT}

    # Criar jogadores
    jogador1 = Jogador(recursos['jogador1'], LARGURA // 4, ALTURA - 60, controles1, recursos)
    jogador2 = Jogador(recursos['jogador2'], LARGURA * 3 // 4, 60, controles2, recursos)

    todos_sprites.add(jogador1, jogador2)

    while executando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        teclas = pygame.key.get_pressed()
        jogador1.atualizar(teclas, balas, todos_sprites)
        jogador2.atualizar(teclas, balas, todos_sprites)
        balas.update()

        janela.fill(CINZA_ESCURO)
        todos_sprites.draw(janela)
        pygame.display.flip()