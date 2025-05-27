import pygame
from sprites import Soldado
from config import FPS, FUNDO_BRANCO

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

        janela.fill(FUNDO_BRANCO)

        # Desenhar todos os sprites manualmente
        for sprite in grupo:
            sprite.draw(janela)

        pygame.display.flip()
