# base_orc_armadura.py
import pygame
import os
import random
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
        self.esta_atacando = False
        self.tempo_dano = 0
        self.animacao_morte_concluida = False
        self.direita = True
        self.xp_entregue = False
        self.escudo_hp = 0
        self.escudo_hp_max = 0
        self.escudo_ativo = False
        self.tempo_bloqueio = 0
        self.velocidade_x = 0  # Novo atributo
        self.velocidade_y = 0
        self.raio_perseguicao = 200

    def carregar_animacoes(self):
        animacoes = {
            'parado': [],
            'andando': [],
            'morrendo': [],
            'ataque1': [],
            'ataque2': [],
            'ataque3': [],
            'dano': [],
            'bloqueio': []
        }
        print(f"Frames do ataque3: {len(animacoes['ataque3'])}")

        def carregar_frames(pasta, prefixo, inicio, fim, escala=4):
            frames = []
            for i in range(inicio, fim + 1):
                nome_arquivo = f"{prefixo}{i:02d}.png"
                caminho = os.path.join('assets', 'inimigos', 'inimigos_mapa2', 'Armored_Orc', pasta, nome_arquivo)
                img = pygame.image.load(caminho).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * escala, img.get_height() * escala))
                frames.append(img)
            return frames

        animacoes['parado'] = carregar_frames('Idle_ArmoredOrc', 'Idle - ', 1, 6, 3)
        animacoes['andando'] = carregar_frames('Walk_ArmoredOrc', 'Walk - ', 1, 8, 3)
        animacoes['morrendo'] = carregar_frames('Death_ArmoredOrc', 'Death - ', 1, 4, 3)
        animacoes['ataque1'] = carregar_frames('Attack1_ArmoredOrc', 'Attack1 - ', 1, 6, 3)
        animacoes['ataque2'] = carregar_frames('Attack2_ArmoredOrc', 'Attack2 - ', 1, 8, 3)
        animacoes['ataque3'] = carregar_frames('Attack3_ArmoredOrc', 'Attack3 - ', 1, 9, 3)
        animacoes['dano'] = carregar_frames('Hurt_ArmoredOrc', 'Hurt - ', 1, 4, 3)
        animacoes['bloqueio'] = carregar_frames('Block_ArmoredOrc', 'Block - ', 1, 4, 3)

        return animacoes

    def verificar_distancia_ataque(self):
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        return (dx**2 + dy**2)**0.5 <= 70

    def update(self, dt):
        if not self.esta_morto:
            self.perseguir_alvo()
            self.atualizar_animacao(dt)
        elif self.estado == 'morrendo' and not self.animacao_morte_concluida:
            self.velocidade_x = 0  # Forçar velocidade zero
            self.velocidade_y = 0  # Forçar velocidade zero
            self.atualizar_animacao(dt)
            
        # Resetar estados temporários
        agora = pygame.time.get_ticks()
        if self.estado == 'dano' and agora - self.tempo_dano > 500:
            self.estado = 'parado'
        if self.estado == 'bloqueio' and agora - self.tempo_bloqueio > 300:  # Timer para bloqueio
            self.estado = 'parado'

    def perseguir_alvo(self):
    # 1. Verificar condições para perseguir
        if (self.esta_morto or 
            self.estado in ['dano', 'bloqueio'] or 
            not self.alvo or 
            self.alvo.esta_morto):
            self.velocidade_x = 0
            self.velocidade_y = 0
            return

    # 2. Calcular direção e distância
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = (dx**2 + dy**2)**0.5

    # 3. Verificar se está dentro do raio de perseguição (NOVO)
        if distancia > self.raio_perseguicao:
            self.velocidade_x = 0
            self.velocidade_y = 0
            self.estado = 'parado'
            return

    # 4. Lógica de movimento original
        if distancia > 70:
            self.estado = 'andando'
        
        # 5. Calcular vetor de perseguição normalizado
            if distancia > 0:
                dir_x = dx / distancia
                dir_y = dy / distancia
            else:
                self.velocidade_x = 0
                self.velocidade_y = 0
        # Não altera o estado se já estiver atacando ou em outros estados importantes
                if not self.esta_atacando and self.estado not in ['ataque1', 'ataque2', 'ataque3', 'dano', 'bloqueio']:
                    self.estado = 'parado'
            
        # 6. Evitar outros inimigos
            evitar_x, evitar_y = self.calcular_evitar_inimigos()
        
        # 7. Combinar vetores
            self.velocidade_x = (dir_x * self.velocidade) + evitar_x
            self.velocidade_y = (dir_y * self.velocidade) + evitar_y
        
        # 8. Normalizar velocidade combinada
            comprimento = (self.velocidade_x**2 + self.velocidade_y**2)**0.5
            if comprimento > 0:
                fator = self.velocidade / comprimento
                self.velocidade_x *= fator
                self.velocidade_y *= fator
            
        # 9. Atualizar posição
            self.rect.x += self.velocidade_x
            self.rect.y += self.velocidade_y
        
        # 10. Atualizar direção do sprite
            if dx != 0:
                self.direita = dx > 0
        else:
        # 11. Parar se estiver perto o suficiente para atacar
            self.velocidade_x = 0
            self.velocidade_y = 0
            if self.estado not in ['ataque1', 'ataque2', 'ataque3', 'dano', 'bloqueio']:
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
                if pygame.sprite.collide_rect(self, self.alvo):
                    self.alvo.receber_dano(self.dano)

    def receber_dano(self, quantidade):
        if not self.esta_morto and not self.animacao_morte_concluida:
            if self.escudo_ativo:
                self.escudo_hp = max(0, self.escudo_hp - quantidade)
                self.estado = 'bloqueio'
                self.tempo_bloqueio = pygame.time.get_ticks()  # Ativar timer
                if self.escudo_hp <= 0:
                    self.escudo_ativo = False
                return
            
            self.hp_atual = max(0, self.hp_atual - quantidade)
            self.estado = 'dano'
            self.indice_animacao = 0
            self.tempo_dano = pygame.time.get_ticks()
            if self.hp_atual <= 0:
                self.esta_morto = True
                self.velocidade_x = 0  # Zera velocidade
                self.velocidade_y = 0  # Zera velocidade
                self.estado = 'morrendo'
                self.indice_animacao = 0
                self.animacao_morte_concluida = False
    
    def draw_hp_bar(self, tela, camera):
        if not self.esta_morto and not getattr(self, 'animacao_morte_concluida', False):
            offset_extra_y = -10  # ajuste conforme necessário
            barra_x = self.rect.centerx - (LARGURA_BARRA // 2)
            barra_y = self.rect.centery + POSICAO_BARRA_OFFSET_Y + offset_extra_y

        # --- Barra de Vida ---
            proporcao_hp = self.hp_atual / self.hp_max
            largura_hp = int(LARGURA_BARRA * proporcao_hp)
            fundo_hp = pygame.Rect(barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA)
            barra_hp = pygame.Rect(barra_x, barra_y, largura_hp, ALTURA_BARRA)

            fundo_hp_cam = camera.aplicar_rect(fundo_hp)
            barra_hp_cam = camera.aplicar_rect(barra_hp)

            pygame.draw.rect(tela, COR_HP_PERDIDO, fundo_hp_cam, border_radius=2)
            if largura_hp > 0:
                pygame.draw.rect(tela, COR_HP_ATUAL, barra_hp_cam, border_radius=2)
            pygame.draw.rect(tela, (255, 255, 255), fundo_hp_cam, width=1, border_radius=2)

        # --- Barra de Escudo (acima da barra de vida) ---
            if self.escudo_hp > 0:
                offset_escudo_y = -12  # coloca a barra de escudo acima da de vida
                escudo_y = barra_y + offset_escudo_y

                proporcao_escudo = self.escudo_hp / self.escudo_hp_max
                largura_escudo = int(LARGURA_BARRA * proporcao_escudo)

                fundo_escudo = pygame.Rect(barra_x, escudo_y, LARGURA_BARRA, 7)  # altura menor para a barra de escudo
                barra_escudo = pygame.Rect(barra_x, escudo_y, largura_escudo, 7)

                fundo_escudo_cam = camera.aplicar_rect(fundo_escudo)
                barra_escudo_cam = camera.aplicar_rect(barra_escudo)

                cor_escudo = (70, 130, 200)  # azul clássico para escudo
                pygame.draw.rect(tela, (30, 30, 30), fundo_escudo_cam, border_radius=2)
                pygame.draw.rect(tela, cor_escudo, barra_escudo_cam, border_radius=2)
                pygame.draw.rect(tela, (255, 255, 255), fundo_escudo_cam, width=1, border_radius=2)

            # Adicionar na classe InimigoBase:
    def calcular_evitar_inimigos(self):
        evitar_x = 0
        evitar_y = 0
        evitar_raio = 70
        for inimigo in self.grupo_inimigos:  # Adicionar grupo_inimigos no __init__
            if inimigo != self and not inimigo.esta_morto:
                dx = inimigo.rect.centerx - self.rect.centerx
                dy = inimigo.rect.centery - self.rect.centery
                distancia = (dx**2 + dy**2)**0.5
                if 0 < distancia < evitar_raio:
                    fator = (evitar_raio - distancia) / evitar_raio
                    direcao_x = -dx / distancia
                    direcao_y = -dy / distancia
                    evitar_x += direcao_x * fator * self.velocidade * 0.8
                    evitar_y += direcao_y * fator * self.velocidade * 0.8
            return evitar_x, evitar_y

    def verificar_colisao(self, tilemap):
        original_x = self.rect.x
        original_y = self.rect.y
    
    # Movimento horizontal
        self.rect.x += self.velocidade_x
        for rect in tilemap.collision_rects:
            if self.rect.colliderect(rect):
                if self.velocidade_x > 0:
                    self.rect.right = rect.left
                else:
                    self.rect.left = rect.right
                break
    
    # Movimento vertical
        self.rect.y += self.velocidade_y
        for rect in tilemap.collision_rects:
            if self.rect.colliderect(rect):
                if self.velocidade_y > 0:
                    self.rect.bottom = rect.top
                else:
                    self.rect.top = rect.bottom
                break