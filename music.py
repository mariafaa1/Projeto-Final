import pygame

def iniciar_musica_de_fundo():
    """
    Inicia a música de fundo do jogo.
    """
    pygame.mixer.init()
    pygame.mixer.music.load('assets/dungeon-air-6983.mp3')  # Ajuste o nome conforme o arquivo que baixou
    pygame.mixer.music.set_volume(0.7)  # Volume entre 0.0 e 1.0
    pygame.mixer.music.play(-1)  # -1 para loop infinito

def parar_musica():
    pygame.mixer.music.stop()
