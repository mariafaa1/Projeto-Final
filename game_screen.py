import pygame
import random
from sprites import Jogador, Projetil, Granada, GranadaLançada
from config import FPS, LARGURA, ALTURA, CINZA_ESCURO
from pygame.locals import *

def desenhar_vidas(janela, recursos, jogador1, jogador2):
    coracao = recursos['coracao']
    espacamento = -15
    for i in range(jogador1.vidas):
        x = jogador1.rect.centerx - ((coracao.get_width() * jogador1.vidas + espacamento * (jogador1.vidas - 1)) // 2) + i * (coracao.get_width() + espacamento)
        janela.blit(coracao, (x, jogador1.rect.top - 30))
    for i in range(jogador2.vidas):
        x = jogador2.rect.centerx - ((coracao.get_width() * jogador2.vidas + espacamento * (jogador2.vidas - 1)) // 2) + i * (coracao.get_width() + espacamento)
        janela.blit(coracao, (x, jogador2.rect.top - 30))

def desenhar_menu_pausa(janela, fonte):
    overlay = pygame.Surface((LARGURA, ALTURA))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    janela.blit(overlay, (0, 0))

    texto = fonte.render("JOGO PAUSADO", True, (255, 255, 255))
    continuar = fonte.render("Pressione C para CONTINUAR", True, (0, 255, 0))
    reiniciar = fonte.render("Pressione R para REINICIAR", True, (255, 0, 0))

    janela.blit(texto, (LARGURA//2 - texto.get_width()//2, 80))
    janela.blit(continuar, (LARGURA//2 - continuar.get_width()//2, 130))
    janela.blit(reiniciar, (LARGURA//2 - reiniciar.get_width()//2, 170))

def desenhar_menu_texto(janela, fonte):
    texto_menu = fonte.render("Menu (P)", True, (255, 255, 0))
    janela.blit(texto_menu, (LARGURA - texto_menu.get_width() - 30, 30))

def tela_jogo(janela, recursos):
    clock = pygame.time.Clock()
    pausado = False
    executando = True

    todos_sprites = pygame.sprite.Group()
    projeteis = pygame.sprite.Group()
    granadas = pygame.sprite.Group()
    explosoes = pygame.sprite.Group()

    controles1 = {'cima': K_w, 'baixo': K_s, 'esquerda': K_a, 'direita': K_d, 'disparo': K_SPACE, 'granada': K_g}
    controles2 = {'cima': K_UP, 'baixo': K_DOWN, 'esquerda': K_LEFT, 'direita': K_RIGHT, 'disparo': K_RSHIFT, 'granada': K_k}

    jogador1 = Jogador(recursos['jogador1'], 100, ALTURA // 2, controles1, recursos, 1, 1)
    jogador2 = Jogador(recursos['jogador2'], LARGURA - 100, ALTURA // 2, controles2, recursos, -1, 2)

    todos_sprites.add(jogador1, jogador2)

    def spawn_granadas():
        granadas.empty()
        for _ in range(2):
            x = random.randint(100, LARGURA - 100)
            y = random.randint(100, ALTURA - 100)
            g = Granada(recursos['granada'], x, y)
            granadas.add(g)
            todos_sprites.add(g)

    spawn_granadas()

    while executando:
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                executando = False
            elif evento.type == KEYDOWN:
                if evento.key == K_p:
                    pausado = not pausado
                if pausado:
                    if evento.key == K_c:
                        pausado = False
                    elif evento.key == K_r:
                        tela_jogo(janela, recursos)
                        return
                if evento.key == jogador1.controles['granada'] and jogador1.tem_granada:
                    g = GranadaLançada(jogador2.rect.centerx, jogador2.rect.centery, recursos, jogador2)
                    explosoes.add(g)
                    todos_sprites.add(g)
                    jogador1.tem_granada = False
                if evento.key == jogador2.controles['granada'] and jogador2.tem_granada:
                    g = GranadaLançada(jogador1.rect.centerx, jogador1.rect.centery, recursos, jogador1)
                    explosoes.add(g)
                    todos_sprites.add(g)
                    jogador2.tem_granada = False

        if pausado:
            desenhar_menu_pausa(janela, recursos['fonte_padrao'])
            pygame.display.flip()
            continue

        teclas = pygame.key.get_pressed()
        jogador1.atualizar(teclas, projeteis, todos_sprites, granadas)
        jogador2.atualizar(teclas, projeteis, todos_sprites, granadas)

        projeteis.update()
        explosoes.update()

        for proj in projeteis:
            if proj.dono != jogador1 and proj.rect.colliderect(jogador1.rect):
                jogador1.perder_vida()
                proj.kill()
            elif proj.dono != jogador2 and proj.rect.colliderect(jogador2.rect):
                jogador2.perder_vida()
                proj.kill()

        janela.blit(recursos['fundo'], (0, 0))
        todos_sprites.draw(janela)
        desenhar_vidas(janela, recursos, jogador1, jogador2)
        desenhar_menu_texto(janela, recursos['fonte_padrao'])
        pygame.display.flip()
