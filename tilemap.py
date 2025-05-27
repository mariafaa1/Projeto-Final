#tilemap.py
import pygame as pg
from pytmx.util_pygame import load_pygame
import pytmx

import pygame as pg
from pytmx.util_pygame import load_pygame
import pytmx

class TileMap:
    def __init__(self, filename, zoom=3):
        self.tmxdata = load_pygame(filename)
        self.collision_rects = []
        self.spawn_points = {}
        self.zoom = zoom

        tile_width = int(self.tmxdata.tilewidth * self.zoom)
        tile_height = int(self.tmxdata.tileheight * self.zoom)

        self.surface_completa = pg.Surface(
            (self.tmxdata.width * tile_width,
             self.tmxdata.height * tile_height)
        ).convert_alpha()
        self.surface_completa.fill((0, 0, 0, 0))

        for layer in self.tmxdata.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.render_tile_layer(layer, tile_width, tile_height)
            elif isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name.lower() == "colisão":
                    self.process_collision_objects(layer)
                else:
                    self.process_object_layer(layer)

    def process_collision_objects(self, layer):
        """Processa objetos de colisão da camada 'colisão'"""
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
        for x, y, tile in layer.tiles():
            if tile:
                scaled_tile = pg.transform.smoothscale(tile, (tile_width, tile_height))
                self.surface_completa.blit(
                    scaled_tile,
                    (x * tile_width, y * tile_height)
                )
        print(f"Processado layer: {layer.name}")

    def process_object_layer(self, layer):
        for obj in layer:
            if obj.type == "SpawnPoint":
                self.spawn_points[obj.name] = pg.Rect(
                    obj.x * self.zoom,
                    obj.y * self.zoom,
                    obj.width * self.zoom,
                    obj.height * self.zoom
                )
                print(f"Registrado spawn point: {obj.name} em ({obj.x}, {obj.y})")
            elif obj.type == "Collision":
                self.collision_rects.append(pg.Rect(
                    obj.x * self.zoom,
                    obj.y * self.zoom,
                    obj.width * self.zoom,
                    obj.height * self.zoom
                ))
                print(f"Registrada colisão em ({obj.x}, {obj.y}, {obj.width}, {obj.height})")

    @property
    def map_size(self):
        return (
            self.tmxdata.width * self.tmxdata.tilewidth * self.zoom,
            self.tmxdata.height * self.tmxdata.tileheight * self.zoom
        )

    def render(self, surface, camera):
        surface.blit(self.surface_completa, (-int(camera.offset.x), -int(camera.offset.y)))