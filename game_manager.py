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

    def executar(self):
        if self.estado == CARREGANDO:
            if not self.carregar_level():  # Agora retorna sucesso/falha
                return GAME_OVER
            self.estado = JOGANDO
    
        return self.loop_jogo()

    def carregar_level(self):
        try:
            self.tilemap = TileMap(f'Mapas/Mapa{self.level_atual}/mapa{self.level_atual}.tmx', zoom=3)
            self.grupo_inimigos = pygame.sprite.Group()
            self.grupo_projeteis = pygame.sprite.Group()
        
            self.soldado = Soldado(
                self.animacoes['soldado'],
                self.grupo_inimigos,
                self.grupo_projeteis
            )

            largura_janela, altura_janela = self.janela.get_size()
            self.camera = Camera(largura_janela, altura_janela)
            self.camera.configurar_limites(*self.tilemap.map_size)
        
            self.processar_spawns()
            return True  # ← Sucesso

        except FileNotFoundError:
            print("ERRO: Arquivo do mapa não encontrado!")
            return False
        except Exception as e:
            print(f"ERRO: {str(e)}")
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
        self.grupo_inimigos.update(pygame.time.get_ticks())
        self.grupo_projeteis.update(self.tilemap)

    def verificar_colisoes(self):
        self.soldado.verificar_colisao(self.tilemap)
        for inimigo in self.grupo_inimigos:
            inimigo.verificar_colisao(self.tilemap)
            if inimigo.esta_morto and not inimigo.xp_entregue:
                self.soldado.ganhar_xp(inimigo.xp_drop)
                inimigo.xp_entregue = True

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