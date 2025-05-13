import pygame
from config import LARGURA, ALTURA, VELOCIDADE_JOGADOR, VELOCIDADE_BALA, INTERVALO_TIROS

class Jogador(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, controles, recursos):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = VELOCIDADE_JOGADOR
        self.controles = controles
        self.recursos = recursos
        self.ultimo_tiro = pygame.time.get_ticks()

    def atualizar(self, teclas, grupo_balas, grupo_todos):
        if teclas[self.controles['cima']]:
            self.rect.y -= self.velocidade
        if teclas[self.controles['baixo']]:
            self.rect.y += self.velocidade
        if teclas[self.controles['esquerda']]:
            self.rect.x -= self.velocidade
        if teclas[self.controles['direita']]:
            self.rect.x += self.velocidade

        self.rect.clamp_ip(pygame.Rect(0, 0, LARGURA, ALTURA))

        agora = pygame.time.get_ticks()
        if teclas[self.controles['atirar']] and agora - self.ultimo_tiro > INTERVALO_TIROS:
            bala = Bala(self.rect.centerx, self.rect.top, self.recursos['bala'], self)
            grupo_balas.add(bala)
            grupo_todos.add(bala)
            self.recursos['som_tiro'].play()
            self.ultimo_tiro = agora

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem, jogador):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = VELOCIDADE_BALA
        self.direcao = -1 if jogador.controles['cima'] == pygame.K_w else 1

    def update(self):
        self.rect.y += self.direcao * -self.velocidade
        if self.rect.bottom < 0 or self.rect.top > ALTURA:
            self.kill()