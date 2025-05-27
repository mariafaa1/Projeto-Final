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
from inimigos_codigos.Inimigos_mapa2.orc_armadura import OrcArmadura  
from inimigos_codigos.Inimigos_mapa2.esqueleto_arqueiro import EsqueletoArqueiro

def debug_draw_hitboxes(surface, grupos, cor=(255, 0, 0), espessura=2):
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
                'inimigos_normais': 1,
                'boss': {
                    'classe': BossBase,
                    'pos': (LARGURA//2, ALTURA//2)
                }
            },
            3: {  # Nova fase para testar arqueiros
                'inimigos_normais': 3,
                'boss': {
                    'classe': BossBase,
                    'pos': (LARGURA//2, ALTURA//2)
                }
            }
        }

    def spawn_fase(self, grupo_inimigos, alvo, grupo_jogador, grupo_projeteis):
        config = self.config_fases[self.fase_atual]
        
        # Spawn Boss
        boss = config['boss']['classe'](
            x=config['boss']['pos'][0],
            y=config['boss']['pos'][1],
            alvo=alvo
        )
        grupo_inimigos.add(boss)

        # Spawn Inimigos
        for _ in range(config['inimigos_normais']):
            pos_x = random.randint(100, LARGURA-100)
            pos_y = random.randint(100, ALTURA-100)
            
            if self.fase_atual == 2:
                inimigo = OrcArmadura(pos_x, pos_y, alvo)
            elif self.fase_atual == 3:
                inimigo = EsqueletoArqueiro(pos_x, pos_y, alvo, grupo_projeteis)
            else:
                if random.random() > 0.5:
                    inimigo = Esqueleto(pos_x, pos_y, alvo)
                else:
                    inimigo = OrcNormal(pos_x, pos_y, alvo)
            
            grupo_inimigos.add(inimigo)

def tela_jogo(janela, animacoes):
    relogio = pygame.time.Clock()
    
    # Inicialização
    level_manager = LevelManager()
    grupo_inimigos = pygame.sprite.Group()
    grupo_projeteis = pygame.sprite.Group()
    
    soldado = Soldado(animacoes, grupo_inimigos, grupo_projeteis)
    grupo_jogador = pygame.sprite.Group(soldado)
    level_manager.spawn_fase(grupo_inimigos, soldado, grupo_jogador, grupo_projeteis)
    
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
            
            grupo_jogador.update(teclas)
            grupo_inimigos.update(dt)
            grupo_projeteis.update()

            if soldado.animacao_morte_concluida:
                estado_jogo = GAME_OVER

            boss_vivo = any(hasattr(inimigo, 'eh_boss') and not inimigo.esta_morto for inimigo in grupo_inimigos)
            if not boss_vivo and level_manager.fase_atual < 3:  # Correção aplicada
                level_manager.fase_atual += 1
                grupo_inimigos.empty()
                level_manager.spawn_fase(grupo_inimigos, soldado, grupo_jogador, grupo_projeteis)

            # Sistema de XP
            for inimigo in grupo_inimigos:
                if inimigo.esta_morto and not inimigo.xp_entregue:
                    if hasattr(inimigo, 'xp_drop') and inimigo.xp_drop > 0:
                        soldado.ganhar_xp(inimigo.xp_drop)
                        inimigo.xp_entregue = True

        # Renderização
        janela.fill(FUNDO_BRANCO)
        
        if estado_jogo == JOGANDO:
            grupo_jogador.draw(janela)
            grupo_projeteis.draw(janela)
            
            for inimigo in grupo_inimigos:
                if isinstance(inimigo, BossBase):
                    inimigo.draw(janela)
                else:
                    janela.blit(inimigo.image, inimigo.rect)
            
            soldado.draw_hud(janela)
            for sprite in grupo_jogador:
                sprite.draw_hp_bar(janela)
            for inimigo in grupo_inimigos:
                inimigo.draw_hp_bar(janela)
            
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