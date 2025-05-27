import pygame
import os
from config import (
    LARGURA_BARRA, ALTURA_BARRA, COR_HP_ATUAL, COR_HP_PERDIDO,
    BORDA_HP, COR_BORDA, POSICAO_BARRA_OFFSET_Y
)

class InimigoBase(pygame.sprite.Sprite):
    def __init__(self, x, y, hp_max, velocidade, alvo):
        super().__init__()
        self.animacoes = self.carregar_animacoes()
        self.estado = 'parado'
        self.indice_animacao = 0
        self.image = self.animacoes[self.estado][self.indice_animacao]
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.hp_max = hp_max
        self.hp_atual = hp_max
        self.velocidade = velocidade
        self.alvo = alvo
        self.tempo_animacao = 200
        self.ultimo_update = pygame.time.get_ticks()
        self.esta_morto = False
        self.esta_atacando = False
        self.tempo_dano = 0
        self.animacao_morte_concluida = False
        self.direita = True  # Controle de direção

    def carregar_animacoes(self):
        animacoes = {
            'parado': [],
            'andando': [],
            'morrendo': [],
            'ataque1': [],
            'ataque2': [],
            'dano': []
        }

        # Carregar frames parado
        pasta_parado = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_parado')
        for i in range(6):
            img = pygame.image.load(os.path.join(pasta_parado, f'orc_parado{i}.png')).convert_alpha()
            animacoes['parado'].append(img)

        # Carregar frames andando
        pasta_andando = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_andando')
        for i in range(6):
            img = pygame.image.load(os.path.join(pasta_andando, f'orc_andando{i}.png')).convert_alpha()
            animacoes['andando'].append(img)

        # Carregar frames morrendo
        pasta_morrendo = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_morrendo')
        for i in range(16, 20):
            img = pygame.image.load(os.path.join(pasta_morrendo, f'Orc-Attack01-{i}.png.png')).convert_alpha()
            animacoes['morrendo'].append(img)

        # Carregar frames ataque1
        pasta_ataque1 = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_ataque1')
        for i in range(20, 26):
            img = pygame.image.load(os.path.join(pasta_ataque1, f'Orc-Attack01-{i}.png.png')).convert_alpha()
            animacoes['ataque1'].append(img)

        # Carregar frames ataque2
        pasta_ataque2 = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_ataque_2')
        for i in range(6):
            img = pygame.image.load(os.path.join(pasta_ataque2, f'orc{i}.png')).convert_alpha()
            animacoes['ataque2'].append(img)

        # Carregar frames dano
        pasta_dano = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_dano')
        for i in range(1, 5):
            img = pygame.image.load(os.path.join(pasta_dano, f'morte{i}.png')).convert_alpha()
            animacoes['dano'].append(img)

        return animacoes

    def update(self, dt):
        if not self.esta_morto:
            self.perseguir_alvo()
            self.atualizar_animacao(dt)
        elif self.estado == 'morrendo' and not self.animacao_morte_concluida:
            self.atualizar_animacao(dt)
            
        if self.estado == 'dano' and pygame.time.get_ticks() - self.tempo_dano > 500:
            self.estado = 'parado'

    def perseguir_alvo(self):
        if not self.esta_morto and self.estado != 'dano' and self.alvo and not self.alvo.esta_morto:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = (dx**2 + dy**2)**0.5

            if distancia > 50:
                self.estado = 'andando'
                # Atualizar direção
                if dx != 0:
                    self.direita = dx > 0
                # Movimentação
                self.rect.x += (dx / distancia) * self.velocidade
                self.rect.y += (dy / distancia) * self.velocidade

    def atualizar_animacao(self, dt):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            
            # Avançar animação
            if self.estado == 'morrendo':
                if self.indice_animacao < len(self.animacoes['morrendo']) - 1:
                    self.indice_animacao += 1
                else:
                    self.animacao_morte_concluida = True
            else:
                self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])
            
            # Aplicar flip se necessário
            self.image = self.animacoes[self.estado][self.indice_animacao]
            if not self.direita:
                self.image = pygame.transform.flip(self.image, True, False)
            
            self.mask = pygame.mask.from_surface(self.image)

    def receber_dano(self, quantidade):
        if not self.esta_morto and not self.animacao_morte_concluida:
            self.hp_atual = max(0, self.hp_atual - quantidade)
            self.estado = 'dano'
            self.indice_animacao = 0
            self.tempo_dano = pygame.time.get_ticks()
            if self.hp_atual <= 0:
                self.esta_morto = True
                self.estado = 'morrendo'
                self.indice_animacao = 0
                self.animacao_morte_concluida = False

    def draw_hp_bar(self, tela):
        if not self.esta_morto and not self.animacao_morte_concluida:
            barra_x = self.rect.centerx - (LARGURA_BARRA // 2)
            barra_y = self.rect.centery + POSICAO_BARRA_OFFSET_Y
            proporcao_hp = self.hp_atual / self.hp_max
            largura_atual = int(LARGURA_BARRA * proporcao_hp)
            pygame.draw.rect(tela, COR_HP_PERDIDO, (barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA))
            pygame.draw.rect(tela, COR_HP_ATUAL, (barra_x, barra_y, largura_atual, ALTURA_BARRA))
            if BORDA_HP:
                pygame.draw.rect(tela, COR_BORDA, (barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA), 1)