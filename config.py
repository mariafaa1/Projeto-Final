

# Tamanho da janela
WIDTH = 800
HEIGHT = 600

# Cores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VERDE_ESCURO = (30, 30, 30)

# Velocidades
PLAYER_SPEED = 5
BULLET_SPEED = 10

# FPS
FPS = 60

# Número de vidas por jogador
MAX_LIVES = 3

# Cooldown entre tiros (em milissegundos)
SHOOT_COOLDOWN = 500

import pygame
from config import WIDTH, HEIGHT, PLAYER_SPEED, BULLET_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, controls, assets):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = PLAYER_SPEED
        self.controls = controls  # dicionário com teclas de movimento e tiro
        self.assets = assets
        self.last_shot = pygame.time.get_ticks()

    def update(self, keys_pressed, bullets_group, all_sprites):
        if keys_pressed[self.controls['up']]:
            self.rect.y -= self.speed
        if keys_pressed[self.controls['down']]:
            self.rect.y += self.speed
        if keys_pressed[self.controls['left']]:
            self.rect.x -= self.speed
        if keys_pressed[self.controls['right']]:
            self.rect.x += self.speed

        # Mantém o jogador na tela
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        # Disparo
        now = pygame.time.get_ticks()
        if keys_pressed[self.controls['shoot']] and now - self.last_shot > 500:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.assets['bullet'], self)
            bullets_group.add(bullet)
            all_sprites.add(bullet)
            self.assets['som_tiro'].play()
            self.last_shot = now

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, player):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BULLET_SPEED
        self.direction = -1 if player.controls['up'] == pygame.K_w else 1  # simples distinção

    def update(self):
        self.rect.y += self.direction * -self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
