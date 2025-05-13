import pygame
from assets import carregar_recursos
from game_screen import tela_jogo
from config import LARGURA, ALTURA

pygame.init()
pygame.mixer.init()

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Duelos Pixelados")

recursos = carregar_recursos()
tela_jogo(janela, recursos)

pygame.quit()
