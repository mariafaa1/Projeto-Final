# base_esqueleto_arqueiro.py
import pygame
import os
import math
from config import (
    LARGURA_BARRA, ALTURA_BARRA, COR_HP_ATUAL, COR_HP_PERDIDO,
    BORDA_HP, COR_BORDA, POSICAO_BARRA_OFFSET_Y, LARGURA
)

class BaseEsqueletoArqueiro(pygame.sprite.Sprite):
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
        self.tempo_animacao = 150
        self.ultimo_update = pygame.time.get_ticks()
        self.esta_morto = False
        self.esta_atacando = False
        self.tempo_dano = 0
        self.animacao_morte_concluida = False
        self.direita = True
        self.xp_entregue = False

    def carregar_animacoes(self):
        animacoes = {
            'parado': [],
            'andando': [],
            'morrendo': [],
            'ataque': [],
            'dano': []
        }

        def carregar_frames(pasta, prefixo, qtd_frames, escala=3):
            frames = []
            for i in range(1, qtd_frames + 1):
                caminho = os.path.join(
                    'assets', 'inimigos', 'inimigos_mapa2', 'esqueleto_arqueiro',
                    pasta, f"{prefixo}{i}.png"
                )
                img = pygame.image.load(caminho).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * escala, img.get_height() * escala))
                frames.append(img)
            return frames

        animacoes['parado'] = carregar_frames('parado', 'idle', 6)
        animacoes['andando'] = carregar_frames('andando', 'andando', 8)
        animacoes['morrendo'] = carregar_frames('morte', 'morte', 4)
        animacoes['ataque'] = carregar_frames('Ataque', 'ataque', 9)
        animacoes['dano'] = carregar_frames('dano', 'dano', 4)

        return animacoes

    def verificar_distancia_ataque(self):
        # Verifica apenas distância horizontal
        dx = abs(self.alvo.rect.centerx - self.rect.centerx)
        return 200 <= dx <= 400

    def update(self, dt):
        if not self.esta_morto:
            self.controlar_estados()
            self.atualizar_animacao(dt)
        elif self.estado == 'morrendo' and not self.animacao_morte_concluida:
            self.atualizar_animacao(dt)
            
        if self.estado == 'dano' and pygame.time.get_ticks() - self.tempo_dano > 500:
            self.estado = 'parado'

    def controlar_estados(self):
        if self.esta_morto or self.esta_atacando:
            return
            
        dx = self.alvo.rect.centerx - self.rect.centerx
        self.direita = dx > 0  # Atualiza direção primeiro

        # Só persegue se o alvo estiver na frente
        if (self.direita and dx > 50) or (not self.direita and dx < -50):
            if self.verificar_distancia_ataque():
                self.esta_atacando = True
                self.estado = 'ataque'
            else:
                self.mover_em_direcao_alvo()
        else:
            self.estado = 'parado'

    def mover_em_direcao_alvo(self):
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        
        if distancia == 0:
            return

        # Movimento em arco para melhor posicionamento
        if distancia < self.raio_ataque_ideal:
            # Movimento lateral circular
            angulo = math.atan2(dy, dx) + math.pi/2
            self.rect.x += math.cos(angulo) * self.velocidade
            self.rect.y += math.sin(angulo) * self.velocidade
        else:
            # Aproximação direta
            self.rect.x += (dx / distancia) * self.velocidade
            self.rect.y += (dy / distancia) * self.velocidade

        self.direita = dx > 0
        self.estado = 'andando' if distancia > 50 else 'parado'

    def atualizar_animacao(self, dt):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            
            if self.estado == 'morrendo':
                self.processar_animacao_morte()
            else:
                self.avancar_frame_animacao()
            
            self.atualizar_frame()

    # ... (mantidos os outros métodos como antes)

    def processar_animacao_morte(self):
        if self.indice_animacao < len(self.animacoes['morrendo']) - 1:
            self.indice_animacao += 1
        else:
            self.animacao_morte_concluida = True

    def avancar_frame_animacao(self):
        self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])
        if self.estado == 'ataque' and self.indice_animacao == 0:
            self.esta_atacando = False

    def atualizar_frame(self):
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