import pygame
from config import LARGURA, ALTURA, VELOCIDADE_JOGADOR

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

    def update(self, teclas):
        agora = pygame.time.get_ticks()

        if not self.executando_ataque:
            self.estado = 'parado'
            movendo = False

            if teclas[pygame.K_a]:
                self.rect.x -= VELOCIDADE_JOGADOR
                self.estado = 'andando'
                self.virado_para_esquerda = True
                movendo = True
            elif teclas[pygame.K_d]:
                self.rect.x += VELOCIDADE_JOGADOR
                self.estado = 'andando'
                self.virado_para_esquerda = False
                movendo = True

            if teclas[pygame.K_w]:
                self.rect.y -= VELOCIDADE_JOGADOR
                self.estado = 'andando'
                movendo = True
            elif teclas[pygame.K_s]:
                self.rect.y += VELOCIDADE_JOGADOR
                self.estado = 'andando'
                movendo = True

            if teclas[pygame.K_j]:
                self.estado = 'ataque_leve'
                self.indice_animacao = 0
                self.executando_ataque = True
                self.ultimo_update = agora

        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            self.indice_animacao += 1

            if self.estado in self.animacoes:
                if self.indice_animacao >= len(self.animacoes[self.estado]):
                    self.indice_animacao = 0
                    if self.executando_ataque:
                        self.executando_ataque = False
                        self.estado = 'parado'

        # Atualiza a imagem com segurança
        frame_list = self.animacoes.get(self.estado)
        if frame_list and self.indice_animacao < len(frame_list):
            frame = frame_list[self.indice_animacao]
            if self.virado_para_esquerda:
                frame = pygame.transform.flip(frame, True, False)
            self.image = frame
