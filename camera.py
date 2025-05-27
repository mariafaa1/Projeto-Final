import pygame as pg

class Camera:
    def __init__(self, largura_jogo, altura_jogo):
        self.offset = pg.Vector2(0, 0)
        self.limites = None
        self.largura_jogo = largura_jogo
        self.altura_jogo = altura_jogo

    def configurar_limites(self, mapa_width, mapa_height):
        self.limites = pg.Rect(0, 0, mapa_width - self.largura_jogo, mapa_height - self.altura_jogo)

    def aplicar(self, entidade):
        return entidade.rect.move(-int(self.offset.x), -int(self.offset.y))  # ✅ Arredondado!

    def aplicar_rect(self, rect):
        return rect.move(-int(self.offset.x), -int(self.offset.y))  # ✅ Arredondado!

    def update(self, alvo):
        x = alvo.rect.centerx - self.largura_jogo // 2
        y = alvo.rect.centery - self.altura_jogo // 2

        if self.limites:
            x = max(self.limites.left, min(x, self.limites.right))
            y = max(self.limites.top, min(y, self.limites.bottom))

        self.offset += (pg.Vector2(x, y) - self.offset) * 0.1
