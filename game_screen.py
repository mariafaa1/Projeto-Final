import pygame
from sprites import Jogador, Projetil
from config import FPS, LARGURA, ALTURA, CINZA_ESCURO

def desenhar_vidas(janela, recursos, jogador):
    imagem_coracao = recursos['coracao']
    espacamento = 22
    for i in range(jogador.vidas):
        pos_x = jogador.rect.centerx - (jogador.vidas * espacamento // 2) + i * espacamento
        pos_y = jogador.rect.top - 28
        janela.blit(imagem_coracao, (pos_x, pos_y))

def tela_jogo(janela, recursos):
    relogio = pygame.time.Clock()
    executando = True

    todos_sprites = pygame.sprite.Group()
    projeteis = pygame.sprite.Group()

    controles1 = {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d, 'disparo': pygame.K_SPACE}
    controles2 = {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT, 'disparo': pygame.K_RSHIFT}

    jogador1 = Jogador(recursos['jogador1'], LARGURA // 4, ALTURA - 60, controles1, recursos)
    jogador2 = Jogador(recursos['jogador2'], LARGURA * 3 // 4, 60, controles2, recursos)

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

        # Colisões
        for projetil in projeteis:
            if projetil.jogador_origem != jogador1 and projetil.rect.colliderect(jogador1.rect):
                jogador1.perder_vida()
                projetil.kill()
            elif projetil.jogador_origem != jogador2 and projetil.rect.colliderect(jogador2.rect):
                jogador2.perder_vida()
                projetil.kill()

        janela.fill(CINZA_ESCURO)
        todos_sprites.draw(janela)
        desenhar_vidas(janela, recursos, jogador1)
        desenhar_vidas(janela, recursos, jogador2)
        pygame.display.flip()
