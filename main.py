import pygame
import sys
from config import LARGURA, ALTURA
from screens import MenuInicial, TelaCarregamento, TelaJogo
from game_manager import GameManager

class GerenciadorTelas:
    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Jogo de Fantasia - Soldado")
        self.telas = {
            "menu": MenuInicial(self.janela),
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

if __name__ == "__main__":
    try:
        jogo = GerenciadorTelas()
        jogo.executar()
    except Exception as e:
        print(f"ERRO FATAL: {str(e)}")
        pygame.quit()