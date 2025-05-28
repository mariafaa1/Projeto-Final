import pygame
import random
from inimigos_codigos.base_esqueleto import InimigoBase  # Classe base com lógica comum dos esqueletos

# Classe que representa o inimigo Esqueleto, herdando de InimigoBase
class Esqueleto(InimigoBase):
    def __init__(self, x, y, alvo, inimigos_group):
        """
        Construtor do esqueleto.
        Define atributos de vida, velocidade, alvo e grupo.
        Também define ataques com cooldowns diferentes.
        """
        super().__init__(
            x=x,
            y=y,
            hp_max=60,  # Vida máxima do esqueleto
            velocidade=1.8,  # Velocidade maior que a de orcs
            alvo=alvo,  # Referência ao jogador
            inimigos_group=inimigos_group  # Grupo ao qual pertence
        )
        
        # Definição dos ataques
        self.dano_ataque1 = 15
        self.dano_ataque2 = 20
        self.cooldown_ataque1 = 1500  # Cooldown em milissegundos
        self.cooldown_ataque2 = 2000
        self.ultimo_ataque1 = 0  # Timestamp do último ataque1
        self.ultimo_ataque2 = 0  # Timestamp do último ataque2

        # Tipo de ataque ativo e dano correspondente
        self.tipo_ataque = 'ataque1'
        self.dano = self.dano_ataque1
        self.xp_drop = 15  # XP concedido ao jogador ao derrotá-lo

    def update(self, dt):
        """
        Atualiza o estado do esqueleto a cada frame:
        - Verifica se pode atacar.
        - Persegue o jogador.
        - Atualiza a animação conforme o estado.
        """
        agora = pygame.time.get_ticks()  # Tempo atual do jogo
        
        # Se não estiver morto nem atacando, verifica se pode atacar
        if not self.esta_morto and not self.esta_atacando:
            if self.verificar_distancia_ataque():  # Está perto do jogador
                ataques_disponiveis = []

                # Verifica cooldowns para cada tipo de ataque
                if agora - self.ultimo_ataque1 >= self.cooldown_ataque1:
                    ataques_disponiveis.append('ataque1')
                if agora - self.ultimo_ataque2 >= self.cooldown_ataque2:
                    ataques_disponiveis.append('ataque2')

                # Se há ataques disponíveis, sorteia um e inicia
                if ataques_disponiveis:
                    self.tipo_ataque = random.choice(ataques_disponiveis)
                    self.iniciar_ataque(agora)

        # Se ainda estiver vivo:
        if not self.esta_morto:
            if not self.esta_atacando:
                self.perseguir_alvo()  # Move em direção ao jogador
            self.atualizar_animacao(dt)  # Atualiza frames da animação
        elif self.estado == 'morrendo' and not self.animacao_morte_concluida:
            self.atualizar_animacao(dt)  # Continua animação de morte

        # Volta ao estado 'parado' após tempo de dano
        if self.estado == 'dano' and pygame.time.get_ticks() - self.tempo_dano > 500:
            self.estado = 'parado'

    def iniciar_ataque(self, tempo_atual):
        """
        Inicia a animação e os efeitos do ataque selecionado.
        Zera movimento e configura o dano de acordo com o ataque.
        """
        self.esta_atacando = True
        self.estado = self.tipo_ataque  # Define o estado como o tipo de ataque
        self.indice_animacao = 0  # Começa a animação do início
        self.velocidade_x = 0  # Para movimentação
        self.velocidade_y = 0

        # Define o dano com base no tipo de ataque
        if self.tipo_ataque == 'ataque1':
            self.dano = self.dano_ataque1
        else:
            self.dano = self.dano_ataque2

    def atualizar_animacao(self, dt):
        """
        Atualiza a animação do esqueleto.
        No fim da animação de ataque, aplica o dano ao jogador (se estiver colidindo).
        """
        super().atualizar_animacao(dt)  # Chama a animação da classe base

        # Verifica se a animação de ataque terminou
        if self.esta_atacando and self.indice_animacao == len(self.animacoes[self.estado]) - 1:
            self.esta_atacando = False
            self.estado = 'parado'  # Retorna ao estado parado

            agora = pygame.time.get_ticks()  # Marca o tempo do ataque
            # Atualiza o tempo do último ataque conforme o tipo
            if self.tipo_ataque == 'ataque1':
                self.ultimo_ataque1 = agora
            else:
                self.ultimo_ataque2 = agora

            # Se ainda estiver colidindo com o jogador, aplica o dano
            if pygame.sprite.collide_rect(self, self.alvo):
                self.alvo.receber_dano(self.dano)
