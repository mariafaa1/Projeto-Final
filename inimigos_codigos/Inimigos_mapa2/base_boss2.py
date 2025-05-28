#base_boss2.py
import pygame
import os
import math
import random
from config import (
    LARGURA_BARRA, ALTURA_BARRA, COR_HP_ATUAL, COR_HP_PERDIDO,
    BORDA_HP, COR_BORDA, POSICAO_BARRA_OFFSET_Y
)
from inimigos_codigos.base import InimigoBase  

class Boss2Base(InimigoBase):
    def __init__(self, x, y, alvo, inimigos_group):
        super().__init__(x, y, hp_max=6000, velocidade=0.7, alvo=alvo, inimigos_group=inimigos_group)
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.dano_ataque_fraco = 35
        self.dano_ataque_pesado = 50
        self.dano_ataque_especial = 75
        self.cooldown_ataque_fraco = 2000
        self.cooldown_ataque_pesado = 2000
        self.cooldown_ataque_especial = 2000
        self.ultimo_ataque_fraco = 0
        self.ultimo_ataque_pesado = 0
        self.ultimo_ataque_especial = 0
        self.eh_boss = True
        self.distancia_ataque = 140
        self.frame_dano = {'ataque_fraco': 6, 'ataque_pesado': 6, 'ataque_especial': 10}
        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.animacoes = self.carregar_animacoes()
        self.image = self.animacoes['parado'][0]
        self.rect = self.image.get_rect(center=(x, y))
        self.x_real = x
        self.y_real = y
        self.mask = pygame.mask.from_surface(self.image)
        self.xp_drop = 2000
        self.xp_entregue = False
        self.velocidade_x = 0  
        self.velocidade_y = 0
        self.raio_perseguicao = 500
        self.inimigos_group = inimigos_group
        

    def carregar_animacoes(self):
        animacoes = {
            'parado': [],
            'andando': [],
            'morrendo': [],
            'ataque_fraco': [],  # ← Alterado de 'ataque1'
            'ataque_pesado': [],  # ← Alterado de 'ataque2'
            'ataque_especial': [],  # ← Alterado de 'ataque3'
            'dano': []
        }

        def carregar_frames(pasta, prefixo, qtd_frames, escala=15):
            frames = []
            for i in range(1, qtd_frames + 1):
                caminho = os.path.join(
                    'assets', 'inimigos', 'boss2',
                    pasta, f"{prefixo}{i}.png"
                )
                img = pygame.image.load(caminho).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * escala, img.get_height() * escala))
                frames.append(img)
            return frames

        animacoes['parado'] = carregar_frames('parado', 'parado', 8)
        animacoes['andando'] = carregar_frames('andando', 'andando', 8)
        animacoes['morrendo'] = carregar_frames('morte', 'morre', 4)
        animacoes['dano'] = carregar_frames('dano', 'dano', 4)
        animacoes['ataque_fraco'] = carregar_frames('ataque1', 'ataque', 8)
        animacoes['ataque_pesado'] = carregar_frames('ataque2', 'ataque', 8)
        animacoes['ataque_especial'] = carregar_frames('ataque3', 'ataque', 12)

        return animacoes

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def perseguir_alvo(self):
    # Zera as velocidades SEMPRE (antes de qualquer verificação)
        self.velocidade_x = 0  
        self.velocidade_y = 0  

        if self.esta_atacando:
            return  # ⭐️ Retorna imediatamente se estiver atacando

    # Restante do código de perseguição (só executa se NÃO estiver atacando)
        if not self.esta_morto and self.estado != 'dano' and self.alvo and not self.alvo.esta_morto:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = (dx**2 + dy**2)**0.5

            if distancia <= self.raio_perseguicao:
                if distancia > 50:  # Se está longe o suficiente para se mover
                    self.estado = 'andando'
                    if dx != 0:  # Só muda direção se houver movimento horizontal
                        self.direita = dx > 0
                    # Calcula novas velocidades
                        self.velocidade_x = (dx / distancia) * self.velocidade
                        self.velocidade_y = (dy / distancia) * self.velocidade
                    # Aplica o movimento
                        self.rect.x += self.velocidade_x
                        self.rect.y += self.velocidade_y
                    else:
                        self.estado = 'parado'  # Se não há movimento horizontal, fica parado
                else:  # Se está muito perto, para
                    self.estado = 'parado'
            else:  # Se está fora do raio de perseguição, para
                self.estado = 'parado'

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
        self.estado_anterior = tipo_ataque
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
        
        # Atualiza o frame da animação conforme o estado
            frames = self.animacoes[self.estado]
            frame_atual = frames[self.indice_animacao]
        
        # Inverte a imagem se necessário (direita/esquerda)
            if not self.direita:
                frame_atual = pygame.transform.flip(frame_atual, True, False)
        
            self.image = frame_atual  # ⭐️ **Linha adicionada: atualiza a imagem!**
        
            if self.estado == 'morrendo':
                if self.indice_animacao < len(frames) - 1:
                    self.indice_animacao += 1
                else:
                    self.animacao_morte_concluida = True
            else:
                self.indice_animacao = (self.indice_animacao + 1) % len(frames)
        
            if self.esta_atacando:
                if self.indice_animacao == self.frame_dano.get(self.estado, 0):
                    if pygame.sprite.collide_rect(self, self.alvo):
                        self.alvo.receber_dano(self.dano)
            
                if self.indice_animacao >= len(self.animacoes[self.estado]) - 1:
                    self.esta_atacando = False
                    self.estado = 'parado'
                    self.indice_animacao = 0
                    agora = pygame.time.get_ticks()
                    if self.estado_anterior == 'ataque_fraco':
                        self.ultimo_ataque_fraco = agora
                    elif self.estado_anterior == 'ataque_pesado':
                        self.ultimo_ataque_pesado = agora
                    elif self.estado_anterior == 'ataque_especial':
                        self.ultimo_ataque_especial = agora

            if self.estado == 'dano' and agora - self.tempo_dano > 500:
                self.estado = 'parado'

    def verificar_colisao(self, tilemap):
        original_x = self.hitbox_rect.x
        original_y = self.hitbox_rect.y
    
    # Movimento horizontal
        self.hitbox_rect.x += self.velocidade_x
        for rect in tilemap.collision_rects:
            if self.hitbox_rect.colliderect(rect):
                if self.velocidade_x > 0:
                    self.hitbox_rect.right = rect.left
                else:
                    self.hitbox_rect.left = rect.right
                break
    
    # Movimento vertical
        self.hitbox_rect.y += self.velocidade_y
        for rect in tilemap.collision_rects:
            if self.hitbox_rect.colliderect(rect):
                if self.velocidade_y > 0:
                    self.hitbox_rect.bottom = rect.top
                else:
                    self.hitbox_rect.top = rect.bottom
                break
    
        self.rect.center = self.hitbox_rect.center