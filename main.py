import pygame
from assets import load_assets
from game_screen import game_screen
from config import WIDTH, HEIGHT

pygame.init()

# Configurações iniciais da janela
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duelos Pixelados: Arena 3x")

# Carrega os assets (imagens, sons, fontes)
assets = load_assets()

# Executa a tela principal do jogo
game_screen(window, assets)

pygame.quit()