import pygame
import os
import random
from config import *
from inimigos_codigos.base import InimigoBase

class OrcArmaduraBase(InimigoBase):
    def __init__(self, x, y, alvo):
        super().__init__(x, y, 
                       hp_max=250, 
                       velocidade=1.2, 
                       alvo=alvo,
                       dano_base=30,
                       xp_drop=80)
        
        self.defesa = 15
        self.recuperacao_escudo = 5000
        self.ultimo_dano = 0
        self.escudo_ativo = True
        self.escudo_hp = 100
        self.escudo_hp_max = 100
        self.raio_impacto = 80
        self.dano_impacto = 40
        
        self.animacoes = self.carregar_animacoes()
        self.image = self.animacoes['parado'][0]
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.x_real = x
        self.y_real = y

    def carregar_animacoes(self):
        animacoes = {
            'parado': [],
            'andando': [],
            'ataque_normal': [],
            'ataque_carregado': [],
            'ataque_especial': [],
            'dano': [],
            'bloqueio': [],
            'morrendo': []
        }

        def carregar_frames(pasta, prefixo, inicio, fim, escala=3):
            frames = []
            for i in range(inicio, fim + 1):
                nome_arquivo = f"{prefixo} {i:02d}.png"
                caminho = os.path.join(
                    'assets', 'inimigos', 'inimigos_mapa2', 'Armored_Orc',
                    pasta, nome_arquivo
                )
                img = pygame.image.load(caminho).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * escala, img.get_height() * escala))
                frames.append(img)
            return frames

        animacoes.update({
            'morrendo': carregar_frames('Death_ArmoredOrc', 'Death -', 1, 4),
            'ataque_especial': carregar_frames('Attack3_ArmoredOrc', 'Attack3 -', 1, 9),
            'ataque_carregado': carregar_frames('Attack2_ArmoredOrc', 'Attack2 -', 1, 8),
            'ataque_normal': carregar_frames('Attack1_ArmoredOrc', 'Attack1 -', 1, 7),
            'dano': carregar_frames('Hurt_ArmoredOrc', 'Hurt -', 1, 4),
            'bloqueio': carregar_frames('Block_ArmoredOrc', 'Block -', 1, 4),
            'andando': carregar_frames('Walk_ArmoredOrc', 'Walk -', 1, 8),
            'parado': carregar_frames('Idle_ArmoredOrc', 'Idle -', 1, 6)
        })
        return animacoes

    def receber_dano(self, dano):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_dano > self.recuperacao_escudo:
            self.escudo_ativo = True
            
        if self.escudo_ativo:
            dano = max(0, dano - self.defesa)
            self.escudo_hp = max(0, self.escudo_hp - dano)
            
            if self.escudo_hp <= 0:
                self.escudo_ativo = False
                self.ultimo_dano = agora
        else:
            super().receber_dano(dano)

        if self.hp_atual > 0:
            self.estado = 'dano' if not self.escudo_ativo else 'bloqueio'
            self.indice_animacao = 0

    def verificar_impacto_ataque(self):
        frame_ataque = {
            'ataque_normal': 4,
            'ataque_carregado': 5,
            'ataque_especial': 6
        }
        
        if self.estado in frame_ataque and self.indice_animacao == frame_ataque[self.estado]:
            alvos = pygame.sprite.spritecollide(
                self, 
                self.grupo_jogador, 
                False, 
                collided=pygame.sprite.collide_circle_ratio(0.7)
            )
            for alvo in alvos:
                dano = self.dano_base if self.estado == 'ataque_normal' else self.dano_impacto
                alvo.receber_dano(dano)

    def atualizar_ataques(self, dt):
        if self.esta_morto or self.esta_atacando:
            return
            
        distancia = self.calcular_distancia_alvo()
        
        if distancia < 100:
            self.iniciar_ataque_especial()
        elif distancia < 70:
            self.iniciar_ataque_carregado()
        elif distancia < 40:
            self.iniciar_ataque_normal()

    def iniciar_ataque_normal(self):
        self.esta_atacando = True
        self.estado = 'ataque_normal'
        self.indice_animacao = 0

    def iniciar_ataque_carregado(self):
        self.esta_atacando = True
        self.estado = 'ataque_carregado'
        self.indice_animacao = 0

    def iniciar_ataque_especial(self):
        self.esta_atacando = True
        self.estado = 'ataque_especial'
        self.indice_animacao = 0

    def update(self, dt):
        super().update(dt)
        if not self.escudo_ativo and self.escudo_hp < self.escudo_hp_max:
            if pygame.time.get_ticks() - self.ultimo_dano > self.recuperacao_escudo:
                self.escudo_hp = min(self.escudo_hp_max, self.escudo_hp + 0.1 * dt)