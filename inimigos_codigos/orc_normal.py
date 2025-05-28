from .base import InimigoBase  # Importa a classe base genérica de inimigos
import random
import pygame

# Classe que representa o inimigo "Orc Normal", herdando da classe base de inimigos
class OrcNormal(InimigoBase):
    def __init__(self, x, y, alvo, inimigos_group):
        """
        Construtor do Orc Normal.
        Define atributos iniciais como vida, velocidade, alvo e grupo.
        """
        super().__init__(
            x=x,
            y=y,
            hp_max=70,  # Vida máxima do orc
            velocidade=1,  # Velocidade de movimentação
            alvo=alvo,  # Referência ao jogador para perseguição
            inimigos_group=inimigos_group  # Grupo de inimigos
        )
        self.dano_ataque = 15  # Dano causado por ataque
        self.xp_drop = 50  # XP concedido ao jogador ao derrotar o orc

    def update(self, dt):
        """
        Atualiza o estado do orc a cada frame.
        Se ele não estiver morto nem atacando, verifica se pode atacar.
        """
        super().update(dt)  # Atualiza movimentação e animação
        if not self.esta_morto and not self.esta_atacando and self.estado not in ['dano', 'morrendo']:
            self.verificar_ataque()

    def verificar_ataque(self):
        """
        Verifica se o jogador está ao alcance de ataque.
        Se estiver próximo o suficiente, inicia o ataque.
        """
        dx = self.alvo.rect.centerx - self.rect.centerx  # Diferença em X até o alvo
        dy = self.alvo.rect.centery - self.rect.centery  # Diferença em Y até o alvo
        distancia = (dx**2 + dy**2)**0.5  # Distância euclidiana
        if distancia <= 50:  # Raio de alcance para iniciar o ataque
            self.iniciar_ataque()

    def iniciar_ataque(self):
        """
        Inicia a animação de ataque do orc.
        Define o estado como ataque1 ou ataque2 aleatoriamente.
        """
        self.esta_atacando = True
        self.estado = random.choice(['ataque1', 'ataque2'])  # Escolhe aleatoriamente uma das animações de ataque
        self.indice_animacao = 0  # Reinicia a animação do ataque
        self.velocidade_x = 0  # Orc para de se mover ao atacar
        self.velocidade_y = 0

    def atualizar_animacao(self, dt):
        """
        Atualiza a animação do orc.
        Ao final da animação de ataque, aplica o dano se o orc ainda colide com o jogador.
        """
        super().atualizar_animacao(dt)  # Atualiza o frame da animação

        # Se o ataque terminou (último frame), volta ao estado parado e aplica o dano
        if self.esta_atacando and self.indice_animacao == len(self.animacoes[self.estado]) - 1:
            self.esta_atacando = False
            self.estado = 'parado'

            # Aplica o dano ao jogador se ainda estiver colidindo com o orc
            if pygame.sprite.collide_rect(self, self.alvo):
                self.alvo.receber_dano(self.dano_ataque)
