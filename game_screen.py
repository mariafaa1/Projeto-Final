import pygame
from sprites import Player, Bullet
from config import FPS, WIDTH, HEIGHT, DARK_GRAY

def game_screen(window, assets):
    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Define controles para os dois jogadores
    controls1 = {
        'up': pygame.K_w,
        'down': pygame.K_s,
        'left': pygame.K_a,
        'right': pygame.K_d,
        'shoot': pygame.K_SPACE
    }

    controls2 = {
        'up': pygame.K_UP,
        'down': pygame.K_DOWN,
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'shoot': pygame.K_RSHIFT
    }

    # Cria jogadores
    player1 = Player(assets['player1'], WIDTH // 4, HEIGHT - 60, controls1, assets)
    player2 = Player(assets['player2'], WIDTH * 3 // 4, 60, controls2, assets)

    all_sprites.add(player1, player2)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player1.update(keys, bullets, all_sprites)
        player2.update(keys, bullets, all_sprites)
        bullets.update()

        window.fill(DARK_GRAY)
        all_sprites.draw(window)
        pygame.display.flip()
