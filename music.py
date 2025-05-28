import pygame

def iniciar_musica_de_fundo():
    """
    Inicia a música de fundo do jogo.
    - Inicializa o mixer do pygame.
    - Carrega o arquivo de áudio especificado.
    - Define o volume.
    - Inicia a reprodução em loop infinito.
    """
    pygame.mixer.init()  # Inicializa o sistema de áudio
    pygame.mixer.music.load('assets/dungeon-air-6983.mp3')  # Carrega a música de fundo
    pygame.mixer.music.set_volume(0.7)  # Define o volume (entre 0.0 e 1.0)
    pygame.mixer.music.play(-1)  # Reproduz a música em loop infinito

def parar_musica():
    """
    Interrompe a reprodução da música de fundo atual.
    """
    pygame.mixer.music.stop()  # Para a música atual
