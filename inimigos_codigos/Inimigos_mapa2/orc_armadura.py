# orc_armadura.py
import pygame
import random
from inimigos_codigos.Inimigos_mapa2.base_orc_armadura import InimigoBase

class OrcArmadura(InimigoBase):
    def __init__(self, x, y, alvo, grupo_inimigos):
        super().__init__(x, y, hp_max=400, velocidade=1, alvo=alvo)
        
        # Configurações de ataque atualizadas
        self.ataques = {
            'ataque1': {'dano': 10, 'frame_dano': 3, 'cooldown': 2000},
            'ataque2': {'dano': 15, 'frame_dano': 6, 'cooldown': 2000},
            'ataque3': {'dano': 20, 'frame_dano': 7, 'cooldown': 2000}
        }
        
        self.ultimo_ataque = 0
        self.xp_drop = 120
        self.escudo_hp = 150
        self.escudo_hp_max = 150
        self.escudo_ativo = True
        self.grupo_inimigos = grupo_inimigos
        self.tilemap = alvo.tilemap
        self.raio_perseguicao = 200

    def update(self, dt):
        super().update(dt)
        agora = pygame.time.get_ticks()
    
        if self.esta_morto:
            self.velocidade_x = 0
            self.velocidade_y = 0
            return
    
    # Verificar se pode atacar (usando o cooldown do ataque selecionado)
        if not self.esta_atacando and not self.esta_morto:
            if self.verificar_distancia_ataque():
            # Usar o cooldown do último ataque realizado
                cooldown_atual = self.ataques[self.tipo_ataque]['cooldown'] if hasattr(self, 'tipo_ataque') else 2000
                if agora - self.ultimo_ataque >= cooldown_atual:
                    self.iniciar_ataque_aleatorio(agora)

    def iniciar_ataque_aleatorio(self, tempo_atual):
        self.tipo_ataque = random.choice(list(self.ataques.keys()))
        self.esta_atacando = True
        self.estado = self.tipo_ataque
        self.indice_animacao = 0
        self.ultimo_ataque = tempo_atual 

    def atualizar_animacao(self, dt):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
        
        # Animação de morte
            if self.estado == 'morrendo':
                if self.indice_animacao < len(self.animacoes['morrendo']) - 1:
                    self.indice_animacao += 1
                else:
                    self.animacao_morte_concluida = True
        
        # Animação de ataque (VERIFICAÇÃO DE ESTADO CORRIGIDA)
            elif self.estado in ['ataque1', 'ataque2', 'ataque3']:
                if self.estado in self.animacoes:
        # Aplicar dano no frame correto
                    if self.indice_animacao == self.ataques[self.tipo_ataque]['frame_dano']:
                        self.aplicar_dano()
        
        # Avançar apenas se não for o último frame
                    if self.indice_animacao < len(self.animacoes[self.estado]) - 1:
                        self.indice_animacao += 1
                    else:
                        self.esta_atacando = False
                        self.estado = 'parado'
                        self.indice_animacao = 0
        
        # Outras animações (GARANTIR QUE O ESTADO EXISTA)
            else:
                if self.estado in self.animacoes:
                    self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])
        
        # Atualização segura da imagem
            if self.estado in self.animacoes:
                self.image = self.animacoes[self.estado][self.indice_animacao]
                if not self.direita:
                    self.image = pygame.transform.flip(self.image, True, False)
            
                self.mask = pygame.mask.from_surface(self.image)

    def aplicar_dano(self):
        if pygame.sprite.collide_rect(self, self.alvo):
            dano = self.ataques[self.tipo_ataque]['dano']
            self.alvo.receber_dano(dano)

    # Mantemos as funções herdadas
    def draw_hp_bar(self, tela, camera):
        super().draw_hp_bar(tela, camera)

    def verificar_colisao(self, tilemap):
        super().verificar_colisao(tilemap)

    def receber_dano(self, quantidade):
        super().receber_dano(quantidade)