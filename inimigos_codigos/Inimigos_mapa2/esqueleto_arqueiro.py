# esqueleto_arqueiro.py
import pygame
import math
from random import uniform
from inimigos_codigos.Inimigos_mapa2.base_esqueleto_arqueiro import BaseEsqueletoArqueiro

class FlechaEsqueleto(pygame.sprite.Sprite):
    def __init__(self, posicao, angulo, velocidade, dano, alvo):
        super().__init__()
        self.original_image = pygame.image.load('assets/inimigos/inimigos_mapa2/esqueleto_arqueiro/projetil_esqueleto/flecha.png').convert_alpha()
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(angulo))
        self.rect = self.image.get_rect(center=posicao)
        self.velocidade = velocidade
        self.angulo = angulo
        self.dano = dano
        self.alvo = alvo
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += math.cos(self.angulo) * self.velocidade
        self.rect.y += math.sin(self.angulo) * self.velocidade
        
        if pygame.sprite.collide_mask(self, self.alvo):
            self.alvo.receber_dano(self.dano)
            self.kill()
        
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()

class EsqueletoArqueiro(BaseEsqueletoArqueiro):
    def __init__(self, x, y, alvo, grupo_projeteis):
        super().__init__(x, y, hp_max=150, velocidade=1.8, alvo=alvo)
        self.grupo_projeteis = grupo_projeteis
        self.cooldown_ataque = 3000
        self.ultimo_ataque = 0
        self.dano_ataque = 25
        self.xp_drop = 120
        self.raio_visao = 500
        self.raio_ataque_ideal = 350
        self.margem_erro = 0.1
        self.ultimo_alvo_pos = (0, 0)
        self.esta_atacando = False

    def update(self, dt):
        self.ultimo_alvo_pos = (self.alvo.rect.centerx, self.alvo.rect.centery)
        agora = pygame.time.get_ticks()
        
        if not self.esta_morto:
            if not self.esta_atacando:
                self.verificar_disparo(agora)
            self.atualizar_animacao(dt)
        
        super().update(dt)

    def verificar_disparo(self, agora):
        if agora - self.ultimo_ataque >= self.cooldown_ataque:
            distancia = math.dist(self.rect.center, self.ultimo_alvo_pos)
            
            if distancia <= self.raio_visao:
                self.esta_atacando = True
                self.estado = 'ataque'
                self.indice_animacao = 0
                self.ultimo_ataque = agora
                self.posicionar_para_ataque()

    def posicionar_para_ataque(self):
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        
        if distancia < self.raio_ataque_ideal * 0.8:
            self.rect.x -= dx/distancia * self.velocidade * 1.2
            self.rect.y -= dy/distancia * self.velocidade * 1.2
        elif distancia > self.raio_ataque_ideal * 1.2:
            self.rect.x += dx/distancia * self.velocidade * 0.8
            self.rect.y += dy/distancia * self.velocidade * 0.8

    def calcular_angulo_disparo(self):
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        tempo_voo = distancia / 12
        
        pred_x = self.alvo.rect.centerx + self.alvo.vel_x * tempo_voo * uniform(1-self.margem_erro, 1+self.margem_erro)
        pred_y = self.alvo.rect.centery + self.alvo.vel_y * tempo_voo * uniform(1-self.margem_erro, 1+self.margem_erro)
        
        dx_pred = pred_x - self.rect.centerx
        dy_pred = pred_y - self.rect.centery
        return math.atan2(dy_pred, dx_pred)

    def atualizar_animacao(self, dt):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            
            if self.estado == 'morrendo':
                self.processar_animacao_morte()
            elif self.estado == 'ataque':
                self.processar_animacao_ataque()
            else:
                self.processar_animacao_normal()

            self.atualizar_frame()

    def processar_animacao_morte(self):
        if self.indice_animacao < len(self.animacoes['morrendo']) - 1:
            self.indice_animacao += 1
        else:
            self.animacao_morte_concluida = True

    def processar_animacao_ataque(self):
        if self.indice_animacao < len(self.animacoes['ataque']) - 1:
            self.indice_animacao += 1
            if self.indice_animacao == 5:
                self.atirar_flecha()
        else:
            self.esta_atacando = False
            self.estado = 'parado'
            self.indice_animacao = 0

    def processar_animacao_normal(self):
        self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])

    def atualizar_frame(self):
        try:
            self.image = self.animacoes[self.estado][self.indice_animacao]
        except (IndexError, KeyError):
            self.image = self.animacoes['parado'][0]
        
        if not self.direita:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def atirar_flecha(self):
        angulo = self.calcular_angulo_disparo()
        velocidade = 12 * uniform(0.95, 1.05)
        
        flecha = FlechaEsqueleto(
            posicao=self.rect.center,
            angulo=angulo,
            velocidade=velocidade,
            dano=self.dano_ataque,
            alvo=self.alvo
        )
        self.grupo_projeteis.add(flecha)