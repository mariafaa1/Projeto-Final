import pygame
from config import LARGURA, ALTURA, VELOCIDADE_JOGADOR, VELOCIDADE_PROJETIL, TEMPO_RECARGA_DISPARO, VIDAS_MAXIMAS

class Jogador(pygame.sprite.Sprite):
    def __init__(self, imagem, pos_x, pos_y, controles, recursos):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.velocidade = VELOCIDADE_JOGADOR
        self.controles = controles
        self.recursos = recursos
        self.ultimo_disparo = pygame.time.get_ticks()
        self.vidas = VIDAS_MAXIMAS
        self.direcao_tiro = -1 if pos_y > ALTURA // 2 else 1  # Tiro depende da posição inicial

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
            projetil = Projetil(self.rect.centerx, self.rect.top, self.recursos['bala'], self, self.direcao_tiro)
            grupo_projeteis.add(projetil)
            todos_sprites.add(projetil)
            self.recursos['som_tiro'].play()
            self.ultimo_disparo = agora

    def perder_vida(self):
        self.vidas -= 1
        print(f"Jogador perdeu uma vida! Vidas restantes: {self.vidas}")
        if self.vidas <= 0:
            self.kill()

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem, jogador_origem, direcao_tiro):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = VELOCIDADE_PROJETIL
        self.jogador_origem = jogador_origem
        self.direcao = direcao_tiro

    def update(self):
        self.rect.y += self.direcao * self.velocidade
        if self.rect.bottom < 0 or self.rect.top > ALTURA:
            self.kill()
