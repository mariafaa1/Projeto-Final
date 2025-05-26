import pygame
from sprites import Soldado
from config import FPS

def tela_jogo(janela, animacoes):
    relogio = pygame.time.Clock()
    soldado = Soldado(animacoes)
    grupo = pygame.sprite.Group(soldado)

    executando = True
    while executando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        teclas = pygame.key.get_pressed()
        grupo.update(teclas)

        janela.fill((30, 30, 30))
        grupo.draw(janela)
        pygame.display.flip()
