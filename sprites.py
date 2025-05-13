import pygame
import random
from config import LARGURA, ALTURA, VELOCIDADE_JOGADOR, VELOCIDADE_PROJETIL, VIDAS_MAXIMAS, TEMPO_EXPLOSAO, DANO_GRANADA

class Jogador(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, controles, recursos, direcao_tiro, id_jogador):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = VELOCIDADE_JOGADOR
        self.controles = controles
        self.recursos = recursos
        self.direcao_tiro = direcao_tiro
        self.ultimo_disparo = pygame.time.get_ticks()
        self.vidas = VIDAS_MAXIMAS
        self.id_jogador = id_jogador
        self.tem_granada = False

    def atualizar(self, teclas, grupo_projeteis, todos_sprites, grupo_granadas):
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
        if teclas[self.controles['disparo']] and agora - self.ultimo_disparo > 500:
            imagem_bala = self.recursos['bala1'] if self.id_jogador == 1 else self.recursos['bala2']
            bala = Projetil(self.rect.centerx, self.rect.centery, imagem_bala, self.direcao_tiro, self)
            grupo_projeteis.add(bala)
            todos_sprites.add(bala)
            self.recursos['som_tiro'].play()
            self.ultimo_disparo = agora

        # coleta granada
        for granada in pygame.sprite.spritecollide(self, grupo_granadas, True):
            self.tem_granada = True

    def perder_vida(self, dano=1):
        self.vidas -= dano
        if self.vidas <= 0:
            self.kill()

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem, direcao, dono):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = VELOCIDADE_PROJETIL
        self.direcao = direcao
        self.dono = dono

    def update(self):
        self.rect.x += self.direcao * self.velocidade
        if self.rect.right < 0 or self.rect.left > LARGURA:
            self.kill()

class Granada(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))

class GranadaLançada(pygame.sprite.Sprite):
    def __init__(self, x, y, recursos, jogador_alvo):
        super().__init__()
        self.image = recursos['explosao']
        self.rect = self.image.get_rect(center=(x, y))
        self.criada_em = pygame.time.get_ticks()
        self.jogador_alvo = jogador_alvo
        self.recursos = recursos

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.criada_em > TEMPO_EXPLOSAO:
            if self.rect.colliderect(self.jogador_alvo.rect):
                self.jogador_alvo.perder_vida(DANO_GRANADA)
            self.kill()
