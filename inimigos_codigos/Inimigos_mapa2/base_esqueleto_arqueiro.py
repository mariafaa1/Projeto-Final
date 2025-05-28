import pygame
import os
import math
from config import (
    LARGURA_BARRA, ALTURA_BARRA, COR_HP_ATUAL, COR_HP_PERDIDO,
    BORDA_HP, COR_BORDA, POSICAO_BARRA_OFFSET_Y, LARGURA
)

class BaseEsqueletoArqueiro(pygame.sprite.Sprite):
    def __init__(self, x, y, hp_max, velocidade, alvo, grupo_inimigos):
        # Inicializa o esqueleto arqueiro com atributos base de posição, vida, velocidade e alvo
        super().__init__()
        self.raio_perseguicao = 500 
        self.raio_ataque = 350
        self.grupo_inimigos = grupo_inimigos
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
        self.velocidade_x = 0
        self.velocidade_y = 0

    def carregar_animacoes(self):
        # Carrega os frames de cada animação (parado, andando, ataque, etc.)
        animacoes = {
            'parado': [],
            'andando': [],
            'morrendo': [],
            'ataque': [],
            'dano': []
        }

        def carregar_frames(pasta, prefixo, qtd_frames, escala=3):
            # Função auxiliar que carrega e redimensiona imagens da pasta especificada
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
        # Verifica se o jogador está a uma distância horizontal adequada para ataque
        dx = abs(self.alvo.rect.centerx - self.rect.centerx)
        return 200 <= dx <= 400

    def update(self, dt):
        # Atualiza o estado e animação do arqueiro a cada frame
        if not self.esta_morto:
            if self.estado == 'dano' and pygame.time.get_ticks() - self.tempo_dano > 500:
                self.estado = 'parado'
                self.indice_animacao = 0
            
            if self.estado != 'dano':
                self.controlar_estados()
            
            self.rect.x += self.velocidade_x
            self.rect.y += self.velocidade_y
            self.atualizar_animacao(dt)
        
        elif self.estado == 'morrendo' and not self.animacao_morte_concluida:
            self.atualizar_animacao(dt)
        
        self.velocidade_x = 0
        self.velocidade_y = 0

    def controlar_estados(self):
        # Define se o inimigo deve andar, atacar ou ficar parado baseado na posição do jogador
        if self.esta_morto or self.esta_atacando:
            return
        
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia > self.raio_perseguicao:
            self.estado = 'parado'
            self.velocidade_x = 0
            self.velocidade_y = 0
            return

        self.direita = dx > 0

        if self.raio_ataque <= distancia <= self.raio_perseguicao:
            self.estado = 'andando'
            self.mover_em_direcao_alvo()
        elif distancia < self.raio_ataque:
            self.esta_atacando = True
            self.estado = 'ataque'
        else:
            self.estado = 'parado'
            self.velocidade_x = 0
            self.velocidade_y = 0

    def mover_em_direcao_alvo(self):
        # Move o inimigo na direção do jogador com ajuste de evasão de outros inimigos
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia == 0:
            return
        
        self.velocidade_x = (dx / distancia) * min(self.velocidade, distancia)
        self.velocidade_y = (dy / distancia) * min(self.velocidade, distancia)

        evitar_x, evitar_y = self.calcular_evitar_inimigos()
        self.velocidade_x += evitar_x
        self.velocidade_y += evitar_y

        comprimento = math.hypot(self.velocidade_x, self.velocidade_y)
        if comprimento > 0:
            fator = self.velocidade / comprimento
            self.velocidade_x *= fator
            self.velocidade_y *= fator

    def atualizar_animacao(self, dt):
        # Processa a animação conforme o estado atual
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora

            if self.estado == 'morrendo':
                self.processar_animacao_morte()
            elif self.estado == 'dano':
                self.processar_animacao_dano()
            elif self.estado == 'ataque':
                self.processar_animacao_ataque()
            elif self.estado == 'andando':
                self.processar_animacao_andando()
            else:
                self.processar_animacao_parado()

            self.atualizar_frame()

    def processar_animacao_morte(self):
        # Avança a animação de morte ou volta ao estado parado
        if self.velocidade_x != 0 or self.velocidade_y != 0:
            self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes['andando'])
        else:
            self.estado = 'parado'
            self.indice_animacao = 0

    def avancar_frame_animacao(self):
        # Avança para o próximo frame da animação
        self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])
        if self.estado == 'ataque' and self.indice_animacao == 0:
            self.esta_atacando = False

    def atualizar_frame(self):
        # Atualiza a imagem atual baseada no frame e estado
        self.image = self.animacoes[self.estado][self.indice_animacao]
        if not self.direita:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def receber_dano(self, quantidade):
        # Reduz o HP e inicia animação de dano ou morte
        if not self.esta_morto and not self.animacao_morte_concluida:
            self.hp_atual = max(0, self.hp_atual - quantidade)
            self.estado = 'dano'
            self.indice_animacao = 0
            self.tempo_dano = pygame.time.get_ticks()
            if self.hp_atual <= 0:
                self.esta_morto = True
                self.estado = 'morrendo'
                self.indice_animacao = 0

    def draw_hp_bar(self, tela, camera):
        # Desenha a barra de vida do inimigo na tela
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

    def calcular_evitar_inimigos(self):
        # Calcula vetores de evasão para evitar empilhamento com outros inimigos
        evitar_x = 0
        evitar_y = 0
        evitar_raio = 70
        for inimigo in self.grupo_inimigos:
            if inimigo != self and not inimigo.esta_morto:
                dx = inimigo.rect.centerx - self.rect.centerx
                dy = inimigo.rect.centery - self.rect.centery
                distancia = math.hypot(dx, dy)
                if 0 < distancia < evitar_raio:
                    fator = (evitar_raio - distancia) / evitar_raio
                    direcao_x = -dx / distancia
                    direcao_y = -dy / distancia
                    evitar_x += direcao_x * fator * self.velocidade * 0.8
                    evitar_y += direcao_y * fator * self.velocidade * 0.8
        return evitar_x, evitar_y

    def verificar_colisao(self, tilemap):
        # Verifica e resolve colisão com paredes do mapa
        original_x = self.rect.x
        self.rect.x += self.velocidade_x
        for rect in tilemap.collision_rects:
            if self.rect.colliderect(rect):
                if self.velocidade_x > 0:
                    self.rect.right = rect.left
                else:
                    self.rect.left = rect.right
                break

        original_y = self.rect.y
        self.rect.y += self.velocidade_y
        for rect in tilemap.collision_rects:
            if self.rect.colliderect(rect):
                if self.velocidade_y > 0:
                    self.rect.bottom = rect.top
                else:
                    self.rect.top = rect.bottom
                break

        self.velocidade_x = self.rect.x - original_x
        self.velocidade_y = self.rect.y - original_y
