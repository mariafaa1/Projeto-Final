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
from camera import Camera
from tilemap import TileMap

def debug_draw_hitboxes(surface, grupos, camera, cor=(255, 0, 0), espessura=2):
    for grupo in grupos:
        for sprite in grupo:
            pygame.draw.rect(surface, cor, camera.aplicar(sprite), espessura)
            centro = camera.aplicar_rect(sprite.rect).center
            pygame.draw.circle(surface, (0, 255, 0), centro, 3)

class LevelManager:
    def __init__(self):
        self.fase_atual = 1
        self.config_fases = {
            1: {'inimigos_normais': 2, 'boss': {'classe': BossBase, 'pos': (1500, 500)}},
            2: {'inimigos_normais': 1, 'boss': {'classe': BossBase, 'pos': (2000, 500)}},
            3: {'inimigos_normais': 3, 'boss': {'classe': BossBase, 'pos': (2500, 500)}}
        }

    def spawn_fase(self, grupo_inimigos, alvo, grupo_jogador, grupo_projeteis):
        config = self.config_fases[self.fase_atual]
        boss = config['boss']['classe'](x=config['boss']['pos'][0], y=config['boss']['pos'][1], alvo=alvo)
        grupo_inimigos.add(boss)

        for _ in range(config['inimigos_normais']):
            pos_x = random.randint(200, 2800)
            pos_y = random.randint(200, 800)

            if self.fase_atual == 2:
                inimigo = OrcArmadura(pos_x, pos_y, alvo)
            elif self.fase_atual == 3:
                inimigo = EsqueletoArqueiro(pos_x, pos_y, alvo, grupo_projeteis)
            else:
                inimigo = Esqueleto(pos_x, pos_y, alvo) if random.random() > 0.5 else OrcNormal(pos_x, pos_y, alvo)

            grupo_inimigos.add(inimigo)

def tela_jogo(janela, animacoes):
    relogio = pygame.time.Clock()

    mapa = TileMap("Mapas/Mapa1/mapa1.tmx", zoom=4)  # Zoom ajustável

    grupo_inimigos = pygame.sprite.Group()
    grupo_projeteis = pygame.sprite.Group()
    soldado = Soldado(animacoes, grupo_inimigos, grupo_projeteis)
    grupo_jogador = pygame.sprite.Group(soldado)

    if "player" in mapa.spawn_points:
        spawn_rect = mapa.spawn_points["player"]
        soldado.rect.center = spawn_rect.center

    camera = Camera(LARGURA, ALTURA)
    camera.configurar_limites(*mapa.map_size)

    level_manager = LevelManager()
    level_manager.spawn_fase(grupo_inimigos, soldado, grupo_jogador, grupo_projeteis)

    estado_jogo = JOGANDO
    fonte = pygame.font.Font(CAMINHO_FONTE, FONTE_TAMANHO)
    executando = True
    debug_hitboxes = False

    while executando:
        dt = relogio.tick(FPS) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and estado_jogo == GAME_OVER:
                if 300 <= pygame.mouse.get_pos()[0] <= 500 and 400 <= pygame.mouse.get_pos()[1] <= 450:
                    return True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_u:
                    debug_hitboxes = not debug_hitboxes

        if estado_jogo == JOGANDO:
            teclas = pygame.key.get_pressed()
            grupo_jogador.update(teclas)
            grupo_inimigos.update(dt)
            grupo_projeteis.update()
            camera.update(soldado)

            if soldado.animacao_morte_concluida:
                estado_jogo = GAME_OVER

            boss_vivo = any(hasattr(i, 'eh_boss') and not i.esta_morto for i in grupo_inimigos)
            if not boss_vivo and level_manager.fase_atual < 3:
                level_manager.fase_atual += 1
                grupo_inimigos.empty()
                level_manager.spawn_fase(grupo_inimigos, soldado, grupo_jogador, grupo_projeteis)

            for inimigo in grupo_inimigos:
                if inimigo.esta_morto and not inimigo.xp_entregue and hasattr(inimigo, 'xp_drop'):
                    soldado.ganhar_xp(inimigo.xp_drop)
                    inimigo.xp_entregue = True

        janela.fill(FUNDO_BRANCO)

        # ✅ Renderiza mapa pré-renderizado completo
        janela.blit(mapa.surface_completa, (-int(camera.offset.x), -int(camera.offset.y)))

        if estado_jogo == JOGANDO:
            for entidade in grupo_inimigos:
                janela.blit(entidade.image, camera.aplicar(entidade))

            janela.blit(soldado.image, camera.aplicar(soldado))
            for projetil in grupo_projeteis:
                janela.blit(projetil.image, camera.aplicar(projetil))

            soldado.draw_hud(janela)
            soldado.draw_hp_bar(janela, camera)
            for inimigo in grupo_inimigos:
                inimigo.draw_hp_bar(janela, camera)

            if debug_hitboxes:
                debug_draw_hitboxes(janela, [grupo_jogador, grupo_inimigos, grupo_projeteis], camera)

        elif estado_jogo == GAME_OVER:
            texto_game_over = fonte.render("GAME OVER", True, BRANCO)
            texto_rect = texto_game_over.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
            janela.blit(texto_game_over, texto_rect)

            pygame.draw.rect(janela, BRANCO, (300, 400, 200, 50))
            texto_reiniciar = fonte.render("Reiniciar", True, PRETO)
            texto_reiniciar_rect = texto_reiniciar.get_rect(center=(LARGURA // 2, 425))
            janela.blit(texto_reiniciar, texto_reiniciar_rect)

        pygame.display.flip()

    return False
