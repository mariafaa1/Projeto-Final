# game_screen.py
import pygame
import random
from sprites import Soldado
from config import (
    FPS, FUNDO_BRANCO, LARGURA, ALTURA,
    JOGANDO, GAME_OVER, PRETO, BRANCO,
    FONTE_TAMANHO, CAMINHO_FONTE
)
from inimigos_codigos.orc_normal import OrcNormal
from inimigos_codigos.esqueleto import Esqueleto
from inimigos_codigos.boss1.base_boss1 import BossBase

def debug_draw_hitboxes(surface, grupos, cor=(255, 0, 0), espessura=2):
    """Desenha hitboxes de todos os sprites nos grupos especificados"""
    for grupo in grupos:
        for sprite in grupo:
            pygame.draw.rect(surface, cor, sprite.rect, espessura)
            centro = sprite.rect.center
            pygame.draw.circle(surface, (0, 255, 0), centro, 3)

class LevelManager:
    def __init__(self):
        self.fase_atual = 1
        self.config_fases = {
            1: {
                'inimigos_normais': 2,
                'boss': {
                    'classe': BossBase,
                    'pos': (LARGURA//2, ALTURA//2)
                }
            },
            2: {
                'inimigos_normais': 2,
                'boss': {
                    'classe': BossBase,
                    'pos': (LARGURA//2, ALTURA//2)
                }
            }
        }

    def spawn_fase(self, grupo_inimigos, alvo):
        config = self.config_fases[self.fase_atual]
        
        # Spawn Boss
        boss = config['boss']['classe'](
            x=config['boss']['pos'][0],
            y=config['boss']['pos'][1],
            alvo=alvo
        )
        grupo_inimigos.add(boss)

        # Spawn Inimigos Normais
        for _ in range(config['inimigos_normais']):
            pos_x = random.randint(100, LARGURA-100)
            pos_y = random.randint(100, ALTURA-100)
            
            if random.random() > 0.5:
                inimigo = Esqueleto(pos_x, pos_y, alvo)
            else:
                inimigo = OrcNormal(pos_x, pos_y, alvo)
            
            grupo_inimigos.add(inimigo)

def tela_jogo(janela, animacoes):
    relogio = pygame.time.Clock()
    
    # Inicialização dos sistemas
    level_manager = LevelManager()
    grupo_inimigos = pygame.sprite.Group()
    grupo_projeteis = pygame.sprite.Group()
    
    soldado = Soldado(animacoes, grupo_inimigos, grupo_projeteis)
    level_manager.spawn_fase(grupo_inimigos, soldado)
    
    grupo_jogador = pygame.sprite.Group(soldado)
    estado_jogo = JOGANDO
    fonte = pygame.font.Font(CAMINHO_FONTE, FONTE_TAMANHO)
    executando = True
    debug_hitboxes = False

    while executando:
        dt = relogio.tick(FPS) / 1000

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and estado_jogo == GAME_OVER:
                if 300 <= pygame.mouse.get_pos()[0] <= 500 and 400 <= pygame.mouse.get_pos()[1] <= 450:
                    return True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_u:
                    debug_hitboxes = not debug_hitboxes

        # Atualizações
        if estado_jogo == JOGANDO:
            teclas = pygame.key.get_pressed()
            
            # Atualizar entidades
            grupo_jogador.update(teclas)
            grupo_inimigos.update(dt)
            grupo_projeteis.update()

            # Verificar morte do jogador
            if soldado.animacao_morte_concluida:
                estado_jogo = GAME_OVER

            # Verificar progressão de fase
            boss_vivo = any(hasattr(inimigo, 'eh_boss') and not inimigo.esta_morto for inimigo in grupo_inimigos)
            if not boss_vivo:
                level_manager.fase_atual += 1
                grupo_inimigos.empty()
                level_manager.spawn_fase(grupo_inimigos, soldado)

            # Sistema de XP (corrigido)
            for inimigo in grupo_inimigos:
                if inimigo.esta_morto and hasattr(inimigo, 'xp_entregue') and not inimigo.xp_entregue:
                    soldado.ganhar_xp(inimigo.xp_drop)
                    inimigo.xp_entregue = True

        # Renderização
        janela.fill(FUNDO_BRANCO)
        
        if estado_jogo == JOGANDO:
            # Desenhar todos os elementos
            grupo_jogador.draw(janela)
            grupo_projeteis.draw(janela)
            
            # Desenhar inimigos com renderização customizada para o boss
            for inimigo in grupo_inimigos:
                if isinstance(inimigo, BossBase):
                    inimigo.draw(janela)
                else:
                    janela.blit(inimigo.image, inimigo.rect)
            
            # UI
            soldado.draw_hud(janela)
            for sprite in grupo_jogador:
                sprite.draw_hp_bar(janela)
            for inimigo in grupo_inimigos:
                inimigo.draw_hp_bar(janela)
            
            # Debug de hitboxes
            if debug_hitboxes:
                debug_draw_hitboxes(janela, [grupo_jogador, grupo_inimigos, grupo_projeteis])
                
        elif estado_jogo == GAME_OVER:
            texto_game_over = fonte.render("GAME OVER", True, BRANCO)
            texto_rect = texto_game_over.get_rect(center=(LARGURA//2, ALTURA//2-50))
            janela.blit(texto_game_over, texto_rect)
            
            pygame.draw.rect(janela, BRANCO, (300, 400, 200, 50))
            texto_reiniciar = fonte.render("Reiniciar", True, PRETO)
            texto_reiniciar_rect = texto_reiniciar.get_rect(center=(LARGURA//2, 425))
            janela.blit(texto_reiniciar, texto_reiniciar_rect)

        pygame.display.flip()

    return False