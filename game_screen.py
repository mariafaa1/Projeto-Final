#game_screen.py
import pygame
from config import FPS, FUNDO_BRANCO, JOGANDO, GAME_OVER
from sprites import Soldado
from inimigos_codigos.orc_normal import OrcNormal
from inimigos_codigos.esqueleto import Esqueleto
from inimigos_codigos.boss1.base_boss1 import BossBase
from inimigos_codigos.Inimigos_mapa2.orc_armadura import OrcArmadura
from inimigos_codigos.Inimigos_mapa2.esqueleto_arqueiro import EsqueletoArqueiro
from camera import Camera
from tilemap import TileMap
import pygame as pg

def processar_spawns(tilemap, soldado, grupo_inimigos, grupo_projeteis):
    for obj in tilemap.tmxdata.objects:
        if obj.name == 'spawn_soldado':
            spawn_rect = pg.Rect(
                obj.x * tilemap.zoom,
                obj.y * tilemap.zoom,
                obj.width * tilemap.zoom,
                obj.height * tilemap.zoom
            )
            soldado.rect.center = spawn_rect.center
            soldado.hitbox_rect.center = spawn_rect.center
        elif obj.name == 'spawn_orc':
            orc = OrcNormal(obj.x * tilemap.zoom, obj.y * tilemap.zoom, soldado, grupo_inimigos)
            grupo_inimigos.add(orc)

        elif obj.name == 'spawn_esqueleto':
            esqueleto = Esqueleto(obj.x * tilemap.zoom, obj.y * tilemap.zoom, soldado, grupo_inimigos)
            grupo_inimigos.add(esqueleto)

        elif obj.name == 'spawn_esqueleto_arqueiro':
            arqueiro = EsqueletoArqueiro(obj.x * tilemap.zoom, obj.y * tilemap.zoom, soldado, grupo_projeteis)
            grupo_inimigos.add(arqueiro)

        elif obj.name == 'spawn_orc_armadura':
            orc_armadura = OrcArmadura(obj.x * tilemap.zoom, obj.y * tilemap.zoom, soldado)
            grupo_inimigos.add(orc_armadura)

        elif obj.name == 'spawn_boss':
            boss = BossBase(obj.x * tilemap.zoom, obj.y * tilemap.zoom, soldado, grupo_inimigos)
            grupo_inimigos.add(boss)

    print("[INFO] Spawns processados com sucesso!")

def tela_jogo(janela, animacoes_soldado):
    clock = pygame.time.Clock()
    estado = JOGANDO

    tilemap = TileMap('Mapas/Mapa1/mapa1.tmx', zoom=3)
    largura_janela, altura_janela = janela.get_size()

    grupo_inimigos = pygame.sprite.Group()
    grupo_projeteis = pygame.sprite.Group()

    soldado = Soldado(animacoes_soldado, grupo_inimigos, grupo_projeteis)

    mapa_largura, mapa_altura = tilemap.map_size
    camera = Camera(largura_janela, altura_janela)
    mapa_largura, mapa_altura = tilemap.map_size
    camera.configurar_limites(mapa_largura, mapa_altura)

    processar_spawns(tilemap, soldado, grupo_inimigos, grupo_projeteis)

    while estado == JOGANDO:
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado = GAME_OVER

        teclas = pygame.key.get_pressed()
        
        soldado.update(teclas)
        grupo_inimigos.update(pygame.time.get_ticks())
        grupo_projeteis.update(tilemap)

        soldado.verificar_colisao(tilemap)
        for inimigo in grupo_inimigos:
            inimigo.verificar_colisao(tilemap)

        for inimigo in grupo_inimigos:
            if inimigo.esta_morto and not inimigo.xp_entregue:
                soldado.ganhar_xp(inimigo.xp_drop)
                inimigo.xp_entregue = True

        camera.update(soldado)

        janela.fill(FUNDO_BRANCO)
        tilemap.render(janela, camera)

        for inimigo in grupo_inimigos:
            janela.blit(inimigo.image, camera.aplicar(inimigo))
            inimigo.draw_hp_bar(janela, camera)

        for projetil in grupo_projeteis:
            janela.blit(projetil.image, camera.aplicar(projetil))

        janela.blit(soldado.image, camera.aplicar(soldado))
        soldado.draw_hp_bar(janela, camera)
        soldado.draw_hud(janela)

        pygame.display.update()

    return estado
