#game_screen.py
import pygame
from config import FPS, FUNDO_BRANCO, JOGANDO, GAME_OVER
from sprites import Soldado
from inimigos_codigos.orc_normal import OrcNormal
from inimigos_codigos.esqueleto import Esqueleto
from inimigos_codigos.boss1.base_boss1 import BossBase
from inimigos_codigos.Inimigos_mapa2.orc_armadura import OrcArmadura
from inimigos_codigos.Inimigos_mapa2.esqueleto_arqueiro import EsqueletoArqueiro
from inimigos_codigos.Inimigos_mapa2.boss2 import Boss2
from camera import Camera
from tilemap import TileMap
import pygame as pg


def processar_eventos(self):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.estado = PAUSADO  # Implemente a lógica de pausa se necessário
    return True

def loop_jogo(self):
    try:
        while self.estado == JOGANDO:
            self.clock.tick(FPS)
            
            if not self.processar_eventos():
                return GAME_OVER
            
            self.atualizar_entidades()
            self.verificar_colisoes()
            self.atualizar_camera()
            self.desenhar()
    
    except KeyboardInterrupt:
        print("Jogo interrompido pelo usuário")
        return GAME_OVER
    
    return self.estado



def tela_jogo(janela, animacoes_soldado, tilemap):
    clock = pygame.time.Clock()
    estado = JOGANDO

    tilemap = TileMap('Mapas/Mapa1/mapa1.tmx', zoom=3)
    largura_janela, altura_janela = janela.get_size()

    grupo_inimigos = pygame.sprite.Group()
    grupo_projeteis = pygame.sprite.Group()

    soldado = Soldado(animacoes_soldado, grupo_inimigos, grupo_projeteis, tilemap)

    camera = Camera(largura_janela, altura_janela)
    mapa_largura, mapa_altura = tilemap.map_size
    camera.configurar_limites(mapa_largura, mapa_altura)

    while estado == JOGANDO:
        dt = clock.tick(FPS) / 1000  # Calcula delta time

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado = GAME_OVER

        teclas = pygame.key.get_pressed()
        
        soldado.update(teclas, dt)  # Passando delta time
        grupo_inimigos.update(pygame.time.get_ticks())
        grupo_projeteis.update(tilemap)
        soldado.verificar_colisao()

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
