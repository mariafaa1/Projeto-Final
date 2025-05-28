#main.py
import pygame
import sys
from config import LARGURA, ALTURA
from screens import MenuInicial, TelaCarregamento, TelaJogo, TelaGenerica, TelaControles, TelaHistoria
from game_manager import GameManager

class GerenciadorTelas:
    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Pixel Fantasy")
        
        self.telas = {
            # Telas principais
            "menu": MenuInicial(self.janela),
            "historia1": TelaHistoria(self.janela, "assets/tela1.png", "historia2"),
            "historia2": TelaHistoria(self.janela, "assets/tela2.png", "historia3"),
            "historia3": TelaHistoria(self.janela, "assets/tela3.png", "controles"),
            "controles": TelaControles(self.janela),
            
            # Sequência pós-boss (CORRIGIDO)
            "fase_concluida1": TelaGenerica(self.janela, "assets/fase1_concluida.png", "dialogo1"),
            "dialogo1": TelaGenerica(self.janela, "assets/dialogo1.png", "dialogo2"),
            "dialogo2": TelaGenerica(self.janela, "assets/dialogo2.png", "dialogo3"),
            "dialogo3": TelaGenerica(self.janela, "assets/dialogo3.png", "fase2_1"),
            "fase2_1": TelaGenerica(self.janela, "assets/fase2_1.png", "fase2_2"),
            "fase2_2": TelaGenerica(self.janela, "assets/fase2_2.png", "loading"),
            
            # Telas de sistema
            "loading": None,
            "jogo": None
        }
        self.tela_atual = "menu"
        self.animacoes = None

    def executar(self):
        while True:
            if self.tela_atual == "loading" and self.telas["loading"] is None:
                self.telas["loading"] = TelaCarregamento(self.janela)
            elif self.tela_atual == "jogo" and self.telas["jogo"] is None:
                self.telas["jogo"] = TelaJogo(self.janela, self.animacoes, GameManager)

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
                    self.tela_atual = tela.proxima_tela
                    rodando = False
                if isinstance(tela, TelaJogo) and tela.game_manager.boss_derrotado:
                    self.tela_atual = "fase_concluida1"
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