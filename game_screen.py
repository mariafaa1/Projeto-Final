# game_screen.py

import pygame
from config import FPS, FUNDO_BRANCO, JOGANDO, GAME_OVER
from sprites import Soldado
from inimigos_codigos.orc_normal import OrcNormal
from inimigos_codigos.esqueleto import Esqueleto
from inimigos_codigos.boss1.base_boss1 import BossBase
from inimigos_codigos.Inimigos_mapa2.orc_armadura import OrcArmadura
from inimigos_codigos.Inimigos_mapa2.esqueleto_arqueiro import EsqueletoArqueiro
from inimigos_codigos.Inimigos_mapa2.boss2 import Boss2  # Novo boss importado
from camera import Camera
from tilemap import TileMap
import pygame as pg

# ----------------------------------------
# Função de tratamento de eventos do jogo
# ----------------------------------------
def processar_eventos(self):
    """
    Trata os eventos do jogo, como fechar a janela ou pressionar ESC.
    Pode futuramente incluir pausa (PAUSADO).
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.estado = PAUSADO  # Placeholder para lógica de pausa
    return True

# ----------------------------------------
# Loop principal de execução do jogo
# ----------------------------------------
def loop_jogo(self):
    """
    Executa o loop principal do jogo, mantendo o jogo ativo enquanto o estado for JOGANDO.
    """
    try:
        while self.estado == JOGANDO:
            self.clock.tick(FPS)  # Controla o FPS

            if not self.processar_eventos():
                return GAME_OVER

            self.atualizar_entidades()      # Atualiza todos os objetos
            self.verificar_colisoes()       # Checa colisões
            self.atualizar_camera()         # Atualiza posição da câmera
            self.desenhar()                 # Renderiza a tela

    except KeyboardInterrupt:
        print("Jogo interrompido pelo usuário")
        return GAME_OVER

    return self.estado  # Retorna o estado final (GAME_OVER ou outro)

# ----------------------------------------
# Função principal de execução da fase
# ----------------------------------------
def tela_jogo(janela, animacoes_soldado, tilemap):
    """
    Executa o jogo dentro da tela recebida, carregando o mapa e todos os elementos necessários.
    """
    clock = pygame.time.Clock()
    estado = JOGANDO

    # Carrega o mapa com zoom definido
    tilemap = TileMap('Mapas/Mapa1/mapa1.tmx', zoom=3)
    largura_janela, altura_janela = janela.get_size()

    # Grupos de entidades do jogo
    grupo_inimigos = pygame.sprite.Group()
    grupo_projeteis = pygame.sprite.Group()

    # Cria o jogador
    soldado = Soldado(animacoes_soldado, grupo_inimigos, grupo_projeteis, tilemap)

    # Configura a câmera
    camera = Camera(largura_janela, altura_janela)
    mapa_largura, mapa_altura = tilemap.map_size
    camera.configurar_limites(mapa_largura, mapa_altura)

    # Loop principal do jogo
    while estado == JOGANDO:
        dt = clock.tick(FPS) / 1000  # Calcula o delta time em segundos

        # Eventos do pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado = GAME_OVER

        teclas = pygame.key.get_pressed()

        # Atualizações
        soldado.update(teclas, dt)
        grupo_inimigos.update(pygame.time.get_ticks())  # Inimigos usam tempo como parâmetro
        grupo_projeteis.update(tilemap)  # Projéteis usam o tilemap para colisões
        soldado.verificar_colisao()  # Verifica colisão com o mapa

        # Verifica colisões dos inimigos com o mapa
        for inimigo in grupo_inimigos:
            inimigo.verificar_colisao(tilemap)

        # Verifica se inimigos morreram e entrega XP
        for inimigo in grupo_inimigos:
            if inimigo.esta_morto and not inimigo.xp_entregue:
                soldado.ganhar_xp(inimigo.xp_drop)
                inimigo.xp_entregue = True

        # Atualiza a câmera com base na posição do soldado
        camera.update(soldado)

        # Desenho da tela
        janela.fill(FUNDO_BRANCO)
        tilemap.render(janela, camera)

        # Desenha inimigos e suas barras de vida
        for inimigo in grupo_inimigos:
            janela.blit(inimigo.image, camera.aplicar(inimigo))
            inimigo.draw_hp_bar(janela, camera)

        # Desenha projéteis na tela
        for projetil in grupo_projeteis:
            janela.blit(projetil.image, camera.aplicar(projetil))

        # Desenha o jogador e HUD
        janela.blit(soldado.image, camera.aplicar(soldado))
        soldado.draw_hp_bar(janela, camera)
        soldado.draw_hud(janela)

        # Atualiza a tela com tudo desenhado
        pygame.display.update()

    return estado  # Retorna o estado final da fase (ex: GAME_OVER)
