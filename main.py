import pygame
from config import LARGURA, ALTURA
from assets import carregar_animacoes
from game_screen import game_screen

pygame.init()
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Animação do Soldado")

animacoes = carregar_animacoes()

game_screen(janela, animacoes)
pygame.quit()
