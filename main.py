# main.py

import pygame
import sys
from config import LARGURA, ALTURA
from screens import MenuInicial, TelaCarregamento, TelaJogo, TelaGenerica, TelaControles, TelaHistoria, TelaMenuPosJogo
from game_manager import GameManager
from music import iniciar_musica_de_fundo

# Constantes que definem os tipos de reinício possíveis
REINICIO_NENHUM = 0
REINICIO_FASE = 1
REINICIO_JOGO = 2

class GerenciadorTelas:
    def __init__(self):
        # Inicializa os módulos do pygame
        pygame.init()

        # Inicia a música de fundo do jogo
        iniciar_musica_de_fundo()

        # Cria a janela principal do jogo com as dimensões especificadas
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Pixel Fantasy")

        # Define o nível atual como 1
        self.level_corrente = 1

        # Define o estado inicial de reinício como nenhum
        self.estado_reinicio = REINICIO_NENHUM

        # Dicionário com todas as telas do jogo, com suas instâncias ou placeholders
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

            "tela1": TelaGenerica(self.janela, "assets/tela1.1.png", "tela2"),
            "tela2": TelaGenerica(self.janela, "assets/tela2.1.png", "tela3"),
            "tela3": TelaGenerica(self.janela, "assets/tela3.1.png", "agradecimentos"),
            "agradecimentos": TelaGenerica(self.janela, "assets/agradecimentos.png", "creditos"),
            "creditos": TelaGenerica(self.janela, "assets/creditos.png", "menu"),

            "menu_pos_jogo": TelaMenuPosJogo(self.janela),
            "reiniciar_fase_confirmado": None,
            "loading": TelaCarregamento(self.janela),
            "jogo": None  # Esta tela será criada dinamicamente quando necessário
        }

        # Define a tela inicial como o menu
        self.tela_atual = "menu"

        # Variável para armazenar animações carregadas
        self.animacoes = None

    def executar(self):
        # Loop principal do jogo
        while True:
            # Verifica se há um pedido de reinício de fase
            if self.estado_reinicio == REINICIO_FASE:
                self.telas["jogo"] = None
                self.tela_atual = "loading"
                self.estado_reinicio = REINICIO_NENHUM

            # Verifica se há um pedido de reinício completo do jogo
            elif self.estado_reinicio == REINICIO_JOGO:
                self.level_corrente = 1
                self.telas["jogo"] = None
                self.tela_atual = "loading"
                self.estado_reinicio = REINICIO_NENHUM

            # Obtém a tela atual do dicionário
            tela = self.telas.get(self.tela_atual)
            if not tela:
                print(f"ERRO: Tela {self.tela_atual} não encontrada!")
                pygame.quit()
                return

            # Loop interno para a execução da tela atual
            rodando = True
            while rodando:
                eventos = pygame.event.get()
                for evento in eventos:
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        return

                # Processa os eventos, atualiza e desenha a tela
                tela.tratar_eventos(eventos)
                tela.atualizar()
                tela.desenhar()
                pygame.display.update()

                # Verifica se a tela atual definiu uma próxima tela
                if tela.proxima_tela:
                    # Atualiza o level caso entre na tela "fase2_2"
                    if tela.proxima_tela == "fase2_2":
                        self.level_corrente = 2
                        print(f"[DEBUG] Level atualizado para {self.level_corrente}")

                    # Se saindo da tela de loading, inicializa a tela de jogo com as animações carregadas
                    if self.tela_atual == "loading":
                        self.animacoes = tela.animacoes
                        self.telas["jogo"] = TelaJogo(
                            self.janela,
                            self.animacoes,
                            GameManager,
                            level_atual=self.level_corrente
                        )

                    # Verifica se está saindo do menu pós-jogo com alguma opção de reinício
                    if self.tela_atual == "menu_pos_jogo":
                        if tela.proxima_tela == "reiniciar_fase":
                            self.estado_reinicio = REINICIO_FASE
                        elif tela.proxima_tela == "reiniciar_jogo":
                            self.estado_reinicio = REINICIO_JOGO

                    # Atualiza a tela atual
                    self.tela_atual = tela.proxima_tela
                    rodando = False

                # Verifica se é hora de voltar ao menu pós-jogo após jogar
                if isinstance(tela, TelaJogo) and tela.proxima_tela == "menu_pos_jogo":
                    self.tela_atual = "menu_pos_jogo"
                    rodando = False

                # Verifica se o jogo deve ser encerrado
                if tela.proxima_tela == "sair":
                    pygame.quit()
                    sys.exit()

# Bloco principal que inicia o jogo se o arquivo for executado diretamente
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
