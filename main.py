# main.py
import pygame
import sys
from config import LARGURA, ALTURA
from screens import MenuInicial, TelaCarregamento, TelaJogo, TelaGenerica, TelaControles, TelaHistoria, TelaMenuPosJogo
from game_manager import GameManager

# Estados de reinício
REINICIO_NENHUM = 0
REINICIO_FASE = 1
REINICIO_JOGO = 2

class GerenciadorTelas:
    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Pixel Fantasy")

        self.level_corrente = 1
        self.estado_reinicio = REINICIO_NENHUM  # Controle de reinício

        self.telas = {
            "reiniciar_fase": None,
            "reiniciar_jogo": None,
            "menu": MenuInicial(self.janela),
            "historia1": TelaHistoria(self.janela, "assets/tela1.png", "historia2"),
            "historia2": TelaHistoria(self.janela, "assets/tela2.png", "historia3"),
            "historia3": TelaHistoria(self.janela, "assets/tela3.png", "controles"),
            "controles": TelaControles(self.janela),

            "fase_concluida1": TelaGenerica(self.janela, "assets/fase1_concluida.png", "dialogo1"),
            "dialogo1": TelaGenerica(self.janela, "assets/dialogo1.png", "dialogo2"),
            "dialogo2": TelaGenerica(self.janela, "assets/dialogo2.png", "dialogo3"),
            "dialogo3": TelaGenerica(self.janela, "assets/dialogo3.png", "fase2_1"),
            "fase2_1": TelaGenerica(self.janela, "assets/fase2_1.png", "fase2_2"),
            "fase2_2": TelaGenerica(self.janela, "assets/fase2_2.png", "loading"),

            "menu_pos_jogo": TelaMenuPosJogo(self.janela),
            "reiniciar_fase_confirmado": None,
            "loading": TelaCarregamento(self.janela),
            "jogo": None
        }

        self.tela_atual = "menu"
        self.animacoes = None

    def executar(self):
        while True:
            # Controle centralizado de reinício
            if self.estado_reinicio == REINICIO_FASE:
                self.telas["jogo"] = None
                self.tela_atual = "loading"
                self.estado_reinicio = REINICIO_NENHUM
            elif self.estado_reinicio == REINICIO_JOGO:
                self.level_corrente = 1
                self.telas["jogo"] = None
                self.tela_atual = "loading"
                self.estado_reinicio = REINICIO_NENHUM

            tela = self.telas.get(self.tela_atual)
            if not tela:
                print(f"ERRO: Tela {self.tela_atual} não encontrada!")
                pygame.quit()
                return

            rodando = True
            while rodando:
                eventos = pygame.event.get()
                for evento in eventos:
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        return

                tela.tratar_eventos(eventos)
                tela.atualizar()
                tela.desenhar()
                pygame.display.update()

                if tela.proxima_tela:
                    if self.tela_atual == "loading":
                        self.animacoes = tela.animacoes
                        self.telas["jogo"] = TelaJogo(
                            self.janela,
                            self.animacoes,
                            GameManager,
                            level_atual=self.level_corrente
                        )

                    if self.tela_atual == "jogo":
                        self.level_corrente = self.telas["jogo"].game_manager.level_atual

                    # Tratamento das escolhas no menu_pos_jogo
                    if self.tela_atual == "menu_pos_jogo":
                        if tela.proxima_tela == "reiniciar_fase":
                            self.estado_reinicio = REINICIO_FASE
                        elif tela.proxima_tela == "reiniciar_jogo":
                            self.estado_reinicio = REINICIO_JOGO

                    self.tela_atual = tela.proxima_tela
                    rodando = False

                if isinstance(tela, TelaJogo) and tela.proxima_tela == "menu_pos_jogo":
                    self.tela_atual = "menu_pos_jogo"
                    rodando = False

                if tela.proxima_tela:
                    if tela.proxima_tela == "sair":
                        pygame.quit()
                        sys.exit()
                    if tela.proxima_tela == "reiniciar_jogo":
                        self.animacoes = None
                    self.tela_atual = tela.proxima_tela
                    rodando = False

if __name__ == "__main__":
    try:
        jogo = GerenciadorTelas()
        jogo.executar()
    except KeyboardInterrupt:
        print("\nJogo encerrado pelo usuário")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"ERRO FATAL: {str(e)}")
        pygame.quit()
