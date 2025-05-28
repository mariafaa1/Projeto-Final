#orc_normal.py
from .base import InimigoBase
import random
import pygame
class OrcNormal(InimigoBase):
    def __init__(self, x, y, alvo, inimigos_group):
        super().__init__(
            x=x,
            y=y,
            hp_max=100,
            velocidade=1,
            alvo=alvo,
            inimigos_group=inimigos_group
            
        )
        self.dano_ataque = 15
        self.xp_drop = 100

    def update(self, dt):
        super().update(dt)
        if not self.esta_morto and not self.esta_atacando and self.estado not in ['dano', 'morrendo']:
            self.verificar_ataque()

    def verificar_ataque(self):
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = (dx**2 + dy**2)**0.5
        if distancia <= 50:
            self.iniciar_ataque()

    def iniciar_ataque(self):
        self.esta_atacando = True
        self.estado = random.choice(['ataque1', 'ataque2'])
        self.indice_animacao = 0
        self.velocidade_x = 0  
        self.velocidade_y = 0

    def atualizar_animacao(self, dt):
        super().atualizar_animacao(dt)
        if self.esta_atacando and self.indice_animacao == len(self.animacoes[self.estado])-1:
            self.esta_atacando = False
            self.estado = 'parado'
            if pygame.sprite.collide_rect(self, self.alvo):
                self.alvo.receber_dano(self.dano_ataque)