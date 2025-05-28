#game_manager.py
import pygame
from config import JOGANDO, GAME_OVER, CARREGANDO, FPS, FUNDO_BRANCO
from sprites import Soldado
from camera import Camera
from tilemap import TileMap
from inimigos_codigos.orc_normal import OrcNormal
from inimigos_codigos.esqueleto import Esqueleto
from inimigos_codigos.boss1.base_boss1 import BossBase

class GameManager:
    def __init__(self, janela, animacoes):
        self.janela = janela
        self.animacoes = animacoes
        self.estado = CARREGANDO
        self.level_atual = 1
        self.clock = pygame.time.Clock()
        
        self.tilemap = None
        self.grupo_inimigos = None
        self.grupo_projeteis = None
        self.soldado = None
        self.camera = None
        self.boss_derrotado = False
        self.novas_telas_executadas = False


    def executar(self):
        if self.estado == CARREGANDO:
            if not self.carregar_level():
                return GAME_OVER
            self.estado = JOGANDO
        elif self.boss_derrotado and not self.novas_telas_executadas:
            return self.iniciar_sequencia_telas()
        
        return self.loop_jogo()

    def iniciar_sequencia_telas(self):
        return "fase_concluida1"

    def carregar_level(self):
        try:
        # Carrega o mapa dinamicamente
            mapa_path = f'Mapas/Mapa{self.level_atual}/mapa{self.level_atual}.tmx'
            self.tilemap = TileMap(mapa_path, zoom=3)
        
        # Inicializa grupos e jogador
            self.grupo_inimigos = pygame.sprite.Group()
            self.grupo_projeteis = pygame.sprite.Group()
        
            self.soldado = Soldado(
                self.animacoes['soldado'],
                self.grupo_inimigos,
                self.grupo_projeteis,
                self.tilemap
            )

        # Configuração da câmera
            largura_janela, altura_janela = self.janela.get_size()
            self.camera = Camera(largura_janela, altura_janela)
            self.camera.configurar_limites(*self.tilemap.map_size)
        
        # Processa os spawn points
            self.processar_spawns()
            return True

        except FileNotFoundError:
            print(f"ERRO: Mapa {self.level_atual} não encontrado!")
            return False
        except KeyError as e:
            print(f"ERRO: Animação não encontrada - {str(e)}")
            return False
        except Exception as e:
            print(f"ERRO CRÍTICO: {str(e)}")
            return False


    def processar_spawns(self):
        """Processa os pontos de spawn do tilemap"""
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

    def loop_jogo(self):
        while self.estado == JOGANDO:
            self.clock.tick(FPS)
        
            if self.processar_eventos() == False:  # Exemplo: retorna False se QUIT
                return GAME_OVER
            
            self.atualizar_entidades()
            self.verificar_colisoes()
            self.atualizar_camera()
            self.desenhar()
    
        return self.estado

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.estado = GAME_OVER
                return False
        return True  # ← Padrão para continuar execução

    def atualizar_entidades(self):

        teclas = pygame.key.get_pressed()
        self.soldado.update(teclas)
        self.soldado.verificar_colisao()
    
    # Segundo: verificar colisões
        self.soldado.verificar_colisao()  # Adicionar esta linha
    
    # Terceiro: atualizar outras entidades
        self.grupo_inimigos.update(pygame.time.get_ticks())
        self.grupo_projeteis.update(self.tilemap)

    def verificar_colisoes(self):
        boss_vivo = False
        for inimigo in self.grupo_inimigos:
            inimigo.verificar_colisao(self.tilemap)
            if inimigo.esta_morto and not inimigo.xp_entregue:
                self.soldado.ganhar_xp(inimigo.xp_drop)
                inimigo.xp_entregue = True
                if isinstance(inimigo, BossBase):
                    self.boss_derrotado = True
            if isinstance(inimigo, BossBase) and not inimigo.esta_morto:
                boss_vivo = True
        
        if not boss_vivo and not self.novas_telas_executadas:
            self.iniciar_transicao_fase()

    def atualizar_camera(self):
        self.camera.update(self.soldado)

    def desenhar(self):
        self.janela.fill(FUNDO_BRANCO)
        self.tilemap.render(self.janela, self.camera)
        
        # Desenhar entidades
        for entidade in [*self.grupo_inimigos, *self.grupo_projeteis, self.soldado]:
            self.janela.blit(entidade.image, self.camera.aplicar(entidade))
            if hasattr(entidade, 'draw_hp_bar'):
                entidade.draw_hp_bar(self.janela, self.camera)
        
        self.soldado.draw_hud(self.janela)
        pygame.display.update()

    def iniciar_transicao_fase(self):
        self.novas_telas_executadas = True
        self.level_atual += 1  # Avança para próxima fase
        if self.level_atual > 2:
            self.estado = GAME_OVER
        else:
            self.estado = CARREGANDO

    def carregar_proxima_fase(self):
        self.level_atual += 1
        if self.level_atual > 2:  # Ajuste conforme o número de fases
            self.estado = GAME_OVER
            return
        self.carregar_level()
