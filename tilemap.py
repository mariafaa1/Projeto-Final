# tilemap.py

import pygame as pg
from pytmx.util_pygame import load_pygame
import pytmx

class TileMap:
    def __init__(self, filename, zoom=3):
        """
        Construtor da classe TileMap.
        Responsável por carregar o mapa .tmx, aplicar o zoom, processar camadas de tiles e objetos,
        gerar a superfície completa do mapa e preparar listas de colisões e spawns.
        """
        self.tmxdata = load_pygame(filename)  # Carrega o arquivo .tmx
        self.collision_rects = []             # Lista para armazenar os retângulos de colisão
        self.spawn_points = {}                # Dicionário para armazenar pontos de spawn
        self.zoom = zoom                      # Fator de zoom do mapa

        # Define a largura e altura de cada tile após o zoom
        tile_width = int(self.tmxdata.tilewidth * self.zoom)
        tile_height = int(self.tmxdata.tileheight * self.zoom)

        # Cria uma superfície do tamanho total do mapa (já com o zoom aplicado)
        self.surface_completa = pg.Surface(
            (self.tmxdata.width * tile_width,
             self.tmxdata.height * tile_height)
        ).convert_alpha()

        # Torna a superfície completamente transparente
        self.surface_completa.fill((0, 0, 0, 0))

        # Processa cada camada do mapa (tiles e objetos)
        for layer in self.tmxdata.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # Renderiza os tiles visuais da camada
                self.render_tile_layer(layer, tile_width, tile_height)
            elif isinstance(layer, pytmx.TiledObjectGroup):
                # Se for camada de colisão, processa como área de bloqueio
                if layer.name.lower() == "colisão":
                    self.process_collision_objects(layer)
                else:
                    # Caso contrário, processa como objetos de spawn ou colisões personalizadas
                    self.process_object_layer(layer)

    def process_collision_objects(self, layer):
        """
        Processa uma camada do tipo 'colisão', convertendo cada objeto em retângulos de colisão.
        Armazena esses retângulos em uma lista para serem usados na física do jogo.
        """
        for obj in layer:
            collision_rect = pg.Rect(
                obj.x * self.zoom,
                obj.y * self.zoom,
                obj.width * self.zoom,
                obj.height * self.zoom
            )
            self.collision_rects.append(collision_rect)
            print(f"Colisão carregada: {collision_rect}")

    def render_tile_layer(self, layer, tile_width, tile_height):
        """
        Renderiza visualmente uma camada de tiles.
        Cada tile é redimensionado com o zoom e desenhado na superfície completa do mapa.
        """
        for x, y, tile in layer.tiles():
            if tile:
                # Redimensiona o tile com base no zoom
                scaled_tile = pg.transform.smoothscale(tile, (tile_width, tile_height))

                # Desenha o tile na posição correspondente na superfície
                self.surface_completa.blit(
                    scaled_tile,
                    (x * tile_width, y * tile_height)
                )
        print(f"Processado layer: {layer.name}")

    def process_object_layer(self, layer):
        """
        Processa uma camada de objetos do mapa.
        Detecta pontos de spawn (type=SpawnPoint) e colisões (type=Collision) definidas manualmente.
        """
        for obj in layer:
            if obj.type == "SpawnPoint":
                # Adiciona ponto de spawn identificado pelo nome do objeto
                self.spawn_points[obj.name] = pg.Rect(
                    obj.x * self.zoom,
                    obj.y * self.zoom,
                    obj.width * self.zoom,
                    obj.height * self.zoom
                )
                print(f"Registrado spawn point: {obj.name} em ({obj.x}, {obj.y})")

            elif obj.type == "Collision":
                # Adiciona retângulo de colisão (caso tenha sido definido fora da camada "colisão")
                self.collision_rects.append(pg.Rect(
                    obj.x * self.zoom,
                    obj.y * self.zoom,
                    obj.width * self.zoom,
                    obj.height * self.zoom
                ))
                print(f"Registrada colisão em ({obj.x}, {obj.y}, {obj.width}, {obj.height})")

    @property
    def map_size(self):
        """
        Propriedade que retorna o tamanho total do mapa em pixels, considerando o zoom.
        Utilizado para limitar a câmera ou definir limites de movimentação.
        """
        return (
            self.tmxdata.width * self.tmxdata.tilewidth * self.zoom,
            self.tmxdata.height * self.tmxdata.tileheight * self.zoom
        )

    def render(self, surface, camera):
        """
        Renderiza a superfície completa do mapa na tela principal, aplicando o deslocamento da câmera.
        Garante que apenas a parte visível do mapa seja exibida na janela.
        """
        surface.blit(self.surface_completa, (-int(camera.offset.x), -int(camera.offset.y)))
