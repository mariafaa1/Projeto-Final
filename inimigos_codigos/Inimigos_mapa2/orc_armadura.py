import pygame
import random
from inimigos_codigos.Inimigos_mapa2.base_orc_armadura import InimigoBase

# Classe OrcArmadura herda de InimigoBase e define um inimigo forte com escudo e ataques variados
class OrcArmadura(InimigoBase):
    def __init__(self, x, y, alvo, grupo_inimigos):
        super().__init__(x, y, hp_max=400, velocidade=1, alvo=alvo)

        # Define os três tipos de ataques com seus danos, frame de dano e cooldowns
        self.ataques = {
            'ataque1': {'dano': 10, 'frame_dano': 3, 'cooldown': 2000},
            'ataque2': {'dano': 15, 'frame_dano': 6, 'cooldown': 2000},
            'ataque3': {'dano': 20, 'frame_dano': 7, 'cooldown': 2000}
        }

        self.ultimo_ataque = 0  # Guarda o tempo do último ataque
        self.xp_drop = 120  # XP que o jogador ganha ao derrotar
        self.escudo_hp = 150  # Vida do escudo
        self.escudo_hp_max = 150
        self.escudo_ativo = True  # Define se o escudo ainda está ativo
        self.grupo_inimigos = grupo_inimigos  # Grupo com os outros inimigos
        self.tilemap = alvo.tilemap  # Referência ao tilemap
        self.raio_perseguicao = 200  # Distância máxima de perseguição

    # Função principal de update chamada a cada frame
    def update(self, dt):
        super().update(dt)  # Atualizações básicas da classe base
        agora = pygame.time.get_ticks()

        # Se estiver morto, zera a velocidade
        if self.esta_morto:
            self.velocidade_x = 0
            self.velocidade_y = 0
            return

        # Se não está atacando nem morto, verifica se está na distância ideal para atacar
        if not self.esta_atacando and not self.esta_morto:
            if self.verificar_distancia_ataque():
                cooldown = self.ataques[self.tipo_ataque]['cooldown'] if hasattr(self, 'tipo_ataque') else 2000
                if agora - self.ultimo_ataque >= cooldown:
                    self.iniciar_ataque_aleatorio(agora)

    # Define aleatoriamente um tipo de ataque e inicia a animação
    def iniciar_ataque_aleatorio(self, tempo_atual):
        self.tipo_ataque = random.choice(list(self.ataques.keys()))  # Escolhe ataque1, 2 ou 3
        self.esta_atacando = True
        self.estado = self.tipo_ataque
        self.indice_animacao = 0
        self.ultimo_ataque = tempo_atual

    # Atualiza animações de acordo com o estado (andando, atacando, morrendo, etc.)
    def atualizar_animacao(self, dt):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora

            if self.estado == 'morrendo':
                if self.indice_animacao < len(self.animacoes['morrendo']) - 1:
                    self.indice_animacao += 1
                else:
                    self.animacao_morte_concluida = True

            elif self.estado in ['ataque1', 'ataque2', 'ataque3']:
                if self.estado in self.animacoes:
                    # Aplica o dano no frame exato definido no dicionário de ataques
                    if self.indice_animacao == self.ataques[self.tipo_ataque]['frame_dano']:
                        self.aplicar_dano()

                    # Avança a animação do ataque até o fim
                    if self.indice_animacao < len(self.animacoes[self.estado]) - 1:
                        self.indice_animacao += 1
                    else:
                        self.esta_atacando = False
                        self.estado = 'parado'
                        self.indice_animacao = 0

            else:
                # Caso esteja em outro estado (parado, andando, etc.), roda a animação normalmente
                if self.estado in self.animacoes:
                    self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])

            # Atualiza a imagem atual do personagem
            if self.estado in self.animacoes:
                self.image = self.animacoes[self.estado][self.indice_animacao]
                if not self.direita:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.mask = pygame.mask.from_surface(self.image)

    # Aplica dano ao jogador se estiver colidindo com ele
    def aplicar_dano(self):
        if pygame.sprite.collide_rect(self, self.alvo):
            dano = self.ataques[self.tipo_ataque]['dano']
            self.alvo.receber_dano(dano)

    # Reutiliza a função de desenhar barra de vida da classe base
    def draw_hp_bar(self, tela, camera):
        super().draw_hp_bar(tela, camera)

    # Verifica colisão com obstáculos do tilemap (parede, objetos etc.)
    def verificar_colisao(self, tilemap):
        super().verificar_colisao(tilemap)

    # Aplica o dano recebido, delegando à classe base (que já lida com escudo e morte)
    def receber_dano(self, quantidade):
        super().receber_dano(quantidade)
