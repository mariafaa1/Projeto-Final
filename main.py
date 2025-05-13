import pygame
from assets import carregar_recursos
from game_screen import tela_jogo
from config import LARGURA, ALTURA

pygame.init()

# Criar a janela
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Duelos Pixelados: Arena 3x")

# Carregar imagens, sons e fontes
recursos = carregar_recursos()

# Executar o jogo
tela_jogo(janela, recursos)

pygame.quit()