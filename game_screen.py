import pygame
from sprites import Jogador, Projetil
from config import FPS, LARGURA, ALTURA, CINZA_ESCURO

def tela_jogo(janela, recursos):
    relogio = pygame.time.Clock()
    executando = True

    todos_sprites = pygame.sprite.Group()
    projeteis = pygame.sprite.Group()

    # Teclas dos jogadores
    controles1 = {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d, 'disparo': pygame.K_SPACE}
    controles2 = {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT, 'disparo': pygame.K_RSHIFT}

    # Criar jogadores
    jogador1 = Jogador(recursos['jogador1'], LARGURA // 4, ALTURA - 60, controles1, recursos)
    jogador2 = Jogador(recursos['jogador2'], LARGURA * 3 // 4, 60, controles2, recursos)

    todos_sprites.add(jogador1, jogador2)

    while executando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        # Atualizar estado dos jogadores
        teclas = pygame.key.get_pressed()
        jogador1.atualizar(teclas, projeteis, todos_sprites)
        jogador2.atualizar(teclas, projeteis, todos_sprites)
        projeteis.update()

        # Verificar colisões: Projetil do jogador1 atinge jogador2
        for proj in projeteis:
            if proj.jogador_origem == jogador1 and proj.rect.colliderect(jogador2.rect):
                jogador2.perder_vida()
                proj.kill()
            elif proj.jogador_origem == jogador2 and proj.rect.colliderect(jogador1.rect):
                jogador1.perder_vida()
                proj.kill()

        # Verifica se algum jogador perdeu todas as vidas
        if jogador1.vidas <= 0 or jogador2.vidas <= 0:
            print("Fim da fase!")
            executando = False

        # Desenhar na tela
        janela.fill(CINZA_ESCURO)
        todos_sprites.draw(janela)
        pygame.display.flip()