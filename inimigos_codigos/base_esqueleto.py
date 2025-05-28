import pygame
import os
from config import (
    LARGURA_BARRA, ALTURA_BARRA, COR_HP_ATUAL, COR_HP_PERDIDO,
    BORDA_HP, COR_BORDA, POSICAO_BARRA_OFFSET_Y
)

class InimigoBase(pygame.sprite.Sprite):
    def __init__(self, x, y, hp_max, velocidade, alvo, inimigos_group):
        super().__init__()
        self.animacoes = self.carregar_animacoes()
        self.estado = 'parado'
        self.indice_animacao = 0
        self.image = self.animacoes[self.estado][self.indice_animacao]
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox_rect = pygame.Rect(0, 0, 35, 60)  # Ajuste conforme o inimigo
        self.hitbox_rect.center = self.rect.center
        self.mask = pygame.mask.from_surface(self.image)
        self.hp_max = hp_max
        self.hp_atual = hp_max
        self.velocidade = velocidade
        self.alvo = alvo
        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.esta_morto = False
        self.esta_atacando = False
        self.tempo_dano = 0
        self.animacao_morte_concluida = False
        self.direita = True
        self.ultimo_ataque = 0
        self.cooldown_ataque = 3000
        self.xp_entregue = False
        self.velocidade_x = 0  
        self.velocidade_y = 0
        self.raio_perseguicao = 300
        self.inimigos_group = inimigos_group


    def calcular_evitar_inimigos(self):
        evitar_x = 0
        evitar_y = 0
        evitar_raio = 70  # Use a variável de configuração evitar_inimigos
        for inimigo in self.inimigos_group:
            if inimigo != self and not inimigo.esta_morto:
                dx = inimigo.rect.centerx - self.rect.centerx
                dy = inimigo.rect.centery - self.rect.centery
                distancia = (dx**2 + dy**2)**0.5
                if 0 < distancia < evitar_raio:
                    fator = (evitar_raio - distancia) / evitar_raio
                    direcao_x = -dx / distancia  # Direção oposta
                    direcao_y = -dy / distancia
                    evitar_x += direcao_x * fator * self.velocidade * 0.8  # Ajuste o fator conforme necessário
                    evitar_y += direcao_y * fator * self.velocidade * 0.8
        return evitar_x, evitar_y

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
            

    def perseguir_alvo(self):
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

                # Velocidade base em direção ao jogador
                    vel_base_x = (dx / distancia) * self.velocidade
                    vel_base_y = (dy / distancia) * self.velocidade

                # Velocidade de evasão
                    evitar_x, evitar_y = self.calcular_evitar_inimigos()

                # Combina as velocidades
                    self.velocidade_x = vel_base_x + evitar_x
                    self.velocidade_y = vel_base_y + evitar_y

                # Normaliza para manter a velocidade constante
                    comprimento = (self.velocidade_x**2 + self.velocidade_y**2)**0.5
                    if comprimento > 0:
                        fator = self.velocidade / comprimento
                        self.velocidade_x *= fator
                        self.velocidade_y *= fator

                # Aplica o movimento
                    self.rect.x += self.velocidade_x
                    self.rect.y += self.velocidade_y
                else:
                    self.estado = 'parado'
            else:
                self.estado = 'parado'

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
                self.velocidade_x = 0 
                self.velocidade_y = 0

    def draw_hp_bar(self, tela, camera):
        if not self.esta_morto and not getattr(self, 'animacao_morte_concluida', False):
            offset_extra_y = -10  # ajuste este valor conforme necessário para subir/descer a barra
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
    
    # Atualiza a posição real
        self.rect.center = self.hitbox_rect.center