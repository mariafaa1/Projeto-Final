#boss2.py
from inimigos_codigos.Inimigos_mapa2.base_boss2 import Boss2Base
import pygame

class Boss2(Boss2Base):
    def __init__(self, x, y, alvo, grupo_inimigos):
        super().__init__(x, y, alvo, grupo_inimigos)
        
        # Ajustar atributos específicos
        self.hp_atual = self.hp_max
        self.distancia_ataque = 150

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