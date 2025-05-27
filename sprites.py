import pygame
from config import (
    LARGURA, ALTURA, VELOCIDADE_JOGADOR, VELOCIDADE_PROJETIL,
    TEMPO_COOLDOWN_ATAQUE_PESADO, TEMPO_COOLDOWN_ARCO, TEMPO_COOLDOWN_ATAQUE_LEVE,
    HP_MAXIMO, HP_INICIAL, POSICAO_BARRA_OFFSET_Y, LARGURA_BARRA, ALTURA_BARRA,
    COR_HP_ATUAL, COR_HP_PERDIDO, BORDA_HP, COR_BORDA, TESTE_MANUAL_DANO,
    DANO_ATAQUE_LEVE, DANO_ATAQUE_PESADO, DANO_ARCO
)

class Soldado(pygame.sprite.Sprite):
    def __init__(self, animacoes, grupo_inimigos, grupo_projeteis):
        super().__init__()
        self.animacoes = animacoes
        self.estado = 'parado'
        self.indice_animacao = 0
        self.image = self.animacoes[self.estado][self.indice_animacao]
        self.rect = self.image.get_rect(center=(LARGURA//2, ALTURA//2))
        self.dano_ataque_leve = DANO_ATAQUE_LEVE 
        self.dano_ataque_pesado = DANO_ATAQUE_PESADO
        self.dano_arco = DANO_ARCO
        self.tempo_animacao = 100       
        self.tempo_animacao_morte = 150
        self.vel_x = 0 
        self.vel_y = 0  
        
        # ======================================================
        # PARÂMETROS AJUSTÁVEIS - ATAQUES
        # ======================================================
        self.ataques = {
            'ataque_leve': {
                'frame_dano': 3,                          # Frame que aplica o dano
                'cooldown': TEMPO_COOLDOWN_ATAQUE_LEVE,   # Tempo entre ataques
                'hitbox': {'offset_x': 30, 'offset_y': -25, 'largura': 30, 'altura': 27}  # Posição e tamanho
            },
            'ataque_pesado': {
                'frame_dano': 4,
                'cooldown': TEMPO_COOLDOWN_ATAQUE_PESADO,
                'hitbox': {'offset_x': 40, 'offset_y': -30, 'largura': 40, 'altura': 30}
            },
            'ataque_arco': {
                'frame_dano': len(animacoes['ataque_arco']) - 2,  # Penúltimo frame (automatico)
                'cooldown': TEMPO_COOLDOWN_ARCO,
                'deslocamento_flecha_y': 5  # Ajuste vertical do ponto de disparo
            }
        }

        self.ultimo_update = pygame.time.get_ticks()
        self.virado_para_esquerda = False
        self.executando_ataque = False
        self.ultimo_ataque_pesado = 0
        self.ultimo_ataque_arco = 0
        self.grupo_projeteis = grupo_projeteis
        self.disparar_flecha_pendente = False
        self.ultimo_ataque_leve = 0
        self.hp_max = HP_MAXIMO
        self.hp_atual = HP_INICIAL
        self.animacao_dano_ativa = False
        self.esta_morto = False
        self.animacao_morte_ativa = False
        self.animacao_morte_concluida = False
        self.tempo_morte_concluida = 0
        self.grupo_inimigos = grupo_inimigos
        self.indice_dano = 0
        self.ultimo_update_dano = 0
        # ======================================================
        # NOVOS ATRIBUTOS PARA HUD/XP (ADICIONADOS)
        # ======================================================
        self.xp = 0
        self.nivel = 1
        self.xp_para_prox_nivel = 100
        self.cor_xp = (0, 150, 200)    # Azul
        self.cor_nivel = (255, 215, 0) # Dourado

    def update(self, teclas):
        agora = pygame.time.get_ticks()
        
        if self.esta_morto:
            self.processar_morte(agora)
            return

        self.processar_movimento_ataque(teclas, agora)
        self.processar_dano(agora)
        self.processar_animacoes(agora)

    def processar_morte(self, agora):
        if not self.animacao_morte_ativa:
            self.animacao_morte_ativa = True
            self.estado = 'morrer'
            self.indice_animacao = 0
            self.ultimo_update = agora
        else:
            if agora - self.ultimo_update > self.tempo_animacao_morte:
                self.ultimo_update = agora
                if self.indice_animacao < len(self.animacoes['morrer']) - 1:
                    self.indice_animacao += 1
                else:
                    if not self.animacao_morte_concluida:
                        self.animacao_morte_concluida = True
                        self.tempo_morte_concluida = agora
        
        frame = self.animacoes['morrer'][min(self.indice_animacao, len(self.animacoes['morrer']) - 1)]
        if self.virado_para_esquerda:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

    def processar_movimento_ataque(self, teclas, agora):
        self.vel_x = 0 
        self.vel_y = 0
        movimento = False
        novo_estado = 'parado'
        
        # Controles de movimento
        if teclas[pygame.K_a]:
            self.rect.x -= VELOCIDADE_JOGADOR
            novo_estado = 'andando'
            self.virado_para_esquerda = True
            movimento = True
        if teclas[pygame.K_d]:
            self.rect.x += VELOCIDADE_JOGADOR
            novo_estado = 'andando'
            self.virado_para_esquerda = False
            movimento = True
        if teclas[pygame.K_w]:
            self.rect.y -= VELOCIDADE_JOGADOR
            novo_estado = 'andando'
            movimento = True
        if teclas[pygame.K_s]:
            self.rect.y += VELOCIDADE_JOGADOR
            novo_estado = 'andando'
            movimento = True

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if not self.executando_ataque:
            self.estado = novo_estado

        # Controle de ataques
        if not self.executando_ataque:
            if teclas[pygame.K_k] and (agora - self.ultimo_ataque_pesado > self.ataques['ataque_pesado']['cooldown']):
                self.iniciar_ataque('ataque_pesado', agora)
                self.ultimo_ataque_pesado = agora
                
            elif teclas[pygame.K_j] and (agora - self.ultimo_ataque_leve > self.ataques['ataque_leve']['cooldown']):
                self.iniciar_ataque('ataque_leve', agora)
                self.ultimo_ataque_leve = agora
                
            elif teclas[pygame.K_l] and (agora - self.ultimo_ataque_arco > self.ataques['ataque_arco']['cooldown']):
                self.iniciar_ataque('ataque_arco', agora)
                self.ultimo_ataque_arco = agora

        if TESTE_MANUAL_DANO and teclas[pygame.K_h]:
            self.receber_dano(50)

    def iniciar_ataque(self, tipo_ataque, agora):
        self.estado = tipo_ataque
        self.indice_animacao = 0
        self.executando_ataque = True
        self.ultimo_update = agora
        if tipo_ataque == 'ataque_arco':
            self.disparar_flecha_pendente = True

    def processar_dano(self, agora):
        if self.animacao_dano_ativa:
            if agora - self.ultimo_update_dano > self.tempo_animacao:
                self.ultimo_update_dano = agora
                self.indice_dano += 1
                if self.indice_dano >= len(self.animacoes['dano']):
                    self.animacao_dano_ativa = False
                    self.indice_dano = 0

    def processar_animacoes(self, agora):
        # Atualização normal da animação
        if not self.executando_ataque and agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            if self.estado in self.animacoes:
                self.indice_animacao = (self.indice_animacao + 1) % len(self.animacoes[self.estado])

        # Processamento especial para ataques
        if self.executando_ataque:
            self.processar_animacao_ataque(agora)

        # Seleção do frame
        if self.animacao_dano_ativa:
            frame_index = min(self.indice_dano, len(self.animacoes['dano'])-1)
            frame = self.animacoes['dano'][frame_index]
        else:
            if self.estado in self.animacoes:
                frame_list = self.animacoes[self.estado]
                frame_index = min(self.indice_animacao, len(frame_list)-1)
                frame = frame_list[frame_index]
            else:
                frame = self.image

        if self.virado_para_esquerda:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

    def processar_animacao_ataque(self, agora):
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
        
            if self.indice_animacao < len(self.animacoes[self.estado]) - 1:
                self.indice_animacao += 1
            else:
                self.indice_animacao = len(self.animacoes[self.estado]) - 1

            # Aplicar dano/projétil no frame especificado
            if self.indice_animacao == self.ataques[self.estado]['frame_dano']:
                if self.estado == 'ataque_arco':
                    self.disparar_flecha()
                else:
                    dano = self.dano_ataque_leve if self.estado == 'ataque_leve' else self.dano_ataque_pesado
                    self.aplicar_dano_corpo_a_corpo(dano)

            # Finalizar animação
            if self.indice_animacao >= len(self.animacoes[self.estado]) - 1:
                self.indice_animacao = 0
                self.executando_ataque = False
                self.estado = 'parado'

    def disparar_flecha(self):
        deslocamento_y = self.ataques['ataque_arco']['deslocamento_flecha_y']
        centro_personagem = (self.rect.centerx, self.rect.centery + deslocamento_y)
        novo_proj = Projetil(centro_personagem, self.virado_para_esquerda, self.grupo_inimigos, self.dano_arco)
        self.grupo_projeteis.add(novo_proj)
        self.disparar_flecha_pendente = False

    def aplicar_dano_corpo_a_corpo(self, dano):
        config = self.ataques[self.estado]['hitbox']
        offset_x = -config['offset_x'] if self.virado_para_esquerda else config['offset_x']
        
        hitbox = pygame.Rect(
            self.rect.centerx + offset_x - (config['largura']//2),
            self.rect.centery + config['offset_y'],
            config['largura'],
            config['altura']
        )
        
        # Visualização da hitbox (debug)
        # pygame.draw.rect(pygame.display.get_surface(), (255,0,0), hitbox, 2)
        
        for inimigo in self.grupo_inimigos:
            if hitbox.colliderect(inimigo.rect):
                inimigo.receber_dano(dano)

    def receber_dano(self, quantidade):
        if not self.esta_morto and not self.animacao_dano_ativa:
            self.hp_atual = max(0, self.hp_atual - quantidade)
            if self.hp_atual <= 0:
                self.esta_morto = True
            else:
                self.animacao_dano_ativa = True
                self.indice_dano = 0
                self.ultimo_update_dano = pygame.time.get_ticks()

    def draw_hp_bar(self, tela):
        if not self.esta_morto:
            barra_x = self.rect.centerx - LARGURA_BARRA // 2
            barra_y = self.rect.centery + POSICAO_BARRA_OFFSET_Y
            proporcao_hp = self.hp_atual / self.hp_max
            largura_atual = int(LARGURA_BARRA * proporcao_hp)
            pygame.draw.rect(tela, COR_HP_PERDIDO, (barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA))
            pygame.draw.rect(tela, COR_HP_ATUAL, (barra_x, barra_y, largura_atual, ALTURA_BARRA))
            if BORDA_HP:
                pygame.draw.rect(tela, COR_BORDA, (barra_x, barra_y, LARGURA_BARRA, ALTURA_BARRA), 1)

    def draw(self, tela):
        tela.blit(self.image, self.rect)
        self.draw_hp_bar(tela)
    def draw_hud(self, tela):
        """Desenha a interface do usuário (barra de XP e nível)"""
        # Configurações da barra de XP
        largura_max = 200
        altura = 20
        borda = 2
        pos_x = 10
        pos_y = 10

        # Calcula a proporção do XP
        proporcao = self.xp / self.xp_para_prox_nivel
        largura_atual = int(largura_max * proporcao)

        # Desenha o fundo da barra
        pygame.draw.rect(tela, (50, 50, 50), (
            pos_x - borda,
            pos_y - borda,
            largura_max + 2*borda,
            altura + 2*borda
        ))
        
        # Barra de XP
        pygame.draw.rect(tela, self.cor_xp, (
            pos_x,
            pos_y,
            largura_atual,
            altura
        ))

        # Texto do nível
        fonte = pygame.font.Font(None, 24)
        texto = fonte.render(f"Nv. {self.nivel}", True, self.cor_nivel)
        tela.blit(texto, (pos_x + largura_max + 10, pos_y - 3))

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        while self.xp >= self.xp_para_prox_nivel:
            self.subir_nivel()
            self.xp -= self.xp_para_prox_nivel
            print(f"Subiu para o nível {self.nivel}!")

    def subir_nivel(self):
        self.nivel += 1
        self.xp_para_prox_nivel = int(self.xp_para_prox_nivel * 1.5)
        self.hp_max += 20
        self.hp_atual = self.hp_max

        # Melhoria de atributos
        self.dano_ataque_leve *= 3  
        self.dano_ataque_pesado *= 3
        self.dano_arco *= 3
class Projetil(pygame.sprite.Sprite):
    def __init__(self, position, virado_para_esquerda, grupo_inimigos, dano):
        super().__init__()
        try:
            self.image = pygame.image.load('assets/projetil_arco/flecha.png').convert_alpha()
            if virado_para_esquerda:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(center=position)
        except Exception as e:
            print(f"Erro ao carregar flecha: {e}")
            self.kill()
        self.velocidade = VELOCIDADE_PROJETIL
        self.direcao = -1 if virado_para_esquerda else 1
        self.grupo_inimigos = grupo_inimigos
        self.dano = dano
        self.mask = pygame.mask.from_surface(self.image)  # Mask para colisão precisa

    def update(self):
        self.rect.x += self.velocidade * self.direcao
        
        # Verificação de colisão com máscara
        for inimigo in pygame.sprite.spritecollide(self, self.grupo_inimigos, False, pygame.sprite.collide_mask):
            inimigo.receber_dano(self.dano)
            self.kill()
            break
        
        if self.rect.right < -50 or self.rect.left > LARGURA + 50:
            self.kill()