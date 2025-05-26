import pygame
from config import LARGURA, ALTURA
from assets import carregar_animacoes
from game_screen import tela_jogo

pygame.init()
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Fantasia - Soldado")
animacoes = carregar_animacoes()
tela_jogo(janela, animacoes)
pygame.quit()
