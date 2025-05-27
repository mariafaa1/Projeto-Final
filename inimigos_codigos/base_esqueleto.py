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
        self.direita = True
        self.ultimo_ataque = 0
        self.cooldown_ataque = 1500
        self.xp_entregue = False

    def carregar_animacoes(self):
        animacoes = {
            'parado': [],
            'andando': [],
            'morrendo': [],
            'ataque1': [],
            'ataque2': [],
            'dano': []
        }

        def carregar_frames(pasta, prefixo, inicio, fim):
            frames = []
            for i in range(inicio, fim + 1):
                caminho = os.path.join(pasta, f"{prefixo}{i}.png")
                img = pygame.image.load(caminho).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() *4, (img.get_height() *4)))
                frames.append(img)
            return frames

        base_path = "assets/inimigos/esqueleto"

        animacoes['parado'] = carregar_frames(os.path.join(base_path, "esqueleto_parado"), "Idle_", 1, 4)
        animacoes['andando'] = carregar_frames(os.path.join(base_path, "andando"), "Andar_", 1, 8)
        animacoes['ataque1'] = carregar_frames(os.path.join(base_path, "ataque1"), "Ataque1_", 1, 6)
        animacoes['ataque2'] = carregar_frames(os.path.join(base_path, "ataque2"), "Ataque2_", 1, 7)
        animacoes['dano'] = carregar_frames(os.path.join(base_path, "esqueleto_dano"), "Machucar_", 1, 4)
        animacoes['morrendo'] = carregar_frames(os.path.join(base_path, "esqueleto_morte"), "Morte_", 1, 4)

        return animacoes

    def verificar_distancia_ataque(self):
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        return (dx**2 + dy**2)**0.5 <= 50

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
                if dx != 0:
                    self.direita = dx > 0
                self.rect.x += (dx / distancia) * self.velocidade
                self.rect.y += (dy / distancia) * self.velocidade

    def atualizar_animacao(self, dt):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            
            if self.estado == 'morrendo':
                if self.indice_animacao < len(self.animacoes['morrendo']) - 1:
                    self.indice_animacao += 1
                else:
                    self.animacao_morte_concluida = True
            else:
                self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])
            
            self.image = self.animacoes[self.estado][self.indice_animacao]
            if not self.direita:
                self.image = pygame.transform.flip(self.image, True, False)
            
            self.mask = pygame.mask.from_surface(self.image)

            if self.esta_atacando and self.indice_animacao == len(self.animacoes[self.estado]) - 1:
                self.esta_atacando = False
                self.ultimo_ataque = pygame.time.get_ticks()
                if pygame.sprite.collide_rect(self, self.alvo):
                    self.alvo.receber_dano(self.dano)

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