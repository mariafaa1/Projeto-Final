<<<<<<< HEAD
#base.py
=======
>>>>>>> 924f1a4 (commit - jogo desoft - commit dia 21 rubrica)
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
<<<<<<< HEAD
        self.hitbox_rect = pygame.Rect(0, 0, 35, 60)  # Ajuste conforme o inimigo
        self.hitbox_rect.center = self.rect.center
=======
>>>>>>> 924f1a4 (commit - jogo desoft - commit dia 21 rubrica)
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
        self.direita = True  # Controle de direção
        self.xp_entregue = False
<<<<<<< HEAD
        self.velocidade_x = 0  
        self.velocidade_y = 0
        self.raio_perseguicao = 500
        
=======
>>>>>>> 924f1a4 (commit - jogo desoft - commit dia 21 rubrica)

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
            img = pygame.image.load(os.path.join(pasta_parado, f'Idle_{i+1}.png')).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() *4, (img.get_height() *4)))
            animacoes['parado'].append(img)

        # Carregar frames andando
        pasta_andando = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_andando')
        for i in range(6):
            img = pygame.image.load(os.path.join(pasta_andando, f'Andar_{i+1}.png')).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() *4, (img.get_height() *4)))
            animacoes['andando'].append(img)

        # Carregar frames morrendo
        pasta_morrendo = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_morrendo')
        for i in range(4):
            img = pygame.image.load(os.path.join(pasta_morrendo, f'Morte_{i+1}.png')).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() *4, (img.get_height() *4)))
            animacoes['morrendo'].append(img)

        # Carregar frames ataque1
        pasta_ataque1 = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_ataque1')
        for i in range(6):
            img = pygame.image.load(os.path.join(pasta_ataque1, f'Ataque1_{i+1}.png')).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() *4, (img.get_height() *4)))
            animacoes['ataque1'].append(img)

        # Carregar frames ataque2
        pasta_ataque2 = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_ataque_2')
        for i in range(6):
            img = pygame.image.load(os.path.join(pasta_ataque2, f'Ataque2_{i+1}.png')).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() *4, (img.get_height() *4)))
            animacoes['ataque2'].append(img)

        # Carregar frames dano
        pasta_dano = os.path.join('assets', 'inimigos', 'orc_normal', 'orc_dano')
        for i in range(4):
            img = pygame.image.load(os.path.join(pasta_dano, f'Machucar_{i+1}.png')).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() *4, (img.get_height() *4)))
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
<<<<<<< HEAD
        if self.esta_atacando:
            return
        self.velocidade_x = 0  # Reinicia as velocidades a cada frame
        self.velocidade_y = 0  #
=======
>>>>>>> 924f1a4 (commit - jogo desoft - commit dia 21 rubrica)
        if not self.esta_morto and self.estado != 'dano' and self.alvo and not self.alvo.esta_morto:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = (dx**2 + dy**2)**0.5

<<<<<<< HEAD
            if distancia <= self.raio_perseguicao:
                if distancia > 50:
                    self.estado = 'andando'
                    if dx != 0:
                        self.direita = dx > 0
                # Calcula a velocidade em X e Y
                        self.velocidade_x = (dx / distancia) * self.velocidade
                        self.velocidade_y = (dy / distancia) * self.velocidade
                # Aplica o movimento
                        self.rect.x += self.velocidade_x
                        self.rect.y += self.velocidade_y
                    else:
                        self.estado = 'parado'
                else:
                    self.estado = 'parado'  # ✅ **Adiciona isso: garante que fora do raio fique parado**
            else:
                self.estado = 'parado'
=======
            if distancia > 50:
                self.estado = 'andando'
                # Atualizar direção
                if dx != 0:
                    self.direita = dx > 0
                # Movimentação
                self.rect.x += (dx / distancia) * self.velocidade
                self.rect.y += (dy / distancia) * self.velocidade
>>>>>>> 924f1a4 (commit - jogo desoft - commit dia 21 rubrica)

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
<<<<<<< HEAD
                self.velocidade_x = 0 
                self.velocidade_y = 0 
=======
>>>>>>> 924f1a4 (commit - jogo desoft - commit dia 21 rubrica)

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
<<<<<<< HEAD
                pygame.draw.rect(tela, (255, 255, 255), fundo_rect_camera, width=1, border_radius=2)

    def verificar_colisao(self, tilemap):
        # Colisão horizontal
        for rect in tilemap.collision_rects:
            if self.rect.colliderect(rect):
                if self.velocidade_x > 0:  # Movendo para direita
                    self.rect.right = rect.left
                elif self.velocidade_x < 0:  # Movendo para esquerda
                    self.rect.left = rect.right
        
        # Colisão vertical
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
=======
                pygame.draw.rect(tela, (255, 255, 255), fundo_rect_camera, width=1, border_radius=2)
>>>>>>> 924f1a4 (commit - jogo desoft - commit dia 21 rubrica)
