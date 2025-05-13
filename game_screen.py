import pygame
from sprites import Jogador, Projetil
from config import FPS, LARGURA, ALTURA, CINZA_ESCURO

def desenhar_vidas(janela, recursos, jogador1, jogador2):
    imagem_coracao = recursos['coracao']
    coracao_largura = imagem_coracao.get_width()
    espacamento = -10  

    for i in range(jogador1.vidas):
        x = jogador1.rect.centerx - ((coracao_largura * jogador1.vidas + espacamento * (jogador1.vidas - 1)) // 2) + i * (coracao_largura + espacamento)
        y = jogador1.rect.top - 30
        janela.blit(imagem_coracao, (x, y))

    for i in range(jogador2.vidas):
        x = jogador2.rect.centerx - ((coracao_largura * jogador2.vidas + espacamento * (jogador2.vidas - 1)) // 2) + i * (coracao_largura + espacamento)
        y = jogador2.rect.top - 30
        janela.blit(imagem_coracao, (x, y))

def tela_jogo(janela, recursos):
    relogio = pygame.time.Clock()
    executando = True

    todos_sprites = pygame.sprite.Group()
    projeteis = pygame.sprite.Group()

    controles1 = {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d, 'disparo': pygame.K_SPACE}
    controles2 = {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT, 'disparo': pygame.K_RSHIFT}

    # Jogador 1 (esquerda) atira para a direita (direcao_tiro = 1)
    jogador1 = Jogador(recursos['jogador1'], 100, ALTURA // 2, controles1, recursos, direcao_tiro=1, id_jogador=1)

    # Jogador 2 (direita) atira para a esquerda (direcao_tiro = -1)
    jogador2 = Jogador(recursos['jogador2'], LARGURA - 100, ALTURA // 2, controles2, recursos, direcao_tiro=-1, id_jogador=2)

    todos_sprites.add(jogador1, jogador2)

    while executando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        teclas = pygame.key.get_pressed()
        jogador1.atualizar(teclas, projeteis, todos_sprites)
        jogador2.atualizar(teclas, projeteis, todos_sprites)
        projeteis.update()

        for projetil in projeteis:
            if projetil.jogador_dono != jogador1 and projetil.rect.colliderect(jogador1.rect):
                jogador1.perder_vida()
                projetil.kill()
            elif projetil.jogador_dono != jogador2 and projetil.rect.colliderect(jogador2.rect):
                jogador2.perder_vida()
                projetil.kill()

        janela.fill(CINZA_ESCURO)
        desenhar_vidas(janela, recursos, jogador1, jogador2)
        todos_sprites.draw(janela)
        pygame.display.flip()
