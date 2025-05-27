import pygame
import os
import random
from config import (
    LARGURA_BARRA, ALTURA_BARRA, COR_HP_ATUAL, COR_HP_PERDIDO,
    BORDA_HP, COR_BORDA, POSICAO_BARRA_OFFSET_Y
)
from inimigos_codigos.base import InimigoBase

class BossBase(InimigoBase):
    def __init__(self, x, y, alvo):
        super().__init__(x, y, hp_max=600, velocidade=0.7, alvo=alvo)
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.dano_ataque_fraco = 35
        self.dano_ataque_pesado = 50
        self.dano_ataque_especial = 75
        self.cooldown_ataque_fraco = 2000
        self.cooldown_ataque_pesado = 3000
        self.cooldown_ataque_especial = 8000
        self.ultimo_ataque_fraco = 0
        self.ultimo_ataque_pesado = 0
        self.ultimo_ataque_especial = 0
        self.eh_boss = True
        self.distancia_ataque = 70
        self.frame_dano = {'ataque_fraco': 3, 'ataque_pesado': 5, 'ataque_especial': 6}
        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.animacoes = self.carregar_animacoes()
        self.image = self.animacoes['parado'][0]
        self.rect = self.image.get_rect(center=(x, y))
        self.x_real = x
        self.y_real = y
        self.mask = pygame.mask.from_surface(self.image)
        self.xp_drop = 0
        self.xp_entregue = False

    def carregar_animacoes(self):
        animacoes = {
            'parado': [],
            'andando': [],
            'ataque_fraco': [],
            'ataque_pesado': [],
            'ataque_especial': [],
            'dano': [],
            'morrendo': []
        }

        def carregar_frames(pasta, prefixo, inicio, fim):
            frames = []
            M = 4
            for i in range(inicio, fim + 1):
                nome_arquivo = f"{prefixo} {i:02d}.png"
                caminho = os.path.join('assets', 'inimigos', 'boss1', pasta, nome_arquivo)
                img = pygame.image.load(caminho).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * M, img.get_height() * M))
                frames.append(img)
            return frames

        animacoes.update({
            'morrendo': carregar_frames('morte', 'death -', 1, 4),
            'ataque_especial': carregar_frames('ataque_especial', 'ataque3 -', 1, 9),
            'dano': carregar_frames('dano', 'Hurt -', 1, 4),
            'ataque_pesado': carregar_frames('ataque_pesado', 'ataque2 -', 1, 11),
            'ataque_fraco': carregar_frames('ataque_fraco', 'ataque1 -', 1, 7),
            'andando': carregar_frames('andando', 'Walk -', 1, 8),
            'parado': carregar_frames('parado', 'Idle -', 1, 4)
        })
        return animacoes

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def perseguir_alvo(self):
        if self.esta_morto or self.esta_atacando or self.estado == 'dano':
            return
            
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = (dx**2 + dy**2)**0.5
        limiar_parada = self.distancia_ataque * 0.8

        if distancia > limiar_parada:
            if distancia != 0:
                velocidade_x = (dx / distancia) * self.velocidade
                velocidade_y = (dy / distancia) * self.velocidade
                self.x_real += velocidade_x
                self.y_real += velocidade_y
                self.rect.center = (int(self.x_real), int(self.y_real))

            if distancia > 5:
                self.estado = 'andando'
                self.direita = dx > 0
            else:
                self.estado = 'parado'
                self.indice_animacao = 0
        else:
            self.estado = 'parado'
            self.indice_animacao = 0

    def verificar_distancia_ataque(self):
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        return (dx**2 + dy**2)**0.5 <= self.distancia_ataque

    def verificar_ataques(self):
        agora = pygame.time.get_ticks()
        if self.esta_morto or self.esta_atacando:
            return
        if self.verificar_distancia_ataque():
            ataques_disponiveis = []
            if agora - self.ultimo_ataque_fraco > self.cooldown_ataque_fraco:
                ataques_disponiveis.append('ataque_fraco')
            if agora - self.ultimo_ataque_pesado > self.cooldown_ataque_pesado:
                ataques_disponiveis.append('ataque_pesado')
            if (agora - self.ultimo_ataque_especial > self.cooldown_ataque_especial and 
                self.hp_atual < self.hp_max * 0.4):
                ataques_disponiveis.append('ataque_especial')
            if ataques_disponiveis:
                tipo_ataque = random.choice(ataques_disponiveis)
                self.iniciar_ataque(tipo_ataque, agora)

    def iniciar_ataque(self, tipo_ataque, tempo_atual):
        self.esta_atacando = True
        self.estado = tipo_ataque
        self.indice_animacao = 0
        if tipo_ataque == 'ataque_fraco':
            self.ultimo_ataque_fraco = tempo_atual
            self.dano = self.dano_ataque_fraco
        elif tipo_ataque == 'ataque_pesado':
            self.ultimo_ataque_pesado = tempo_atual
            self.dano = self.dano_ataque_pesado
        else:
            self.ultimo_ataque_especial = tempo_atual
            self.dano = self.dano_ataque_especial

    def update(self, dt):
        agora = pygame.time.get_ticks()
        if not self.esta_morto:
            self.perseguir_alvo()
            self.verificar_ataques()
            self.atualizar_animacao(dt)
        elif self.estado == 'morrendo' and not self.animacao_morte_concluida:
            self.atualizar_animacao(dt)
        if self.estado == 'dano' and agora - self.tempo_dano > 500:
            self.estado = 'parado'

    def atualizar_animacao(self, dt):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update >= self.tempo_animacao:
            self.ultimo_update = agora
            if self.estado == 'morrendo':
                if self.indice_animacao < len(self.animacoes['morrendo']) - 1:
                    self.indice_animacao += 1
                else:
                    self.animacao_morte_concluida = True
            else:
                if not self.esta_atacando:
                    self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])
            if self.esta_atacando:
                if self.indice_animacao == self.frame_dano.get(self.estado, 0):
                    if pygame.sprite.collide_rect(self, self.alvo):
                        self.alvo.receber_dano(self.dano)
                if self.indice_animacao < len(self.animacoes[self.estado]) - 1:
                    self.indice_animacao += 1
                else:
                    self.esta_atacando = False
                    self.estado = 'parado'
                    self.indice_animacao = 0
            self.image = self.animacoes[self.estado][self.indice_animacao]
            if not self.direita:
                self.image = pygame.transform.flip(self.image, True, False)
            self.mask = pygame.mask.from_surface(self.image)