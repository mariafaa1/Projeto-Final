import pygame
import math
from random import uniform
from inimigos_codigos.Inimigos_mapa2.base_esqueleto_arqueiro import BaseEsqueletoArqueiro

# Classe da flecha disparada pelo esqueleto arqueiro
class FlechaEsqueleto(pygame.sprite.Sprite):
    def __init__(self, posicao, angulo, velocidade, dano, alvo):
        super().__init__()
        # Carrega imagem da flecha e rotaciona de acordo com o ângulo de disparo
        self.original_image = pygame.image.load('assets/inimigos/inimigos_mapa2/esqueleto_arqueiro/projetil_esqueleto/flecha.png').convert_alpha()
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(angulo))
        self.rect = self.image.get_rect(center=posicao)
        self.velocidade = velocidade
        self.angulo = angulo
        self.dano = dano
        self.alvo = alvo
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        # Move a flecha com base no ângulo e velocidade
        self.rect.x += math.cos(self.angulo) * self.velocidade
        self.rect.y += math.sin(self.angulo) * self.velocidade

        # Verifica colisão com o jogador (alvo)
        if pygame.sprite.collide_mask(self, self.alvo):
            self.alvo.receber_dano(self.dano)
            self.kill()
            return

        # Verifica colisão com o tilemap (paredes ou obstáculos)
        for rect in self.alvo.tilemap.collision_rects:
            if self.rect.colliderect(rect):
                self.kill()
                return

        # Remove a flecha se sair dos limites do mapa
        if not pygame.Rect(0, 0, *self.alvo.tilemap.map_size).colliderect(self.rect):
            self.kill()

# Classe principal do inimigo arqueiro
class EsqueletoArqueiro(BaseEsqueletoArqueiro):
    def __init__(self, x, y, alvo, grupo_projeteis, grupo_inimigos):
        super().__init__(x, y, hp_max=60, velocidade=1.8, alvo=alvo, grupo_inimigos=grupo_inimigos)
        self.grupo_projeteis = grupo_projeteis  # Grupo para adicionar flechas
        self.cooldown_ataque = 3000  # Tempo de recarga do ataque (ms)
        self.ultimo_ataque = 0
        self.dano_ataque = 15
        self.xp_drop = 120
        self.raio_visao = 500
        self.raio_ataque_ideal = 150
        self.margem_erro = 0.1  # Fator de erro ao prever a posição do alvo
        self.ultimo_alvo_pos = (0, 0)
        self.esta_atacando = False

    def update(self, dt):
        # Atualiza a posição mais recente do alvo
        self.ultimo_alvo_pos = (self.alvo.rect.centerx, self.alvo.rect.centery)
        agora = pygame.time.get_ticks()
        
        # Lógica do inimigo se estiver vivo
        if not self.esta_morto:
            if not self.esta_atacando:
                self.verificar_disparo(agora)
            self.atualizar_animacao(dt)
        
        super().update(dt)

    def verificar_disparo(self, agora):
        # Verifica se o tempo de cooldown passou
        if agora - self.ultimo_ataque >= self.cooldown_ataque:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)
        
            # Verifica se o alvo está dentro da faixa ideal de ataque
            if self.raio_visao >= distancia >= self.raio_ataque_ideal:
                self.esta_atacando = True
                self.estado = 'ataque'
                self.indice_animacao = 0
                self.ultimo_ataque = agora

    def posicionar_para_ataque(self):
        # Move o arqueiro para se posicionar melhor para atirar
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        
        if distancia < self.raio_ataque_ideal * 0.8:
            # Recuar se estiver muito perto
            self.rect.x -= dx/distancia * self.velocidade * 1.2
            self.rect.y -= dy/distancia * self.velocidade * 1.2
        elif distancia > self.raio_ataque_ideal * 1.2:
            # Avançar se estiver muito longe
            self.rect.x += dx/distancia * self.velocidade * 0.8
            self.rect.y += dy/distancia * self.velocidade * 0.8

    def calcular_angulo_disparo(self):
        # Calcula o ângulo do disparo levando em conta a posição prevista do jogador
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        tempo_voo = distancia / 12  # Estimativa do tempo até a flecha chegar

        # Predição da posição futura do jogador com margem de erro aleatória
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
        # Avança a animação de morte até o fim
        if self.indice_animacao < len(self.animacoes['morrendo']) - 1:
            self.indice_animacao += 1
        else:
            self.animacao_morte_concluida = True

    def processar_animacao_ataque(self):
        # Processa os quadros do ataque e dispara a flecha no momento certo
        if self.indice_animacao < len(self.animacoes['ataque']) - 1:
            self.indice_animacao += 1
            if self.indice_animacao == 5:
                self.atirar_flecha()
        else:
            self.esta_atacando = False
            self.estado = 'parado'
            self.indice_animacao = 0

    def processar_animacao_normal(self):
        # Animação contínua para o estado atual
        self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])

    def atualizar_frame(self):
        # Atualiza o frame atual da animação e faz espelhamento horizontal se necessário
        try:
            self.image = self.animacoes[self.estado][self.indice_animacao]
        except (IndexError, KeyError):
            self.image = self.animacoes['parado'][0]
        
        if not self.direita:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def atirar_flecha(self):
        # Dispara uma flecha em direção ao alvo, com leve variação na velocidade
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
