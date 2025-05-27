import pygame
from sprites import Soldado
from config import FPS, FUNDO_BRANCO
from mapa import gerar_mapa  # Importando a função de gerar o mapa

def tela_jogo(janela, animacoes):
    # Relógio para controle de FPS
    relogio = pygame.time.Clock()
    
    # Criar o jogador (Soldado) e o grupo de sprites
    soldado = Soldado(animacoes)
    grupo = pygame.sprite.Group(soldado)

    # Gerar o mapa
    mapa = gerar_mapa()  # Gera as paredes e o chão

    # Loop principal do jogo
    executando = True
    while executando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        teclas = pygame.key.get_pressed()
        grupo.update(teclas)

        janela.fill(FUNDO_BRANCO)

        # Desenha o mapa
        mapa.draw(janela)  # Desenha as paredes no mapa
        grupo.draw(janela)  # Desenha o soldado (personagem principal)

        pygame.display.flip()
