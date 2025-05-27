#esqueleto.py
import pygame
import random
from inimigos_codigos.base_esqueleto import InimigoBase

class Esqueleto(InimigoBase):
    def __init__(self, x, y, alvo):
        super().__init__(x, y, hp_max=70, velocidade=1.8, alvo=alvo)
        
        self.dano_ataque1 = 15
        self.dano_ataque2 = 20
        self.cooldown_ataque1 = 1500
        self.cooldown_ataque2 = 2000
        self.ultimo_ataque1 = 0
        self.ultimo_ataque2 = 0
        self.tipo_ataque = 'ataque1'
        self.dano = self.dano_ataque1
        self.xp_drop = 15

    def update(self, dt):
        agora = pygame.time.get_ticks()
    
        if not self.esta_morto and not self.esta_atacando:
            if self.verificar_distancia_ataque():
                ataques_disponiveis = []
            
                if agora - self.ultimo_ataque1 >= self.cooldown_ataque1:
                    ataques_disponiveis.append('ataque1')
                if agora - self.ultimo_ataque2 >= self.cooldown_ataque2:
                    ataques_disponiveis.append('ataque2')
            
                if ataques_disponiveis:
                    self.tipo_ataque = random.choice(ataques_disponiveis)
                    self.iniciar_ataque(agora)

    # ✅ Movimentação e animação - mesma lógica da base
        if not self.esta_morto:
            if not self.esta_atacando:
                self.perseguir_alvo()
            self.atualizar_animacao(dt)
        elif self.estado == 'morrendo' and not self.animacao_morte_concluida:
            self.atualizar_animacao(dt)
        
        if self.estado == 'dano' and pygame.time.get_ticks() - self.tempo_dano > 500:
            self.estado = 'parado'


    def iniciar_ataque(self, tempo_atual):
        self.esta_atacando = True
        self.estado = self.tipo_ataque
        self.indice_animacao = 0
        self.velocidade_x = 0  
        self.velocidade_y = 0
        
        if self.tipo_ataque == 'ataque1':
            self.dano = self.dano_ataque1
        else:
            self.dano = self.dano_ataque2

    def atualizar_animacao(self, dt):
        super().atualizar_animacao(dt)
        
        if self.esta_atacando and self.indice_animacao == len(self.animacoes[self.estado]) - 1:
            self.esta_atacando = False
            self.estado = 'parado'
            agora = pygame.time.get_ticks()
            
            if self.tipo_ataque == 'ataque1':
                self.ultimo_ataque1 = agora
            else:
                self.ultimo_ataque2 = agora
            
            if pygame.sprite.collide_rect(self, self.alvo):
                self.alvo.receber_dano(self.dano)