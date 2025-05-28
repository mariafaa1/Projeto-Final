# Importa pygame e a classe base do Boss
import pygame
from boss1.base_boss1 import BossBase

# Classe específica para a Fase 1 do Boss
class BossPhase1(BossBase):
    def __init__(self, x, y, alvo):
        # Chama o construtor da classe base (BossBase)
        super().__init__(x, y, alvo)

        # Define atributos específicos para o Boss da fase 1
        self.hp_max = 500  # Vida máxima reduzida
        self.hp_atual = self.hp_max  # Inicializa a vida atual
        self.xp_drop = 300  # XP concedido ao derrotar
        self.dano_ataque_fraco = 10
        self.dano_ataque_pesado = 15
        self.dano_ataque_especial = 25
        self.distancia_ataque = 50  # Alcance de ataque menor que o padrão da base

        # Define o frame exato em que o dano é aplicado para cada tipo de ataque
        self.frame_dano = {
            'ataque_fraco': 5,
            'ataque_pesado': 9,
            'ataque_especial': 7
        }

    # Método específico para aplicar dano em área (ataque especial)
    def aplicar_dano_area(self, raio):
        # Cria uma área retangular ao redor do boss com base no raio informado
        area_ataque = pygame.Rect(
            self.rect.centerx - raio,
            self.rect.centery - raio,
            raio * 2,
            raio * 2
        )

        # Se o jogador estiver dentro da área, aplica o dano especial
        if area_ataque.colliderect(self.alvo.rect):
            self.alvo.receber_dano(self.dano_ataque_especial)

    # Sobrescreve o método de animação para adicionar lógica do ataque especial
    def atualizar_animacao(self, dt):
        # Chama o comportamento padrão de animação do BossBase
        super().atualizar_animacao(dt)

        # Se está realizando o ataque especial e chegou no frame certo, aplica dano em área
        if self.esta_atacando and self.estado == 'ataque_especial':
            if self.indice_animacao == self.frame_dano['ataque_especial']:
                self.aplicar_dano_area(150)  # Raio de alcance de 150px ao redor
