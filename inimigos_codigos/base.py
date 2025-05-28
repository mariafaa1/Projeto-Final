import pygame
import os
from config import (
    LARGURA_BARRA, ALTURA_BARRA, COR_HP_ATUAL, COR_HP_PERDIDO,
    BORDA_HP, COR_BORDA, POSICAO_BARRA_OFFSET_Y
)
import tilemap
import math

# Classe base para todos os inimigos simples (como orcs e esqueletos)
class InimigoBase(pygame.sprite.Sprite):
    def __init__(self, x, y, hp_max, velocidade, alvo, inimigos_group):
        super().__init__()
        # Carrega animações e inicializa estado
        self.animacoes = self.carregar_animacoes()
        self.estado = 'parado'
        self.indice_animacao = 0
        self.image = self.animacoes[self.estado][self.indice_animacao]
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox_rect = pygame.Rect(0, 0, 35, 60)
        self.hitbox_rect.center = self.rect.center
        self.mask = pygame.mask.from_surface(self.image)

        # Atributos de combate e estado
        self.hp_max = hp_max
        self.hp_atual = hp_max
        self.velocidade = velocidade
        self.alvo = alvo
        self.raio_perseguicao = 300
        self.esta_morto = False
        self.esta_atacando = False
        self.animacao_morte_concluida = False
        self.xp_entregue = False
        self.direita = True

        # Controles de animação e movimento
        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.tempo_dano = 0
        self.velocidade_x = 0
        self.velocidade_y = 0

        # Grupo de inimigos (usado para evitar sobreposição)
        self.inimigos_group = inimigos_group

    def calcular_evitar_inimigos(self):
        """
        Calcula vetores de repulsão de outros inimigos próximos para evitar colisões visuais.
        """
        evitar_x = 0
        evitar_y = 0
        evitar_raio = 70
        for inimigo in self.inimigos_group:
            if inimigo != self and not inimigo.esta_morto:
                dx = inimigo.rect.centerx - self.rect.centerx
                dy = inimigo.rect.centery - self.rect.centery
                distancia = math.hypot(dx, dy)
                if 0 < distancia < evitar_raio:
                    fator = (evitar_raio - distancia) / evitar_raio
                    evitar_x += (-dx / distancia) * fator * self.velocidade * 0.8
                    evitar_y += (-dy / distancia) * fator * self.velocidade * 0.8
        return evitar_x, evitar_y

    def carregar_animacoes(self):
        """
        Carrega e organiza as animações do inimigo (parado, andando, atacando, dano e morte).
        """
        animacoes = {k: [] for k in ['parado', 'andando', 'morrendo', 'ataque1', 'ataque2', 'dano']}
        base_path = os.path.join('assets', 'inimigos', 'orc_normal')

        for nome, pasta, prefixo, total in [
            ('parado', 'orc_parado', 'Idle_', 6),
            ('andando', 'orc_andando', 'Andar_', 6),
            ('morrendo', 'orc_morrendo', 'Morte_', 4),
            ('ataque1', 'orc_ataque1', 'Ataque1_', 6),
            ('ataque2', 'orc_ataque_2', 'Ataque2_', 6),
            ('dano', 'orc_dano', 'Machucar_', 4)
        ]:
            caminho = os.path.join(base_path, pasta)
            for i in range(total):
                img = pygame.image.load(os.path.join(caminho, f'{prefixo}{i+1}.png')).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
                animacoes[nome].append(img)

        return animacoes

    def update(self, dt):
        """
        Atualiza o inimigo: perseguição, animação, e controle de estado 'dano'.
        """
        if not self.esta_morto:
            self.perseguir_alvo()
            self.atualizar_animacao(dt)
        elif self.estado == 'morrendo' and not self.animacao_morte_concluida:
            self.atualizar_animacao(dt)

        if self.estado == 'dano' and pygame.time.get_ticks() - self.tempo_dano > 500:
            self.estado = 'parado'

    def perseguir_alvo(self):
        """
        Move o inimigo em direção ao jogador, com desvio de outros inimigos.
        """
        if self.esta_atacando:
            return
        self.velocidade_x = 0
        self.velocidade_y = 0

        if not self.esta_morto and self.estado != 'dano' and self.alvo and not self.alvo.esta_morto:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = (dx**2 + dy**2)**0.5

            if distancia <= self.raio_perseguicao:
                if distancia > 50:
                    self.estado = 'andando'
                    if dx != 0:
                        self.direita = dx > 0

                    vel_base_x = (dx / distancia) * self.velocidade
                    vel_base_y = (dy / distancia) * self.velocidade
                    evitar_x, evitar_y = self.calcular_evitar_inimigos()

                    self.velocidade_x = vel_base_x + evitar_x
                    self.velocidade_y = vel_base_y + evitar_y

                    comprimento = (self.velocidade_x**2 + self.velocidade_y**2)**0.5
                    if comprimento > 0:
                        fator = self.velocidade / comprimento
                        self.velocidade_x *= fator
                        self.velocidade_y *= fator

                    self.rect.x += self.velocidade_x
                    self.rect.y += self.velocidade_y
                else:
                    self.estado = 'parado'
            else:
                self.estado = 'parado'

    def atualizar_animacao(self, dt):
        """
        Controla a transição dos quadros da animação, incluindo flip de direção.
        """
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

    def receber_dano(self, quantidade):
        """
        Reduz o HP do inimigo. Se morrer, troca estado para 'morrendo'.
        """
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
                self.velocidade_x = 0
                self.velocidade_y = 0

    def draw_hp_bar(self, tela, camera):
        """
        Desenha a barra de vida do inimigo acima de sua cabeça.
        """
        if not self.esta_morto and not getattr(self, 'animacao_morte_concluida', False):
            offset_extra_y = -10
            barra_x = self.rect.centerx - (LARGURA_BARRA // 2)
            barra_y = self.rect.centery + POSICAO_BARRA_OFFSET_Y + offset_extra_y
            proporcao_hp = self.hp_atual / self.hp_max
            largura_atual = int(LARGURA_BARRA * proporcao_hp)

            barra_rect = pygame.Rect(barra_x, barra_y, largura_atual, ALTURA_BARRA)
            fundo_rect = pygame.Rect(barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA)

            barra_rect_camera = camera.aplicar_rect(barra_rect)
            fundo_rect_camera = camera.aplicar_rect(fundo_rect)

            pygame.draw.rect(tela, COR_HP_PERDIDO, fundo_rect_camera, border_radius=2)

            if largura_atual > 0:
                pygame.draw.rect(tela, COR_HP_ATUAL, barra_rect_camera, border_radius=2)
                pygame.draw.rect(tela, (255, 255, 255), fundo_rect_camera, width=1, border_radius=2)

    def verificar_colisao(self, tilemap):
        """
        Verifica e corrige colisões com paredes do mapa (layer oculta de colisão).
        """
        original_x = self.rect.x
        self.rect.x += self.velocidade_x
        colidiu_x = False
        for rect in tilemap.collision_rects:
            if self.rect.colliderect(rect):
                if self.velocidade_x > 0:
                    self.rect.right = rect.left
                else:
                    self.rect.left = rect.right
                colidiu_x = True
                break

        original_y = self.rect.y
        self.rect.y += self.velocidade_y
        colidiu_y = False
        for rect in tilemap.collision_rects:
            if self.rect.colliderect(rect):
                if self.velocidade_y > 0:
                    self.rect.bottom = rect.top
                else:
                    self.rect.top = rect.bottom
                colidiu_y = True
                break

        self.velocidade_x = self.rect.x - original_x
        self.velocidade_y = self.rect.y - original_y

        if colidiu_x and colidiu_y:
            self.velocidade_x = 0
            self.velocidade_y = 0
