import pygame
from config import LARGURA, ALTURA
from assets import carregar_animacoes
from game_screen import tela_jogo

pygame.init()
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Fantasia - Soldado")

animacoes = carregar_animacoes()

reiniciar = True
while reiniciar:
    reiniciar = tela_jogo(janela, animacoes)  # A função retorna True se o jogador quiser reiniciar

pygame.quit()