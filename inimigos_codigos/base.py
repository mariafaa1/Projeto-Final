import pygame
import os
from config import (  # Adicione esta linha
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

    def carregar_animacoes(self):
        animacoes = {
            'parado': [],
            'andando': []
        }

        # Animação parado
        pasta_parado = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_parado')
        for i in range(6):
            try:
                img = pygame.image.load(os.path.join(pasta_parado, f'orc_parado{i}.png')).convert_alpha()
                animacoes['parado'].append(img)
            except FileNotFoundError:
                print(f"ERRO: Frame {i} da animação 'parado' não encontrado em {pasta_parado}!")
                exit()

        # Animação andando
        pasta_andando = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_andando')
        for i in range(6):
            try:
                img = pygame.image.load(os.path.join(pasta_andando, f'orc_andando{i}.png')).convert_alpha()
                animacoes['andando'].append(img)
            except FileNotFoundError:
                print(f"ERRO: Frame {i} da animação 'andando' não encontrado em {pasta_andando}!")
                exit()

        return animacoes

    def update(self):
        self.perseguir_alvo()
        self.atualizar_animacao()

    def perseguir_alvo(self):
        if self.alvo and not self.alvo.esta_morto:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = (dx**2 + dy**2)**0.5

            if distancia > 0:
                self.rect.x += (dx / distancia) * self.velocidade
                self.rect.y += (dy / distancia) * self.velocidade
                self.estado = 'andando' if distancia > 50 else 'parado'

    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])
            self.image = self.animacoes[self.estado][self.indice_animacao]
            self.mask = pygame.mask.from_surface(self.image)

    def receber_dano(self, quantidade):
        self.hp_atual = max(0, self.hp_atual - quantidade)
        if self.hp_atual <= 0:
            self.kill()
        # Adicione este método na classe InimigoBase (arquivo base.py)
    def draw_hp_bar(self, tela):
        if self.hp_atual > 0:
            barra_x = self.rect.centerx - (LARGURA_BARRA // 2)
            barra_y = self.rect.centery - 40  # Ajuste a posição Y conforme necessário
            proporcao_hp = self.hp_atual / self.hp_max
            largura_atual = int(LARGURA_BARRA * proporcao_hp)
            pygame.draw.rect(tela, COR_HP_PERDIDO, (barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA))
            pygame.draw.rect(tela, COR_HP_ATUAL, (barra_x, barra_y, largura_atual, ALTURA_BARRA))
            if BORDA_HP:
                pygame.draw.rect(tela, COR_BORDA, (barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA), 1)