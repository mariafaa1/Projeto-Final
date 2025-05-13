import pygame
from config import LARGURA, ALTURA, VELOCIDADE_JOGADOR, VELOCIDADE_PROJETIL, TEMPO_RECARGA_DISPARO, VIDAS_MAXIMAS

class Jogador(pygame.sprite.Sprite):
    def __init__(self, imagem, pos_x, pos_y, controles, recursos, direcao_tiro):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.velocidade = VELOCIDADE_JOGADOR
        self.controles = controles
        self.recursos = recursos
        self.ultimo_disparo = pygame.time.get_ticks()
        self.vidas = VIDAS_MAXIMAS
        self.direcao_tiro = direcao_tiro

    def atualizar(self, teclas, grupo_projeteis, todos_sprites):
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
        if teclas[self.controles['disparo']] and agora - self.ultimo_disparo > TEMPO_RECARGA_DISPARO:
            projetil = Projetil(self.rect.centerx, self.rect.centery, self.recursos['bala'], self.direcao_tiro, self)
            grupo_projeteis.add(projetil)
            todos_sprites.add(projetil)
            self.recursos['som_tiro'].play()
            self.ultimo_disparo = agora

    def perder_vida(self):
        self.vidas -= 1
        if self.vidas <= 0:
            self.kill()

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem, direcao, jogador_dono):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = VELOCIDADE_PROJETIL
        self.direcao = direcao
        self.jogador_dono = jogador_dono

    def update(self):
        self.rect.x += self.direcao * self.velocidade
        if self.rect.right < 0 or self.rect.left > LARGURA:
            self.kill()
