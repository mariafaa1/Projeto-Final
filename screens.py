#screens.py
import pygame
from assets import carregar_animacoes
from config import LARGURA, ALTURA, FUNDO_BRANCO, JOGANDO, GAME_OVER
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

class TelaCarregamento:
    def __init__(self, janela):
        self.janela = janela
        self.fonte = pygame.font.Font(None, 36)
        self.progresso = 0
        self.total_itens = 3
        self.animacoes = None
        self.carregado = False
        self.proxima_tela = None
        self.texto_status = ""

    def atualizar(self):
        if not self.carregado:
            self.carregar_recursos()
            self.carregado = True
            self.proxima_tela = "jogo"  # Mantém a transição para o jogo

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
            self.animacoes = carregar_animacoes()
            self.desenhar()
            pygame.display.update()

        except Exception as e:
            print(f"Falha crítica no carregamento: {e}")
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
        texto_rect = texto.get_rect(center=(LARGURA // 2, y - 40))
        self.janela.blit(texto, texto_rect)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.proxima_tela = "sair"

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
        pygame.display.flip()

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
    def __init__(self, janela, animacoes, game_manager_class, level_atual=1):
        super().__init__(janela)
        # Agora GameManager recebe o level_atual corretamente
        self.game_manager = game_manager_class(janela, animacoes, level_atual)
        self.proxima_tela = None

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.proxima_tela = "sair"

    def atualizar(self):
        estado = self.game_manager.executar()
        if estado == "menu_pos_jogo":
            self.proxima_tela = "menu_pos_jogo"
        elif estado == "menu":
            self.proxima_tela = "menu"
        elif estado == "fase_concluida1":
            self.proxima_tela = "fase_concluida1"
        elif estado == "tela1":  # Alterado de "tela1_fase2" para "tela1"
            self.proxima_tela = "tela1"
        elif estado == "game_over":
            self.proxima_tela = "menu_pos_jogo"


class TelaMenuPosJogo(TelaBase):
    def __init__(self, janela):
        super().__init__(janela)
        self.fonte_titulo = pygame.font.Font(None, 72)
        self.fonte_botoes = pygame.font.Font(None, 48)
        self.cor_base = (200, 200, 200)
        self.cor_hover = (255, 255, 0)
        self.opcoes = [
            {"texto": "Reiniciar Fase", "acao": "reiniciar_fase"},
            {"texto": "Reiniciar Jogo", "acao": "reiniciar_jogo"},
            {"texto": "Menu Principal", "acao": "menu"},
            {"texto": "Sair", "acao": "sair"}
        ]
        self.botoes = []
        self.inicializar_botoes()

    def inicializar_botoes(self):
        y = ALTURA // 2 - 100
        for opcao in self.opcoes:
            rect = pygame.Rect(
                (LARGURA - 300) // 2,
                y,
                300,
                60
            )
            self.botoes.append({
                "rect": rect,
                "texto": opcao["texto"],
                "acao": opcao["acao"],
                "hover": False
            })
            y += 80

    def tratar_eventos(self, eventos):
        mouse_pos = pygame.mouse.get_pos()
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for botao in self.botoes:
                    if botao["rect"].collidepoint(mouse_pos):
                        self.proxima_tela = botao["acao"]
                        return

    def desenhar(self):
        self.janela.fill((30, 30, 40))
        
        # Título
        titulo = self.fonte_titulo.render("Game Over", True, (255, 0, 0))
        titulo_rect = titulo.get_rect(center=(LARGURA//2, 150))
        self.janela.blit(titulo, titulo_rect)
        
        # Botões
        for botao in self.botoes:
            cor = self.cor_hover if botao["hover"] else self.cor_base
            pygame.draw.rect(self.janela, cor, botao["rect"], border_radius=10)
            texto = self.fonte_botoes.render(botao["texto"], True, (0, 0, 0))
            texto_rect = texto.get_rect(center=botao["rect"].center)
            self.janela.blit(texto, texto_rect)
        
        pygame.display.flip()

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

class TelaGenerica(TelaBase):
    def __init__(self, janela, imagem_path, proxima_tela):
        super().__init__(janela)
        try:
            self.imagem = pygame.image.load(imagem_path).convert()
            self.imagem = pygame.transform.scale(self.imagem, (LARGURA, ALTURA))
            self.proxima_tela_definida = proxima_tela
        except Exception as e:
            print(f"Erro ao carregar tela: {e}")
            sys.exit()

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                print(f"[DEBUG] Tecla ENTER pressionada na tela: {self.proxima_tela_definida}")  # ✅ Adicionado
                self.proxima_tela = self.proxima_tela_definida

    def desenhar(self):
        self.janela.blit(self.imagem, (0, 0))
        pygame.display.flip()
    
