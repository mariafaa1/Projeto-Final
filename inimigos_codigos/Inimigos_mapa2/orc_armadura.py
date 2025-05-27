# orc_armadura.py
import pygame
import random
from inimigos_codigos.Inimigos_mapa2.base_orc_armadura import InimigoBase

class OrcArmadura(InimigoBase):
    
    def __init__(self, x, y, alvo):
        super().__init__(x, y, hp_max=400, velocidade=1.5, alvo=alvo)
        self.dano_ataque1 = 25
        self.dano_ataque2 = 35
        self.cooldown_ataque1 = 2000
        self.cooldown_ataque2 = 3000
        self.ultimo_ataque1 = 0
        self.ultimo_ataque2 = 0
        self.tipo_ataque = 'ataque1'
        self.dano = self.dano_ataque1
        self.xp_drop = 120
        self.escudo_hp = 150
        self.escudo_hp_max = 150
        self.escudo_ativo = True

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
        
        super().update(dt)

    def iniciar_ataque(self, tempo_atual):
        self.esta_atacando = True
        self.estado = self.tipo_ataque
        self.indice_animacao = 0
        
        if self.tipo_ataque == 'ataque1':
            self.dano = self.dano_ataque1
        else:
            self.dano = self.dano_ataque2

    def atualizar_animacao(self, dt):
        super().atualizar_animacao(dt)
        
        # Resetar animação de bloqueio
        if self.estado == 'bloqueio' and self.indice_animacao >= len(self.animacoes['bloqueio']) - 1:
            self.indice_animacao = 0
        
        if self.esta_atacando and self.indice_animacao == len(self.animacoes[self.estado]) - 1:
            self.esta_atacando = False
            self.estado = 'parado'
            agora = pygame.time.get_ticks()
            
            if self.tipo_ataque == 'ataque1':
                self.ultimo_ataque1 = agora
            else:
                self.ultimo_ataque2 = agora