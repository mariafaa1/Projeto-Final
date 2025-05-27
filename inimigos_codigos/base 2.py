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
        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.esta_morto = False

    def carregar_animacoes(self):
        animacoes = {
            'parado': [],
            'andando': [],
            'morrendo': [],
            'ataque1': [],
            'ataque2': []
        }

        # Animação Parado
        pasta_parado = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_parado')
        for i in range(6):
            try:
                img = pygame.image.load(os.path.join(pasta_parado, f'orc_parado{i}.png')).convert_alpha()
                animacoes['parado'].append(img)
            except FileNotFoundError:
                print(f"ERRO: Frame {i} da animação 'parado' não encontrado!")
                exit()

        # Animação Andando
        pasta_andando = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_andando')
        for i in range(6):
            try:
                img = pygame.image.load(os.path.join(pasta_andando, f'orc_andando{i}.png')).convert_alpha()
                animacoes['andando'].append(img)
            except FileNotFoundError:
                print(f"ERRO: Frame {i} da animação 'andando' não encontrado!")
                exit()

        # Animação Morrendo (4 frames)
        pasta_morrendo = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_morrendo')
        for i in range(16, 20):
            try:
                img = pygame.image.load(os.path.join(pasta_morrendo, f'Orc-Attack01-{i}.png.png')).convert_alpha()
                animacoes['morrendo'].append(img)
            except FileNotFoundError:
                print(f"ERRO: Frame de morte {i} não encontrado!")
                exit()

        # Animação Ataque1 (6 frames)
        pasta_ataque1 = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_ataque1')
        for i in range(20, 26):
            try:
                img = pygame.image.load(os.path.join(pasta_ataque1, f'Orc-Attack01-{i}.png.png')).convert_alpha()
                animacoes['ataque1'].append(img)
            except FileNotFoundError:
                print(f"ERRO: Frame de ataque1 {i} não encontrado!")
                exit()

        # Animação Ataque2 (6 frames)
        pasta_ataque2 = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_ataque_2')
        for i in range(6):
            try:
                img = pygame.image.load(os.path.join(pasta_ataque2, f'orc{i}.png')).convert_alpha()
                animacoes['ataque2'].append(img)
            except FileNotFoundError:
                print(f"ERRO: Frame de ataque2 {i} não encontrado!")
                exit()

        return animacoes

    def update(self):
        self.perseguir_alvo()
        self.atualizar_animacao()

    def perseguir_alvo(self):
        if self.alvo and not self.alvo.esta_morto and not self.esta_morto:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = (dx**2 + dy**2)**0.5

            if distancia > 50:  # Raio de perseguição
                self.estado = 'andando'
                self.rect.x += (dx / distancia) * self.velocidade
                self.rect.y += (dy / distancia) * self.velocidade
            else:
                self.estado = 'ataque1'  # Inicia ataque quando perto

    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            if self.estado == 'morrendo' and self.indice_animacao >= len(self.animacoes['morrendo'])-1:
                self.kill()
            else:
                self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])
                self.image = self.animacoes[self.estado][self.indice_animacao]
                self.mask = pygame.mask.from_surface(self.image)

    def receber_dano(self, quantidade):
        self.hp_atual = max(0, self.hp_atual - quantidade)
        if self.hp_atual <= 0 and not self.esta_morto:
            self.esta_morto = True
            self.estado = 'morrendo'
            self.indice_animacao = 0

    def draw_hp_bar(self, tela):
        if not self.esta_morto:
            barra_x = self.rect.centerx - (LARGURA_BARRA // 2)
            barra_y = self.rect.centery + POSICAO_BARRA_OFFSET_Y
            proporcao_hp = self.hp_atual / self.hp_max
            largura_atual = int(LARGURA_BARRA * proporcao_hp)
            pygame.draw.rect(tela, COR_HP_PERDIDO, (barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA))
            pygame.draw.rect(tela, COR_HP_ATUAL, (barra_x, barra_y, largura_atual, ALTURA_BARRA))
            if BORDA_HP:
                pygame.draw.rect(tela, COR_BORDA, (barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA), 1)