import pygame
from sprites import Soldado
from config import (
    FPS, FUNDO_BRANCO, LARGURA, ALTURA,
    JOGANDO, GAME_OVER, PRETO, BRANCO,
    FONTE_TAMANHO, CAMINHO_FONTE
)
# No início do arquivo:
from inimigos_codigos.orc_normal import OrcNormal
from inimigos_codigos.esqueleto import Esqueleto

def tela_jogo(janela, animacoes):
    relogio = pygame.time.Clock()
    
    grupo_inimigos = pygame.sprite.Group()
    grupo_projeteis = pygame.sprite.Group()
    
    soldado = Soldado(animacoes, grupo_inimigos, grupo_projeteis)
    grupo_inimigos.add(OrcNormal(x=300, y=300, alvo=soldado))
    grupo_inimigos.add(Esqueleto(x=500, y=300, alvo=soldado))
    
    grupo_jogador = pygame.sprite.Group(soldado)
    
    estado_jogo = JOGANDO
    fonte = pygame.font.Font(CAMINHO_FONTE, FONTE_TAMANHO)
    executando = True

    while executando:
        dt = relogio.tick(FPS) / 1000  # Delta time em segundos

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and estado_jogo == GAME_OVER:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 300 <= mouse_x <= 500 and 400 <= mouse_y <= 450:
                    return True

        teclas = pygame.key.get_pressed()

        if estado_jogo == JOGANDO:
            grupo_jogador.update(teclas)
            grupo_inimigos.update(dt)  # Passando dt aqui
            grupo_projeteis.update()

            if soldado.animacao_morte_concluida and (pygame.time.get_ticks() - soldado.tempo_morte_concluida >= 3000):
                estado_jogo = GAME_OVER

        janela.fill(FUNDO_BRANCO)

        if estado_jogo == JOGANDO:
            grupo_jogador.draw(janela)
            grupo_inimigos.draw(janela)
            grupo_projeteis.draw(janela)
            
            for sprite in grupo_jogador:
                sprite.draw_hp_bar(janela)
            for inimigo in grupo_inimigos:
                inimigo.draw_hp_bar(janela)
        elif estado_jogo == GAME_OVER:
            texto_game_over = fonte.render("GAME OVER", True, BRANCO)
            texto_rect = texto_game_over.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
            janela.blit(texto_game_over, texto_rect)

            pygame.draw.rect(janela, BRANCO, (300, 400, 200, 50))
            texto_reiniciar = fonte.render("Reiniciar", True, PRETO)
            texto_reiniciar_rect = texto_reiniciar.get_rect(center=(LARGURA // 2, 425))
            janela.blit(texto_reiniciar, texto_reiniciar_rect)

        pygame.display.flip()

    return False  # Retorna False se o jogo não for reiniciado