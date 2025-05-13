import pygame
from sprites import Jogador, Projetil
from config import FPS, LARGURA, ALTURA, CINZA_ESCURO

def desenhar_vidas(janela, recursos, jogador1, jogador2):
    imagem_coracao = recursos['coracao']
    coracao_largura = imagem_coracao.get_width()
    espacamento = -15

    for i in range(jogador1.vidas):
        x = jogador1.rect.centerx - ((coracao_largura * jogador1.vidas + espacamento * (jogador1.vidas - 1)) // 2) + i * (coracao_largura + espacamento)
        y = jogador1.rect.top - 30
        janela.blit(imagem_coracao, (x, y))

    for i in range(jogador2.vidas):
        x = jogador2.rect.centerx - ((coracao_largura * jogador2.vidas + espacamento * (jogador2.vidas - 1)) // 2) + i * (coracao_largura + espacamento)
        y = jogador2.rect.top - 30
        janela.blit(imagem_coracao, (x, y))

def desenhar_menu_pausa(janela, fonte):
    overlay = pygame.Surface((LARGURA, ALTURA))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    janela.blit(overlay, (0, 0))

    texto = fonte.render("JOGO PAUSADO", True, (255, 255, 255))
    continuar = fonte.render("Pressione C para CONTINUAR", True, (200, 200, 200))
    reiniciar = fonte.render("Pressione R para REINICIAR", True, (200, 200, 200))

    janela.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - 80))
    janela.blit(continuar, (LARGURA//2 - continuar.get_width()//2, ALTURA//2 - 20))
    janela.blit(reiniciar, (LARGURA//2 - reiniciar.get_width()//2, ALTURA//2 + 30))
    pygame.display.flip()

def tela_jogo(janela, recursos):
    relogio = pygame.time.Clock()
    executando = True
    pausado = False

    todos_sprites = pygame.sprite.Group()
    projeteis = pygame.sprite.Group()

    controles1 = {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d, 'disparo': pygame.K_SPACE}
    controles2 = {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT, 'disparo': pygame.K_RSHIFT}

    jogador1 = Jogador(recursos['jogador1'], 100, ALTURA // 2, controles1, recursos, direcao_tiro=1, id_jogador=1)
    jogador2 = Jogador(recursos['jogador2'], LARGURA - 100, ALTURA // 2, controles2, recursos, direcao_tiro=-1, id_jogador=2)

    todos_sprites.add(jogador1, jogador2)

    # Fonte extra para Menu (P)
    fonte_menu = pygame.font.SysFont('Courier New', 22, bold=True)

    while executando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausado = not pausado

                if pausado:
                    if evento.key == pygame.K_c:
                        pausado = False
                    elif evento.key == pygame.K_r:
                        tela_jogo(janela, recursos)
                        return

        if pausado:
            desenhar_menu_pausa(janela, recursos['fonte_padrao'])
            continue

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

        # Texto "Menu (P)" estilo arcade
        texto_menu = fonte_menu.render("Menu (P)", True, (255, 215, 0))  # amarelo estilo arcade
        janela.blit(texto_menu, (LARGURA - texto_menu.get_width() - 10, 30))  # margem superior de 30px

        todos_sprites.draw(janela)
        pygame.display.flip()
