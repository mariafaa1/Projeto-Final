import pygame
from sprites import Soldado
from config import LARGURA, ALTURA, FPS

def game_screen(janela, animacoes):
    relogio = pygame.time.Clock()
    todos_sprites = pygame.sprite.Group()

    soldado = Soldado(animacoes, LARGURA//2, ALTURA//2)
    todos_sprites.add(soldado)

    executando = True
    while executando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        teclas = pygame.key.get_pressed()
        todos_sprites.update(teclas)

        janela.fill((20, 20, 20))
        todos_sprites.draw(janela)
        pygame.display.flip()
