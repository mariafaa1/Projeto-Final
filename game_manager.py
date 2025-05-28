# game_manager.py

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
from inimigos_codigos.Inimigos_mapa2.boss2 import Boss2  # Novo boss da fase 2

# Classe principal que gerencia o estado do jogo por fase
class GameManager:
    def __init__(self, janela, animacoes, level_atual=1):
        # Inicializa atributos e estado inicial
        self.janela = janela
        self.animacoes = animacoes
        self.estado = CARREGANDO
        self.level_atual = level_atual
        self.nivel_inicial = 1
        self.clock = pygame.time.Clock()

        # Componentes principais da fase
        self.tilemap = None
        self.grupo_inimigos = None
        self.grupo_projeteis = None
        self.soldado = None
        self.camera = None

        # Controle de progresso e transição
        self.boss_derrotado = False
        self.novas_telas_executadas = False
        self.level_ao_morrer = self.level_atual

    def executar(self):
        """
        Executa o estado atual do jogo, controlando transições e mortes.
        """
        # Se o jogador morreu, direciona imediatamente para o menu pós-jogo
        if self.soldado and self.soldado.esta_morto:
            if self.soldado.animacao_morte_concluida:
                self.level_ao_morrer = self.level_atual
                return "menu_pos_jogo"

        # Carregamento inicial da fase
        if self.estado == CARREGANDO:
            if not self.carregar_level():
                return GAME_OVER
            self.estado = JOGANDO

        # Executa o loop da fase
        estado_jogo = self.loop_jogo()

        if estado_jogo == GAME_OVER or (self.soldado and self.soldado.esta_morto):
            return "menu_pos_jogo"

        return estado_jogo

    def iniciar_sequencia_telas(self):
        """
        Retorna qual tela deve ser exibida após conclusão de fase.
        """
        if self.level_atual == 1:
            return "fase_concluida1"
        elif self.level_atual == 2:
            return "tela1"
        else:
            return "menu"

    def carregar_level(self):
        """
        Carrega o mapa, soldado, câmera e inimigos da fase atual.
        """
        try:
            mapa_path = f'Mapas/Mapa{self.level_atual}/mapa{self.level_atual}.tmx'
            print(f"[DEBUG] Carregando mapa: {mapa_path}")
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
        """
        Lê os objetos definidos no mapa (.tmx) e instancia os elementos no jogo.
        """
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
                OrcNormal(obj.x * self.tilemap.zoom, obj.y * self.tilemap.zoom,
                          self.soldado, self.grupo_inimigos).add(self.grupo_inimigos)

            elif obj.name == 'spawn_esqueleto':
                Esqueleto(obj.x * self.tilemap.zoom, obj.y * self.tilemap.zoom,
                          self.soldado, self.grupo_inimigos).add(self.grupo_inimigos)

            elif obj.name == 'spawn_boss':
                BossBase(obj.x * self.tilemap.zoom, obj.y * self.tilemap.zoom,
                         self.soldado, self.grupo_inimigos).add(self.grupo_inimigos)

            elif obj.name == 'spawn_orc_armadura':
                OrcArmadura(obj.x * self.tilemap.zoom, obj.y * self.tilemap.zoom,
                            self.soldado, self.grupo_inimigos).add(self.grupo_inimigos)

            elif obj.name == 'spawn_esqueleto_arqueiro':
                EsqueletoArqueiro(obj.x * self.tilemap.zoom, obj.y * self.tilemap.zoom,
                                  self.soldado, self.grupo_projeteis, self.grupo_inimigos).add(self.grupo_inimigos)

            elif obj.name == 'spawn_boss2':
                Boss2(obj.x * self.tilemap.zoom, obj.y * self.tilemap.zoom,
                      self.soldado, self.grupo_inimigos).add(self.grupo_inimigos)

    def loop_jogo(self):
        """
        Loop principal de execução da fase.
        """
        while self.estado == JOGANDO:
            dt = self.clock.tick(FPS) / 1000

            if not self.processar_eventos():
                return GAME_OVER

            self.atualizar_entidades(dt)

            if self.soldado and self.soldado.esta_morto:
                return "menu_pos_jogo"

            estado_colisao = self.verificar_colisoes()
            if estado_colisao:
                return estado_colisao

            self.atualizar_camera()
            self.desenhar()

        return self.estado

    def processar_eventos(self):
        """
        Trata eventos como fechar a janela.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.estado = GAME_OVER
                return False
        return True

    def atualizar_entidades(self, dt):
        """
        Atualiza jogador, inimigos e projéteis com base no tempo.
        """
        teclas = pygame.key.get_pressed()
        if self.soldado:
            self.soldado.update(teclas, dt)
            self.soldado.verificar_colisao()

        self.grupo_inimigos.update(pygame.time.get_ticks())
        self.grupo_projeteis.update(self.tilemap)

        for inimigo in self.grupo_inimigos:
            if inimigo.esta_morto and not inimigo.xp_entregue:
                self.soldado.ganhar_xp(inimigo.xp_drop)
                inimigo.xp_entregue = True

    def verificar_colisoes(self):
        """
        Verifica se todos os bosses da fase foram derrotados e define transição.
        """
        boss_vivo = False
        for inimigo in self.grupo_inimigos:
            if isinstance(inimigo, (BossBase, Boss2)):
                if not inimigo.esta_morto:
                    boss_vivo = True
                    print(f"[DEBUG] Boss vivo: {inimigo}")
                    break

        if not boss_vivo and not self.novas_telas_executadas:
            print(f"[DEBUG] Todos os Bosses derrotados! Nível: {self.level_atual}")
            if self.level_atual == 1:
                self.novas_telas_executadas = True
                return "fase_concluida1"
            elif self.level_atual == 2:
                self.novas_telas_executadas = True
                return "tela1"

        return None

    def iniciar_transicao_fase(self):
        """
        Controla a transição de uma fase para a próxima.
        """
        if self.level_atual == 1:
            self.novas_telas_executadas = True
            self.level_atual += 1
            self.estado = CARREGANDO
        elif self.level_atual == 2:
            self.boss_derrotado = True
            self.novas_telas_executadas = False

    def atualizar_camera(self):
        """
        Atualiza a posição da câmera baseada na posição do soldado.
        """
        if self.camera and self.soldado:
            self.camera.update(self.soldado)

    def desenhar(self):
        """
        Renderiza todos os elementos do jogo na tela.
        """
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
