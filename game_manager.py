import pygame
from config import JOGANDO, GAME_OVER, CARREGANDO, FPS, FUNDO_BRANCO
from sprites import Soldado
from camera import Camera
from tilemap import TileMap
from inimigos_codigos.orc_normal import OrcNormal
from inimigos_codigos.esqueleto import Esqueleto
from inimigos_codigos.boss1.base_boss1 import BossBase
from inimigos_codigos.Inimigos_mapa2.orc_armadura import OrcArmadura
from inimigos_codigos.Inimigos_mapa2.esqueleto_arqueiro import EsqueletoArqueiro
from inimigos_codigos.Inimigos_mapa2.boss2 import Boss2

class GameManager:
    def __init__(self, janela, animacoes, level_atual=1):
        self.janela = janela
        self.animacoes = animacoes
        self.estado = CARREGANDO
        self.level_atual = level_atual
        self.nivel_inicial = 1
        self.clock = pygame.time.Clock()

        self.tilemap = None
        self.grupo_inimigos = None
        self.grupo_projeteis = None
        self.soldado = None
        self.camera = None
        self.boss_derrotado = False
        self.novas_telas_executadas = False
        self.level_ao_morrer = self.level_atual

    def executar(self):
        if self.soldado and self.soldado.esta_morto:
            self.level_ao_morrer = self.level_atual
            return "menu_pos_jogo"

        if self.estado == CARREGANDO:
            if not self.carregar_level():
                return GAME_OVER
            self.estado = JOGANDO

        if self.boss_derrotado and not self.novas_telas_executadas:
            return self.iniciar_sequencia_telas()

        estado_jogo = self.loop_jogo()

        if estado_jogo == GAME_OVER:
            return "menu_pos_jogo"

        return estado_jogo

    def iniciar_sequencia_telas(self):
        if self.level_atual == 1:
            return "fase_concluida1"
        elif self.level_atual == 2:
            return "tela1_fase2"
        else:
            return "menu"

    def carregar_level(self):
        try:
            mapa_path = f'Mapas/Mapa{self.level_atual}/mapa{self.level_atual}.tmx'
            self.tilemap = TileMap(mapa_path, zoom=3)

            self.grupo_inimigos = pygame.sprite.Group()
            self.grupo_projeteis = pygame.sprite.Group()

            self.soldado = Soldado(
                self.animacoes['soldado'],
                self.grupo_inimigos,
                self.grupo_projeteis,
                self.tilemap
            )

            largura_janela, altura_janela = self.janela.get_size()
            self.camera = Camera(largura_janela, altura_janela)
            self.camera.configurar_limites(*self.tilemap.map_size)

            self.processar_spawns()
            return True

        except Exception as e:
            print(f"ERRO AO CARREGAR LEVEL: {str(e)}")
            return False

    def processar_spawns(self):
        for obj in self.tilemap.tmxdata.objects:
            if obj.name == 'spawn_soldado':
                spawn_rect = pygame.Rect(
                    obj.x * self.tilemap.zoom,
                    obj.y * self.tilemap.zoom,
                    obj.width * self.tilemap.zoom,
                    obj.height * self.tilemap.zoom
                )
                self.soldado.rect.center = spawn_rect.center
                self.soldado.hitbox_rect.center = spawn_rect.center
            elif obj.name == 'spawn_orc':
                OrcNormal(
                    obj.x * self.tilemap.zoom,
                    obj.y * self.tilemap.zoom,
                    self.soldado,
                    self.grupo_inimigos
                ).add(self.grupo_inimigos)
            elif obj.name == 'spawn_esqueleto':
                Esqueleto(
                    obj.x * self.tilemap.zoom,
                    obj.y * self.tilemap.zoom,
                    self.soldado,
                    self.grupo_inimigos
                ).add(self.grupo_inimigos)
            elif obj.name == 'spawn_boss':
                BossBase(
                    obj.x * self.tilemap.zoom,
                    obj.y * self.tilemap.zoom,
                    self.soldado,
                    self.grupo_inimigos
                ).add(self.grupo_inimigos)
            elif obj.name == 'spawn_orc_armadura':
                OrcArmadura(
                    obj.x * self.tilemap.zoom,
                    obj.y * self.tilemap.zoom,
                    self.soldado,
                    self.grupo_inimigos
                ).add(self.grupo_inimigos)
            elif obj.name == 'spawn_esqueleto_arqueiro':
                EsqueletoArqueiro(
                    obj.x * self.tilemap.zoom,
                    obj.y * self.tilemap.zoom,
                    self.soldado,
                    self.grupo_projeteis,
                    self.grupo_inimigos
                ).add(self.grupo_inimigos)
            elif obj.name == 'spawn_boss2':
                Boss2(
                    obj.x * self.tilemap.zoom,
                    obj.y * self.tilemap.zoom,
                    self.soldado,
                    self.grupo_inimigos
                ).add(self.grupo_inimigos)

    def loop_jogo(self):
        while self.estado == JOGANDO:
            dt = self.clock.tick(FPS) / 1000

            if not self.processar_eventos():
                return GAME_OVER

            self.atualizar_entidades(dt)
            self.verificar_colisoes()
            self.atualizar_camera()
            self.desenhar()

        return self.estado

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.estado = GAME_OVER
                return False
        return True

    def atualizar_entidades(self, dt):
        teclas = pygame.key.get_pressed()
        if self.soldado:
            self.soldado.update(teclas, dt)
            self.soldado.verificar_colisao()

        self.grupo_inimigos.update(pygame.time.get_ticks())
        self.grupo_projeteis.update(self.tilemap)

    def verificar_colisoes(self):
        boss_vivo = False
        for inimigo in self.grupo_inimigos:
            inimigo.verificar_colisao(self.tilemap)
            if inimigo.esta_morto and not inimigo.xp_entregue:
                if self.soldado:
                    self.soldado.ganhar_xp(inimigo.xp_drop)
                inimigo.xp_entregue = True
            if isinstance(inimigo, (BossBase, Boss2)) and not inimigo.esta_morto:
                boss_vivo = True

        if not boss_vivo and not self.novas_telas_executadas:
            self.iniciar_transicao_fase()

        if self.soldado and self.soldado.hp_atual <= 0:
            self.estado = GAME_OVER

    def iniciar_transicao_fase(self):
        self.novas_telas_executadas = True
        if self.level_atual < 2:
            self.level_atual += 1
            self.estado = CARREGANDO
        else:
            self.estado = GAME_OVER

    def atualizar_camera(self):
        if self.camera and self.soldado:
            self.camera.update(self.soldado)

    def desenhar(self):
        self.janela.fill(FUNDO_BRANCO)
        self.tilemap.render(self.janela, self.camera)

        for entidade in [*self.grupo_inimigos, *self.grupo_projeteis]:
            self.janela.blit(entidade.image, self.camera.aplicar(entidade))
            if hasattr(entidade, 'draw_hp_bar'):
                entidade.draw_hp_bar(self.janela, self.camera)

        if self.soldado:
            self.janela.blit(self.soldado.image, self.camera.aplicar(self.soldado))
            self.soldado.draw_hp_bar(self.janela, self.camera)
            self.soldado.draw_hud(self.janela)

        pygame.display.update()
