# camera.py
import pygame as pg

# Classe que representa a câmera do jogo, que acompanha o jogador
class Camera:
    def __init__(self, largura_jogo, altura_jogo):
        """
        Inicializa a câmera com o tamanho da janela do jogo.
        - largura_jogo e altura_jogo: dimensões da tela visível.
        - offset: deslocamento da câmera no mapa.
        - limites: área máxima em que a câmera pode se mover (tamanho do mapa).
        """
        self.offset = pg.Vector2(0, 0)  # Deslocamento da câmera
        self.limites = None  # Limites do mapa (serão definidos depois)
        self.largura_jogo = largura_jogo  # Largura visível da tela
        self.altura_jogo = altura_jogo    # Altura visível da tela

    def configurar_limites(self, mapa_width, mapa_height):
        """
        Define os limites da câmera com base no tamanho do mapa.
        Isso impede a câmera de mostrar áreas fora do mapa.
        """
        self.limites = pg.Rect(
            0, 
            0, 
            mapa_width - self.largura_jogo, 
            mapa_height - self.altura_jogo
        )

    def aplicar(self, entidade):
        """
        Aplica o deslocamento da câmera ao retângulo da entidade.
        Isso faz a entidade aparecer na posição correta na tela.
        """
        return entidade.rect.move(-int(self.offset.x), -int(self.offset.y))

    def aplicar_rect(self, rect):
        """
        Aplica o deslocamento da câmera a um retângulo genérico.
        Útil para elementos que não são sprites.
        """
        return rect.move(-int(self.offset.x), -int(self.offset.y))

    def update(self, alvo):
        """
        Atualiza a posição da câmera com base na posição do alvo (normalmente o jogador).
        Centraliza o alvo na tela e limita a câmera ao mapa.
        """
        # Centraliza o alvo na tela
        x = alvo.rect.centerx - self.largura_jogo // 2
        y = alvo.rect.centery - self.altura_jogo // 2

        # Garante que a câmera não ultrapasse os limites do mapa
        if self.limites:
            x = max(self.limites.left, min(x, self.limites.right))
            y = max(self.limites.top, min(y, self.limites.bottom))

        # Move suavemente a câmera em direção ao novo deslocamento (efeito de suavização)
        self.offset += (pg.Vector2(x, y) - self.offset) * 0.1
