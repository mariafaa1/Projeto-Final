from .base import InimigoBase
import random
import pygame

class OrcNormal(InimigoBase):
    def __init__(self, x, y, alvo):
        super().__init__(x, y, 100, 1, alvo)
        self.tipos_ataque = ["ataque1", "ataque2"]
        self.dano_ataque = 15

    def update(self, dt):
        super().update(dt)
        if not self.esta_morto and not self.esta_atacando:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = (dx**2 + dy**2)**0.5
            if distancia <= 50:
                self.iniciar_ataque()

    def iniciar_ataque(self):
        self.esta_atacando = True
        self.estado = random.choice(self.tipos_ataque)
        self.indice_animacao = 0

    def atualizar_animacao(self, dt):
        super().atualizar_animacao(dt)
        if self.esta_atacando and self.indice_animacao == len(self.animacoes[self.estado])-1:
            self.esta_atacando = False
            self.estado = 'parado'
            if pygame.sprite.collide_mask(self, self.alvo):
                self.alvo.receber_dano(self.dano_ataque)