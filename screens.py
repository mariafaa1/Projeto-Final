import pygame
from assets import carregar_animacoes
from config import LARGURA, ALTURA, FUNDO_BRANCO, JOGANDO, GAME_OVER
# Adicione no início do arquivo screens.py
import sys


def tratar_eventos(self, eventos):
    for evento in eventos:
        if evento.type == pygame.QUIT:
            self.proxima_tela = "sair"
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.proxima_tela = "menu"

class TelaBase:
    def __init__(self, janela):
        self.janela = janela
        self.proxima_tela = None

    def tratar_eventos(self, eventos):
        pass  # Implementação base vazia

    def atualizar(self):
        pass  # Implementação base vazia

    def desenhar(self):
        pass  # Implementação base vazia

class MenuInicial(TelaBase):
    def __init__(self, janela):
        super().__init__(janela)
        try:
            self.imagem = pygame.image.load("assets/tela0.png").convert()
            self.imagem = pygame.transform.scale(self.imagem, (LARGURA, ALTURA))
        except Exception as e:
            print(f"Erro ao carregar tela inicial: {e}")
            sys.exit()

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.proxima_tela = "historia1"

    def desenhar(self):
        self.janela.blit(self.imagem, (0, 0))
        pygame.display.flip()

class TelaCarregamento(TelaBase):
    def __init__(self, janela):
        super().__init__(janela)
        self.fonte = pygame.font.Font(None, 36)
        self.progresso = 0
        self.total_itens = 3
        self.animacoes = None
        self.carregado = False

    def atualizar(self):
        if not self.carregado:
            self.carregar_recursos()
            self.carregado = True
            self.proxima_tela = "jogo"

    def carregar_recursos(self):
        try:
            # Estágio 1: Carregar animações básicas
            self.texto_status = "Carregando personagem..."
            self.progresso = 1
            self.desenhar()
            pygame.display.update()
            
            # Estágio 2: Inimigos
            self.texto_status = "Carregando inimigos..."
            self.progresso = 2
            self.desenhar()
            pygame.display.update()
            
            # Estágio 3: Chefões
            self.texto_status = "Carregando chefões..."
            self.progresso = 3
            self.animacoes = carregar_animacoes()  # Carrega tudo
            self.desenhar()
            pygame.display.update()

        except Exception as e:
            print(f"Falha crítica: {e}")
            pygame.quit()
            sys.exit()

    def desenhar(self):
        self.janela.fill((30, 30, 40))
        largura_barra = 400
        x = (LARGURA - largura_barra) // 2
        y = ALTURA // 2
        pygame.draw.rect(self.janela, (50, 50, 60), (x, y, largura_barra, 30))
        progresso_width = int((self.progresso / self.total_itens) * largura_barra)
        pygame.draw.rect(self.janela, (100, 200, 100), (x, y, progresso_width, 30))
        texto = self.fonte.render(self.texto_status, True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(LARGURA//2, y - 40))
        self.janela.blit(texto, texto_rect)

class TelaHistoria(TelaBase):
    def __init__(self, janela, imagem_path, proxima_tela):
        super().__init__(janela)
        self.imagem = pygame.image.load(imagem_path).convert()
        self.imagem = pygame.transform.scale(self.imagem, (LARGURA, ALTURA))
        self.proxima_tela_definida = proxima_tela

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.proxima_tela = self.proxima_tela_definida

    def desenhar(self):
        self.janela.blit(self.imagem, (0, 0))

class TelaControles(TelaBase):
    def __init__(self, janela):
        super().__init__(janela)
        try:
            self.imagem = pygame.image.load("assets/comandos.png").convert()
            self.imagem = pygame.transform.scale(self.imagem, (LARGURA, ALTURA))
        except Exception as e:
            print(f"Erro ao carregar tela de controles: {e}")
            sys.exit()

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.proxima_tela = "loading"

    def desenhar(self):
        self.janela.blit(self.imagem, (0, 0))
        pygame.display.flip()

class TelaJogo(TelaBase):
    def __init__(self, janela, animacoes, game_manager_class):
        super().__init__(janela)
        self.game_manager = game_manager_class(janela, animacoes)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.proxima_tela = "sair"

    def atualizar(self):
        estado = self.game_manager.executar()
        if estado == GAME_OVER:
            self.proxima_tela = "menu"

    def desenhar(self):
        pass  # O desenho é feito pelo GameManager

class TelaFaseConcluida(TelaBase):
    def __init__(self, janela, imagem_path, proxima_tela):
        super().__init__(janela)
        try:
            self.imagem = pygame.image.load(imagem_path).convert()
            self.imagem = pygame.transform.scale(self.imagem, (LARGURA, ALTURA))
            self.proxima_tela_definida = proxima_tela
        except Exception as e:
            print(f"Erro ao carregar tela de fase concluída: {e}")
            sys.exit()

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.proxima_tela = self.proxima_tela_definida

    def desenhar(self):
        self.janela.blit(self.imagem, (0, 0))
        pygame.display.flip()