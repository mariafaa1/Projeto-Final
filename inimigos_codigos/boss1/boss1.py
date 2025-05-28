import pygame
from boss1.base_boss1 import BossBase

class BossPhase1(BossBase):
    def __init__(self, x, y, alvo):
        super().__init__(x, y, alvo)
        
        self.hp_max = 500
        self.hp_atual = self.hp_max
        self.xp_drop = 300
        self.dano_ataque_fraco = 10
        self.dano_ataque_pesado = 15
        self.dano_ataque_especial = 25
        self.distancia_ataque = 50
        self.frame_dano = {
            'ataque_fraco': 5,
            'ataque_pesado': 9,
            'ataque_especial': 7
        }

    def aplicar_dano_area(self, raio):
        area_ataque = pygame.Rect(
            self.rect.centerx - raio,
            self.rect.centery - raio,
            raio * 2,
            raio * 2
        )
        if area_ataque.colliderect(self.alvo.rect):
            self.alvo.receber_dano(self.dano_ataque_especial)

    def atualizar_animacao(self, dt):
        super().atualizar_animacao(dt)
        if self.esta_atacando and self.estado == 'ataque_especial':
            if self.indice_animacao == self.frame_dano['ataque_especial']:
                self.aplicar_dano_area(150)