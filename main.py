#main.py
import pygame
from config import LARGURA, ALTURA
from assets import carregar_animacoes
from game_screen import tela_jogo
import sys

def main():
    # Inicialização do Pygame
    pygame.init()

    # Criar janela principal
    janela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Jogo de Fantasia - Soldado")

    # Carregar todas as animações necessárias
    animacoes = carregar_animacoes()

    # Loop principal do jogo
    reiniciar = Tue
    while reiniciar:
        reiniciar = tela_jogo(janela, animacoes)

    # Encerrar Pygame ao sair
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
