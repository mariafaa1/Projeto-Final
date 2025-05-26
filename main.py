import pygame
from config import LARGURA, ALTURA
from assets import carregar_animacoes
from game_screen import tela_jogo

# Inicialização do Pygame
pygame.init()

# Criação da janela do jogo
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Fantasia - Soldado")

# Carregamento das animações
animacoes = carregar_animacoes()

# Chamada da função tela_jogo
tela_jogo(janela, animacoes)

# Finaliza o Pygame após o jogo terminar
pygame.quit()
