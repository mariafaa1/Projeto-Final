from inimigos_codigos.Inimigos_mapa2.base_boss2 import Boss2Base
import pygame

# Classe específica do boss2, que herda da classe base Boss2Base
class Boss2(Boss2Base):
    def __init__(self, x, y, alvo, grupo_inimigos):
        # Chama o construtor da classe base
        super().__init__(x, y, alvo, grupo_inimigos)
        
        # Garante que o HP atual começa no máximo
        self.hp_atual = self.hp_max
        # Define a distância de ataque específica deste boss
        self.distancia_ataque = 150

    # Função responsável por aplicar dano em área ao jogador
    def aplicar_dano_area(self, raio):
        # Cria um retângulo ao redor do boss com raio definido
        area_ataque = pygame.Rect(
            self.rect.centerx - raio,
            self.rect.centery - raio,
            raio * 2,
            raio * 2
        )
        # Verifica se o jogador está dentro da área de ataque e aplica dano
        if area_ataque.colliderect(self.alvo.rect):
            self.alvo.receber_dano(self.dano_ataque_especial)

    # Sobrescreve a função de animação para incluir ataque especial com dano em área
    def atualizar_animacao(self, dt):
        # Chama a animação normal da classe base
        super().atualizar_animacao(dt)
        # Se estiver atacando e for o ataque especial
        if self.esta_atacando and self.estado == 'ataque_especial':
            # Se chegou no frame do golpe, aplica o dano em área
            if self.indice_animacao == self.frame_dano['ataque_especial']:
                self.aplicar_dano_area(150)
