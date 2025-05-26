import pygame
from config import LARGURA, ALTURA

class Soldado(pygame.sprite.Sprite):
    def __init__(self, animacoes, x, y):
        super().__init__()
        self.animacoes = animacoes
        self.estado = 'parado'
        self.frame = 0
        self.image = self.animacoes[self.estado][self.frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.velocidade = 3
        self.andando_para_tras = False

    def update(self, teclas):
        self.estado = 'parado'
        self.andando_para_tras = False

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
            self.estado = 'andando'
            self.andando_para_tras = True
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
            self.estado = 'andando'

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            self.rect.y -= self.velocidade
            self.estado = 'andando'
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidade
            self.estado = 'andando'

        self.rect.clamp_ip(pygame.Rect(0, 0, LARGURA, ALTURA))

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            self.frame = (self.frame + 1) % len(self.animacoes[self.estado])
            anim = self.estado
            if self.estado == 'andando' and self.andando_para_tras:
                anim = 'andando_invertido'
            self.image = self.animacoes[anim][self.frame]
