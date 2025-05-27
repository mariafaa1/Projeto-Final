import pygame
from config import (
    LARGURA, ALTURA,
    VELOCIDADE_JOGADOR,
    VELOCIDADE_PROJETIL,
    TEMPO_COOLDOWN_ATAQUE_PESADO,
    TEMPO_COOLDOWN_ARCO
)

class Soldado(pygame.sprite.Sprite):
    def __init__(self, animacoes):
        super().__init__()
        self.animacoes = animacoes
        self.estado = 'parado'
        self.indice_animacao = 0
        self.image = self.animacoes[self.estado][self.indice_animacao]
        self.rect = self.image.get_rect(center=(LARGURA // 2, ALTURA // 2))
        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.virado_para_esquerda = False
        self.executando_ataque = False
        self.ultimo_ataque_pesado = 0
        self.ultimo_ataque_arco = 0
        self.projeteis = pygame.sprite.Group()
        self.disparar_flecha_pendente = False

    def update(self, teclas):
        agora = pygame.time.get_ticks()

        if not self.executando_ataque:
            self.estado = 'parado'

            # Movimento
            if teclas[pygame.K_a]:
                self.rect.x -= VELOCIDADE_JOGADOR
                self.estado = 'andando'
                self.virado_para_esquerda = True
            elif teclas[pygame.K_d]:
                self.rect.x += VELOCIDADE_JOGADOR
                self.estado = 'andando'
                self.virado_para_esquerda = False

            if teclas[pygame.K_w]:
                self.rect.y -= VELOCIDADE_JOGADOR
                self.estado = 'andando'
            elif teclas[pygame.K_s]:
                self.rect.y += VELOCIDADE_JOGADOR
                self.estado = 'andando'

            # Ataque pesado (K)
            if teclas[pygame.K_k] and agora - self.ultimo_ataque_pesado > TEMPO_COOLDOWN_ATAQUE_PESADO:
                self.estado = 'ataque_pesado'
                self.indice_animacao = 0
                self.executando_ataque = True
                self.ultimo_ataque_pesado = agora
                self.ultimo_update = agora

            # Ataque leve (J)
            elif teclas[pygame.K_j]:
                self.estado = 'ataque_leve'
                self.indice_animacao = 0
                self.executando_ataque = True
                self.ultimo_update = agora

            # Ataque à distância (L)
            elif teclas[pygame.K_l] and agora - self.ultimo_ataque_arco > TEMPO_COOLDOWN_ARCO:
                self.estado = 'ataque_arco'
                self.indice_animacao = 0
                self.executando_ataque = True
                self.disparar_flecha_pendente = True
                self.ultimo_ataque_arco = agora
                self.ultimo_update = agora

        # Animação
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            self.indice_animacao += 1

            total_frames = len(self.animacoes[self.estado])

            # Disparar no penúltimo frame da animação de ataque com arco
            if (
                self.estado == 'ataque_arco'
                and self.disparar_flecha_pendente
                and self.indice_animacao == total_frames - 2
            ):
                deslocamento_y = 10 
                centro_personagem = (self.rect.centerx, self.rect.centery + deslocamento_y)
                novo_proj = Projetil(centro_personagem, self.virado_para_esquerda)
                self.projeteis.add(novo_proj)
                self.disparar_flecha_pendente = False

            if self.estado in self.animacoes and self.indice_animacao >= total_frames:
                self.indice_animacao = 0
                if self.executando_ataque:
                    self.executando_ataque = False
                    self.estado = 'parado'

        # Atualiza imagem
        frame_list = self.animacoes.get(self.estado)
        if frame_list and self.indice_animacao < len(frame_list):
            frame = frame_list[self.indice_animacao]
            if self.virado_para_esquerda:
                frame = pygame.transform.flip(frame, True, False)
            self.image = frame

        # Atualiza projéteis
        self.projeteis.update()

    def draw(self, tela):
        tela.blit(self.image, self.rect)
        self.projeteis.draw(tela)

class Projetil(pygame.sprite.Sprite):
    def __init__(self, position, virado_para_esquerda):
        super().__init__()
        self.image = pygame.image.load('assets/projetil_arco/flecha.png').convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.velocidade = VELOCIDADE_PROJETIL
        self.direcao = -1 if virado_para_esquerda else 1

    def update(self):
        self.rect.x += self.velocidade * self.direcao
